// apps/frontend/src/App.tsx
import React, { useState, useEffect } from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar 
} from 'recharts';


const TRADING_API_URL = 'http://localhost:8000';

const Chart = ResponsiveContainer as any;
const BarChartComponent = BarChart as any;
const CartesianGridComponent = CartesianGrid as any;
const XAxisComponent = XAxis as any;
const YAxisComponent = YAxis as any;
const TooltipComponent = Tooltip as any;
const BarComponent = Bar as any;

const API_BASE_URL = 'http://localhost:8000';

interface AccountInfo {
  account_type: string;
  can_trade: boolean;
  balances: Array<{
    asset: string;
    free: number;
    total: number;
  }>;
}

interface Price {
  symbol: string;
  price: number;
}

interface Strategy {
  id: string;
  name: string;
  description: string;
  active: boolean;
}

interface Order {
  orderId: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  type: string;
  quantity: string;
  price: string | null;
  status: string;
  time: number;
}

interface TradeForm {
  symbol: string;
  side: 'BUY' | 'SELL';
  type: 'MARKET' | 'LIMIT';
  quantity: string;
  price: string;
}

const TradingDashboard: React.FC = () => {
  const [accountInfo, setAccountInfo] = useState<AccountInfo | null>(null);
  const [prices, setPrices] = useState<Price[]>([]);
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<string>('disconnected');
  const [selectedSymbol, setSelectedSymbol] = useState<string>('BTCUSDT');
  const [orders, setOrders] = useState<Order[]>([]);
  const [tradeForm, setTradeForm] = useState<TradeForm>({
    symbol: 'BTCUSDT',
    side: 'BUY',
    type: 'MARKET',
    quantity: '',
    price: ''
  });

  // Fetch data functions
  const fetchHealthCheck = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/health`);
      const data = await response.json();
      setConnectionStatus(data.binance_testnet);
    } catch (error) {
      console.error('Health check failed:', error);
      setConnectionStatus('error');
    }
  };

  const fetchAccountInfo = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/account`);
      if (response.ok) {
        const data = await response.json();
        setAccountInfo(data);
      }
    } catch (error) {
      console.error('Failed to fetch account info:', error);
    }
  };

  const fetchPrices = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/prices`);
      if (response.ok) {
        const data = await response.json();
        setPrices(data.prices);
      }
    } catch (error) {
      console.error('Failed to fetch prices:', error);
    }
  };

  const fetchStrategies = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/strategies`);
      if (response.ok) {
        const data = await response.json();
        setStrategies(data.strategies);
      }
    } catch (error) {
      console.error('Failed to fetch strategies:', error);
    }
  };

  const fetchOrders = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/orders/${selectedSymbol}`);
      if (response.ok) {
        const data = await response.json();
        setOrders(data.orders);
      }
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    }
  };

  const placeTrade = async (): Promise<void> => {
    try {
      const response = await fetch(`${TRADING_API_URL}/trade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: tradeForm.symbol,
          side: tradeForm.side,
          type: tradeForm.type,
          quantity: parseFloat(tradeForm.quantity),
          price: tradeForm.price ? parseFloat(tradeForm.price) : null
        }),
      });
      
      const result = await response.json();
      if (result.success) {
        alert('Trade placed successfully!');
        fetchOrders();
        fetchAccountInfo();
      } else {
        alert(`Trade failed: ${result.message}`);
      }
    } catch (error) {
      console.error('Failed to place trade:', error);
      alert('Failed to place trade');
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchHealthCheck();
    fetchAccountInfo();
    fetchPrices();
    fetchStrategies();
    fetchOrders();

    // Set up periodic updates
    const interval = setInterval(() => {
      fetchPrices();
      fetchHealthCheck();
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, [selectedSymbol]);

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'connected': return 'text-green-500';
      case 'disconnected': return 'text-red-500';
      default: return 'text-yellow-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-800">Trading Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Binance Testnet:</span>
              <span className={`font-semibold ${getStatusColor(connectionStatus)}`}>
                {connectionStatus.toUpperCase()}
              </span>
            </div>
          </div>
        </div>

        {/* Account Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Account Status</h3>
            <p className="text-2xl font-bold text-blue-600">
              {accountInfo?.account_type || 'N/A'}
            </p>
            <p className="text-sm text-gray-500">
              Trading: {accountInfo?.can_trade ? '✅' : '❌'}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Balances</h3>
            <p className="text-2xl font-bold text-green-600">
              {accountInfo?.balances?.length || 0}
            </p>
            <p className="text-sm text-gray-500">Assets with balance</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Active Strategies</h3>
            <p className="text-2xl font-bold text-purple-600">
              {strategies.filter(s => s.active).length}
            </p>
            <p className="text-sm text-gray-500">Running strategies</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Recent Orders</h3>
            <p className="text-2xl font-bold text-orange-600">
              {orders.length}
            </p>
            <p className="text-sm text-gray-500">Orders today</p>
          </div>
        </div>

        {/* Main Content Grid */}
        /*this is where i am up to i just removed for now due to the erros */
        
        <div>
          {/* Portfolio Balances */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Portfolio Balances</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {accountInfo?.balances?.map((balance, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                  <span className="font-medium">{balance.asset}</span>
                  <div className="text-right">
                    <div className="font-semibold">{balance.total.toFixed(8)}</div>
                    <div className="text-sm text-gray-500">
                      Free: {balance.free.toFixed(8)}
                    </div>
                  </div>
                </div>
              )) || (
                <p className="text-gray-500 text-center py-4">No balances available</p>
              )}
            </div>
          </div>

          {/* Trading Form */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Place Trade</h3>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Symbol</label>
                  <input
                    type="text"
                    value={tradeForm.symbol}
                    onChange={(e) => setTradeForm({...tradeForm, symbol: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                    placeholder="BTCUSDT"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Side</label>
                  <select
                    value={tradeForm.side}
                    onChange={(e) => setTradeForm({...tradeForm, side: e.target.value as 'BUY' | 'SELL'})}
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="BUY">BUY</option>
                    <option value="SELL">SELL</option>
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                  <select
                    value={tradeForm.type}
                    onChange={(e) => setTradeForm({...tradeForm, type: e.target.value as 'MARKET' | 'LIMIT'})}
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="MARKET">MARKET</option>
                    <option value="LIMIT">LIMIT</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                  <input
                    type="number"
                    step="0.00001"
                    value={tradeForm.quantity}
                    onChange={(e) => setTradeForm({...tradeForm, quantity: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                    placeholder="0.001"
                  />
                </div>
              </div>

              {tradeForm.type === 'LIMIT' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Price</label>
                  <input
                    type="number"
                    step="0.01"
                    value={tradeForm.price}
                    onChange={(e) => setTradeForm({...tradeForm, price: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                    placeholder="0.00"
                  />
                </div>
              )}

              <button
                onClick={placeTrade}
                disabled={connectionStatus !== 'connected' || !tradeForm.quantity}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Place Trade
              </button>
            </div>
          </div>

          {/* Strategies */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Trading Strategies</h3>
            <div className="space-y-3">
              {strategies.map((strategy) => (
                <div key={strategy.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">{strategy.name}</div>
                    <div className="text-sm text-gray-500">{strategy.description}</div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`text-sm px-2 py-1 rounded ${
                      strategy.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'
                    }`}>
                      {strategy.active ? 'Active' : 'Inactive'}
                    </span>
                    <button
                      className="text-blue-600 hover:text-blue-800 text-sm"
                      onClick={() => alert('Strategy configuration coming soon!')}
                    >
                      Configure
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Orders */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-700">Recent Orders</h3>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
            >
              <option value="BTCUSDT">BTC/USDT</option>
              <option value="ETHUSDT">ETH/USDT</option>
              <option value="BNBUSDT">BNB/USDT</option>
            </select>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left p-2">Order ID</th>
                  <th className="text-left p-2">Symbol</th>
                  <th className="text-left p-2">Side</th>
                  <th className="text-left p-2">Type</th>
                  <th className="text-left p-2">Quantity</th>
                  <th className="text-left p-2">Price</th>
                  <th className="text-left p-2">Status</th>
                  <th className="text-left p-2">Time</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.orderId} className="border-t">
                    <td className="p-2">{order.orderId}</td>
                    <td className="p-2">{order.symbol}</td>
                    <td className="p-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        order.side === 'BUY' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {order.side}
                      </span>
                    </td>
                    <td className="p-2">{order.type}</td>
                    <td className="p-2">{order.quantity}</td>
                    <td className="p-2">{order.price || 'Market'}</td>
                    <td className="p-2">
                      <span className={`px-2 py-1 rounded text-xs ${
                        order.status === 'FILLED' ? 'bg-green-100 text-green-800' : 
                        order.status === 'CANCELED' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="p-2">{new Date(order.time).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {orders.length === 0 && (
              <p className="text-gray-500 text-center py-4">No orders found</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingDashboard;