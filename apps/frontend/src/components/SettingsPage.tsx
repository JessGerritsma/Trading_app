import React, { useEffect, useState } from 'react';

const sections = [
  { key: 'ai', label: 'AI Trading' },
  { key: 'notifications', label: 'Notifications' },
  { key: 'appearance', label: 'Appearance' },
  { key: 'risk', label: 'Risk Management' },
  { key: 'chart', label: 'Chart Preferences' },
  { key: 'account', label: 'Account & Security' },
  { key: 'privacy', label: 'Data & Privacy' },
  { key: 'advanced', label: 'Advanced' },
];

const SettingsPage: React.FC = () => {
  const [activeSection, setActiveSection] = useState('ai');
  const [settings, setSettings] = useState<any>(null);
  const [notifications, setNotifications] = useState(true);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [theme, setTheme] = useState('light');

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/settings');
      const data = await res.json();
      setSettings(data);
    } catch (e) {
      setSettings(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    try {
      const res = await fetch('http://localhost:8000/notifications');
      const data = await res.json();
      setNotifications(data.enabled);
    } catch (e) {}
  };

  useEffect(() => {
    fetchSettings();
    fetchNotifications();
  }, []);

  const handleChange = (k: string, v: any) => {
    setSettings((s: any) => ({ ...s, [k]: v }));
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      await fetch('http://localhost:8000/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      });
    } finally {
      setSaving(false);
    }
  };

  const saveNotifications = async (enabled: boolean) => {
    setNotifications(enabled);
    await fetch('http://localhost:8000/notifications', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled }),
    });
  };

  const toggleTheme = () => {
    setTheme(t => (t === 'light' ? 'dark' : 'light'));
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white dark:bg-green-950 rounded-2xl shadow-xl p-6 mb-6">
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-gray-500 dark:text-green-200">Configure your trading preferences and AI parameters</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-[250px_1fr] gap-6">
        <div className="bg-white dark:bg-green-900 rounded-2xl shadow-xl h-fit">
          {sections.map(s => (
            <div
              key={s.key}
              className={`px-6 py-4 border-b last:border-b-0 cursor-pointer transition-colors ${activeSection === s.key ? 'bg-blue-100 dark:bg-green-800 border-l-4 border-blue-500 dark:border-teal-400' : 'hover:bg-gray-100 dark:hover:bg-green-800'}`}
              onClick={() => setActiveSection(s.key)}
            >
              {s.label}
            </div>
          ))}
        </div>
        <div className="bg-white dark:bg-green-900 rounded-2xl shadow-xl p-8">
          {activeSection === 'ai' && (
            <div>
              <h2 className="text-xl font-bold mb-4">AI Trading Parameters</h2>
              {/* Add AI trading settings here */}
            </div>
          )}
          {activeSection === 'notifications' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Notifications</h2>
              {/* Add notification settings here */}
            </div>
          )}
          {activeSection === 'appearance' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Appearance</h2>
              {/* Add appearance settings here */}
            </div>
          )}
          {activeSection === 'risk' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Risk Management</h2>
              {/* Add risk management settings here */}
            </div>
          )}
          {activeSection === 'chart' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Chart Preferences</h2>
              {/* Add chart preferences here */}
            </div>
          )}
          {activeSection === 'account' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Account & Security</h2>
              {/* Add account & security settings here */}
            </div>
          )}
          {activeSection === 'privacy' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Data & Privacy</h2>
              {/* Add data & privacy settings here */}
            </div>
          )}
          {activeSection === 'advanced' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Advanced</h2>
              {/* Add advanced settings here */}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
export default SettingsPage; 