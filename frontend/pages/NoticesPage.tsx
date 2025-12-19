import React from 'react';
import { MOCK_NOTICES } from '../constants';
import { Calendar } from 'lucide-react';

export const NoticesPage: React.FC = () => {
  return (
    <div className="space-y-6 animate-in slide-in-from-right-4 duration-500">
      <h2 className="text-3xl font-black mb-8">공지사항</h2>
      <div className="space-y-4">
        {MOCK_NOTICES.map((notice) => (
          <div key={notice.notice_no} className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 hover:bg-zinc-800/50 transition-colors cursor-pointer group">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-xl font-bold text-white group-hover:text-primary transition-colors">{notice.title}</h3>
              <span className="flex items-center gap-1.5 text-xs text-zinc-500 font-mono">
                <Calendar className="w-3 h-3" /> {notice.created_at}
              </span>
            </div>
            <p className="text-zinc-400 line-clamp-2 text-sm leading-relaxed">{notice.content}</p>
            <div className="mt-4 pt-4 border-t border-zinc-800 flex items-center text-xs text-zinc-500">
              <span className="bg-zinc-950 px-2 py-1 rounded border border-zinc-800">운영자 공지</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
