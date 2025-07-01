import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  BarChart3,
  Target,
  Shield,
  DollarSign,
  Activity,
  Play,
  Pause,
  Settings,
  Zap,
  Clock,
  Calendar,
  PieChart,
  LineChart,
  AlertCircle,
  Info,
  RefreshCw,
  Eye,
  EyeOff
} from 'lucide-react';

interface AIAnalysis {
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  analysis: string;
  entry_price?: number;
  stop_loss?: number;
  take_profit?: number;
  position_size: string;
}

interface TradeEvaluation {
  approved: boolean;
  risk_score: number;
  recommended_position_size: string;
  concerns: string[];
  suggestions: string[];
  reasoning: string;
}

interface PortfolioAnalysis {
  performance_grade: 'A' | 'B' | 'C' | 'D' | 'F';
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  risk_assessment: 'HIGH' | 'MEDIUM' | 'LOW';
  suggested_adjustments: {
    position_sizing: string;
    strategy_mix: string;
    risk_management: string;
  };
}

interface AutomatedTradingStatus {
  is_running: boolean;
  last_analysis: Record<string, any>;
  daily_trades: Record<string, any>;
  cooldowns: Record<string, any>;
}

interface AIDecision {
  id: string;
  symbol: string;
  action: string;
  confidence: number;
  reasoning: string;
  timestamp: string;
  executed: boolean;
}

