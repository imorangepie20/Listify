# -*- coding: utf-8 -*-
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


def insert_music_to_playlist(playlist_no: int, music_no: int) -> bool:
    """플레이리스트에 음악 추가"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO music_list (playlist_no, music_no) VALUES (%s, %s)"
            cursor.execute(sql, (playlist_no, music_no))
            conn.commit()
            return True
    except Exception:
        return False
    finally:
        conn.close()


def delete_music_from_playlist(playlist_no: int, music_no: int) -> bool:
    """플레이리스트에서 음악 삭제"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM music_list WHERE playlist_no = %s AND music_no = %s"
            cursor.execute(sql, (playlist_no, music_no))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_all_music_from_playlist(playlist_no: int) -> bool:
    """플레이리스트의 모든 음악 삭제"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM music_list WHERE playlist_no = %s"
            cursor.execute(sql, (playlist_no,))
            conn.commit()
            return True
    finally:
        conn.close()


def find_by_playlist_no(playlist_no: int):
    """플레이리스트의 음악 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT ml.playlist_no, ml.music_no, m.title, m.artist, m.album, m.duration
                FROM music_list ml
                LEFT JOIN music m ON ml.music_no = m.music_no
                WHERE ml.playlist_no = %s
            """
            cursor.execute(sql, (playlist_no,))
            return cursor.fetchall()
    finally:
        conn.close()


def find_by_music_no(music_no: int):
    """특정 음악이 포함된 플레이리스트 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT ml.playlist_no, ml.music_no, p.title as playlist_title
                FROM music_list ml
                LEFT JOIN playlist p ON ml.playlist_no = p.playlist_no
                WHERE ml.music_no = %s
            """
            cursor.execute(sql, (music_no,))
            return cursor.fetchall()
    finally:
        conn.close()


def exists(playlist_no: int, music_no: int) -> bool:
    """플레이리스트에 음악이 존재하는지 확인"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT 1 FROM music_list WHERE playlist_no = %s AND music_no = %s"
            cursor.execute(sql, (playlist_no, music_no))
            return cursor.fetchone() is not None
    finally:
        conn.close()


def count_by_playlist_no(playlist_no: int) -> int:
    """플레이리스트의 음악 개수 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM music_list WHERE playlist_no = %s"
            cursor.execute(sql, (playlist_no,))
            result = cursor.fetchone()
            return result['count'] if result else 0
    finally:
        conn.close()
