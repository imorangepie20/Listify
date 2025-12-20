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


def insert_music(spotify_track_id, track_name, artist_name, album_name,
                 album_image_url, duration_ms, popularity, spotify_url,
                 release_date=None, release_year=None, genre_no=None):
    """음악 정보 저장"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO music (
                    spotify_track_id, track_name, artist_name, album_name,
                    album_image_url, duration_ms, popularity, spotify_url,
                    release_date, release_year, genre_no
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                spotify_track_id, track_name, artist_name, album_name,
                album_image_url, duration_ms, popularity, spotify_url,
                release_date, release_year, genre_no
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error inserting music: {e}")
        return None
    finally:
        conn.close()


def find_by_spotify_track_id(spotify_track_id):
    """Spotify Track ID로 음악 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM music WHERE spotify_track_id = %s"
            cursor.execute(sql, (spotify_track_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def find_by_music_no(music_no):
    """Music No로 음악 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM music WHERE music_no = %s"
            cursor.execute(sql, (music_no,))
            return cursor.fetchone()
    finally:
        conn.close()


def search_music(query, limit=20):
    """음악 검색 (track_name, artist_name, album_name)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM music
                WHERE track_name LIKE %s
                   OR artist_name LIKE %s
                   OR album_name LIKE %s
                ORDER BY popularity DESC
                LIMIT %s
            """
            search_pattern = f"%{query}%"
            cursor.execute(sql, (search_pattern, search_pattern, search_pattern, limit))
            return cursor.fetchall()
    finally:
        conn.close()


def list_all(limit=50, offset=0):
    """전체 음악 목록 조회 (페이지네이션)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM music
                ORDER BY created_at DESC, popularity DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (limit, offset))
            return cursor.fetchall()
    finally:
        conn.close()


def list_by_artist(artist_name, limit=50):
    """아티스트별 음악 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM music
                WHERE artist_name LIKE %s
                ORDER BY popularity DESC
                LIMIT %s
            """
            cursor.execute(sql, (f"%{artist_name}%", limit))
            return cursor.fetchall()
    finally:
        conn.close()


def list_by_genre(genre_no, limit=50):
    """장르별 음악 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM music
                WHERE genre_no = %s
                ORDER BY popularity DESC
                LIMIT %s
            """
            cursor.execute(sql, (genre_no, limit))
            return cursor.fetchall()
    finally:
        conn.close()


def list_by_year(year, limit=50):
    """연도별 음악 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT * FROM music
                WHERE release_year = %s
                ORDER BY popularity DESC
                LIMIT %s
            """
            cursor.execute(sql, (year, limit))
            return cursor.fetchall()
    finally:
        conn.close()


def count_all():
    """전체 음악 개수"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM music"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['count'] if result else 0
    finally:
        conn.close()


def delete_music(music_no):
    """음악 삭제"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM music WHERE music_no = %s"
            cursor.execute(sql, (music_no,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
