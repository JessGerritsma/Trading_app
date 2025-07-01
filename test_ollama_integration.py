#!/usr/bin/env python3
"""
Test script for Ollama integration with the trading system
"""

import requests
import json
import time

def test_ollama_connection():
    """Test direct connection to Ollama"""
    print("🔍 Testing direct Ollama connection...")
    
    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running")
            print(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
            return True
        else:
            print(f"❌ Ollama responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama at http://localhost:11434")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Ollama connection error: {e}")
        return False

def test_simple_prompt():
    """Test a simple prompt with Ollama"""
    print("\n🧪 Testing simple prompt...")
    
    try:
        payload = {
            "model": "llama3.1:8b-instruct-q4_0",
            "prompt": "Hello! Can you respond with 'Ollama is working'?",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama responded: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prompt test failed: {e}")
        return False

def test_backend_ai_endpoints():
    """Test the backend AI endpoints"""
    print("\n🌐 Testing backend AI endpoints...")
    
    # Test AI status endpoint
    try:
        response = requests.get("http://localhost:8000/ai/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ AI Status: {status}")
            return True
        else:
            print(f"❌ AI status endpoint error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("💡 Make sure backend is running: cd apps/backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Backend AI test failed: {e}")
        return False

def test_market_analysis():
    """Test market analysis with AI"""
    print("\n📊 Testing market analysis...")
    
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
            "http://localhost:8000/ai/analyze-market",
            json=market_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Market analysis successful:")
            print(f"   Signal: {result['analysis'].get('signal', 'N/A')}")
            print(f"   Confidence: {result['analysis'].get('confidence', 'N/A')}")
            print(f"   Risk Level: {result['analysis'].get('risk_level', 'N/A')}")
            return True
        else:
            print(f"❌ Market analysis error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Market analysis test failed: {e}")
        return False

def test_trade_evaluation():
    """Test trade evaluation with AI"""
    print("\n💰 Testing trade evaluation...")
    
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
            "http://localhost:8000/ai/evaluate-trade",
            json=trade_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Trade evaluation successful:")
            print(f"   Approved: {result['evaluation'].get('approved', 'N/A')}")
            print(f"   Risk Score: {result['evaluation'].get('risk_score', 'N/A')}")
            print(f"   Position Size: {result['evaluation'].get('recommended_position_size', 'N/A')}")
            return True
        else:
            print(f"❌ Trade evaluation error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Trade evaluation test failed: {e}")
        return False

def main():
    """Run all Ollama integration tests"""
    print("🤖 Ollama Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Direct Ollama Connection", test_ollama_connection),
        ("Simple Prompt Test", test_simple_prompt),
        ("Backend AI Status", test_backend_ai_endpoints),
        ("Market Analysis", test_market_analysis),
        ("Trade Evaluation", test_trade_evaluation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Ollama integration is working perfectly.")
    elif passed >= 3:
        print("⚠️  Most tests passed. Check the failed tests above.")
    else:
        print("❌ Multiple tests failed. Please check your Ollama setup.")
    
    print("\n🚀 Next steps:")
    print("1. If all tests passed, your AI integration is ready!")
    print("2. You can now use AI-powered trading decisions in your system.")
    print("3. Test the frontend integration with these AI endpoints.")

if __name__ == "__main__":
    main() 