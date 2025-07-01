import React, { useEffect, useState } from 'react';

interface Trade {
  id: number;
  symbol: string;
  side: string;
  type: string;
  quantity: number;
  price: number;
  status: string;
  timestamp: string;
  strategy?: string;
  ai_decision?: boolean;
  ai_reasoning?: string;
  pnl?: number;
}

const JournalPage: React.FC = () => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);

  const fetchTrades = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/trades');
      const data = await res.json();
      setTrades(data.trades);
    } catch (e) {
      setTrades([]);
    } finally {
      setLoading(false);
    }
  };

  const exportCSV = () => {
    window.open('http://localhost:8000/trades/export', '_blank');
  };

  useEffect(() => {
    fetchTrades();
  }, []);

  const filteredTrades = filter
    ? trades.filter(t => t.symbol.toLowerCase().includes(filter.toLowerCase()))
    : trades;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-2xl font-bold">Trade Journal</h2>
        <button onClick={exportCSV} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Export CSV</button>
      </div>
      <div className="mb-4 flex gap-2 items-center">
        <input
          type="text"
          placeholder="Filter by symbol..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
          className="border px-2 py-1 rounded"
        />
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded shadow">
          <thead>
            <tr>
              <th className="px-2 py-2">Date</th>
              <th className="px-2 py-2">Symbol</th>
              <th className="px-2 py-2">Side</th>
              <th className="px-2 py-2">Type</th>
              <th className="px-2 py-2">Quantity</th>
              <th className="px-2 py-2">Price</th>
              <th className="px-2 py-2">Status</th>
              <th className="px-2 py-2">P&L</th>
              <th className="px-2 py-2">Reasoning</th>
            </tr>
          </thead>
          <tbody>
            {filteredTrades.map(trade => (
              <React.Fragment key={trade.id}>
                <tr className="hover:bg-gray-50 cursor-pointer" onClick={() => setExpanded(expanded === trade.id ? null : trade.id)}>
                  <td className="px-2 py-2">{new Date(trade.timestamp).toLocaleString()}</td>
                  <td className="px-2 py-2">{trade.symbol}</td>
                  <td className="px-2 py-2">{trade.side}</td>
                  <td className="px-2 py-2">{trade.type}</td>
                  <td className="px-2 py-2">{trade.quantity}</td>
                  <td className="px-2 py-2">${trade.price}</td>
                  <td className="px-2 py-2">{trade.status}</td>
                  <td className="px-2 py-2">{trade.pnl ?? '-'}</td>
                  <td className="px-2 py-2 text-blue-600 underline">{trade.ai_reasoning ? 'View' : '-'}</td>
                </tr>
                {expanded === trade.id && trade.ai_reasoning && (
                  <tr>
                    <td colSpan={9} className="bg-gray-50 px-4 py-3">
                      <div>
                        <strong>Reasoning:</strong> {trade.ai_reasoning}
                      </div>
                      {trade.strategy && <div><strong>Strategy:</strong> {trade.strategy}</div>}
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
      {loading && <div>Loading...</div>}
    </div>
  );
};
export default JournalPage; 