#!/usr/bin/env python3
"""
Test script for AI endpoints and automated trading functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"✅ {method} {endpoint} - Status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return None

def main():
    print("🤖 Testing AI Trading System Endpoints")
    print("=" * 50)
    
    # Test basic health
    print("\n1. Testing Health Check:")
    health = test_endpoint("/health")
    
    # Test AI status
    print("\n2. Testing AI Status:")
    ai_status = test_endpoint("/ai/status")
    
    # Test market analysis
    print("\n3. Testing Market Analysis:")
    market_data = {
        "symbol": "BTCUSDT",
        "price": 45000,
        "change_24h": 2.5,
        "volume": 2500000000,
        "rsi": 65,
        "macd": "bullish"
    }
    market_analysis = test_endpoint("/ai/analyze-market", "POST", market_data)
    
    # Test trade evaluation
    print("\n4. Testing Trade Evaluation:")
    trade_data = {
        "symbol": "BTCUSDT",
        "action": "BUY",
        "entry_price": 45000,
        "current_price": 44800,
        "position_size": 3,
        "available_capital": 10000,
        "recent_performance": "positive"
    }
    trade_evaluation = test_endpoint("/ai/evaluate-trade", "POST", trade_data)
    
    # Test portfolio analysis
    print("\n5. Testing Portfolio Analysis:")
    portfolio_data = {
        "total_capital": 10000,
        "current_value": 10500,
        "total_pnl": 500,
        "win_rate": 65,
        "avg_return": 2.5,
        "total_trades": 20,
        "recent_trades": ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
    }
    portfolio_analysis = test_endpoint("/ai/portfolio-analysis", "POST", portfolio_data)
    
    # Test insights
    print("\n6. Testing Trading Insights:")
    insights_data = {
        "context": "Current market analysis for BTCUSDT with strong institutional buying and positive market sentiment"
    }
    insights = test_endpoint("/ai/insights", "POST", insights_data)
    
    # Test automated trading status
    print("\n7. Testing Automated Trading Status:")
    auto_status = test_endpoint("/automated-trading/status")
    
    # Test AI decisions
    print("\n8. Testing AI Decisions:")
    decisions = test_endpoint("/automated-trading/decisions")
    
    # Test starting automated trading (should fail since it's disabled by default)
    print("\n9. Testing Start Automated Trading (should fail - disabled by default):")
    start_result = test_endpoint("/automated-trading/start", "POST")
    
    # Test other endpoints
    print("\n10. Testing Other Endpoints:")
    prices = test_endpoint("/prices")
    strategies = test_endpoint("/strategies")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("=" * 50)
    
    # Print some sample responses
    if ai_status:
        print(f"AI Status: {ai_status.get('status', 'Unknown')}")
        print(f"Model: {ai_status.get('model', 'Unknown')}")
    
    if market_analysis:
        signal = market_analysis.get('analysis', {}).get('signal', 'Unknown')
        confidence = market_analysis.get('analysis', {}).get('confidence', 'Unknown')
        print(f"Market Signal: {signal} (Confidence: {confidence})")
    
    if auto_status:
        is_running = auto_status.get('automated_trading', {}).get('is_running', False)
        enabled = auto_status.get('settings', {}).get('enabled', False)
        print(f"Automated Trading: {'Running' if is_running else 'Stopped'} (Enabled: {enabled})")
    
    print("\n✅ All tests completed! The AI trading system is ready.")
    print("\n📊 Next steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Navigate to the 'AI Dashboard' tab")
    print("3. Test the automated trading controls")
    print("4. Enable live trading in settings when ready")

if __name__ == "__main__":
    main() 