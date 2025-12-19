# -*- coding: utf-8 -*-
from model import music_list as music_list_model


def add_music_to_playlist(playlist_no: int, music_no: int):
    """플레이리스트에 음악 추가"""
    # 이미 존재하는지 확인
    if music_list_model.exists(playlist_no, music_no):
        return False, "이미 플레이리스트에 추가된 음악입니다."
    
    try:
        success = music_list_model.insert_music_to_playlist(playlist_no, music_no)
        if success:
            return True, "음악이 플레이리스트에 추가되었습니다."
        return False, "음악 추가에 실패했습니다."
    except Exception as e:
        return False, str(e)


def remove_music_from_playlist(playlist_no: int, music_no: int):
    """플레이리스트에서 음악 삭제"""
    # 존재하는지 확인
    if not music_list_model.exists(playlist_no, music_no):
        return False, "플레이리스트에 해당 음악이 없습니다."
    
    try:
        success = music_list_model.delete_music_from_playlist(playlist_no, music_no)
        if success:
            return True, "음악이 플레이리스트에서 삭제되었습니다."
        return False, "음악 삭제에 실패했습니다."
    except Exception as e:
        return False, str(e)


def clear_playlist(playlist_no: int):
    """플레이리스트의 모든 음악 삭제"""
    try:
        success = music_list_model.delete_all_music_from_playlist(playlist_no)
        if success:
            return True, "플레이리스트의 모든 음악이 삭제되었습니다."
        return False, "음악 삭제에 실패했습니다."
    except Exception as e:
        return False, str(e)


def get_playlist_music_list(playlist_no: int):
    """플레이리스트의 음악 목록 조회"""
    try:
        music_list = music_list_model.find_by_playlist_no(playlist_no)
        return music_list, None
    except Exception as e:
        return None, str(e)


def get_playlists_by_music(music_no: int):
    """특정 음악이 포함된 플레이리스트 목록 조회"""
    try:
        playlists = music_list_model.find_by_music_no(music_no)
        return playlists, None
    except Exception as e:
        return None, str(e)


def get_music_count(playlist_no: int):
    """플레이리스트의 음악 개수 조회"""
    try:
        count = music_list_model.count_by_playlist_no(playlist_no)
        return count, None
    except Exception as e:
        return None, str(e)


def check_music_exists(playlist_no: int, music_no: int):
    """플레이리스트에 음악이 존재하는지 확인"""
    try:
        exists = music_list_model.exists(playlist_no, music_no)
        return exists, None
    except Exception as e:
        return None, str(e)
