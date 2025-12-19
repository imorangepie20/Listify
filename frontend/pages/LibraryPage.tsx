import React from 'react';
import { Playlist } from '../types';
import PlaylistCard from '../components/PlaylistCard';
import { Plus, Music as MusicIcon } from 'lucide-react';

interface LibraryPageProps {
  playlists: Playlist[];
  onNavigateToSearch: () => void;
}

export const LibraryPage: React.FC<LibraryPageProps> = ({ playlists, onNavigateToSearch }) => {
  return (
    <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">라이브러리</h2>
        <button 
          onClick={onNavigateToSearch}
          className="bg-white text-black px-6 py-2 rounded-full text-sm font-bold hover:bg-zinc-200 transition-colors flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> 새 플레이리스트
        </button>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {playlists.length === 0 ? (
          <div className="col-span-full py-32 text-center border-2 border-dashed border-zinc-800 rounded-3xl group hover:border-zinc-700 transition-colors">
            <MusicIcon className="w-16 h-16 mx-auto mb-4 text-zinc-700 group-hover:text-zinc-500 transition-colors" />
            <p className="text-zinc-500 text-lg">아직 저장된 플레이리스트가 없습니다.</p>
            <p className="text-zinc-600 text-sm mt-2">좋아하는 곡을 찾아 장바구니에 담아보세요.</p>
          </div>
        ) : (
          playlists.map(p => <PlaylistCard key={p.playlist_no} playlist={p} onClick={() => {}} />)
        )}
      </div>
    </div>
  );
};
