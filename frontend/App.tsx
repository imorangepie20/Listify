import React, { useState, useEffect } from 'react';
import { Music, Playlist, AppView } from './types';
import { getAccessToken, getPopularTracks, searchSpotifyTracks } from './services/spotifyService';
import { SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET } from './constants';

import Header from './components/Header';
import SettingsModal from './components/SettingsModal';
import CartSidebar from './components/CartSidebar';
import { Sidebar } from './components/Sidebar';
import { PlayerBar } from './components/PlayerBar';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { useAuth } from './hooks/useAuth';
import { HomePage } from './pages/HomePage';
import { SearchPage } from './pages/SearchPage';
import { LibraryPage } from './pages/LibraryPage';
import { ProfilePage } from './pages/ProfilePage';
import { NoticesPage } from './pages/NoticesPage';

function App() {
  const { user, authView, setAuthView, handleLoginSuccess, handleLogout } = useAuth();
  const [view, setView] = useState<AppView>('home');
  const [spotifyToken, setSpotifyToken] = useState<string | null>(null);
  const [songs, setSongs] = useState<Music[]>([]);
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [currentSong, setCurrentSong] = useState<Music | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Music[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // Cart state
  const [cart, setCart] = useState<Music[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  useEffect(() => {
    const init = async () => {
      try {
        const data = await getAccessToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET);
        setSpotifyToken(data.access_token);
        const popular = await getPopularTracks(data.access_token);
        setSongs(popular);
      } catch (e) { 
        console.error(e); 
      }
    };
    init();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim() || !spotifyToken) return;
    
    setIsSearching(true);
    try {
      const results = await searchSpotifyTracks(searchQuery, spotifyToken, 30);
      setSearchResults(results);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSearching(false);
    }
  };

  const toggleCart = (song: Music) => {
    const isInCart = cart.some(c => c.spotify_url === song.spotify_url);
    if (isInCart) {
      setCart(cart.filter(c => c.spotify_url !== song.spotify_url));
    } else {
      setCart([...cart, song]);
    }
  };

  if (!user) {
    return (
      <>
        {authView === 'login' && (
          <Login 
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setAuthView('register')}
          />
        )}
        {authView === 'register' && (
          <Register 
            onRegisterSuccess={() => setAuthView('login')}
            onSwitchToLogin={() => setAuthView('login')}
          />
        )}
      </>
    );
  }

  return (
    <div className="flex h-screen bg-black text-white overflow-hidden">
      <SettingsModal 
        isOpen={isSettingsOpen} 
        onClose={() => setIsSettingsOpen(false)}
        onSave={(id, secret) => console.log('Saved Credentials')}
        initialClientId={SPOTIFY_CLIENT_ID}
        initialClientSecret={SPOTIFY_CLIENT_SECRET}
      />

      <Sidebar 
        view={view}
        onViewChange={setView}
        cartCount={cart.length}
        onOpenCart={() => setIsCartOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onLogout={handleLogout}
      />

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 bg-black relative overflow-hidden">
        <Header 
          viewTitle={view === 'home' ? 'Home' : view === 'search' ? 'Search' : view === 'library' ? 'Library' : view === 'profile' ? 'Profile & Analytics' : 'Notices'} 
          user={user} 
        />

        <div className="flex-1 overflow-y-auto p-8 pb-32">
          {view === 'home' && (
            <HomePage 
              songs={songs}
              cart={cart}
              onToggleCart={toggleCart}
              onNavigateToSearch={() => setView('search')}
            />
          )}

          {view === 'search' && (
            <SearchPage 
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              onSearch={handleSearch}
              isSearching={isSearching}
              searchResults={searchResults}
              cart={cart}
              onToggleCart={toggleCart}
            />
          )}

          {view === 'library' && (
            <LibraryPage 
              playlists={playlists}
              onNavigateToSearch={() => setView('search')}
            />
          )}

          {view === 'profile' && (
            <ProfilePage 
              user={user}
              playlists={playlists}
            />
          )}

          {view === 'notices' && <NoticesPage />}
        </div>

        <PlayerBar 
          currentSong={currentSong}
          isPlaying={isPlaying}
          onTogglePlay={() => setIsPlaying(!isPlaying)}
        />

        <CartSidebar 
          isOpen={isCartOpen} 
          onClose={() => setIsCartOpen(false)} 
          items={cart}
          onRemove={(url) => setCart(cart.filter(c => c.spotify_url !== url))}
          onClear={() => setCart([])}
          onSavePlaylist={(title, desc) => {
            const newP: Playlist = {
              playlist_no: Date.now(),
              user_no: user.user_no,
              title,
              content: desc,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              music_items: cart
            };
            setPlaylists([newP, ...playlists]);
            setCart([]);
            setIsCartOpen(false);
            setView('library');
          }}
        />
      </main>
    </div>
  );
}

export default App;
