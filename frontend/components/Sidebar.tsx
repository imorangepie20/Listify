import React from 'react';
import { AppView } from '../types';
import { Home, Library, Search as SearchIcon, User as UserIcon, Bell, LogOut, Settings, Plus, Music as MusicIcon } from 'lucide-react';

interface SidebarProps {
  view: AppView;
  onViewChange: (view: AppView) => void;
  cartCount: number;
  onOpenCart: () => void;
  onOpenSettings: () => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  view,
  onViewChange,
  cartCount,
  onOpenCart,
  onOpenSettings,
  onLogout
}) => {
  const menuItems = [
    { id: 'home' as AppView, icon: Home, label: '홈' },
    { id: 'search' as AppView, icon: SearchIcon, label: '탐색' },
    { id: 'library' as AppView, icon: Library, label: '라이브러리' },
    { id: 'profile' as AppView, icon: UserIcon, label: '프로필' },
    { id: 'notices' as AppView, icon: Bell, label: '공지사항' }
  ];

  return (
    <aside className="w-64 bg-zinc-950 border-r border-zinc-800 flex flex-col z-20">
      <div className="p-6 flex items-center gap-2 text-primary">
        <MusicIcon className="w-8 h-8" />
        <span className="text-xl font-bold tracking-tight">Listify</span>
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        {menuItems.map((item) => (
          <button 
            key={item.id}
            onClick={() => onViewChange(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              view === item.id 
              ? 'bg-zinc-900 text-primary font-bold shadow-inner' 
              : 'text-zinc-400 hover:text-white hover:bg-zinc-900/50'
            }`}
          >
            <item.icon className="w-5 h-5" /> {item.label}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-zinc-800 space-y-2">
        <button 
          onClick={onOpenCart}
          className="w-full flex items-center justify-between px-4 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors text-sm border border-primary/20"
        >
          <span className="flex items-center gap-2 font-medium">
            <Plus className="w-4 h-4" /> 장바구니
          </span>
          <span className="bg-primary text-black text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center">
            {cartCount}
          </span>
        </button>
        <button 
          onClick={onOpenSettings} 
          className="w-full flex items-center gap-3 px-4 py-2 text-zinc-500 hover:text-white text-sm transition-colors"
        >
          <Settings className="w-4 h-4" /> 설정
        </button>
        <button 
          onClick={onLogout} 
          className="w-full flex items-center gap-3 px-4 py-2 text-zinc-500 hover:text-red-400 text-sm transition-colors"
        >
          <LogOut className="w-4 h-4" /> 로그아웃
        </button>
      </div>
    </aside>
  );
};
