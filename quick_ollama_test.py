#!/usr/bin/env python3
"""
Quick test to verify Ollama is working properly
"""

import requests
import json

def test_ollama_direct():
    """Test direct Ollama API calls"""
    print("🤖 Quick Ollama Test")
    print("=" * 30)
    
    # Test 1: Check available models
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Available models: {[model['name'] for model in models.get('models', [])]}")
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting models: {e}")
        return
    
    # Test 2: Simple prompt
    try:
        payload = {
            "model": "llama3.1:8b-instruct-q4_0",
            "prompt": "You are a crypto trading expert. Give me a brief market analysis for Bitcoin in 2 sentences.",
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }
        
        print("\n🧪 Testing trading analysis prompt...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama Response:")
            print(f"   {result.get('response', 'No response')}")
            print(f"\n📊 Model: {result.get('model', 'Unknown')}")
            print(f"⏱️  Duration: {result.get('duration', 0):.2f}s")
        else:
            print(f"❌ Prompt failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Prompt test failed: {e}")
    
    print("\n" + "=" * 30)
    print("💡 Next: Restart backend and test AI endpoints")

if __name__ == "__main__":
    test_ollama_direct() 