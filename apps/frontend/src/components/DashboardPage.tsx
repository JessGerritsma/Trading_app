import React, { useEffect, useState, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

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

  return (
    <div className="space-y-6 rounded-2xl bg-gradient-to-br from-green-900 via-teal-900 to-green-800 p-6 shadow-xl">
      <h2 className="text-3xl font-bold mb-4 text-green-100">Account / Portfolio Metrics</h2>
      {/* Live Prices Table */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2 text-blue-200">Live Prices (WebSocket)</h3>
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