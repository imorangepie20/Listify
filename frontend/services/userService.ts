// frontend/services/userService.ts
import { api } from './api';

export const getUserProfile = async (userNo: number) => {
  return await api.get(`/users/${userNo}/profile`);
};

export const updateUserProfile = async (userNo: number, nickname: string) => {
  return await api.put(`/users/${userNo}/profile`, { nickname });
};

export const deleteAccount = async (userNo: number) => {
  return await api.delete(`/users/${userNo}`);
};
