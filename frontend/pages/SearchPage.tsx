import React, { useState } from 'react';
import { Music } from '../types';
import { Search, Loader2, Plus, Check } from 'lucide-react';
import { searchMusic } from '../services/musicService';

interface Props {
  searchQuery: string;
  setSearchQuery: (v: string) => void;
  isSearching: boolean;
  setIsSearching: (v: boolean) => void;
  searchResults: Music[];
  setSearchResults: (m: Music[]) => void;
  cart: Music[];
  onToggleCart: (song: Music) => void;
}

export function SearchPage({
  searchQuery,
  setSearchQuery,
  isSearching,
  setIsSearching,
  searchResults,
  setSearchResults,
  cart,
  onToggleCart
}: Props) {
  const [hasMore, setHasMore] = useState(false);

  // 🔍 검색
  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsSearching(true);

    try {
      const res = await searchMusic(searchQuery) as any;
      if (res.success && res.data) {
        setSearchResults(res.data);
        setHasMore(res.page * res.size < res.total);
      } else {
        setSearchResults([]);
        setHasMore(false);
      }
    } catch {
      alert('검색 중 오류가 발생했습니다.');
      setSearchResults([]);
      setHasMore(false);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* 검색창 */}
      <form onSubmit={handleSearch} className="relative max-w-xl mx-auto">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400" />
        <input
          value={searchQuery}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setSearchQuery(e.target.value)
          }
          className="w-full bg-zinc-900 rounded-full py-3 pl-12 pr-4"
          placeholder="곡 제목, 아티스트 또는 앨범 검색"
        />
        {isSearching && (
          <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 animate-spin text-zinc-400" />
        )}
      </form>

      {/* 🔥 장르 버튼 */}
      <div className="flex justify-center gap-2 flex-wrap">
        {['K-Pop', 'Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic'].map(g => (
          <button
            key={g}
            onClick={() => {
              setSearchQuery(g);
            }}
            className="px-4 py-1 rounded-full bg-zinc-800 hover:bg-primary hover:text-black text-sm"
          >
            #{g}
          </button>
        ))}
      </div>

      {/* 검색 결과 */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {searchResults.map(song => (
          <div
            key={song.music_no ?? song.spotify_url}
            className="flex gap-4 bg-zinc-900 p-3 rounded"
          >
            <img
              src={song.album_image_url}
              className="w-14 h-14 rounded object-cover"
              alt={song.track_name}
            />
            <div className="flex-1 min-w-0">
              <p className="font-bold truncate">{song.track_name}</p>
              <p className="text-xs text-zinc-400 truncate">
                {song.artist_name}
              </p>
            </div>
            <button onClick={() => onToggleCart(song)}>
              {cart.some(c => c.spotify_url === song.spotify_url)
                ? <Check />
                : <Plus />}
            </button>
          </div>
        ))}
      </div>

      {/* 결과가 없을 때 */}
      {!isSearching && searchResults.length === 0 && searchQuery && (
        <div className="text-center text-zinc-500 py-20">
          <p>검색 결과가 없습니다.</p>
        </div>
      )}
    </div>
  );
}
