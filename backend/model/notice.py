from db import connect_to_mysql
import os


def get_connection():
    """데이터베이스 연결"""
    return connect_to_mysql(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '1234'),
        database=os.getenv('DB_DATABASE', 'listify')
    )


def insert_notice(user_no: int, title: str, content: str) -> int:
    """공지 생성, 생성된 notice_no 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "INSERT INTO notice (user_no, title, content, created_at, updated_at)"
                " VALUES (%s, %s, %s, NOW(), NOW())"
            )
            cursor.execute(sql, (user_no, title, content))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_notice(notice_no: int, title: str, content: str) -> bool:
    """공지 수정, 성공 여부 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "UPDATE notice SET title=%s, content=%s, updated_at=NOW()"
                " WHERE notice_no=%s"
            )
            cursor.execute(sql, (title, content, notice_no))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_notice(notice_no: int) -> bool:
    """공지 삭제, 성공 여부 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM notice WHERE notice_no=%s"
            cursor.execute(sql, (notice_no,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def find_by_notice_no(notice_no: int):
    """단건 조회 (원본 notice 테이블)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM notice WHERE notice_no = %s"
            cursor.execute(sql, (notice_no,))
            return cursor.fetchone()
    finally:
        conn.close()


def list_all_with_user():
    """리스트 조회(작성자 닉네임 포함) - content 제외"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT n.notice_no, n.user_no, n.title,"
                " n.created_at, n.updated_at, u.nickname"
                " FROM notice n LEFT JOIN user u ON n.user_no = u.user_no"
                " ORDER BY n.created_at DESC"
            )
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def find_detail_with_user(notice_no: int):
    """상세 조회(작성자 닉네임 포함)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT n.notice_no, n.user_no, n.title, n.content,"
                " n.created_at, n.updated_at, u.nickname"
                " FROM notice n LEFT JOIN user u ON n.user_no = u.user_no"
                " WHERE n.notice_no = %s"
            )
            cursor.execute(sql, (notice_no,))
            return cursor.fetchone()
    finally:
        conn.close()
