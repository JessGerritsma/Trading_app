import React, { useEffect, useState } from 'react';

const sections = [
  { key: 'ai', label: 'AI Trading' },
  { key: 'trading_pairs', label: 'Trading Pairs' },
  { key: 'notifications', label: 'Notifications' },
  { key: 'appearance', label: 'Appearance' },
  { key: 'risk', label: 'Risk Management' },
  { key: 'chart', label: 'Chart Preferences' },
  { key: 'account', label: 'Account & Security' },
  { key: 'privacy', label: 'Data & Privacy' },
  { key: 'advanced', label: 'Advanced' },
];

const defaultSettings = {
  auto_trade: true,
  ai_confidence_threshold: 75,
  trading_strategy: 'Balanced',
  max_daily_trades: 10,
  position_size: 2,
  trade_notifications: true,
  price_alerts: true,
  ai_recommendations: false,
  email_notifications: true,
  push_notifications: true,
  theme: 'Dark Mode',
  chart_theme: 'Professional',
  compact_view: false,
  stop_loss_default: 5,
  take_profit_default: 10,
  daily_loss_limit: 3,
  risk_tolerance: 'Moderate',
};

const SettingsPage: React.FC = () => {
  const [activeSection, setActiveSection] = useState('ai');
  const [settings, setSettings] = useState<any>(defaultSettings);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [tradingPairs, setTradingPairs] = useState<string[]>([]);
  const [newPair, setNewPair] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      setLoading(true);
      try {
        const res = await fetch('http://localhost:8000/settings');
        const data = await res.json();
        setSettings(data);
      } catch (e) {
        setSettings(defaultSettings);
      } finally {
        setLoading(false);
      }
    };
    const fetchPairs = async () => {
      try {
        const res = await fetch('http://localhost:8000/trading-pairs');
        const data = await res.json();
        setTradingPairs(data.trading_pairs || []);
      } catch { setTradingPairs([]); }
    };
    fetchSettings();
    fetchPairs();
  }, []);

  const handleChange = (k: string, v: any) => {
    setSettings((s: any) => ({ ...s, [k]: v }));
  };

  const addPair = async () => {
    if (!newPair.trim()) return;
    await fetch('http://localhost:8000/trading-pairs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol: newPair.trim().toUpperCase() })
    });
    setNewPair('');
    const res = await fetch('http://localhost:8000/trading-pairs');
    const data = await res.json();
    setTradingPairs(data.trading_pairs || []);
  };

  const removePair = async (symbol: string) => {
    await fetch('http://localhost:8000/trading-pairs', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol })
    });
    const res = await fetch('http://localhost:8000/trading-pairs');
    const data = await res.json();
    setTradingPairs(data.trading_pairs || []);
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      const { trading_pairs, ...rest } = settings;
      await fetch('http://localhost:8000/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rest),
      });
    } finally {
      setSaving(false);
    }
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
          {loading ? <div className="text-green-200">Loading...</div> : (
            <form className="space-y-8" onSubmit={e => { e.preventDefault(); saveSettings(); }}>
              {activeSection === 'ai' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">AI Trading Parameters</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Auto Trade</span>
                      <input type="checkbox" checked={settings.auto_trade} onChange={e => handleChange('auto_trade', e.target.checked)} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>AI Confidence Threshold (%)</span>
                      <input type="number" min={0} max={100} value={settings.ai_confidence_threshold} onChange={e => handleChange('ai_confidence_threshold', Number(e.target.value))} className="input-field" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Trading Strategy</span>
                      <select value={settings.trading_strategy} onChange={e => handleChange('trading_strategy', e.target.value)} className="select-field">
                        <option>Conservative</option>
                        <option>Balanced</option>
                        <option>Aggressive</option>
                        <option>Custom</option>
                      </select>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Max Daily Trades</span>
                      <input type="number" min={1} max={100} value={settings.max_daily_trades} onChange={e => handleChange('max_daily_trades', Number(e.target.value))} className="input-field" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Position Size (% of portfolio)</span>
                      <input type="number" min={0.1} max={10} step={0.1} value={settings.position_size} onChange={e => handleChange('position_size', Number(e.target.value))} className="input-field" />
                    </div>
                  </div>
                </div>
              )}
              {activeSection === 'trading_pairs' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Trading Pairs</h2>
                  <div className="mb-4">
                    <input
                      type="text"
                      value={newPair}
                      onChange={e => setNewPair(e.target.value)}
                      placeholder="Add new pair (e.g. SOLUSDT)"
                      className="border px-2 py-1 rounded mr-2"
                    />
                    <button
                      onClick={addPair}
                      className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >Add</button>
                  </div>
                  <ul className="space-y-2">
                    {tradingPairs.map(pair => (
                      <li key={pair} className="flex items-center justify-between bg-gray-100 rounded px-3 py-2">
                        <span>{pair}</span>
                        <button
                          onClick={() => removePair(pair)}
                          className="text-red-600 hover:underline"
                        >Remove</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {activeSection === 'notifications' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Notifications</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Trade Notifications</span>
                      <input type="checkbox" checked={settings.trade_notifications} onChange={e => handleChange('trade_notifications', e.target.checked)} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Price Alerts</span>
                      <input type="checkbox" checked={settings.price_alerts} onChange={e => handleChange('price_alerts', e.target.checked)} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>AI Recommendations</span>
                      <input type="checkbox" checked={settings.ai_recommendations} onChange={e => handleChange('ai_recommendations', e.target.checked)} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Email Notifications</span>
                      <input type="checkbox" checked={settings.email_notifications} onChange={e => handleChange('email_notifications', e.target.checked)} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Push Notifications</span>
                      <input type="checkbox" checked={settings.push_notifications} onChange={e => handleChange('push_notifications', e.target.checked)} />
                    </div>
                  </div>
                </div>
              )}
              {activeSection === 'appearance' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Appearance</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Theme</span>
                      <select value={settings.theme} onChange={e => handleChange('theme', e.target.value)} className="select-field">
                        <option>Light Mode</option>
                        <option>Dark Mode</option>
                        <option>Auto (System)</option>
                      </select>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Chart Theme</span>
                      <select value={settings.chart_theme} onChange={e => handleChange('chart_theme', e.target.value)} className="select-field">
                        <option>Professional</option>
                        <option>High Contrast</option>
                        <option>Colorblind Friendly</option>
                      </select>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Compact View</span>
                      <input type="checkbox" checked={settings.compact_view} onChange={e => handleChange('compact_view', e.target.checked)} />
                    </div>
                  </div>
                </div>
              )}
              {activeSection === 'risk' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Risk Management</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Stop Loss Default (%)</span>
                      <input type="number" min={0.1} max={20} step={0.1} value={settings.stop_loss_default} onChange={e => handleChange('stop_loss_default', Number(e.target.value))} className="input-field" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Take Profit Default (%)</span>
                      <input type="number" min={1} max={50} step={0.1} value={settings.take_profit_default} onChange={e => handleChange('take_profit_default', Number(e.target.value))} className="input-field" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Daily Loss Limit (%)</span>
                      <input type="number" min={0.5} max={10} step={0.1} value={settings.daily_loss_limit} onChange={e => handleChange('daily_loss_limit', Number(e.target.value))} className="input-field" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Risk Tolerance</span>
                      <select value={settings.risk_tolerance} onChange={e => handleChange('risk_tolerance', e.target.value)} className="select-field">
                        <option>Conservative</option>
                        <option>Moderate</option>
                        <option>Aggressive</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}
              <div className="flex justify-end mt-8">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50" disabled={saving}>
                  Save
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
export default SettingsPage; 