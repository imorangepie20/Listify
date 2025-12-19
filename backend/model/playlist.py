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


def insert_playlist(user_no: int, title: str, content: str = None) -> int:
    """플레이리스트 생성, 생성된 playlist_no 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "INSERT INTO playlist (user_no, title, content, created_at, updated_at)"
                " VALUES (%s, %s, %s, NOW(), NOW())"
            )
            cursor.execute(sql, (user_no, title, content))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_playlist(playlist_no: int, title: str, content: str = None) -> bool:
    """플레이리스트 수정, 성공 여부 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "UPDATE playlist SET title=%s, content=%s, updated_at=NOW()"
                " WHERE playlist_no=%s"
            )
            cursor.execute(sql, (title, content, playlist_no))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_playlist(playlist_no: int) -> bool:
    """플레이리스트 삭제, 성공 여부 반환"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM playlist WHERE playlist_no=%s"
            cursor.execute(sql, (playlist_no,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def find_by_playlist_no(playlist_no: int):
    """단건 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM playlist WHERE playlist_no = %s"
            cursor.execute(sql, (playlist_no,))
            return cursor.fetchone()
    finally:
        conn.close()


def list_all_with_user():
    """전체 리스트 조회 (작성자 닉네임 포함)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT p.playlist_no, p.user_no, p.title, p.content,"
                " p.created_at, p.updated_at, u.nickname"
                " FROM playlist p LEFT JOIN user u ON p.user_no = u.user_no"
                " ORDER BY p.created_at DESC"
            )
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def list_by_user_no(user_no: int):
    """특정 유저의 플레이리스트 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT playlist_no, user_no, title, content, created_at, updated_at"
                " FROM playlist WHERE user_no = %s"
                " ORDER BY created_at DESC"
            )
            cursor.execute(sql, (user_no,))
            return cursor.fetchall()
    finally:
        conn.close()


def find_detail_with_user(playlist_no: int):
    """상세 조회 (작성자 닉네임 포함)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT p.playlist_no, p.user_no, p.title, p.content,"
                " p.created_at, p.updated_at, u.nickname"
                " FROM playlist p LEFT JOIN user u ON p.user_no = u.user_no"
                " WHERE p.playlist_no = %s"
            )
            cursor.execute(sql, (playlist_no,))
            return cursor.fetchone()
    finally:
        conn.close()
