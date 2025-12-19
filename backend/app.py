from flask import Flask
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(auth_bp)

# Spotify 인증
client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 기본 라우트
@app.route('/')
def index():
    return {
        'message': 'Listify Spotify API',
        'version': 'v1.0.0',
        'endpoints': {
            'test': '/test',
            'health': '/health',
            'auth': {
                'register': '/auth/register',
                'login': '/auth/login',
                'verify': '/auth/verify'
            }
        }
    }

@app.route('/test')
def test():
    return {'message': 'hello'}

@app.route('/health')
def health():
    from db import connect_to_mysql
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_DATABASE = os.getenv('DB_DATABASE', 'listify')
    
    conn = connect_to_mysql(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
            
            return {
                'status': 'healthy',
                'database': 'connected',
                'spotify': sp is not None,
                'version': version['VERSION()']
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'database': 'error',
                'message': str(e)
            }, 500
        finally:
            conn.close()
    else:
        return {
            'status': 'unhealthy',
            'database': 'disconnected'
        }, 500

if __name__ == '__main__':
    print("Test: http://localhost:5000/test")
    print("Health: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=5000, debug=True)