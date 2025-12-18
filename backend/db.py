import pymysql

def connect_to_mysql(host, port, user, password, database):
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"MySQL 데이터베이스 '{database}'에 성공적으로 연결되었습니다.")
        return conn
    except pymysql.MySQLError as e:
        print(f"MySQL 연결 오류: {e}")
        return None

if __name__ == '__main__':
    DB_HOST = "localhost" 
    DB_PORT = 3306
    DB_USER = "root" 
    DB_PASSWORD = "1234"
    DB_DATABASE = "listify"

    conn = connect_to_mysql(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)

    if conn:
        try:
            with conn.cursor() as cursor:
                sql = "SELECT VERSION()"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(f"MariaDB 버전: {result}")
        except pymysql.MySQLError as e:
            print(f"데이터베이스 작업 오류: {e}")
        finally:
            if conn:
                conn.close()
                print("MariaDB 연결이 종료되었습니다.")
