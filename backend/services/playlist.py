from model import playlist as playlist_model


def create_playlist(user_no: int, title: str, content: str = None):
    """플레이리스트 생성"""
    # 제목 유효성 검사
    if not title or len(title.strip()) == 0:
        return None, "제목을 입력해주세요."
    
    if len(title) > 40:
        return None, "제목은 40자 이하로 입력해주세요."
    
    try:
        playlist_no = playlist_model.insert_playlist(user_no, title.strip(), content)
        return playlist_no, None
    except Exception as e:
        return None, str(e)


def update_playlist(playlist_no: int, title: str, content: str = None):
    """플레이리스트 수정"""
    # 제목 유효성 검사
    if not title or len(title.strip()) == 0:
        return False, "제목을 입력해주세요."
    
    if len(title) > 40:
        return False, "제목은 40자 이하로 입력해주세요."
    
    try:
        success = playlist_model.update_playlist(playlist_no, title.strip(), content)
        if success:
            return True, "플레이리스트 수정 완료"
        return False, "플레이리스트 수정 실패"
    except Exception as e:
        return False, str(e)


def delete_playlist(playlist_no: int):
    """플레이리스트 삭제"""
    try:
        success = playlist_model.delete_playlist(playlist_no)
        if success:
            return True, "플레이리스트 삭제 완료"
        return False, "플레이리스트 삭제 실패"
    except Exception as e:
        return False, str(e)


def get_playlist_list():
    """전체 플레이리스트 목록 조회"""
    try:
        playlists = playlist_model.list_all_with_user()
        for p in playlists:
            if p.get('created_at'):
                p['created_at'] = p['created_at'].isoformat() if hasattr(p['created_at'], 'isoformat') else str(p['created_at'])
            if p.get('updated_at'):
                p['updated_at'] = p['updated_at'].isoformat() if hasattr(p['updated_at'], 'isoformat') else str(p['updated_at'])
        return playlists, None
    except Exception as e:
        return None, str(e)


def get_user_playlist_list(user_no: int):
    """특정 유저의 플레이리스트 목록 조회"""
    try:
        playlists = playlist_model.list_by_user_no(user_no)
        for p in playlists:
            if p.get('created_at'):
                p['created_at'] = p['created_at'].isoformat() if hasattr(p['created_at'], 'isoformat') else str(p['created_at'])
            if p.get('updated_at'):
                p['updated_at'] = p['updated_at'].isoformat() if hasattr(p['updated_at'], 'isoformat') else str(p['updated_at'])
        return playlists, None
    except Exception as e:
        return None, str(e)


def get_playlist_detail(playlist_no: int):
    """플레이리스트 상세 조회"""
    try:
        playlist = playlist_model.find_detail_with_user(playlist_no)
        if not playlist:
            return None, "존재하지 않는 플레이리스트"
        if playlist.get('created_at'):
            playlist['created_at'] = playlist['created_at'].isoformat() if hasattr(playlist['created_at'], 'isoformat') else str(playlist['created_at'])
        if playlist.get('updated_at'):
            playlist['updated_at'] = playlist['updated_at'].isoformat() if hasattr(playlist['updated_at'], 'isoformat') else str(playlist['updated_at'])
        return playlist, None
    except Exception as e:
        return None, str(e)


def find_playlist_by_no(playlist_no: int):
    """playlist_no로 플레이리스트 조회"""
    try:
        playlist = playlist_model.find_by_playlist_no(playlist_no)
        return playlist, None
    except Exception as e:
        return None, str(e)
