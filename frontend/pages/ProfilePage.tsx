import React from 'react';
import { User, Playlist } from '../types';
import { MOCK_STATS } from '../constants';
import { GenreDistribution, WeeklyActivity, AudioRadar } from '../components/Charts';
import { Plus, Clock, Music as MusicIcon, Edit3 } from 'lucide-react';

interface ProfilePageProps {
  user: User;
  playlists: Playlist[];
}

export const ProfilePage: React.FC<ProfilePageProps> = ({ user, playlists }) => {
  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      {/* Profile Card */}
      <div className="bg-zinc-900 rounded-3xl p-8 border border-zinc-800 flex flex-col md:flex-row items-center gap-8">
        <div className="w-32 h-32 rounded-full border-4 border-primary/20 overflow-hidden shadow-2xl">
          <img src={user.profile_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.nickname}`} className="w-full h-full object-cover" />
        </div>
        <div className="flex-1 text-center md:text-left">
          <div className="flex flex-col md:flex-row md:items-center gap-2 mb-2">
            <h2 className="text-4xl font-black">{user.nickname}</h2>
            <span className="bg-primary/10 text-primary text-xs font-bold px-2 py-1 rounded w-fit mx-auto md:mx-0">PREMIUM</span>
          </div>
          <p className="text-zinc-400 mb-6">{user.email}</p>
          <div className="flex flex-wrap justify-center md:justify-start gap-4">
            <div className="bg-zinc-950 px-4 py-2 rounded-xl border border-zinc-800">
              <p className="text-xs text-zinc-500">플레이리스트</p>
              <p className="text-lg font-bold">{playlists.length}</p>
            </div>
            <div className="bg-zinc-950 px-4 py-2 rounded-xl border border-zinc-800">
              <p className="text-xs text-zinc-500">누적 감상 시간</p>
              <p className="text-lg font-bold">{(MOCK_STATS.totalMinutes / 60).toFixed(0)}시간</p>
            </div>
          </div>
        </div>
        <button className="bg-zinc-800 hover:bg-zinc-700 text-white p-3 rounded-full transition-colors self-start md:self-center">
          <Edit3 className="w-5 h-5" />
        </button>
      </div>

      {/* Analytics Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Plus className="w-4 h-4 text-primary" /> 선호 장르 분포
          </h3>
          <GenreDistribution data={MOCK_STATS.topGenres} />
        </div>
        <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Clock className="w-4 h-4 text-primary" /> 주간 활동 패턴
          </h3>
          <WeeklyActivity data={MOCK_STATS.weeklyActivity} />
        </div>
        <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800 lg:col-span-2">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <MusicIcon className="w-4 h-4 text-primary" /> 음악적 특성 분석
          </h3>
          <div className="max-w-xl mx-auto">
            <AudioRadar data={MOCK_STATS.audioFeatures} />
          </div>
        </div>
      </div>
    </div>
  );
};