const AITradingDashboard: React.FC = () => {
  const [marketAnalysis, setMarketAnalysis] = useState<AIAnalysis | null>(null);
  const [tradeEvaluation, setTradeEvaluation] = useState<TradeEvaluation | null>(null);
  const [portfolioAnalysis, setPortfolioAnalysis] = useState<PortfolioAnalysis | null>(null);
  const [insights, setInsights] = useState<string>('');
  const [automatedTradingStatus, setAutomatedTradingStatus] = useState<AutomatedTradingStatus | null>(null);
  const [aiDecisions, setAiDecisions] = useState<AIDecision[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSDT');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [tradingEnabled, setTradingEnabled] = useState(false);

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

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'HIGH': return 'text-red-600';
      case 'MEDIUM': return 'text-yellow-600';
      case 'LOW': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A': return 'text-green-600 bg-green-100';
      case 'B': return 'text-blue-600 bg-blue-100';
      case 'C': return 'text-yellow-600 bg-yellow-100';
      case 'D': return 'text-orange-600 bg-orange-100';
      case 'F': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const fetchAutomatedTradingStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/automated-trading/status`);
      if (response.ok) {
        const data = await response.json();
        setAutomatedTradingStatus(data.automated_trading);
      }
    } catch (error) {
      console.error('Failed to fetch automated trading status:', error);
    }
  };

  const fetchAiDecisions = async () => {
    try {
      const response = await fetch(`${API_BASE}/automated-trading/decisions?limit=10`);
      if (response.ok) {
        const data = await response.json();
        setAiDecisions(data.decisions);
      }
    } catch (error) {
      console.error('Failed to fetch AI decisions:', error);
    }
  };

  const startAutomatedTrading = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/automated-trading/start`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setTradingEnabled(true);
        await fetchAutomatedTradingStatus();
      }
    } catch (error) {
      console.error('Failed to start automated trading:', error);
    } finally {
      setLoading(false);
    }
  };

  const stopAutomatedTrading = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/automated-trading/stop`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setTradingEnabled(false);
        await fetchAutomatedTradingStatus();
      }
    } catch (error) {
      console.error('Failed to stop automated trading:', error);
    } finally {
      setLoading(false);
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

  const evaluateTrade = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/ai/evaluate-trade`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: selectedSymbol,
          action: 'BUY',
          entry_price: 45000,
          current_price: 44800,
          position_size: 3,
          available_capital: 10000,
          recent_performance: 'positive'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setTradeEvaluation(data.evaluation);
      }
    } catch (error) {
      console.error('Trade evaluation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzePortfolio = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/ai/portfolio-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          total_capital: 10000,
          current_value: 10500,
          total_pnl: 500,
          win_rate: 65,
          avg_return: 2.5,
          total_trades: 20,
          recent_trades: ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setPortfolioAnalysis(data.analysis);
      }
    } catch (error) {
      console.error('Portfolio analysis failed:', error);
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
      fetchAutomatedTradingStatus(),
      fetchAiDecisions(),
      analyzeMarket(),
      getInsights()
    ]);
  };

  useEffect(() => {
    refreshAll();
    
    if (autoRefresh) {
      const interval = setInterval(refreshAll, 30000); // Refresh every 30 seconds
      return () => clearInterval(interval);
    }
  }, [selectedSymbol, autoRefresh]);

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
                <p className="text-gray-600">Powered by Ollama LLM - Real-time market analysis and automated trading</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={refreshAll}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              >
                <Settings className="w-4 h-4" />
                {showAdvanced ? 'Hide' : 'Show'} Advanced
              </button>
            </div>
          </div>
        </div>

        {/* Automated Trading Control Panel */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5 text-orange-600" />
              <h2 className="text-xl font-semibold text-gray-900">Automated Trading Control</h2>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                tradingEnabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {tradingEnabled ? 'ACTIVE' : 'INACTIVE'}
              </span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Last Analysis</span>
              </div>
              <div className="text-lg font-semibold">
                {automatedTradingStatus?.last_analysis?.[selectedSymbol]?.timestamp 
                  ? new Date(automatedTradingStatus.last_analysis[selectedSymbol].timestamp).toLocaleTimeString()
                  : 'Never'
                }
              </div>
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Daily Trades</span>
              </div>
              <div className="text-lg font-semibold">
                {automatedTradingStatus?.daily_trades?.[selectedSymbol]?.count || 0} / 5
              </div>
            </div>
            
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Cooldown</span>
              </div>
              <div className="text-lg font-semibold">
                {automatedTradingStatus?.cooldowns?.[selectedSymbol] === 'None' 
                  ? 'Ready' 
                  : 'Active'
                }
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              onClick={startAutomatedTrading}
              disabled={loading || tradingEnabled}
              className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Play className="w-4 h-4" />
              Start Automated Trading
            </button>
            
            <button
              onClick={stopAutomatedTrading}
              disabled={loading || !tradingEnabled}
              className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Pause className="w-4 h-4" />
              Stop Automated Trading
            </button>
            
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="autoRefresh"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="rounded"
              />
              <label htmlFor="autoRefresh" className="text-sm text-gray-700">
                Auto-refresh (30s)
              </label>
            </div>
          </div>
        </div>

        {/* Symbol Selector and Quick Actions */}
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
            onClick={evaluateTrade}
            disabled={loading}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            <Target className="w-4 h-4" />
            Evaluate Trade
          </button>
          
          <button
            onClick={analyzePortfolio}
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

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Market Analysis */}
          {marketAnalysis && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Market Analysis - {selectedSymbol}</h2>
              </div>
              
              <div className="grid grid-cols-3 gap-4 mb-4">
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
                  <div className={`text-lg font-bold ${getRiskColor(marketAnalysis.risk_level)}`}>
                    {marketAnalysis.risk_level}
                  </div>
                </div>
              </div>
              
              <div className="mb-4">
                <div className="font-medium mb-2">Analysis</div>
                <p className="text-gray-700">{marketAnalysis.analysis}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-600">Entry Price</div>
                  <div className="font-medium">${marketAnalysis.entry_price || 'N/A'}</div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-600">Position Size</div>
                  <div className="font-medium">{marketAnalysis.position_size}%</div>
                </div>
              </div>
            </div>
          )}

          {/* Trade Evaluation */}
          {tradeEvaluation && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center gap-2 mb-4">
                <Target className="w-5 h-5 text-green-600" />
                <h2 className="text-xl font-semibold text-gray-900">Trade Evaluation</h2>
              </div>
              
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className={`p-3 rounded-lg ${tradeEvaluation.approved ? 'bg-green-100' : 'bg-red-100'}`}>
                  <div className="font-medium">Approval</div>
                  <div className="flex items-center gap-2">
                    {tradeEvaluation.approved ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600" />
                    )}
                    <span className="font-bold">{tradeEvaluation.approved ? 'APPROVED' : 'REJECTED'}</span>
                  </div>
                </div>
                
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium">Risk Score</div>
                  <div className="text-lg font-bold">{tradeEvaluation.risk_score}/10</div>
                </div>
                
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium">Position Size</div>
                  <div className="text-lg font-bold">{tradeEvaluation.recommended_position_size}</div>
                </div>
              </div>
              
              <div className="mb-4">
                <div className="font-medium mb-2">Reasoning</div>
                <p className="text-gray-700">{tradeEvaluation.reasoning}</p>
              </div>
              
              {tradeEvaluation.concerns.length > 0 && (
                <div className="mb-4">
                  <div className="font-medium mb-2 text-red-600">Concerns</div>
                  <ul className="list-disc list-inside text-gray-700">
                    {tradeEvaluation.concerns.map((concern, index) => (
                      <li key={index}>{concern}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Portfolio Analysis */}
        {portfolioAnalysis && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <Shield className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold text-gray-900">Portfolio Analysis</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <div className="flex items-center gap-4 mb-4">
                  <div className={`text-4xl font-bold p-4 rounded-lg ${getGradeColor(portfolioAnalysis.performance_grade)}`}>
                    {portfolioAnalysis.performance_grade}
                  </div>
                  <div>
                    <div className="font-medium">Performance Grade</div>
                    <div className="text-sm text-gray-600">Risk: {portfolioAnalysis.risk_assessment}</div>
                  </div>
                </div>
                
                <div className="mb-4">
                  <div className="font-medium mb-2 text-green-600">Strengths</div>
                  <ul className="list-disc list-inside text-gray-700">
                    {portfolioAnalysis.strengths.map((strength, index) => (
                      <li key={index}>{strength}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <div className="font-medium mb-2 text-red-600">Areas for Improvement</div>
                  <ul className="list-disc list-inside text-gray-700">
                    {portfolioAnalysis.weaknesses.map((weakness, index) => (
                      <li key={index}>{weakness}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div>
                <div className="mb-4">
                  <div className="font-medium mb-2">Recommendations</div>
                  <ul className="list-disc list-inside text-gray-700">
                    {portfolioAnalysis.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <div className="font-medium mb-2">Suggested Adjustments</div>
                  <div className="space-y-2">
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-sm font-medium">Position Sizing</div>
                      <div className="text-sm text-gray-600">{portfolioAnalysis.suggested_adjustments.position_sizing}</div>
                    </div>
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-sm font-medium">Strategy Mix</div>
                      <div className="text-sm text-gray-600">{portfolioAnalysis.suggested_adjustments.strategy_mix}</div>
                    </div>
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-sm font-medium">Risk Management</div>
                      <div className="text-sm text-gray-600">{portfolioAnalysis.suggested_adjustments.risk_management}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Decisions History */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Recent AI Decisions</h2>
            </div>
            <button
              onClick={fetchAiDecisions}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              Refresh
            </button>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left p-2">Time</th>
                  <th className="text-left p-2">Symbol</th>
                  <th className="text-left p-2">Action</th>
                  <th className="text-left p-2">Confidence</th>
                  <th className="text-left p-2">Status</th>
                  <th className="text-left p-2">Reasoning</th>
                </tr>
              </thead>
              <tbody>
                {aiDecisions.map((decision) => (
                  <tr key={decision.id} className="border-t">
                    <td className="p-2">{new Date(decision.timestamp).toLocaleString()}</td>
                    <td className="p-2 font-medium">{decision.symbol}</td>
                    <td className="p-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        decision.action === 'BUY' ? 'bg-green-100 text-green-800' : 
                        decision.action === 'SELL' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {decision.action}
                      </span>
                    </td>
                    <td className="p-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        decision.confidence > 0.7 ? 'bg-green-100 text-green-800' :
                        decision.confidence > 0.4 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {Math.round(decision.confidence * 100)}%
                      </span>
                    </td>
                    <td className="p-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        decision.executed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'
                      }`}>
                        {decision.executed ? 'Executed' : 'Pending'}
                      </span>
                    </td>
                    <td className="p-2 text-gray-600 max-w-xs truncate">
                      {decision.reasoning}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {aiDecisions.length === 0 && (
              <p className="text-gray-500 text-center py-4">No AI decisions found</p>
            )}
          </div>
        </div>

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
      </div>
    </div>
  );
};

export default AITradingDashboard; 