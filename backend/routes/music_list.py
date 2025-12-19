# -*- coding: utf-8 -*-
from flask import Blueprint
from controllers import music_list as music_list_controller

music_list_bp = Blueprint('music_list', __name__, url_prefix='/playlist')


@music_list_bp.route('/<int:playlist_no>/music', methods=['POST'])
def add_music(playlist_no):
    """플레이리스트에 음악 추가"""
    return music_list_controller.add_music(playlist_no)


@music_list_bp.route('/<int:playlist_no>/music', methods=['GET'])
def get_music_list(playlist_no):
    """플레이리스트의 음악 목록 조회"""
    return music_list_controller.get_music_list(playlist_no)


@music_list_bp.route('/<int:playlist_no>/music/<int:music_no>', methods=['DELETE'])
def remove_music(playlist_no, music_no):
    """플레이리스트에서 음악 삭제"""
    return music_list_controller.remove_music(playlist_no, music_no)


@music_list_bp.route('/<int:playlist_no>/music', methods=['DELETE'])
def clear_playlist(playlist_no):
    """플레이리스트의 모든 음악 삭제"""
    return music_list_controller.clear_playlist(playlist_no)


@music_list_bp.route('/by-music/<int:music_no>', methods=['GET'])
def get_playlists_by_music(music_no):
    """특정 음악이 포함된 플레이리스트 목록 조회"""
    return music_list_controller.get_playlists_by_music(music_no)
