#!/usr/bin/env python3
"""
Test script to verify Ollama API connection and model functionality
"""

import requests
import json
import time

def test_ollama_connection():
    """Test basic Ollama API connectivity"""
    print("🔍 Testing Ollama API connection...")
    
    # Test if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama API is running")
            models = response.json()
            print(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
            return True
        else:
            print(f"❌ Ollama API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama API: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

def test_model_generation():
    """Test model generation with a simple prompt"""
    print("\n🤖 Testing model generation...")
    
    url = "http://localhost:11434/api/generate"
    prompt = "You are a helpful trading assistant. Respond with just: 'Hello, I can help with trading analysis.'"
    
    payload = {
        "model": "llama3.1:8b-instruct-q4_0",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9
        }
    }
    
    try:
        print("📤 Sending request to Ollama...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Model responded successfully!")
            print(f"📝 Response: {result.get('response', 'No response field')}")
            print(f"⏱️  Generation time: {result.get('total_duration', 0) / 1e9:.2f} seconds")
            return True
        else:
            print(f"❌ Generation failed with status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (model might be loading)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_trading_analysis():
    """Test with a trading-specific prompt"""
    print("\n📊 Testing trading analysis capability...")
    
    url = "http://localhost:11434/api/generate"
    prompt = """You are a crypto trading analyst. Analyze this scenario and respond in JSON format:

Scenario: BTC price is at $45,000, RSI is 70, MACD shows bullish crossover.

Respond with this exact JSON structure:
{
    "analysis": "your analysis here",
    "signal": "BUY/SELL/HOLD",
    "confidence": "HIGH/MEDIUM/LOW",
    "risk_level": "HIGH/MEDIUM/LOW"
}"""
    
    payload = {
        "model": "llama3.1:8b-instruct-q4_0",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }
    
    try:
        print("📤 Sending trading analysis request...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Trading analysis completed!")
            print(f"📝 Response: {result.get('response', 'No response')}")
            
            # Try to parse as JSON
            try:
                analysis_json = json.loads(result.get('response', '{}'))
                print("✅ Response is valid JSON!")
                print(f"📊 Analysis: {analysis_json}")
                return True
            except json.JSONDecodeError:
                print("⚠️  Response is not valid JSON, but model is working")
                return True
        else:
            print(f"❌ Trading analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Trading analysis error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Ollama Integration Tests\n")
    
    # Test 1: Basic connectivity
    if not test_ollama_connection():
        print("\n❌ Basic connectivity failed. Please check Ollama installation.")
        return
    
    # Test 2: Model generation
    if not test_model_generation():
        print("\n❌ Model generation failed. Please check model availability.")
        return
    
    # Test 3: Trading analysis
    if not test_trading_analysis():
        print("\n⚠️  Trading analysis had issues, but basic functionality works.")
    
    print("\n🎉 All tests completed! Your Ollama setup is ready for trading system integration.")
    print("\n📋 Next steps:")
    print("1. Integrate LLM service into your trading app")
    print("2. Set up Binance API connection")
    print("3. Create database schema for trade data")

if __name__ == "__main__":
    main()