import React, { useState, useRef, useEffect } from 'react';
import { FaSpinner } from 'react-icons/fa';

interface ChatMessage {
  user: string;
  ai: string;
}

interface Trade {
  id: number;
  datetime_entered: string;
  datetime_exited?: string;
  price_enter: number;
  price_exit?: number;
  size: number;
  reasoning?: string;
  parameters?: string;
  stop_loss?: number;
  take_profit?: number;
  status: string;
  strategy?: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [newTrade, setNewTrade] = useState<Partial<Trade>>({ status: 'trial' });

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { user: input, ai: '' }];
    setMessages(newMessages);
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, context: newMessages }),
      });
      const data = await res.json();
      setMessages([...newMessages.slice(0, -1), { user: input, ai: data.response }]);
    } catch (e) {
      setMessages([...newMessages.slice(0, -1), { user: input, ai: 'Error: Could not get response.' }]);
    } finally {
      setInput('');
      setLoading(false);
      setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    }
  };

  const clearChat = () => setMessages([]);

  const fetchTrades = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/trades');
      const data = await res.json();
      setTrades(data.trades || []);
    } catch (e) {
      setTrades([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchTrades(); }, []);

  const handleChange = (k: string, v: any) => {
    setNewTrade(t => ({ ...t, [k]: v }));
  };

  const submitTrade = async () => {
    setLoading(true);
    try {
      await fetch('http://localhost:8000/trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTrade),
      });
      setShowModal(false);
      setNewTrade({ status: 'trial' });
      fetchTrades();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[70vh] max-h-[70vh]">
      <div className="flex-1 overflow-y-auto bg-white rounded shadow p-4 mb-2">
        {messages.length === 0 && <div className="text-gray-400">Start a conversation with your trading assistant...</div>}
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-4">
            <div className="font-semibold text-blue-700">You:</div>
            <div className="mb-2 text-gray-900">{msg.user}</div>
            <div className="font-semibold text-green-700">LLM:</div>
            <div className="text-gray-900 whitespace-pre-line">{msg.ai}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          disabled={loading || !input.trim()}
        >
          {loading ? <FaSpinner className="animate-spin" /> : 'Send'}
        </button>
        <button
          onClick={clearChat}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
          disabled={loading}
        >
          Clear
        </button>
      </div>
      {loading && (
        <div className="flex justify-center items-center mt-4">
          <FaSpinner className="animate-spin text-2xl text-blue-600" />
          <span className="ml-2 text-blue-600">Waiting for LLM response...</span>
        </div>
      )}
      <div className="mt-8 rounded-2xl bg-green-950/70 p-6 shadow-xl">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-green-100">Trade Journal</h2>
          <button
            className="px-4 py-2 bg-teal-600 text-white rounded-xl hover:bg-teal-700"
            onClick={() => setShowModal(true)}
          >New Trade</button>
        </div>
        {loading && <div className="text-green-200">Loading...</div>}
        <div className="overflow-x-auto">
          {trades.length === 0 ? (
            <div className="text-green-200 text-center py-8">No trades yet. Your journal will appear here after you add trades.</div>
          ) : (
            <table className="min-w-full text-green-100 rounded-xl">
              <thead>
                <tr className="bg-green-900">
                  <th className="px-2 py-1">ID</th>
                  <th className="px-2 py-1">Entered</th>
                  <th className="px-2 py-1">Exited</th>
                  <th className="px-2 py-1">Entry</th>
                  <th className="px-2 py-1">Exit</th>
                  <th className="px-2 py-1">Size</th>
                  <th className="px-2 py-1">Reasoning</th>
                  <th className="px-2 py-1">Parameters</th>
                  <th className="px-2 py-1">SL</th>
                  <th className="px-2 py-1">TP</th>
                  <th className="px-2 py-1">Status</th>
                  <th className="px-2 py-1">Strategy</th>
                </tr>
              </thead>
              <tbody>
                {trades.map(trade => (
                  <tr key={trade.id} className="odd:bg-green-950 even:bg-green-900">
                    <td className="px-2 py-1">{trade.id ?? '-'}</td>
                    <td className="px-2 py-1">{trade.datetime_entered ?? '-'}</td>
                    <td className="px-2 py-1">{trade.datetime_exited ?? '-'}</td>
                    <td className="px-2 py-1">{trade.price_enter ?? '-'}</td>
                    <td className="px-2 py-1">{trade.price_exit ?? '-'}</td>
                    <td className="px-2 py-1">{trade.size ?? '-'}</td>
                    <td className="px-2 py-1">{trade.reasoning ?? '-'}</td>
                    <td className="px-2 py-1">{trade.parameters ?? '-'}</td>
                    <td className="px-2 py-1">{trade.stop_loss ?? '-'}</td>
                    <td className="px-2 py-1">{trade.take_profit ?? '-'}</td>
                    <td className="px-2 py-1">{trade.status ?? '-'}</td>
                    <td className="px-2 py-1">{trade.strategy ?? '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-green-900 p-6 rounded-2xl shadow-xl w-full max-w-lg">
              <h3 className="text-xl font-bold mb-4 text-green-100">New Trade</h3>
              <div className="grid grid-cols-2 gap-4">
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Entry Price" type="number" onChange={e => handleChange('price_enter', parseFloat(e.target.value))} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Size" type="number" onChange={e => handleChange('size', parseFloat(e.target.value))} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Reasoning" onChange={e => handleChange('reasoning', e.target.value)} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Parameters" onChange={e => handleChange('parameters', e.target.value)} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Stop Loss" type="number" onChange={e => handleChange('stop_loss', parseFloat(e.target.value))} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Take Profit" type="number" onChange={e => handleChange('take_profit', parseFloat(e.target.value))} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Status" onChange={e => handleChange('status', e.target.value)} />
                <input className="p-2 rounded-xl bg-green-950/60 text-green-100" placeholder="Strategy" onChange={e => handleChange('strategy', e.target.value)} />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button className="px-4 py-2 bg-gray-700 text-green-100 rounded-xl" onClick={() => setShowModal(false)}>Cancel</button>
                <button className="px-4 py-2 bg-teal-600 text-white rounded-xl hover:bg-teal-700" onClick={submitTrade} disabled={loading}>Save</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage; 