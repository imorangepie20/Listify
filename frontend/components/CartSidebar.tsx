import React, { useState } from 'react';
import { Trash2, GripVertical, Save, X, ListMusic } from 'lucide-react';
import { Music } from '../types';

interface CartSidebarProps {
  items: Music[];
  onRemove: (url: string) => void;
  onClear: () => void;
  isOpen: boolean;
  onClose: () => void;
  onSavePlaylist: (name: string, desc: string) => void;
}

export default function CartSidebar({
  items,
  onRemove,
  onClear,
  isOpen,
  onClose,
  onSavePlaylist
}: CartSidebarProps) {
  const [isSaving, setIsSaving] = useState(false);
  const [playlistName, setPlaylistName] = useState('');
  const [playlistDesc, setPlaylistDesc] = useState('');

  const handleSave = () => {
    if (!playlistName.trim()) return;
    onSavePlaylist(playlistName, playlistDesc);
    setIsSaving(false);
    setPlaylistName('');
    setPlaylistDesc('');
  };

  return (
    <div
      className={`fixed top-0 right-0 h-full w-80 md:w-96 bg-card border-l border-zinc-800 transition-transform duration-300 z-50 shadow-2xl flex flex-col ${isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
    >
      {/* Header */}
      <div className="p-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900">
        <div className="flex items-center gap-2">
          <ListMusic className="w-5 h-5 text-primary" />
          <h2 className="text-xl font-bold">큐레이션 장바구니</h2>
          <span className="bg-zinc-800 text-xs px-2 py-0.5 rounded-full text-zinc-400">
            {items.length}
          </span>
        </div>
        <button onClick={onClose} className="text-zinc-400 hover:text-white">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {items.length === 0 ? (
          <div className="text-center text-zinc-500 mt-10">
            <p>장바구니가 비어있습니다.</p>
            <p className="text-sm mt-2">음악을 추가하여 큐레이션을 시작하세요.</p>
          </div>
        ) : (
          items.map((item, idx) => (
            <div
              key={item.spotify_url + idx}
              className="group flex items-center bg-zinc-900/50 p-2 rounded-md hover:bg-zinc-800"
            >
              <GripVertical className="w-4 h-4 text-zinc-600 mr-2" />
              <img
                src={item.album_image_url}
                alt={item.track_name}
                className="w-10 h-10 rounded object-cover mr-3"
              />
              <div className="flex-1 min-w-0">
                <h4 className="font-medium text-sm truncate">
                  {item.track_name}
                </h4>
                <p className="text-xs text-zinc-400 truncate">
                  {item.artist_name}
                </p>
              </div>
              <button
                onClick={() => onRemove(item.spotify_url)}
                className="p-1.5 text-zinc-500 hover:text-red-400"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-zinc-800 bg-zinc-900">
        {isSaving ? (
          <div className="space-y-3">
            <input
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-sm"
              placeholder="플레이리스트 이름"
              value={playlistName}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPlaylistName(e.target.value)
              }
              autoFocus
            />
            <textarea
              className="w-full bg-zinc-800 border border-zinc-700 rounded px-3 py-2 text-sm resize-none h-20"
              placeholder="설명 (선택)"
              value={playlistDesc}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                setPlaylistDesc(e.target.value)
              }
            />
            <div className="flex gap-2">
              <button
                onClick={() => setIsSaving(false)}
                className="flex-1 py-2 text-sm text-zinc-400"
              >
                취소
              </button>
              <button
                onClick={handleSave}
                disabled={!playlistName.trim()}
                className="flex-1 py-2 bg-primary text-black font-bold rounded"
              >
                저장
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <button
              onClick={() => setIsSaving(true)}
              disabled={items.length === 0}
              className="w-full flex items-center justify-center gap-2 py-2 bg-primary text-black font-bold rounded"
            >
              <Save className="w-4 h-4" /> 플레이리스트로 저장
            </button>
            <button
              onClick={onClear}
              disabled={items.length === 0}
              className="w-full py-2 text-sm text-zinc-500 hover:text-red-400"
            >
              전체 삭제
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
