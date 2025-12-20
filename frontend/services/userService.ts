import { api } from './api';
import { getToken } from './authService';

export const getUserProfile = async (userNo: number) => {
  const token = getToken();
  if (!token) throw new Error('로그인이 필요합니다.');
  
  return await api.get(`/users/${userNo}/profile`, token);
};

export const updateUserProfile = async (userNo: number, nickname: string) => {
  const token = getToken();
  if (!token) throw new Error('로그인이 필요합니다.');
  
  return await api.put(`/users/${userNo}/profile`, { nickname }, token);
};

export const deleteAccount = async (userNo: number) => {
  const token = getToken();
  if (!token) throw new Error('로그인이 필요합니다.');
  
  return await api.delete(`/users/${userNo}`, token);
};
