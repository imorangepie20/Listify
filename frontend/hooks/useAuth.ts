import { useState, useEffect } from 'react';
import { User } from '../types';
import { verifyToken, logout as logoutApi, getToken } from '../services/authService';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [authView, setAuthView] = useState<'login' | 'register' | null>('login');

  // 🔁 새로고침 시 자동 로그인
  useEffect(() => {
    const token = getToken();
    if (!token) return;

    const checkAuth = async () => {
      try {
        const response = await verifyToken(token);
        if (response.success && response.data) {
          const data = response.data as any;
          setUser({
            user_no: data.user_no ?? parseInt(localStorage.getItem('user_no') || '0'),
            role_no: data.role_no ?? 1,
            email: data.email ?? '',
            nickname: data.nickname ?? localStorage.getItem('nickname') ?? 'User',
            profile_url: data.profile_url ?? null,
            created_at: data.created_at ?? new Date().toISOString(),
          });
          setAuthView(null);
        } else {
          handleLogout();
        }
      } catch {
        handleLogout();
      }
    };

    checkAuth();
  }, []);

  // ✅ 로그인 성공 시 (Login.tsx에서 호출)
  const handleLoginSuccess = (userNo: number, nickname: string) => {
    setUser({
      user_no: userNo,
      role_no: 1,
      email: '',
      nickname: nickname,
      profile_url: null,
      created_at: new Date().toISOString()
    });
    setAuthView(null);
  };

  const handleLogout = () => {
    logoutApi();
    setUser(null);
    setAuthView('login');
  };

  return {
    user,
    authView,
    setAuthView,
    handleLoginSuccess,
    handleLogout,
  };
};
