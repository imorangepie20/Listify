from model import user as user_model

def get_profile(user_no):
    """프로필 조회"""
    user = user_model.find_by_user_no(user_no)
    
    if not user:
        return None, "존재하지 않는 사용자입니다."
    
    return user, None

def update_nickname(user_no, nickname):
    """닉네임 수정"""
    # 유저 존재 확인
    user = user_model.find_by_user_no(user_no)
    if not user:
        return False, "존재하지 않는 사용자입니다."
    
    # 닉네임 유효성 검사
    if not nickname or len(nickname.strip()) == 0:
        return False, "닉네임을 입력해주세요."
    
    if len(nickname) > 30:
        return False, "닉네임은 30자 이하로 입력해주세요."
    
    # 닉네임 수정
    success = user_model.update_nickname(user_no, nickname.strip())
    
    if success:
        return True, "닉네임이 수정되었습니다."
    else:
        return False, "닉네임 수정에 실패했습니다."

def delete_account(user_no):
    """계정 탈퇴"""
    # 유저 존재 확인
    user = user_model.find_by_user_no(user_no)
    if not user:
        return False, "존재하지 않는 사용자입니다."
    
    # soft delete
    success = user_model.soft_delete(user_no)
    
    if success:
        return True, "계정이 탈퇴되었습니다."
    else:
        return False, "계정 탈퇴에 실패했습니다."