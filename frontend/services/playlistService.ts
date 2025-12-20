import { api } from './api';
import { getToken } from './authService';

export const getUserPlaylists = async (userNo: number) => {
  const token = getToken();
  if (!token) throw new Error('로그인이 필요합니다.');
  
  return await api.get(`/playlist/user/${userNo}`, token);
};
