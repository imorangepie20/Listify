# -*- coding: utf-8 -*-
from flask import Blueprint
from controllers import music as music_controller

music_bp = Blueprint('music', __name__, url_prefix='/music')


@music_bp.route('/search', methods=['GET'])
def search_music():
    """
    음악 검색 (Spotify API → DB 저장 → 반환)

    Query Parameters:
    - q: 검색어 (필수)
    - limit: 결과 개수 (기본 20, 최대 50)

    Example: GET /music/search?q=아이유&limit=20
    """
    return music_controller.search_music()


@music_bp.route('/search/db', methods=['GET'])
def search_music_in_db():
    """
    DB에서 음악 검색 (Spotify API 사용 안 함)

    Query Parameters:
    - q: 검색어 (필수)
    - limit: 결과 개수 (기본 20)

    Example: GET /music/search/db?q=아이유&limit=20
    """
    return music_controller.search_music_in_db()


@music_bp.route('/bulk-import', methods=['POST'])
def bulk_import():
    """
    대량 음악 데이터 가져오기 (100~200개)

    Request Body:
    {
      "query": "검색어",
      "count": 100  (기본 100, 최대 200)
    }

    Example: POST /music/bulk-import
    Body: {"query": "kpop", "count": 150}
    """
    return music_controller.bulk_import()


@music_bp.route('', methods=['GET'])
def get_music_list():
    """
    음악 목록 조회 (페이지네이션)

    Query Parameters:
    - limit: 결과 개수 (기본 50, 최대 100)
    - offset: 시작 위치 (기본 0)

    Example: GET /music?limit=50&offset=0
    """
    return music_controller.get_music_list()


@music_bp.route('/category', methods=['GET'])
def get_music_by_category():
    """
    카테고리별 음악 조회

    Query Parameters:
    - category: artist, genre, year (필수)
    - value: 카테고리 값 (필수)
    - limit: 결과 개수 (기본 50)

    Examples:
    - GET /music/category?category=artist&value=아이유&limit=20
    - GET /music/category?category=genre&value=1&limit=20
    - GET /music/category?category=year&value=2023&limit=20
    """
    return music_controller.get_music_by_category()


@music_bp.route('/<int:music_no>', methods=['GET'])
def get_music_detail(music_no):
    """
    음악 상세 조회

    Example: GET /music/1
    """
    return music_controller.get_music_detail(music_no)
