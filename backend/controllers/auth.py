from flask import request, jsonify
from services import auth as auth_service

def register():
    """회원가입"""
    data = request.get_json()

    if not data or "email" not in data or "password" not in data or "nickname" not in data:
        return jsonify({"success": False, "message": "이메일, 비밀번호, 닉네임을 모두 입력해주세요."}), 400

    success, message = auth_service.register_user(
        data["email"],
        data["password"],
        data["nickname"]
    )

    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 400

def login():
    """로그인"""
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"success": False, "message": "이메일과 비밀번호를 입력해주세요."}), 400

    success, message, token = auth_service.login_user(data["email"], data["password"])

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "data": {
                "access_token": token,
                "token_type": "Bearer"
            }
        }), 200
    else:
        return jsonify({"success": False, "message": message}), 401

def verify_token():
    """JWT 토큰 검증"""
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"success": False, "message": "Authorization 헤더가 없습니다."}), 401

    try:
        token = auth_header.split(' ')[1]  # "Bearer <token>"에서 토큰 추출
    except IndexError:
        return jsonify({"success": False, "message": "토큰 형식이 올바르지 않습니다."}), 401

    is_valid, result = auth_service.verify_jwt_token(token)

    if is_valid:
        return jsonify({
            "success": True,
            "message": "유효한 토큰입니다.",
            "data": {
                "user_no": result["user_no"],
                "role_no": result["role_no"]
            }
        }), 200
    else:
        return jsonify({"success": False, "message": result}), 401

