from db import connect_to_mysql
import os

def get_connection():
    """DB 연결을 가져오는 함수"""
    return connect_to_mysql(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_DATABASE', 'listify')
    )

def find_user_by_email(email):
    """이메일로 사용자 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT user_no, role_no, email, password, nickname, profile_url, created_at, updated_at
                FROM user
                WHERE email = %s AND is_deleted = FALSE
            """
            cursor.execute(sql, (email,))
            return cursor.fetchone()
    finally:
        conn.close()

def create_user(role_no, email, password_hash, nickname):
    """회원가입 - 새로운 사용자 생성"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO user (role_no, email, password, nickname)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (role_no, email, password_hash, nickname))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()

def authenticate_user(email, password_hash):
    """로그인 검증 - 이메일과 비밀번호 해시로 사용자 확인"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT user_no, role_no, email, nickname, profile_url
                FROM user
                WHERE email = %s AND password = %s AND is_deleted = FALSE
            """
            cursor.execute(sql, (email, password_hash))
            return cursor.fetchone()
    finally:
        conn.close()

