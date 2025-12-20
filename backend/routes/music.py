from flask import Blueprint
from controllers import music as music_controller

music_bp = Blueprint('music', __name__, url_prefix='/music')


@music_bp.route('/search', methods=['GET'])
def search_music():
    return music_controller.search_music()


@music_bp.route('', methods=['GET'])
def get_music_list():
    return music_controller.get_music_list()


@music_bp.route('/top50', methods=['GET'])
def get_global_top_50():
    return music_controller.get_global_top_50()

@music_bp.route('/bulk-import', methods=['POST'])
def bulk_import():
    return music_controller.bulk_import()

