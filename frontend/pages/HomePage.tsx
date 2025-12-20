import React from 'react';
import { Music } from '../types';
import { Plus, Check } from 'lucide-react';

interface HomePageProps {
  songs: Music[];
  cart: Music[];
  onToggleCart: (song: Music) => void;
  onNavigateToSearch: () => void;
}

export const HomePage: React.FC<HomePageProps> = ({ songs, cart, onToggleCart, onNavigateToSearch }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="bg-gradient-to-br from-primary/30 via-zinc-900 to-black p-10 rounded-3xl border border-white/5 shadow-2xl">
        <h1 className="text-5xl font-extrabold mb-4 tracking-tight">Welcome to Listify</h1>
        <p className="text-zinc-400 text-lg max-w-lg leading-relaxed">
          당신만의 음악 장바구니를 채우고 완벽한 플레이리스트를 만들어보세요.
        </p>
        <button 
          onClick={onNavigateToSearch}
          className="mt-6 bg-white text-black px-6 py-3 rounded-full font-bold hover:scale-105 transition-transform"
        >
          음악 탐색하기
        </button>
      </div>

      <section>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold">인기 트랙</h3>
          <button className="text-zinc-400 hover:text-white text-sm font-medium">전체 보기</button>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {songs.slice(0, 10).map((song, i) => (
            <div key={i} className="bg-zinc-900/40 p-4 rounded-xl border border-zinc-800/50 hover:bg-zinc-800/60 hover:border-zinc-700 transition-all group relative">
              <div className="relative mb-3 aspect-square rounded-lg overflow-hidden">
                <img src={song.album_image_url} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                <button 
                  onClick={() => onToggleCart(song)}
                  className={`absolute bottom-2 right-2 p-2 rounded-full shadow-xl transition-all ${
                    cart.some(c => c.spotify_url === song.spotify_url)
                    ? 'bg-primary text-black opacity-100'
                    : 'bg-black/60 text-white opacity-0 group-hover:opacity-100 hover:bg-white hover:text-black'
                  }`}
                >
                  {cart.some(c => c.spotify_url === song.spotify_url) ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                </button>
              </div>
              <p className="font-bold text-sm truncate">{song.track_name}</p>
              <p className="text-xs text-zinc-500 truncate mt-1">{song.artist_name}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
