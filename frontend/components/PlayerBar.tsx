import React from 'react';
import { Music } from '../types';
import { Play, Pause, Heart } from 'lucide-react';

interface PlayerBarProps {
  currentSong: Music | null;
  isPlaying: boolean;
  onTogglePlay: () => void;
}

export const PlayerBar: React.FC<PlayerBarProps> = ({ currentSong, isPlaying, onTogglePlay }) => {
  if (!currentSong) return null;

  return (
    <div className="h-24 bg-zinc-900/90 backdrop-blur-md border-t border-zinc-800 flex items-center px-8 fixed bottom-0 left-64 right-0 z-30 shadow-2xl">
      <div className="flex items-center gap-4 w-1/3">
        <img src={currentSong.album_image_url} className="w-14 h-14 rounded-lg shadow-lg" />
        <div className="truncate">
          <p className="font-bold text-sm truncate text-white">{currentSong.track_name}</p>
          <p className="text-xs text-zinc-400 truncate mt-1">{currentSong.artist_name}</p>
        </div>
        <button className="ml-2 text-zinc-500 hover:text-primary transition-colors">
          <Heart className="w-4 h-4" />
        </button>
      </div>
      <div className="flex-1 flex flex-col items-center gap-2">
        <div className="flex items-center gap-6">
          <button onClick={onTogglePlay} className="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:scale-110 active:scale-95 transition-all shadow-lg">
            {isPlaying ? <Pause className="w-5 h-5 text-black" /> : <Play className="w-5 h-5 text-black ml-1" />}
          </button>
        </div>
        <div className="w-full max-w-md h-1 bg-zinc-800 rounded-full overflow-hidden">
          <div className="h-full bg-primary w-1/3 shadow-[0_0_10px_rgba(29,185,84,0.5)]"></div>
        </div>
      </div>
      <div className="w-1/3 flex justify-end">
        <div className="flex items-center gap-4 text-zinc-400">
          <p className="text-xs font-mono">1:23 / 3:45</p>
        </div>
      </div>
    </div>
  );
};
