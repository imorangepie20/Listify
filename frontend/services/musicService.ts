// frontend/services/musicService.ts
import { API_URL } from '../constants';
import { Music } from '../types';
import { getToken } from './authService';

interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
}

const authFetch = async (endpoint: string): Promise<ApiResponse<any>> => {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${endpoint}`, { headers });
  return res.json();
};

// 음악 검색 (카테고리 옵션 포함)
export const searchMusic = (q: string, category?: string) => {
  let url = `/music/search?q=${encodeURIComponent(q)}`;
  if (category) {
    url += `&category=${encodeURIComponent(category)}`;
  }
  return authFetch(url);
};

// 전체 음악 조회
export const getAllMusic = () =>
  authFetch('/music');

// 장르별 음악 조회
export const getMusicByGenre = (genre: string) =>
  authFetch(`/music?category=genre&value=${encodeURIComponent(genre)}`);

// Top 50 음악 조회
export const getTop50Music = () =>
  authFetch('/music/top50');
