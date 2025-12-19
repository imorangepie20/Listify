from flask import Blueprint
from controllers import auth as auth_controller

# Blueprint 등록
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# POST /auth/register - 회원가입
@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입"""
    return auth_controller.register()

# POST /auth/login - 로그인
@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인"""
    return auth_controller.login()

# GET /auth/verify - JWT 토큰 검증
@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """JWT 토큰 검증"""
    return auth_controller.verify_token()

