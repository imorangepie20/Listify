from model import music as music_model
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os


GENRE_MAP = {
    "k-pop": "K-Pop",
    "korean pop": "K-Pop",
    "dance pop": "Pop",
    "pop": "Pop",
    "hip hop": "Hip-Hop",
    "r&b": "R&B",
    "jazz": "Jazz",
    "electronic": "Electronic",
    "rock": "Rock",
    "metal": "Metal",
    "indie": "Indie",
}

# Spotify 글로벌 Top 50 플레이리스트 ID
GLOBAL_TOP_50_PLAYLIST_ID = "37i9dQZEVXbMDoHDwVN2tF"


def get_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Spotify 환경변수가 설정되지 않았습니다.")

    return Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )


def extract_genre_no(sp, artist_id):
    """Spotify artist → genres → 우리 DB genre_no"""
    artist = sp.artist(artist_id)
    spotify_genres = artist.get("genres", [])

    for g in spotify_genres:
        key = g.lower()
        if key in GENRE_MAP:
            genre_name = GENRE_MAP[key]
            return music_model.find_genre_no_by_name(genre_name)

    return None


def save_track_if_not_exists(sp, track):
    """트랙이 DB에 없으면 저장, 있으면 기존 데이터 반환"""
    spotify_url = track['external_urls']['spotify']
    
    # 중복 체크
    existing = music_model.find_by_spotify_url(spotify_url)
    if existing:
        return existing, False  # 이미 존재함
    
    # 새로 저장
    artist_id = track['artists'][0]['id']
    genre_no = extract_genre_no(sp, artist_id)

    music = {
        "track_name": track['name'],
        "artist_name": track['artists'][0]['name'],
        "album_name": track['album']['name'],
        "album_image_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
        "duration_ms": track['duration_ms'],
        "popularity": track['popularity'],
        "spotify_url": spotify_url,
        "genre_no": genre_no
    }

    music_no = music_model.insert_music(music)
    if music_no:
        music['music_no'] = music_no
        return music, True  # 새로 저장됨
    
    return None, False


def search_and_save_music(keyword, category):
    """검색 후 중복 체크하여 저장"""
    sp = get_spotify_client()

    query = keyword
    if category:
        query = f"{category}:{keyword}"

    results = sp.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']

    saved = []
    for track in tracks:
        music, is_new = save_track_if_not_exists(sp, track)
        if music:
            music['is_new'] = is_new  # 새로 저장된 건지 표시
            saved.append(music)

    return saved, None

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
            tracks = results['tracks']['items']
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
        tracks = playlist['items']

        saved = []
        for item in tracks:
            track = item['track']
            if track:  # None 체크
                music, is_new = save_track_if_not_exists(sp, track)
                if music:
                    music['is_new'] = is_new
                    saved.append(music)

        return saved, None

    except Exception as e:
        return None, str(e)
    
    


def get_music_list(category=None, value=None):
    return music_model.find_all(category, value), None
