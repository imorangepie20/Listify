from model import music as music_model
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from services import deezer
import os

GENRE_MAP = {
    "k-pop": "K-Pop",
    "korean pop": "K-Pop",
    "dance pop": "Pop",
    "pop": "Pop",
    "hip hop": "Hip-Hop",
    "hip-hop": "Hip-Hop",
    "r&b": "R&B",
    "jazz": "Jazz",
    "electronic": "Electronic",
    "edm": "Electronic",
    "rock": "Rock",
    "metal": "Metal",
    "indie": "Indie",
}

# Spotify 글로벌 Top 50 플레이리스트 ID
GLOBAL_TOP_50_PLAYLIST_ID = "37i9dQZEVXbMDoHDwVN2tF"


def get_spotify_client():
    # ✅ app.py와 동일한 환경변수 이름으로 통일
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Spotify 환경변수(SPOTIFY_CLIENT_ID/SECRET)가 설정되지 않았습니다.")

    return Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )


def extract_genre_no(sp, artist_id):
    """Spotify artist → genres → 우리 DB genre_no"""
    try:
        artist = sp.artist(artist_id)
        spotify_genres = artist.get("genres", [])
    except Exception:
        spotify_genres = []

    for g in spotify_genres:
        key = (g or "").lower()
        if key in GENRE_MAP:
            genre_name = GENRE_MAP[key]
            return music_model.find_genre_no_by_name(genre_name)

    return None


def save_track_if_not_exists(sp, track):
    """트랙이 DB에 없으면 저장, 있으면 기존 데이터 반환 (preview_url 없으면 업데이트)"""
    spotify_url = track.get("external_urls", {}).get("spotify")
    if not spotify_url:
        return None, False

    # 중복 체크
    existing = music_model.find_by_spotify_url(spotify_url)
    if existing:
        # preview_url이 없으면 Deezer에서 가져와서 업데이트
        if not existing.get('preview_url'):
            track_name = existing.get('track_name', '')
            artist_name = existing.get('artist_name', '')
            preview_url = deezer.get_preview_url(track_name, artist_name)
            if preview_url:
                music_model.update_preview_url(existing['music_no'], preview_url)
                existing['preview_url'] = preview_url
        return existing, False  # 이미 존재

    # 새로 저장
    artists = track.get("artists") or []
    artist_id = artists[0].get("id") if artists else None
    artist_name = artists[0].get("name") if artists else ""

    genre_no = extract_genre_no(sp, artist_id) if artist_id else None

    album = track.get("album") or {}
    images = album.get("images") or []
    album_image_url = images[0].get("url") if images else None

    music = {
        "track_name": track.get("name") or "",
        "artist_name": artist_name,
        "album_name": album.get("name") or "",
        "album_image_url": album_image_url,
        "duration_ms": track.get("duration_ms") or 0,
        "popularity": track.get("popularity") or 0,
        "spotify_url": spotify_url,
        "genre_no": genre_no,
        "preview_url": deezer.get_preview_url(track.get("name") or "", artist_name)  # Deezer에서 30초 미리듣기 URL
    }

    music_no = music_model.insert_music(music)
    if music_no:
        music["music_no"] = music_no
        return music, True

    return None, False


def search_and_save_music(keyword, category, page, size):
    """
    ✅ /music/search?q=...&category=...&page=1&size=12
    - Spotify에서 track 검색
    - DB에 저장(중복 제외)
    - 반환: (musics, total, error)
    """
    try:
        sp = get_spotify_client()

        # page/size 안전 처리
        page = max(int(page or 1), 1)
        size = max(int(size or 12), 1)
        offset = (page - 1) * size

        # category 처리(원하는 방식으로 확장 가능)
        # - category=artist: artist 필드 중심으로 검색되게 쿼리 강화
        if category == "artist":
            q = f"artist:{keyword}"
        else:
            q = keyword

        results = sp.search(
            q=q,
            type="track",
            limit=size,
            offset=offset,
            market="KR"
        )

        tracks_obj = results.get("tracks") or {}
        total = tracks_obj.get("total") or 0
        items = tracks_obj.get("items") or []

        musics = []
        for track in items:
            music, is_new = save_track_if_not_exists(sp, track)
            if music:
                music["is_new"] = is_new
                musics.append(music)

        return musics, total, None

    except Exception as e:
        return None, 0, str(e)


def bulk_import_music(query, total_count=100):
    """대량 음악 데이터 가져오기"""
    sp = get_spotify_client()
    all_tracks = []
    limit = 50
    offset = 0

    try:
        while len(all_tracks) < total_count:
            results = sp.search(
                q=query,
                type='track',
                limit=limit,
                offset=offset,
                market='KR'
            )
            tracks = (results.get('tracks') or {}).get('items') or []
            if not tracks:
                break

            for track in tracks:
                if len(all_tracks) >= total_count:
                    break

                music, is_new = save_track_if_not_exists(sp, track)
                if music:
                    music['is_new'] = is_new
                    all_tracks.append(music)

            offset += limit

        return all_tracks, None

    except Exception as e:
        return None, str(e)


def get_global_top_50():
    """Spotify 글로벌 Top 50 가져와서 저장"""
    sp = get_spotify_client()

    try:
        playlist = sp.playlist_tracks(GLOBAL_TOP_50_PLAYLIST_ID, limit=50)
        items = playlist.get('items') or []

        saved = []
        for item in items:
            track = item.get('track')
            if not track:
                continue
            music, is_new = save_track_if_not_exists(sp, track)
            if music:
                music['is_new'] = is_new
                saved.append(music)

        return saved, None

    except Exception as e:
        return None, str(e)


def get_music_list(category=None, value=None):
    return music_model.find_all(category, value), None


def get_fresh_preview_url(track_name, artist_name):
    """실시간으로 Deezer에서 preview URL 가져오기"""
    try:
        preview_url = deezer.get_preview_url(track_name, artist_name)
        if preview_url:
            return preview_url, None
        return None, "Deezer에서 미리듣기를 찾을 수 없습니다."
    except Exception as e:
        return None, str(e)
