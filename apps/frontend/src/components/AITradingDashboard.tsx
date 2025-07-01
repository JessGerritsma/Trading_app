import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  BarChart3,
  Target,
  Shield,
  Activity,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react';

interface AIAnalysis {
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  analysis: string;
  position_size: string;
}

const AITradingDashboard: React.FC = () => {
  const [marketAnalysis, setMarketAnalysis] = useState<AIAnalysis | null>(null);
  const [insights, setInsights] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSDT');

  const API_BASE = 'http://localhost:8000';

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'BUY': return 'text-green-600 bg-green-100';
      case 'SELL': return 'text-red-600 bg-red-100';
      case 'HOLD': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'HIGH': return 'text-green-600';
      case 'MEDIUM': return 'text-yellow-600';
      case 'LOW': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const analyzeMarket = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/ai/analyze-market`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: selectedSymbol,
          price: 45000,
          change_24h: 2.5,
          volume: 2500000000,
          rsi: 65,
          macd: 'bullish'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setMarketAnalysis(data.analysis);
      }
    } catch (error) {
      console.error('Market analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getInsights = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/ai/insights`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          context: `Current market analysis for ${selectedSymbol} with strong institutional buying and positive market sentiment`
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setInsights(data.insights);
      }
    } catch (error) {
      console.error('Insights failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const refreshAll = async () => {
    await Promise.all([
      analyzeMarket(),
      getInsights()
    ]);
  };

  useEffect(() => {
    refreshAll();
  }, [selectedSymbol]);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">AI Trading Dashboard</h1>
                <p className="text-gray-600">Powered by Ollama LLM - Real-time market analysis</p>
              </div>
            </div>
            <button
              onClick={refreshAll}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
        </div>

        {/* Symbol Selector and Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Trading Symbol
            </label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="BTCUSDT">BTCUSDT</option>
              <option value="ETHUSDT">ETHUSDT</option>
              <option value="ADAUSDT">ADAUSDT</option>
              <option value="SOLUSDT">SOLUSDT</option>
            </select>
          </div>
          
          <button
            onClick={analyzeMarket}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <BarChart3 className="w-4 h-4" />
            Market Analysis
          </button>
          
          <button
            onClick={getInsights}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            <Target className="w-4 h-4" />
            Get Insights
          </button>
          
          <button
            onClick={() => alert('Portfolio analysis coming soon!')}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            <Shield className="w-4 h-4" />
            Portfolio Analysis
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">AI is analyzing...</span>
          </div>
        )}

        {/* Market Analysis */}
        {marketAnalysis && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Market Analysis - {selectedSymbol}</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className={`p-3 rounded-lg ${getSignalColor(marketAnalysis.signal)}`}>
                <div className="font-medium">Signal</div>
                <div className="text-lg font-bold">{marketAnalysis.signal}</div>
              </div>
              
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="font-medium">Confidence</div>
                <div className={`text-lg font-bold ${getConfidenceColor(marketAnalysis.confidence)}`}>
                  {marketAnalysis.confidence}
                </div>
              </div>
              
              <div className="p-3 rounded-lg bg-gray-50">
                <div className="font-medium">Risk Level</div>
                <div className={`text-lg font-bold ${getConfidenceColor(marketAnalysis.risk_level)}`}>
                  {marketAnalysis.risk_level}
                </div>
              </div>
            </div>
            
            <div className="mb-4">
              <div className="font-medium mb-2">Analysis</div>
              <p className="text-gray-700">{marketAnalysis.analysis}</p>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Position Size</div>
              <div className="font-medium">{marketAnalysis.position_size}%</div>
            </div>
          </div>
        )}

        {/* Trading Insights */}
        {insights && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold text-gray-900">AI Trading Insights</h2>
            </div>
            
            <div className="prose max-w-none">
              <div className="whitespace-pre-wrap text-gray-700">{insights}</div>
            </div>
          </div>
        )}

        {/* Status Message */}
        {!marketAnalysis && !insights && !loading && (
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">AI Trading Dashboard Ready</h3>
            <p className="text-gray-600 mb-4">
              Click "Market Analysis" to get AI-powered trading signals for {selectedSymbol}
            </p>
            <button
              onClick={analyzeMarket}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Start Analysis
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AITradingDashboard; 