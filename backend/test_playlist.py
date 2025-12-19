# -*- coding: utf-8 -*-
"""
Playlist API 테스트 스크립트
실행: python test_playlist.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask
from dotenv import load_dotenv
import json

load_dotenv()

# Flask 앱 생성 (테스트용)
app = Flask(__name__)

# Blueprint 등록
from routes.playlist import playlist_bp
app.register_blueprint(playlist_bp)

# 테스트 클라이언트 생성
client = app.test_client()


def print_response(title, response):
    """응답 출력"""
    print(f"\n{'='*50}")
    print(f"📌 {title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    try:
        data = response.get_json()
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except:
        print(f"Response: {response.data.decode('utf-8')}")


def test_playlist_crud():
    """Playlist CRUD 테스트"""
    
    print("\n" + "="*60)
    print("   🎵 PLAYLIST API 테스트 시작")
    print("="*60)
    
    # 테스트용 user_no (DB에 존재하는 유저로 변경 필요)
    test_user_no = 1
    
    # 1. 플레이리스트 생성
    print_response(
        "1. 플레이리스트 생성 (POST /playlist)",
        client.post(
            '/playlist',
            headers={'X-User-No': str(test_user_no)},
            json={
                'title': '테스트 플레이리스트',
                'content': '테스트 설명입니다.'
            }
        )
    )
    
    # 두번째 플레이리스트 생성
    response = client.post(
        '/playlist',
        headers={'X-User-No': str(test_user_no)},
        json={
            'title': '두번째 플레이리스트',
            'content': None
        }
    )
    created_data = response.get_json()
    playlist_no = created_data.get('data', {}).get('playlist_no', 1)
    
    print_response("1-2. 두번째 플레이리스트 생성", response)
    
    # 2. 전체 목록 조회
    print_response(
        "2. 전체 플레이리스트 조회 (GET /playlist)",
        client.get('/playlist')
    )
    
    # 3. 유저별 목록 조회
    print_response(
        f"3. 유저 {test_user_no}의 플레이리스트 (GET /playlist/user/{test_user_no})",
        client.get(f'/playlist/user/{test_user_no}')
    )
    
    # 4. 상세 조회
    print_response(
        f"4. 플레이리스트 상세 조회 (GET /playlist/{playlist_no})",
        client.get(f'/playlist/{playlist_no}')
    )
    
    # 5. 수정
    print_response(
        f"5. 플레이리스트 수정 (PUT /playlist/{playlist_no})",
        client.put(
            f'/playlist/{playlist_no}',
            headers={'X-User-No': str(test_user_no)},
            json={
                'title': '수정된 제목',
                'content': '수정된 내용'
            }
        )
    )
    
    # 6. 권한 없는 수정 시도
    print_response(
        "6. 권한 없는 수정 시도 (다른 유저)",
        client.put(
            f'/playlist/{playlist_no}',
            headers={'X-User-No': '99999'},
            json={
                'title': '권한없음',
                'content': '실패해야함'
            }
        )
    )
    
    # 7. 인증 없이 생성 시도
    print_response(
        "7. 인증 없이 생성 시도 (헤더 없음)",
        client.post(
            '/playlist',
            json={'title': '인증없음', 'content': '실패해야함'}
        )
    )
    
    # 8. 제목 없이 생성 시도
    print_response(
        "8. 제목 없이 생성 시도",
        client.post(
            '/playlist',
            headers={'X-User-No': str(test_user_no)},
            json={'content': '제목없음'}
        )
    )
    
    # 9. 삭제
    print_response(
        f"9. 플레이리스트 삭제 (DELETE /playlist/{playlist_no})",
        client.delete(
            f'/playlist/{playlist_no}',
            headers={'X-User-No': str(test_user_no)}
        )
    )
    
    # 10. 삭제 확인
    print_response(
        "10. 삭제된 플레이리스트 조회",
        client.get(f'/playlist/{playlist_no}')
    )
    
    print("\n" + "="*60)
    print("   ✅ 테스트 완료!")
    print("="*60 + "\n")


if __name__ == '__main__':
    print("""
============================================================
                 PLAYLIST API 테스트
============================================================
주의사항:
1. .env 파일에 DB 설정 필요
2. DB에 user, playlist 테이블 필요
3. test_user_no(기본값: 1)가 user 테이블에 존재해야 함
============================================================
    """)
    
    try:
        test_playlist_crud()
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
