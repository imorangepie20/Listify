from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from flask_cors import CORS

from routes.auth import auth_bp
from routes.notice import notice_bp
from routes.user import user_bp
from routes.playlist import playlist_bp          
from routes.music_list import music_list_bp   
from routes.music import music_bp   


load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


# Blueprint 등록
app.register_blueprint(auth_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(user_bp)
app.register_blueprint(playlist_bp) 
app.register_blueprint(music_list_bp) 
app.register_blueprint(music_bp)

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

@app.route('/test_api.html')
def serve_test_page():
    return send_from_directory(BASE_DIR, 'test_api.html')


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
    print("Test: http://localhost:5001/test")
    print("Health: http://localhost:5001/health")
    
    app.run(host='0.0.0.0', port=5001, debug=True)