from db import get_connection


def find_by_spotify_url(spotify_url):
    """spotify_url로 중복 체크"""
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM music WHERE spotify_url = %s", (spotify_url,))
            return c.fetchone()
    finally:
        conn.close()


def insert_music(m):
    conn = get_connection()
    try:
        with conn.cursor() as c:
            sql = """
            INSERT INTO music
            (track_name, artist_name, album_name, album_image_url,
             duration_ms, popularity, spotify_url, genre_no, preview_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            c.execute(sql, (
                m['track_name'],
                m['artist_name'],
                m['album_name'],
                m['album_image_url'],
                m['duration_ms'],
                m['popularity'],
                m['spotify_url'],
                m['genre_no'],
                m.get('preview_url')
            ))
            conn.commit()
            print(f"  ✅ 저장: {m['track_name']}")
            return c.lastrowid
    except Exception as e:
        print(f"  ❌ 저장 실패: {m['track_name']} - {e}")
        return None
    finally:
        conn.close()


def find_all(category=None, value=None):
    conn = get_connection()
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
    conn = get_connection()
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
    conn = get_connection()
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
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT * FROM music WHERE spotify_track_id = %s",
                (track_id,)
            )
            return c.fetchone()
    finally:
        conn.close()


def update_preview_url(music_no, preview_url):
    """기존 음악의 preview_url 업데이트"""
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute(
                "UPDATE music SET preview_url = %s WHERE music_no = %s",
                (preview_url, music_no)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"preview_url 업데이트 실패: {e}")
        return False
    finally:
        conn.close()
