#!/usr/bin/env python3
"""
Fix Python 3.13 compatibility issues with SQLAlchemy and other packages
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 13:
        print("✅ Python 3.13 detected - applying compatibility fixes")
        return True
    else:
        print(f"⚠️  Python {version.major}.{version.minor} detected - compatibility fixes may not be needed")
        return True

def upgrade_sqlalchemy():
    """Upgrade SQLAlchemy to Python 3.13 compatible version"""
    commands = [
        "pip install --upgrade sqlalchemy>=2.0.25",
        "pip install --upgrade alembic>=1.13.0",
        "pip install --upgrade pydantic>=2.5.0",
        "pip install --upgrade pydantic-settings>=2.1.0"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Upgrading {cmd.split()[-1]}"):
            return False
    return True

def install_ollama_integration():
    """Install Ollama integration package"""
    return run_command("pip install ollama>=0.1.7", "Installing Ollama integration")

def test_imports():
    """Test if critical imports work"""
    print("\n🧪 Testing imports...")
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__} imported successfully")
    except Exception as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported successfully")
    except Exception as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import binance
        print("✅ python-binance imported successfully")
    except Exception as e:
        print(f"❌ python-binance import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama package imported successfully")
    except Exception as e:
        print(f"❌ ollama package import failed: {e}")
        return False
    
    return True

def main():
    """Main function to fix Python 3.13 compatibility"""
    print("🔧 Python 3.13 Compatibility Fix")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Upgrade critical packages
    if not upgrade_sqlalchemy():
        print("❌ Failed to upgrade SQLAlchemy")
        return False
    
    # Install Ollama integration
    if not install_ollama_integration():
        print("❌ Failed to install Ollama integration")
        return False
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Python 3.13 compatibility fix completed!")
    print("\n🚀 Next steps:")
    print("1. Try running the backend: cd apps/backend && python app.py")
    print("2. If successful, test the health endpoint: curl http://localhost:8000/health")
    print("3. Start the frontend: cd apps/frontend && npm run dev")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 