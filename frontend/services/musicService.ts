// frontend/services/musicService.ts
import { API_URL } from '../constants';
import { Music } from '../types';
import { getToken } from './authService';

interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
}


// 공통 fetch (JWT 포함)
const authFetch = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {})

  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });
};

// 🔍 Spotify 검색 (가수 / 곡 / 앨범)
export const searchMusic = async (
  keyword: string
): Promise<ApiResponse<Music[]>> => {
  try {
    const res = await authFetch(
      `/music/search?q=${encodeURIComponent(keyword)}`
    );
    return await res.json();
  } catch (e) {
    return { success: false, message: '음악 검색 실패' };
  }
};

// 📚 전체 음악 조회
export const getAllMusic = async (): Promise<ApiResponse<Music[]>> => {
  try {
    const res = await authFetch('/music');
    return await res.json();
  } catch (e) {
    return { success: false, message: '음악 목록 조회 실패' };
  }
};

// 🔥 장르 검색 (DB)
export const getMusicByGenre = async (
  genre: string
): Promise<ApiResponse<Music[]>> => {
  try {
    const res = await authFetch(
      `/music?category=genre&value=${encodeURIComponent(genre)}`
    );
    return await res.json();
  } catch (e) {
    return { success: false, message: '장르 검색 실패' };
  }
};

// 🌍 Top 50
export const getTop50Music = async (): Promise<ApiResponse<Music[]>> => {
  try {
    const res = await authFetch('/music/top50');
    return await res.json();
  } catch (e) {
    return { success: false, message: 'Top 50 조회 실패' };
  }
};

