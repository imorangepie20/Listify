from flask import request, jsonify
from services import user as user_service

def get_profile(user_no):
    """프로필 조회"""
    user, error = user_service.get_profile(user_no)
    
    if error:
        return jsonify({"success": False, "message": error}), 404
    
    return jsonify({
        "success": True,
        "data": {
            "user_no": user["user_no"],
            "email": user["email"],
            "nickname": user["nickname"],
            "profile_url": user["profile_url"],
            "created_at": user["created_at"].isoformat() if user["created_at"] else None,
            "updated_at": user["updated_at"].isoformat() if user["updated_at"] else None
        }
    }), 200

def update_profile(user_no):
    """프로필 수정 (닉네임)"""
    data = request.get_json()
    
    if not data or "nickname" not in data:
        return jsonify({"success": False, "message": "nickname 필드가 필요합니다."}), 400
    
    success, message = user_service.update_nickname(user_no, data["nickname"])
    
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400

def delete_account(user_no):
    """계정 탈퇴"""
    success, message = user_service.delete_account(user_no)
    
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400