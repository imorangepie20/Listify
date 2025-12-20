# -*- coding: utf-8 -*-
from flask import request, jsonify
from services import music as music_svc


# 음악 검색 (Spotify API → DB 저장 → 반환)
def search_music():
    """
    음악 검색
    - DB에 있으면 DB에서 반환
    - 없으면 Spotify에서 가져와서 저장 후 반환
    """
    query = request.args.get('q')
    limit = request.args.get('limit', 20, type=int)

    if not query:
        return jsonify({"success": False, "message": "검색어(q)가 필요합니다."}), 400

    if limit > 50:
        limit = 50

    try:
        tracks, error = music_svc.search_and_save_music(query, limit)
        if error:
            return jsonify({"success": False, "message": error}), 500

        return jsonify({
            "success": True,
            "data": {
                "query": query,
                "tracks": tracks,
                "count": len(tracks)
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 대량 음악 데이터 가져오기 (100~200개)
def bulk_import():
    """
    대량 음악 데이터 가져오기
    - 최대 200개까지 Spotify에서 가져와서 DB에 저장
    """
    data = request.get_json(silent=True) or {}
    query = data.get('query')
    count = data.get('count', 100)

    if not query:
        return jsonify({"success": False, "message": "query 필드가 필요합니다."}), 400

    if count > 200:
        count = 200

    try:
        tracks, error = music_svc.bulk_import_music(query, count)
        if error:
            return jsonify({"success": False, "message": error}), 500

        return jsonify({
            "success": True,
            "message": f"{len(tracks)}개의 음악을 가져왔습니다.",
            "data": {
                "query": query,
                "count": len(tracks),
                "tracks": tracks
            }
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 음악 목록 조회
def get_music_list():
    """음악 목록 조회 (페이지네이션)"""
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)

    if limit > 100:
        limit = 100

    try:
        result, error = music_svc.get_music_list(limit, offset)
        if error:
            return jsonify({"success": False, "message": error}), 500

        return jsonify({
            "success": True,
            "data": {
                "musics": result['musics'],
                "total": result['total'],
                "limit": limit,
                "offset": offset
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 카테고리별 음악 조회 (artist, genre, year)
def get_music_by_category():
    """
    카테고리별 음악 조회
    - artist: 아티스트명으로 검색
    - genre: 장르 번호로 검색
    - year: 발매 연도로 검색
    """
    category = request.args.get('category')
    value = request.args.get('value')
    limit = request.args.get('limit', 50, type=int)

    if not category or not value:
        return jsonify({
            "success": False,
            "message": "category와 value 파라미터가 필요합니다."
        }), 400

    if category not in ['artist', 'genre', 'year']:
        return jsonify({
            "success": False,
            "message": "category는 'artist', 'genre', 'year' 중 하나여야 합니다."
        }), 400

    try:
        musics, error = music_svc.get_music_by_category(category, value, limit)
        if error:
            return jsonify({"success": False, "message": error}), 400

        return jsonify({
            "success": True,
            "data": {
                "category": category,
                "value": value,
                "musics": musics,
                "count": len(musics)
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# 음악 상세 조회
def get_music_detail(music_no):
    """음악 상세 조회"""
    try:
        music, error = music_svc.get_music_detail(music_no)
        if error:
            return jsonify({"success": False, "message": error}), 404

        return jsonify({
            "success": True,
            "data": music
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# DB에서 음악 검색 (Spotify API 사용 안 함)
def search_music_in_db():
    """DB에서 음악 검색 (Spotify API 호출 없음)"""
    query = request.args.get('q')
    limit = request.args.get('limit', 20, type=int)

    if not query:
        return jsonify({"success": False, "message": "검색어(q)가 필요합니다."}), 400

    try:
        musics, error = music_svc.search_music_in_db(query, limit)
        if error:
            return jsonify({"success": False, "message": error}), 500

        return jsonify({
            "success": True,
            "data": {
                "query": query,
                "musics": musics,
                "count": len(musics)
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
