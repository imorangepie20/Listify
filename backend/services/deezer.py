# backend/services/deezer.py
"""
Deezer API를 사용하여 30초 미리듣기 URL을 가져오는 서비스
Spotify에서 곡 정보를 가져온 후, Deezer에서 preview URL만 추출
"""

import requests
from urllib.parse import quote

DEEZER_API_BASE = "https://api.deezer.com"


def search_track(track_name: str, artist_name: str) -> dict | None:
    """
    Deezer에서 곡 검색 후 첫 번째 결과 반환
    """
    query = f"{track_name} {artist_name}"
    url = f"{DEEZER_API_BASE}/search?q={quote(query)}&limit=1"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                return data["data"][0]
    except Exception as e:
        print(f"Deezer API 오류: {e}")
    
    return None


def get_preview_url(track_name: str, artist_name: str) -> str | None:
    """
    곡명과 아티스트로 Deezer에서 30초 미리듣기 URL 가져오기
    """
    track = search_track(track_name, artist_name)
    if track:
        preview = track.get("preview")
        if preview:
            print(f"  🎵 Deezer preview: {track_name}")
            return preview
    
    return None
