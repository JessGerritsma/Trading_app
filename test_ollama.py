 
import requests
import json

def test_ollama():
    print("Testing Ollama connection...")
    
    try:
        # Test if Ollama API is responding
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        print(f"Ollama Status: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            available_models = [m['name'] for m in models.get('models', [])]
            print(f"Available models: {available_models}")
            
            # Test generation if models are available
            if available_models:
                print("\nTesting model generation...")
                test_generation()
            else:
                print("No models found!")
        else:
            print("Ollama API not responding properly")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Ollama")
        print("Solutions:")
        print("1. Make sure Ollama is installed")
        print("2. Run: ollama serve")
        print("3. Check if port 11434 is available")
    except Exception as e:
        print(f"Error: {e}")

def test_generation():
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1:8b-instruct-q4_0",
        "prompt": "Say hello and confirm you can help with trading",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"Model Response: {result.get('response', 'No response')}")
            print("SUCCESS: Ollama is working!")
        else:
            print(f"Generation failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Generation error: {e}")

if __name__ == "__main__":
    test_ollama()