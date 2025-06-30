#!/usr/bin/env python3
"""
Test script to verify the setup is working correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.core.config import settings
        print("✅ Config imported successfully")
        print(f"   App name: {settings.app_name}")
        print(f"   Environment: {settings.environment}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from src.core.database import get_db, create_tables
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from src.models import Trade, Strategy, MarketData, AIDecision
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from binance.client import Client
        print("✅ Binance client imported successfully")
    except Exception as e:
        print(f"❌ Binance client import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and table creation"""
    print("\nTesting database...")
    
    try:
        from src.core.database import create_tables, init_db
        create_tables()
        print("✅ Database tables created successfully")
        
        init_db()
        print("✅ Database initialized with default data")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    return True

def test_binance_connection():
    """Test Binance API connection"""
    print("\nTesting Binance connection...")
    
    try:
        from src.core.config import settings
        from binance.client import Client
        
        if not settings.binance_api_key or not settings.binance_secret_key:
            print("⚠️  Binance API keys not configured (this is expected for initial setup)")
            return True
        
        client = Client(settings.binance_api_key, settings.binance_secret_key, testnet=settings.binance_testnet)
        server_time = client.get_server_time()
        print(f"✅ Binance connection successful (server time: {server_time})")
        
    except Exception as e:
        print(f"❌ Binance connection failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Trading Bot Setup Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test database
    if not test_database():
        success = False
    
    # Test Binance
    if not test_binance_connection():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Configure your .env file with Binance API keys")
        print("2. Run: python app.py")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main() 