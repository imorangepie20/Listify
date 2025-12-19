# -*- coding: utf-8 -*-
"""
Playlist & Music List API 테스트 베드
실행: python test_api.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask
from dotenv import load_dotenv
import json

load_dotenv()

# Flask 앱 생성
app = Flask(__name__)

# Blueprint 등록
from routes.playlist import playlist_bp
from routes.music_list import music_list_bp
app.register_blueprint(playlist_bp)
app.register_blueprint(music_list_bp)

# 테스트 클라이언트
client = app.test_client()


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_response(title, response):
    print(f"\n{'─'*50}")
    print(f"📌 {title}")
    print(f"{'─'*50}")
    print(f"Status: {response.status_code}")
    try:
        data = response.get_json()
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"Response: {response.data.decode('utf-8')}")


def test_playlist_api(user_no=1):
    """Playlist API 테스트"""
    print_header("🎵 PLAYLIST API 테스트")
    
    # 1. 생성
    print_response(
        "1. 플레이리스트 생성",
        client.post('/playlist',
            headers={'X-User-No': str(user_no)},
            json={'title': '테스트 플레이리스트', 'content': '설명'}
        )
    )
    
    # 생성된 playlist_no 얻기
    resp = client.post('/playlist',
        headers={'X-User-No': str(user_no)},
        json={'title': '음악 테스트용', 'content': None}
    )
    data = resp.get_json()
    playlist_no = data.get('data', {}).get('playlist_no', 1)
    print_response("2. 음악 테스트용 플레이리스트 생성", resp)
    
    # 3. 목록 조회
    print_response(
        "3. 전체 목록 조회",
        client.get('/playlist')
    )
    
    # 4. 상세 조회
    print_response(
        f"4. 상세 조회 (playlist_no={playlist_no})",
        client.get(f'/playlist/{playlist_no}')
    )
    
    # 5. 수정
    print_response(
        f"5. 수정 (playlist_no={playlist_no})",
        client.put(f'/playlist/{playlist_no}',
            headers={'X-User-No': str(user_no)},
            json={'title': '수정된 제목', 'content': '수정된 내용'}
        )
    )
    
    return playlist_no


def test_music_list_api(playlist_no, user_no=1):
    """Music List API 테스트"""
    print_header("🎶 MUSIC LIST API 테스트")
    
    # 1. 음악 추가
    print_response(
        f"1. 음악 추가 (playlist={playlist_no}, music=1)",
        client.post(f'/playlist/{playlist_no}/music',
            headers={'X-User-No': str(user_no)},
            json={'music_no': 1}
        )
    )
    
    # 2. 음악 추가 (두번째)
    print_response(
        f"2. 음악 추가 (playlist={playlist_no}, music=2)",
        client.post(f'/playlist/{playlist_no}/music',
            headers={'X-User-No': str(user_no)},
            json={'music_no': 2}
        )
    )
    
    # 3. 중복 추가 시도
    print_response(
        "3. 중복 음악 추가 시도 (실패해야함)",
        client.post(f'/playlist/{playlist_no}/music',
            headers={'X-User-No': str(user_no)},
            json={'music_no': 1}
        )
    )
    
    # 4. 음악 목록 조회
    print_response(
        f"4. 음악 목록 조회 (playlist={playlist_no})",
        client.get(f'/playlist/{playlist_no}/music')
    )
    
    # 5. 특정 음악이 포함된 플레이리스트 조회
    print_response(
        "5. music_no=1이 포함된 플레이리스트 조회",
        client.get('/playlist/by-music/1')
    )
    
    # 6. 음악 삭제
    print_response(
        f"6. 음악 삭제 (playlist={playlist_no}, music=1)",
        client.delete(f'/playlist/{playlist_no}/music/1',
            headers={'X-User-No': str(user_no)}
        )
    )
    
    # 7. 삭제 후 목록 확인
    print_response(
        "7. 삭제 후 음악 목록 확인",
        client.get(f'/playlist/{playlist_no}/music')
    )


def test_error_cases(playlist_no, user_no=1):
    """에러 케이스 테스트"""
    print_header("❌ 에러 케이스 테스트")
    
    # 1. 인증 없이 플레이리스트 생성
    print_response(
        "1. 인증 없이 생성 (401)",
        client.post('/playlist', json={'title': 'test'})
    )
    
    # 2. 제목 없이 생성
    print_response(
        "2. 제목 없이 생성 (400)",
        client.post('/playlist',
            headers={'X-User-No': str(user_no)},
            json={'content': 'no title'}
        )
    )
    
    # 3. 다른 사람 플레이리스트 수정
    print_response(
        "3. 다른 유저의 플레이리스트 수정 (403)",
        client.put(f'/playlist/{playlist_no}',
            headers={'X-User-No': '99999'},
            json={'title': 'hack', 'content': 'test'}
        )
    )
    
    # 4. 다른 사람 플레이리스트에 음악 추가
    print_response(
        "4. 다른 유저의 플레이리스트에 음악 추가 (403)",
        client.post(f'/playlist/{playlist_no}/music',
            headers={'X-User-No': '99999'},
            json={'music_no': 999}
        )
    )
    
    # 5. 존재하지 않는 플레이리스트 조회
    print_response(
        "5. 존재하지 않는 플레이리스트 조회 (404)",
        client.get('/playlist/999999')
    )


def cleanup(playlist_no, user_no=1):
    """테스트 데이터 정리"""
    print_header("🧹 테스트 데이터 정리")
    
    # 플레이리스트 삭제 (CASCADE로 music_list도 삭제됨)
    print_response(
        f"플레이리스트 삭제 (playlist_no={playlist_no})",
        client.delete(f'/playlist/{playlist_no}',
            headers={'X-User-No': str(user_no)}
        )
    )


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║         PLAYLIST & MUSIC LIST API 테스트 베드              ║
╠════════════════════════════════════════════════════════════╣
║  필요 조건:                                                ║
║  1. .env 파일에 DB 설정                                    ║
║  2. user, playlist, music, music_list 테이블 필요          ║
║  3. user_no=1, music_no=1,2 가 DB에 존재해야 함            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    test_user_no = 1
    
    try:
        # 1. Playlist API 테스트
        playlist_no = test_playlist_api(test_user_no)
        
        # 2. Music List API 테스트
        test_music_list_api(playlist_no, test_user_no)
        
        # 3. 에러 케이스 테스트
        test_error_cases(playlist_no, test_user_no)
        
        # 4. 정리
        cleanup(playlist_no, test_user_no)
        
        print("\n" + "="*60)
        print("  ✅ 모든 테스트 완료!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
