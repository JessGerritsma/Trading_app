"""
Test the LLM Service integration
Run this to verify the trading AI is working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.llm_service import LLMService
import json

def test_market_analysis():
    print("🧠 Testing Market Analysis...")
    
    llm = LLMService()
    
    # Sample market data
    market_data = {
        "symbol": "BTCUSDT",
        "price": 45000,
        "change_24h": 3.2,
        "volume": 2500000000,
        "rsi": 68,
        "macd": "bullish crossover"
    }
    
    result = llm.analyze_market_data(market_data)
    print(f"📊 Analysis Result:")
    print(json.dumps(result, indent=2))
    
    return result.get('signal') != 'HOLD'  # Success if we got a real signal

def test_trade_evaluation():
    print("\n⚖️ Testing Trade Evaluation...")
    
    llm = LLMService()
    
    trade_data = {
        "symbol": "ETHUSDT",
        "action": "BUY",
        "entry_price": 2800,
        "current_price": 2820,
        "position_size": 3,
        "available_capital": 1000,
        "recent_performance": "2 wins, 1 loss in last 3 trades"
    }
    
    result = llm.evaluate_trade_opportunity(trade_data)
    print(f"🎯 Trade Evaluation:")
    print(json.dumps(result, indent=2))
    
    return 'approved' in result

def test_portfolio_analysis():
    print("\n📈 Testing Portfolio Analysis...")
    
    llm = LLMService()
    
    portfolio_data = {
        "total_capital": 1000,
        "current_value": 1150,
        "total_pnl": 150,
        "win_rate": 65,
        "avg_return": 2.3,
        "total_trades": 15,
        "recent_trades": ["BTC +5%", "ETH -2%", "ADA +8%"]
    }
    
    result = llm.analyze_portfolio_performance(portfolio_data)
    print(f"💼 Portfolio Analysis:")
    print(json.dumps(result, indent=2))
    
    return 'performance_grade' in result

def test_trading_insights():
    print("\n💡 Testing Trading Insights...")
    
    llm = LLMService()
    
    market_context = """
    Bitcoin is consolidating around $45,000 after breaking above $44,000 resistance.
    Ethereum is showing strength relative to Bitcoin.
    Overall crypto market sentiment is cautiously optimistic.
    Fed meeting next week may impact markets.
    """
    
    insights = llm.generate_trading_insights(market_context)
    print(f"🔍 Market Insights:")
    print(insights)
    
    return len(insights) > 100  # Success if we got substantial insights

def main():
    print("🚀 Testing LLM Trading Service Integration\n")
    
    tests = [
        ("Market Analysis", test_market_analysis),
        ("Trade Evaluation", test_trade_evaluation),
        ("Portfolio Analysis", test_portfolio_analysis),
        ("Trading Insights", test_trading_insights)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"✅ {test_name}: {'PASSED' if success else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    print(f"\n📋 Test Summary:")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your LLM trading service is ready!")
        print("\n📋 Next Steps:")
        print("1. Set up Binance API connection")
        print("2. Create database schema")
        print("3. Build the trading engine")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()