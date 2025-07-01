#!/usr/bin/env python3
"""
Test AI endpoints with the Docker backend
"""

import requests
import json

def test_ai_endpoints():
    """Test all AI endpoints"""
    base_url = "http://localhost:8000"
    
    print("🤖 Testing AI Endpoints")
    print("=" * 40)
    
    # Test 1: AI Status
    print("\n1. Testing AI Status...")
    try:
        response = requests.get(f"{base_url}/ai/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Status: {data}")
        else:
            print(f"❌ AI Status failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ AI Status error: {e}")
        return
    
    # Test 2: Market Analysis
    print("\n2. Testing Market Analysis...")
    market_data = {
        "symbol": "BTCUSDT",
        "price": 45000,
        "change_24h": 2.5,
        "volume": 2500000000,
        "rsi": 65,
        "macd": "bullish"
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/analyze-market",
            json=market_data,
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Market Analysis:")
            print(f"   Signal: {data['analysis'].get('signal', 'N/A')}")
            print(f"   Confidence: {data['analysis'].get('confidence', 'N/A')}")
            print(f"   Risk Level: {data['analysis'].get('risk_level', 'N/A')}")
        else:
            print(f"❌ Market Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Market Analysis error: {e}")
    
    # Test 3: Trade Evaluation
    print("\n3. Testing Trade Evaluation...")
    trade_data = {
        "symbol": "ETHUSDT",
        "action": "BUY",
        "entry_price": 3000,
        "current_price": 2950,
        "position_size": 3,
        "available_capital": 10000,
        "recent_performance": "positive"
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/evaluate-trade",
            json=trade_data,
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trade Evaluation:")
            print(f"   Approved: {data['evaluation'].get('approved', 'N/A')}")
            print(f"   Risk Score: {data['evaluation'].get('risk_score', 'N/A')}")
            print(f"   Position Size: {data['evaluation'].get('recommended_position_size', 'N/A')}")
        else:
            print(f"❌ Trade Evaluation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Trade Evaluation error: {e}")
    
    # Test 4: Portfolio Analysis
    print("\n4. Testing Portfolio Analysis...")
    portfolio_data = {
        "total_capital": 10000,
        "current_value": 10500,
        "total_pnl": 500,
        "win_rate": 65,
        "avg_return": 2.5,
        "total_trades": 20,
        "recent_trades": ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/portfolio-analysis",
            json=portfolio_data,
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Portfolio Analysis:")
            print(f"   Performance Grade: {data['analysis'].get('performance_grade', 'N/A')}")
            print(f"   Risk Assessment: {data['analysis'].get('risk_assessment', 'N/A')}")
        else:
            print(f"❌ Portfolio Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Portfolio Analysis error: {e}")
    
    # Test 5: Trading Insights
    print("\n5. Testing Trading Insights...")
    context_data = {
        "context": "Bitcoin is at $45,000 with strong institutional buying and positive market sentiment"
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/insights",
            json=context_data,
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trading Insights:")
            print(f"   {data['insights'][:200]}...")
        else:
            print(f"❌ Trading Insights failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Trading Insights error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 AI Integration Test Complete!")

if __name__ == "__main__":
    test_ai_endpoints() 