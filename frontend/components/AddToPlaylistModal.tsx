import React, { useState } from 'react';
import { X, Plus, Music as MusicIcon, ChevronRight } from 'lucide-react';
import { Playlist } from '../types';

interface AddToPlaylistModalProps {
    isOpen: boolean;
    onClose: () => void;
    playlists: Playlist[];
    onSelectPlaylist: (playlistNo: number) => void;
    onCreateNew: () => void;
}

const AddToPlaylistModal: React.FC<AddToPlaylistModalProps> = ({
    isOpen,
    onClose,
    playlists,
    onSelectPlaylist,
    onCreateNew
}) => {
    const handleBackdropClick = (e: React.MouseEvent) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={handleBackdropClick}
        >
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl w-full max-w-md shadow-2xl animate-in fade-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="flex items-center justify-between p-5 border-b border-zinc-800">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                            <MusicIcon className="w-5 h-5 text-primary" />
                        </div>
                        <h2 className="text-xl font-bold">플레이리스트에 추가</h2>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 text-zinc-500 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="max-h-96 overflow-y-auto">
                    {/* Create New Playlist Button */}
                    <button
                        onClick={() => {
                            onCreateNew();
                            onClose();
                        }}
                        className="w-full flex items-center gap-4 p-4 hover:bg-zinc-800 transition-colors border-b border-zinc-800"
                    >
                        <div className="w-12 h-12 bg-zinc-800 rounded-lg flex items-center justify-center">
                            <Plus className="w-6 h-6 text-primary" />
                        </div>
                        <span className="flex-1 text-left font-medium">새 플레이리스트 만들기</span>
                        <ChevronRight className="w-5 h-5 text-zinc-500" />
                    </button>

                    {/* Playlist List */}
                    {playlists.length === 0 ? (
                        <div className="p-8 text-center text-zinc-500">
                            <MusicIcon className="w-12 h-12 mx-auto mb-3 text-zinc-700" />
                            <p className="text-sm">플레이리스트가 없습니다.</p>
                            <p className="text-xs mt-1">새 플레이리스트를 만들어보세요.</p>
                        </div>
                    ) : (
                        <div>
                            {playlists.map((playlist) => (
                                <button
                                    key={playlist.playlist_no}
                                    onClick={() => {
                                        onSelectPlaylist(playlist.playlist_no);
                                        onClose();
                                    }}
                                    className="w-full flex items-center gap-4 p-4 hover:bg-zinc-800 transition-colors group"
                                >
                                    {/* Playlist Cover */}
                                    <div className="w-12 h-12 bg-zinc-800 rounded-lg overflow-hidden flex-shrink-0">
                                        {playlist.music_items && playlist.music_items.length > 0 ? (
                                            <div className="grid grid-cols-2 gap-0.5 w-full h-full">
                                                {playlist.music_items.slice(0, 4).map((music, idx) => (
                                                    <img
                                                        key={idx}
                                                        src={music.album_image_url}
                                                        alt=""
                                                        className="w-full h-full object-cover"
                                                    />
                                                ))}
                                            </div>
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center">
                                                <MusicIcon className="w-6 h-6 text-zinc-600" />
                                            </div>
                                        )}
                                    </div>

                                    {/* Playlist Info */}
                                    <div className="flex-1 min-w-0 text-left">
                                        <p className="font-medium truncate">{playlist.title}</p>
                                        <p className="text-xs text-zinc-500 truncate">
                                            {playlist.music_items?.length || 0}곡
                                        </p>
                                    </div>

                                    <ChevronRight className="w-5 h-5 text-zinc-500 group-hover:text-primary transition-colors" />
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AddToPlaylistModal;
