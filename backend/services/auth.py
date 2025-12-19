import bcrypt
import jwt
import os
import re
from datetime import datetime, timedelta
from model import auth as auth_model

# JWT 설정
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
JWT_ALGORITHM = 'HS256'

def hash_password(password):
    """비밀번호 해싱"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """비밀번호 검증"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_email(email):
    """이메일 형식 검증"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """비밀번호 조건 검증"""
    if len(password) < 6:
        return False, "비밀번호는 6자 이상이어야 합니다."

    if len(password) > 30:
        return False, "비밀번호는 30자 이하여야 합니다."

    # 영문, 숫자, 특수문자 중 2가지 이상 포함
    has_alpha = bool(re.search(r'[a-zA-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    if sum([has_alpha, has_digit, has_special]) < 2:
        return False, "비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 포함해야 합니다."

    return True, "비밀번호가 유효합니다."

def validate_nickname(nickname):
    """닉네임 검증"""
    if not nickname or len(nickname.strip()) == 0:
        return False, "닉네임을 입력해주세요."

    if len(nickname) > 30:
        return False, "닉네임은 30자 이하여야 합니다."

    return True, "닉네임이 유효합니다."

def register_user(email, password, nickname):
    """회원가입 처리"""
    # 입력값 검증
    if not validate_email(email):
        return False, "올바른 이메일 형식이 아닙니다."

    is_valid_password, password_message = validate_password(password)
    if not is_valid_password:
        return False, password_message

    is_valid_nickname, nickname_message = validate_nickname(nickname)
    if not is_valid_nickname:
        return False, nickname_message

    # 이메일 중복 검사
    existing_user = auth_model.find_user_by_email(email)
    if existing_user:
        return False, "이미 가입된 이메일입니다."

    # 비밀번호 해싱
    password_hash = hash_password(password)

    # 사용자 생성 (기본 role_no = 1: 일반 사용자)
    success = auth_model.create_user(1, email, password_hash, nickname.strip())

    if success:
        return True, "회원가입이 완료되었습니다."
    else:
        return False, "회원가입에 실패했습니다."

def login_user(email, password):
    """로그인 처리"""
    # 입력값 검증
    if not email or not password:
        return False, "이메일과 비밀번호를 입력해주세요.", None

    # 사용자 조회
    user = auth_model.find_user_by_email(email)
    if not user:
        return False, "존재하지 않는 사용자입니다.", None

    # 비밀번호 검증
    if not verify_password(password, user['password']):
        return False, "비밀번호가 일치하지 않습니다.", None

    # JWT 토큰 생성
    token = generate_jwt_token(user['user_no'], user['role_no'])

    return True, "로그인 성공", token

def generate_jwt_token(user_no, role_no):
    """JWT 토큰 생성"""
    payload = {
        'user_no': user_no,
        'role_no': role_no,
        'exp': datetime.utcnow() + timedelta(hours=24)  # 24시간 유효
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "토큰이 만료되었습니다."
    except jwt.InvalidTokenError:
        return False, "유효하지 않은 토큰입니다."

