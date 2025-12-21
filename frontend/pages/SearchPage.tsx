import React, { useState } from 'react';
import { Music } from '../types';
import { Search, Loader2, Plus, Check } from 'lucide-react';
import { searchMusic } from '../services/musicService';


interface Props {
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  onSearch: (e: React.FormEvent) => void;
  onSearchByGenre: (genre: string) => void;

  isSearching: boolean;
  setIsSearching: (v: boolean) => void;
  searchResults: Music[];
  setSearchResults: (m: Music[]) => void;
  cart: Music[];
  onToggleCart: (song: Music) => void;
}

const GENRES = ['K-Pop', 'Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic'];

export default function SearchPage({
  searchQuery,
  setSearchQuery,
  onSearch,
  onSearchByGenre,

  isSearching,
  setIsSearching,
  searchResults,
  setSearchResults,
  cart,
  onToggleCart,
}: SearchPageProps) {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* 🔍 검색창 */}
      <div className="max-w-2xl mx-auto space-y-4">
        <form onSubmit={onSearch} className="relative">
          <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-500" />
          <input
            type="text"
            placeholder="곡 제목, 아티스트 또는 앨범 검색"
            className="w-full bg-zinc-900 border border-zinc-800 rounded-full py-4 pl-12 pr-4 text-lg focus:outline-none focus:border-primary"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {isSearching && (
            <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 animate-spin text-primary" />
          )}
        </form>

        {/* 🎧 장르 버튼 (여기가 니가 찾던 JSX 위치) */}
        <div className="flex flex-wrap gap-2 justify-center">
          {GENRES.map((genre) => (
            <button
              key={genre}
              type="button"
              onClick={() => onSearchByGenre(genre)}
              className="px-4 py-1.5 rounded-full text-sm bg-zinc-800 text-zinc-300 hover:bg-primary hover:text-black transition"
            >
              #{genre}
            </button>
          ))}
        </div>
      </div>

      {/* 📋 검색 결과 */}
      {searchResults.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {searchResults.map((song) => (
            <div
              key={song.music_no}
              className="flex items-center gap-4 bg-zinc-900 p-3 rounded-xl"
            >
              <img
                src={song.album_image_url}
                className="w-16 h-16 rounded-lg object-cover"
              />
              <div className="flex-1">
                <p className="font-bold text-sm">{song.track_name}</p>
                <p className="text-xs text-zinc-400">{song.artist_name}</p>
              </div>
              <button
                onClick={() => onToggleCart(song)}
                className="p-2 rounded-full bg-zinc-800 hover:bg-primary hover:text-black"
              >
                {cart.some((c) => c.music_no === song.music_no) ? (
                  <Check className="w-4 h-4" />
                ) : (
                  <Plus className="w-4 h-4" />
                )}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
