import React from 'react';
import { Music } from '../types';
import { Search, Loader2, Plus, Check, Search as SearchIcon } from 'lucide-react';

interface SearchPageProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  onSearch: (e: React.FormEvent) => void;
  isSearching: boolean;
  searchResults: Music[];
  cart: Music[];
  onToggleCart: (song: Music) => void;
}

export const SearchPage: React.FC<SearchPageProps> = ({
  searchQuery,
  setSearchQuery,
  onSearch,
  isSearching,
  searchResults,
  cart,
  onToggleCart
}) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="max-w-2xl mx-auto">
        <form onSubmit={onSearch} className="relative group">
          <Search className={`absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors ${isSearching ? 'text-primary' : 'text-zinc-500 group-focus-within:text-primary'}`} />
          <input 
            type="text"
            placeholder="곡 제목, 아티스트 또는 앨범 검색"
            className="w-full bg-zinc-900 border border-zinc-800 rounded-full py-4 pl-12 pr-4 text-lg focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all shadow-xl"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {isSearching && <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-primary animate-spin" />}
        </form>
      </div>

      {searchResults.length > 0 ? (
        <div className="space-y-4">
          <h3 className="text-xl font-bold">검색 결과</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.map((song, i) => (
              <div key={i} className="flex items-center gap-4 bg-zinc-900/40 p-3 rounded-xl border border-zinc-800/50 hover:bg-zinc-800 transition-all group">
                <img src={song.album_image_url} className="w-16 h-16 rounded-lg object-cover" />
                <div className="flex-1 min-w-0">
                  <p className="font-bold text-sm truncate text-white">{song.track_name}</p>
                  <p className="text-xs text-zinc-400 truncate mt-0.5">{song.artist_name}</p>
                </div>
                <button 
                  onClick={() => onToggleCart(song)}
                  className={`p-2 rounded-full transition-all ${
                    cart.some(c => c.spotify_url === song.spotify_url)
                    ? 'bg-primary/20 text-primary border border-primary/30'
                    : 'bg-zinc-800 text-zinc-400 opacity-0 group-hover:opacity-100 hover:text-white'
                  }`}
                >
                  {cart.some(c => c.spotify_url === song.spotify_url) ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : !isSearching && searchQuery && (
        <div className="py-20 text-center text-zinc-500">
          <SearchIcon className="w-12 h-12 mx-auto mb-4 opacity-20" />
          <p>검색 결과가 없습니다.</p>
        </div>
      )}
    </div>
  );
};
