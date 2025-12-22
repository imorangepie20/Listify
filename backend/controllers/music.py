from flask import request, jsonify
from services import music as music_service


def search_music():
    keyword = request.args.get('q')
    category = request.args.get('category')

    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 12))

    if not keyword:
        return jsonify({"success": False, "message": "검색어(q)가 필요합니다."}), 400

    musics, total, error = music_service.search_and_save_music(
        keyword, category, page, size
    )
    if error:
        return jsonify({"success": False, "message": error}), 500

    return jsonify({
        "success": True,
        "data": musics,
        "page": page,
        "size": size,
        "total": total
    }), 200


def get_music_list():
    category = request.args.get('category')
    value = request.args.get('value')

    musics, error = music_service.get_music_list(category, value)
    if error:
        return jsonify({"success": False, "message": error}), 400

    return jsonify({"success": True, "data": musics}), 200


def get_global_top_50():
    musics, error = music_service.get_global_top_50()
    if error:
        return jsonify({"success": False, "message": error}), 500

    new_count = sum(1 for m in musics if m.get('is_new'))
    
    return jsonify({
        "success": True,
        "message": f"총 {len(musics)}곡 (신규 {new_count}곡 저장)",
        "data": musics
    }), 200
    
def bulk_import():
    data = request.get_json()
    query = data.get('query', 'kpop')
    count = data.get('count', 100)
    
    if count > 200:
        return jsonify({"success": False, "message": "최대 200개까지 가능합니다."}), 400
    
    musics, error = music_service.bulk_import_music(query, count)
    if error:
        return jsonify({"success": False, "message": error}), 500
    
    new_count = sum(1 for m in musics if m.get('is_new'))
    
    return jsonify({
        "success": True,
        "message": f"총 {len(musics)}곡 가져옴 (신규 {new_count}곡 저장)",
        "data": musics
    }), 200


def get_preview_url():
    """실시간으로 Deezer에서 preview URL 가져오기"""
    track_name = request.args.get('track')
    artist_name = request.args.get('artist')
    
    if not track_name or not artist_name:
        return jsonify({"success": False, "message": "track과 artist 파라미터가 필요합니다."}), 400
    
    preview_url, error = music_service.get_fresh_preview_url(track_name, artist_name)
    
    if error:
        return jsonify({"success": False, "message": error}), 404
    
    return jsonify({
        "success": True,
        "preview_url": preview_url
    }), 200
