#!/usr/bin/env python3
"""
Setup script for Trading Bot environment configuration
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    backend_dir = Path("apps/backend")
    env_example = backend_dir / "env.example"
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please configure your Binance API keys in apps/backend/.env")
    else:
        print("❌ env.example not found")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    # Check Python packages
    try:
        import fastapi
        print("✅ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not installed - run: pip install -r apps/backend/requirements.txt")
    
    try:
        import binance
        print("✅ python-binance installed")
    except ImportError:
        print("❌ python-binance not installed")
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy installed")
    except ImportError:
        print("❌ SQLAlchemy not installed")

def check_services():
    """Check if required services are running"""
    print("\n🔍 Checking services...")
    
    # Check if backend is running
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server running on http://localhost:8000")
        else:
            print("⚠️  Backend server responding but not healthy")
    except:
        print("❌ Backend server not running - start with: cd apps/backend && python app.py")
    
    # Check if frontend is running
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server running on http://localhost:3000")
        else:
            print("⚠️  Frontend server responding but not healthy")
    except:
        print("❌ Frontend server not running - start with: cd apps/frontend && npm run dev")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🚀 NEXT STEPS TO GET STARTED")
    print("="*60)
    
    print("\n1. 🔑 Configure Binance API Keys:")
    print("   - Visit: https://testnet.binance.vision/")
    print("   - Create testnet account and get API keys")
    print("   - Update apps/backend/.env with your keys")
    
    print("\n2. 🏃‍♂️ Start the Services:")
    print("   Backend: cd apps/backend && python app.py")
    print("   Frontend: cd apps/frontend && npm run dev")
    
    print("\n3. 🌐 Access the Application:")
    print("   Frontend: http://localhost:3000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Health Check: http://localhost:8000/health")
    
    print("\n4. 🧪 Test the Setup:")
    print("   - Check health endpoint")
    print("   - Test price fetching")
    print("   - Verify database connection")
    
    print("\n5. 📊 Start Trading:")
    print("   - Configure trading strategies")
    print("   - Set up risk management")
    print("   - Enable AI decision making")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 Trading Bot Environment Setup")
    print("="*50)
    
    create_env_file()
    check_dependencies()
    check_services()
    print_next_steps()

if __name__ == "__main__":
    main() 