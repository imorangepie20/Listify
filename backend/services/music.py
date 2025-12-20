# -*- coding: utf-8 -*-
from model import music as music_model
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os


# Spotify API 클라이언트 초기화
def get_spotify_client():
    """Spotify API 클라이언트 생성"""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_and_save_music(query, limit=20):
    """
    Spotify에서 음악 검색 후 DB에 저장
    - DB에 이미 있으면 기존 데이터 반환
    - 없으면 Spotify에서 가져와서 저장 후 반환
    """
    try:
        sp = get_spotify_client()

        # Spotify 검색 (최대 50개)
        if limit > 50:
            limit = 50

        results = sp.search(q=query, type='track', limit=limit, market='KR')
        tracks = results['tracks']['items']

        saved_tracks = []

        for track in tracks:
            spotify_track_id = track['id']

            # DB에 이미 있는지 확인
            existing_music = music_model.find_by_spotify_track_id(spotify_track_id)

            if existing_music:
                saved_tracks.append(existing_music)
            else:
                # DB에 저장
                track_name = track['name']
                artist_name = ', '.join([artist['name'] for artist in track['artists']])
                album_name = track['album']['name']
                album_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                duration_ms = track['duration_ms']
                popularity = track['popularity']
                spotify_url = track['external_urls']['spotify']

                # 발매일 처리
                release_date = track['album'].get('release_date')
                release_year = None
                if release_date:
                    try:
                        release_year = int(release_date.split('-')[0])
                    except:
                        release_year = None

                # DB에 저장
                music_no = music_model.insert_music(
                    spotify_track_id=spotify_track_id,
                    track_name=track_name,
                    artist_name=artist_name,
                    album_name=album_name,
                    album_image_url=album_image_url,
                    duration_ms=duration_ms,
                    popularity=popularity,
                    spotify_url=spotify_url,
                    release_date=release_date,
                    release_year=release_year
                )

                if music_no:
                    saved_music = music_model.find_by_music_no(music_no)
                    if saved_music:
                        saved_tracks.append(saved_music)

        return saved_tracks, None

    except Exception as e:
        return None, str(e)


def bulk_import_music(query, total_count=100):
    """
    대량 음악 데이터 가져오기 (100~200개)
    - Spotify API 제한: 한 번에 최대 50개
    - offset을 사용해서 여러 번 요청
    """
    try:
        sp = get_spotify_client()

        all_tracks = []
        limit = 50
        offset = 0

        while len(all_tracks) < total_count:
            results = sp.search(q=query, type='track', limit=limit, offset=offset, market='KR')
            tracks = results['tracks']['items']

            if not tracks:
                break

            for track in tracks:
                if len(all_tracks) >= total_count:
                    break

                spotify_track_id = track['id']

                # 이미 DB에 있으면 스킵
                existing = music_model.find_by_spotify_track_id(spotify_track_id)
                if existing:
                    all_tracks.append(existing)
                    continue

                # 새로 저장
                track_name = track['name']
                artist_name = ', '.join([artist['name'] for artist in track['artists']])
                album_name = track['album']['name']
                album_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                duration_ms = track['duration_ms']
                popularity = track['popularity']
                spotify_url = track['external_urls']['spotify']

                release_date = track['album'].get('release_date')
                release_year = None
                if release_date:
                    try:
                        release_year = int(release_date.split('-')[0])
                    except:
                        pass

                music_no = music_model.insert_music(
                    spotify_track_id=spotify_track_id,
                    track_name=track_name,
                    artist_name=artist_name,
                    album_name=album_name,
                    album_image_url=album_image_url,
                    duration_ms=duration_ms,
                    popularity=popularity,
                    spotify_url=spotify_url,
                    release_date=release_date,
                    release_year=release_year
                )

                if music_no:
                    saved = music_model.find_by_music_no(music_no)
                    if saved:
                        all_tracks.append(saved)

            offset += limit

        return all_tracks, None

    except Exception as e:
        return None, str(e)


def get_music_list(limit=50, offset=0):
    """음악 목록 조회"""
    try:
        musics = music_model.list_all(limit, offset)
        total = music_model.count_all()
        return {"musics": musics, "total": total}, None
    except Exception as e:
        return None, str(e)


def get_music_by_category(category, value, limit=50):
    """카테고리별 음악 조회 (artist, genre, year)"""
    try:
        if category == 'artist':
            musics = music_model.list_by_artist(value, limit)
        elif category == 'genre':
            musics = music_model.list_by_genre(int(value), limit)
        elif category == 'year':
            musics = music_model.list_by_year(int(value), limit)
        else:
            return None, f"Invalid category: {category}. Use 'artist', 'genre', or 'year'"

        return musics, None
    except Exception as e:
        return None, str(e)


def get_music_detail(music_no):
    """음악 상세 조회"""
    try:
        music = music_model.find_by_music_no(music_no)
        if not music:
            return None, "존재하지 않는 음악입니다."
        return music, None
    except Exception as e:
        return None, str(e)


def search_music_in_db(query, limit=20):
    """DB에서 음악 검색"""
    try:
        musics = music_model.search_music(query, limit)
        return musics, None
    except Exception as e:
        return None, str(e)
