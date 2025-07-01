import React, { useState, useRef } from 'react';

interface ChatMessage {
  user: string;
  ai: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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
          Send
        </button>
        <button
          onClick={clearChat}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
          disabled={loading}
        >
          Clear
        </button>
      </div>
      <div className="mt-8 rounded-2xl bg-green-950/70 p-6 shadow-xl">
        <h2 className="text-2xl font-bold mb-4 text-green-100">Trade Journal</h2>
        {/* Trade journal table here, with columns: id, datetime_entered, datetime_exited, price_enter, price_exit, size, reasoning, parameters, stop_loss, take_profit, status, strategy */}
        {/* Add modal/form for new trade entry, supporting multi-stage process */}
      </div>
    </div>
  );
};
export default ChatPage; 