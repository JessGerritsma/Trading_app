import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

interface AccountMetrics {
  pnl: number;
  drawdown: number;
  win_rate: number;
  open_trades: number;
  closed_trades: number;
  equity_curve: number[];
}

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<AccountMetrics | null>(null);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-2">Account / Portfolio Metrics</h2>
      {loading && <div>Loading...</div>}
      {metrics && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded shadow">
              <div className="text-sm text-gray-500">P&L</div>
              <div className="text-2xl font-bold">${metrics.pnl.toFixed(2)}</div>
            </div>
            <div className="bg-red-50 p-4 rounded shadow">
              <div className="text-sm text-gray-500">Drawdown</div>
              <div className="text-2xl font-bold">{metrics.drawdown.toFixed(2)}%</div>
            </div>
            <div className="bg-green-50 p-4 rounded shadow">
              <div className="text-sm text-gray-500">Win Rate</div>
              <div className="text-2xl font-bold">{metrics.win_rate.toFixed(2)}%</div>
            </div>
            <div className="bg-yellow-50 p-4 rounded shadow">
              <div className="text-sm text-gray-500">Open Trades</div>
              <div className="text-2xl font-bold">{metrics.open_trades}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded shadow">
              <div className="text-sm text-gray-500">Closed Trades</div>
              <div className="text-2xl font-bold">{metrics.closed_trades}</div>
            </div>
          </div>
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-2">Equity Curve</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={metrics.equity_curve.map((v, i) => ({ x: i + 1, equity: v }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="x" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="equity" stroke="#2563eb" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  );
};
export default DashboardPage; 