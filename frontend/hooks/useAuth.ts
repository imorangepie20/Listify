import { useState, useEffect } from 'react';
import { User } from '../types';
import { logout as logoutApi, getToken, verifyToken } from '../services/authService';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [authView, setAuthView] = useState<'login' | 'register' | null>('login');

  // 자동 로그인 체크
  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      if (token) {
        const response = await verifyToken(token);
        if (response.success && response.data) {
          const nickname = localStorage.getItem('nickname') || 'User';
          const userNo = parseInt(localStorage.getItem('user_no') || '0');
          setUser({
            user_no: userNo,
            role_no: response.data.role_no,
            email: '',
            nickname: nickname,
            profile_url: null,
            created_at: new Date().toISOString()
          });
          setAuthView(null);
        }
      }
    };
    checkAuth();
  }, []);

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
    handleLogout
  };
};
