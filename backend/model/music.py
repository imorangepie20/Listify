from db import connect_to_mysql
import os
import pymysql

def get_conn():
    conn = connect_to_mysql(
        os.getenv("DB_HOST"),
        int(os.getenv("DB_PORT")),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_DATABASE")
    )

    if conn is None:
        raise RuntimeError(
            f"DB 연결 실패 - "
            f"HOST={os.getenv('DB_HOST')}, "
            f"PORT={os.getenv('DB_PORT')}, "
            f"USER={os.getenv('DB_USER')}, "
            f"DB={os.getenv('DB_DATABASE')}"
        )

    return conn


def find_by_spotify_url(spotify_url):
    """spotify_url로 중복 체크"""
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM music WHERE spotify_url = %s", (spotify_url,))
            return c.fetchone()
    finally:
        conn.close()


def insert_music(m):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            sql = """
            INSERT INTO music
            (track_name, artist_name, album_name, album_image_url,
             duration_ms, popularity, spotify_url, genre_no)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """
            c.execute(sql, (
                m['track_name'],
                m['artist_name'],
                m['album_name'],
                m['album_image_url'],
                m['duration_ms'],
                m['popularity'],
                m['spotify_url'],
                m['genre_no']
            ))
            conn.commit()
            print(f" 저장 성공: {m['track_name']}")  # 디버그 로그
            return c.lastrowid
    except Exception as e:
        print(f" 저장 실패: {m['track_name']} - {e}")  # 에러 로그
        return None
    finally:
        conn.close()

def find_all(category=None, value=None):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            if category == "genre":
                sql = """
                SELECT m.*
                FROM music m
                JOIN genre g ON m.genre_no = g.genre_no
                WHERE g.name = %s
                ORDER BY m.popularity DESC
                """
                c.execute(sql, (value,))
            else:
                c.execute("SELECT * FROM music ORDER BY popularity DESC")
            return c.fetchall()
    finally:
        conn.close()


def find_by_genre(genre_name):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            sql = """
            SELECT m.*
            FROM music m
            JOIN genre g ON m.genre_no = g.genre_no
            WHERE g.name = %s
            ORDER BY m.popularity DESC
            """
            c.execute(sql, (genre_name,))
            return c.fetchall()
    finally:
        conn.close()


def find_genre_no_by_name(name):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT genre_no FROM genre WHERE name = %s",
                (name,)
            )
            row = c.fetchone()
            return row['genre_no'] if row else None
    finally:
        conn.close()
        
def find_by_spotify_track_id(track_id):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT * FROM music WHERE spotify_track_id = %s",
                (track_id,)
            )
            return c.fetchone()
    finally:
        conn.close()
