import React, { useEffect, useState } from 'react';

const SettingsPage: React.FC = () => {
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
    <div className="space-y-6 rounded-2xl bg-gradient-to-br from-green-900 via-teal-900 to-green-800 p-6 shadow-xl">
      <h2 className="text-2xl font-bold mb-4 text-green-100">Settings</h2>
      {loading && <div className="text-green-200">Loading...</div>}
      {settings && (
        <form className="space-y-4" onSubmit={e => { e.preventDefault(); saveSettings(); }}>
          {Object.entries(settings).map(([k, v]) => (
            <div key={k} className="flex items-center gap-4">
              <label className="w-48 font-medium text-green-200">{k}</label>
              <input
                className="flex-1 border px-2 py-1 rounded-xl bg-green-950/60 text-green-100"
                value={String(v)}
                onChange={e => handleChange(k, e.target.value)}
                disabled={saving}
              />
            </div>
          ))}
          <button
            type="submit"
            className="px-4 py-2 bg-teal-600 text-white rounded-xl hover:bg-teal-700 disabled:opacity-50"
            disabled={saving}
          >
            Save
          </button>
        </form>
      )}
      <div className="flex items-center gap-4 mt-6">
        <label className="font-medium text-green-200">Notifications</label>
        <input
          type="checkbox"
          checked={notifications}
          onChange={e => saveNotifications(e.target.checked)}
        />
      </div>
      <div className="flex items-center gap-4 mt-6">
        <label className="font-medium text-green-200">Theme</label>
        <button
          onClick={toggleTheme}
          className="px-4 py-2 bg-green-800 text-green-100 rounded-xl hover:bg-green-700"
        >
          Switch to {theme === 'light' ? 'Dark' : 'Light'}
        </button>
      </div>
    </div>
  );
};
export default SettingsPage; 