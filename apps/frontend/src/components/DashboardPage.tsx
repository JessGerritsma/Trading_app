import React, { useEffect, useState, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Tab } from '@headlessui/react';

interface AccountMetrics {
  pnl: number;
  drawdown: number;
  win_rate: number;
  open_trades: number;
  closed_trades: number;
  equity_curve: number[];
}

interface LivePrice {
  symbol: string;
  price: number | null;
  timestamp?: number;
  error?: string;
}

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<AccountMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [livePrices, setLivePrices] = useState<LivePrice[]>([]);
  const [wsConnected, setWsConnected] = useState(true);
  const wsRef = useRef<WebSocket | null>(null);
  const [selectedPair, setSelectedPair] = useState<string>('');
  const [priceHistory, setPriceHistory] = useState<Record<string, { timestamp: number, price: number|null }[]>>({});

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/account');
      const data = await res.json();
      setMetrics(data);
    } catch (e) {
      setMetrics(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // WebSocket connection for live prices
    const ws = new WebSocket('ws://localhost:8000/ws/prices');
    wsRef.current = ws;
    ws.onopen = () => setWsConnected(true);
    ws.onclose = () => setWsConnected(false);
    ws.onerror = () => setWsConnected(false);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.prices) setLivePrices(data.prices);
      } catch {}
    };
    return () => { ws.close(); };
  }, []);

  // Update price history on new websocket data
  useEffect(() => {
    if (livePrices.length > 0) {
      // Set default selected pair if not set
      if (!selectedPair) setSelectedPair(livePrices[0].symbol);
      setPriceHistory(prev => {
        const updated = { ...prev };
        livePrices.forEach(p => {
          if (!updated[p.symbol]) updated[p.symbol] = [];
          // Only add if price is not null
          if (p.price !== null) {
            updated[p.symbol] = [
              ...updated[p.symbol],
              { timestamp: Date.now(), price: p.price }
            ].slice(-60); // Keep last 60 points (5 min at 5s interval)
          }
        });
        return updated;
      });
    }
  }, [livePrices]);

  return (
    <div className="space-y-6 rounded-2xl bg-gradient-to-br from-green-900 via-teal-900 to-green-800 p-6 shadow-xl">
      <h2 className="text-3xl font-bold mb-4 text-green-100">Account / Portfolio Metrics</h2>
      {/* Live Prices Table */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2 text-blue-200">Live Prices (WebSocket)</h3>
        {/* Tabs for pairs */}
        <div className="mb-4">
          <Tab.Group selectedIndex={livePrices.findIndex(p => p.symbol === selectedPair)} onChange={(i: number) => setSelectedPair(livePrices[i]?.symbol)}>
            <Tab.List className="flex space-x-2">
              {livePrices.map((p) => (
                <Tab key={p.symbol} className={({ selected }: { selected: boolean }) => `px-4 py-2 rounded-t-lg ${selected ? 'bg-blue-600 text-white' : 'bg-green-800 text-blue-200'}`}>{p.symbol}</Tab>
              ))}
            </Tab.List>
          </Tab.Group>
        </div>
        {/* Price history graph for selected pair */}
        <div className="bg-white dark:bg-green-950 rounded-xl p-4 mb-4">
          {selectedPair && priceHistory[selectedPair] && priceHistory[selectedPair].length > 1 ? (
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={priceHistory[selectedPair].map((pt, i) => ({ x: i + 1, price: pt.price }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#14532d" />
                <XAxis dataKey="x" tick={false} />
                <YAxis tick={{ fontSize: 12, fill: '#bbf7d0' }} domain={['auto', 'auto']} />
                <Tooltip contentStyle={{ background: '#134e4a', color: '#bbf7d0', borderRadius: 12 }} />
                <Line type="monotone" dataKey="price" stroke="#22d3ee" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-green-200">Waiting for price history...</div>
          )}
        </div>
        {!wsConnected && (
          <div className="text-red-400 mb-2">Live price connection lost. Trying to reconnect...</div>
        )}
        {livePrices.length === 0 ? (
          <div className="text-green-200">Loading live prices...</div>
        ) : (
          <table className="min-w-full bg-white dark:bg-green-950 rounded-xl overflow-hidden shadow">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-green-700 dark:text-green-200">Symbol</th>
                <th className="px-4 py-2 text-left text-green-700 dark:text-green-200">Price</th>
                <th className="px-4 py-2 text-left text-green-700 dark:text-green-200">Status</th>
              </tr>
            </thead>
            <tbody>
              {livePrices.map((p) => (
                <tr key={p.symbol}>
                  <td className="px-4 py-2 font-mono">{p.symbol}</td>
                  <td className="px-4 py-2">{p.price !== null ? `$${p.price.toLocaleString(undefined, {maximumFractionDigits: 8})}` : '--'}</td>
                  <td className="px-4 py-2 text-sm">
                    {p.error ? <span className="text-red-500">{p.error}</span> : <span className="text-green-500">OK</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      {loading && <div className="text-green-200">Loading...</div>}
      {metrics && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-green-950/70 p-4 rounded-xl shadow">
              <div className="text-sm text-green-300">P&L</div>
              <div className="text-2xl font-bold text-green-100">${metrics.pnl.toFixed(2)}</div>
            </div>
            <div className="bg-teal-950/70 p-4 rounded-xl shadow">
              <div className="text-sm text-teal-300">Drawdown</div>
              <div className="text-2xl font-bold text-teal-100">{metrics.drawdown.toFixed(2)}%</div>
            </div>
            <div className="bg-green-900/70 p-4 rounded-xl shadow">
              <div className="text-sm text-green-300">Win Rate</div>
              <div className="text-2xl font-bold text-green-100">{metrics.win_rate.toFixed(2)}%</div>
            </div>
            <div className="bg-teal-900/70 p-4 rounded-xl shadow">
              <div className="text-sm text-teal-300">Open Trades</div>
              <div className="text-2xl font-bold text-teal-100">{metrics.open_trades}</div>
            </div>
            <div className="bg-green-800/70 p-4 rounded-xl shadow">
              <div className="text-sm text-green-300">Closed Trades</div>
              <div className="text-2xl font-bold text-green-100">{metrics.closed_trades}</div>
            </div>
          </div>
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-2 text-green-200">Equity Curve</h3>
            <div className="rounded-2xl overflow-hidden bg-green-950/60 p-4">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.equity_curve.map((v, i) => ({ x: i + 1, equity: v }))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#14532d" />
                  <XAxis dataKey="x" tick={{ fontSize: 12, fill: '#bbf7d0' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#bbf7d0' }} />
                  <Tooltip contentStyle={{ background: '#134e4a', color: '#bbf7d0', borderRadius: 12 }} />
                  <Line type="monotone" dataKey="equity" stroke="#22d3ee" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
export default DashboardPage; 