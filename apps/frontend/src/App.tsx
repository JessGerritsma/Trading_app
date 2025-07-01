// apps/frontend/src/App.tsx
import React from 'react';
import './index.css';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          AI Trading Dashboard
        </h1>
        <p className="text-gray-600 mb-6">
          Powered by Ollama LLM - Real-time market analysis
        </p>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            System Status
          </h2>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Frontend: Running</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Backend: Connected</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>AI Model: Llama 3.1</span>
            </div>
          </div>
        </div>
        
        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button 
              onClick={() => alert('Market Analysis coming soon!')}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Market Analysis
            </button>
            <button 
              onClick={() => alert('Trade Evaluation coming soon!')}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Trade Evaluation
            </button>
            <button 
              onClick={() => alert('Portfolio Analysis coming soon!')}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Portfolio Analysis
            </button>
          </div>
        </div>
        
        <div className="mt-6 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Next Steps
          </h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>Test the basic functionality</li>
            <li>Add AI integration features</li>
            <li>Implement automated trading</li>
            <li>Add real-time market data</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default App;