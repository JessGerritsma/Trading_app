// apps/frontend/src/App.tsx
import React, { useState } from 'react';
import './index.css';

const Dashboard = React.lazy(() => import('./components/DashboardPage'));
const Journal = React.lazy(() => import('./components/JournalPage'));
const Chat = React.lazy(() => import('./components/ChatPage'));
const Settings = React.lazy(() => import('./components/SettingsPage'));

const NAV_ITEMS = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'journal', label: 'Journal' },
  { key: 'chat', label: 'Chat' },
  { key: 'settings', label: 'Settings' },
];

const App: React.FC = () => {
  const [page, setPage] = useState('dashboard');

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">AI Trading App</h1>
          <nav className="flex gap-4">
            {NAV_ITEMS.map(item => (
              <button
                key={item.key}
                onClick={() => setPage(item.key)}
                className={`px-3 py-2 rounded-md font-medium ${page === item.key ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-200'}`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto w-full p-4">
        <React.Suspense fallback={<div>Loading...</div>}>
          {page === 'dashboard' && <Dashboard />}
          {page === 'journal' && <Journal />}
          {page === 'chat' && <Chat />}
          {page === 'settings' && <Settings />}
        </React.Suspense>
      </main>
    </div>
  );
};

export default App;