# Quick Start Guide - Cryptocurrency Trading System

## 🚀 Immediate Next Steps (Today)

### 1. Set Up Environment Variables
```bash
# Copy the environment template
cp apps/backend/env.example apps/backend/.env

# Edit .env with your Binance testnet credentials
# Get testnet API keys from: https://testnet.binance.vision/
```

### 2. Install Dependencies
```bash
cd apps/backend
pip install -r requirements.txt
```

### 3. Create Basic Backend Structure
```bash
# Create the new directory structure
mkdir -p apps/backend/src/{api,core,models,services,strategies,ai,utils}
mkdir -p apps/backend/tests/{test_api,test_services,test_strategies}
mkdir -p apps/backend/data/{sqlite,logs}
```

### 4. Start with Core Configuration
Create `apps/backend/src/core/config.py`:
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./data/sqlite/trading_bot.db"
    
    # Binance
    binance_api_key: str
    binance_secret_key: str
    binance_testnet: bool = True
    
    # AI/LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # Trading
    default_symbol: str = "BTCUSDT"
    max_position_size: float = 0.1
    stop_loss_percentage: float = 0.02
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 5. Create Database Models
Create `apps/backend/src/models/trade.py`:
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String)  # BUY or SELL
    quantity = Column(Float)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    strategy = Column(String)
    ai_decision = Column(Boolean, default=False)
```

### 6. Enhance Your Existing App
Update `apps/backend/app.py`:
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Trading Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Binance client
binance_client = Client(
    os.getenv("BINANCE_API_KEY"),
    os.getenv("BINANCE_SECRET_KEY"),
    testnet=os.getenv("BINANCE_TESTNET", "true").lower() == "true"
)

@app.get("/health")
async def health_check():
    try:
        # Test Binance connection
        server_time = binance_client.get_server_time()
        return {
            "status": "healthy",
            "binance_testnet": os.getenv("BINANCE_TESTNET", "true"),
            "server_time": server_time
        }
    except BinanceAPIException as e:
        return {
            "status": "error",
            "message": f"Binance API error: {e.message}"
        }

@app.get("/prices")
async def get_prices():
    try:
        # Get current prices for major pairs
        symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT"]
        prices = []
        
        for symbol in symbols:
            ticker = binance_client.get_symbol_ticker(symbol=symbol)
            prices.append({
                "symbol": symbol,
                "price": float(ticker["price"])
            })
        
        return {"prices": prices}
    except BinanceAPIException as e:
        raise HTTPException(status_code=400, detail=f"Binance API error: {e.message}")

@app.get("/account")
async def get_account():
    try:
        account = binance_client.get_account()
        return {
            "account_type": "SPOT",
            "can_trade": account["canTrade"],
            "balances": [
                {
                    "asset": balance["asset"],
                    "free": float(balance["free"]),
                    "total": float(balance["total"])
                }
                for balance in account["balances"]
                if float(balance["total"]) > 0
            ]
        }
    except BinanceAPIException as e:
        raise HTTPException(status_code=400, detail=f"Binance API error: {e.message}")

@app.post("/trade")
async def place_trade(trade_data: dict):
    try:
        # Validate trade data
        required_fields = ["symbol", "side", "type", "quantity"]
        for field in required_fields:
            if field not in trade_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Place order
        order = binance_client.create_order(
            symbol=trade_data["symbol"],
            side=trade_data["side"],
            type=trade_data["type"],
            quantity=trade_data["quantity"],
            price=trade_data.get("price")  # Optional for market orders
        )
        
        return {
            "success": True,
            "order": order
        }
    except BinanceAPIException as e:
        return {
            "success": False,
            "message": f"Binance API error: {e.message}"
        }
```

### 7. Test Your Setup
```bash
# Start the backend
cd apps/backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Test the API
curl http://localhost:8000/health
curl http://localhost:8000/prices
```

## 🎯 Week 1 Goals

### Day 1-2: Foundation
- [x] Set up environment variables
- [x] Install dependencies
- [x] Create basic backend structure
- [x] Test Binance API connection

### Day 3-4: Database
- [ ] Set up SQLite database
- [ ] Create database models
- [ ] Add Alembic migrations
- [ ] Test database operations

### Day 5-7: API Enhancement
- [ ] Add more trading endpoints
- [ ] Implement error handling
- [ ] Add request validation
- [ ] Create API documentation

## 🔧 Essential Tools to Install

### 1. Ollama (for Local LLM)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Test
ollama run llama2 "Hello, world!"
```

### 2. Redis (for Caching)
```bash
# Install Redis
# On Windows: Download from https://redis.io/download
# On Mac: brew install redis
# On Linux: sudo apt-get install redis-server

# Start Redis
redis-server
```

### 3. Development Tools
```bash
# Install development dependencies
pip install pytest pytest-asyncio pytest-cov
pip install black flake8 mypy

# Set up pre-commit hooks
pre-commit install
```

## 📊 Monitoring Your Progress

### Daily Checklist
- [ ] API endpoints responding correctly
- [ ] Database operations working
- [ ] Binance API connection stable
- [ ] No critical errors in logs
- [ ] Frontend can connect to backend

### Weekly Milestones
- **Week 1**: Basic trading infrastructure
- **Week 2**: Strategy implementation
- **Week 3**: AI integration
- **Week 4**: Frontend enhancement
- **Week 5**: Testing and security
- **Week 6**: Production deployment

## 🚨 Important Notes

### Security First
- Never commit API keys to version control
- Use testnet for development
- Implement proper authentication
- Add rate limiting

### Risk Management
- Start with small trade amounts
- Implement stop-losses
- Monitor system performance
- Keep detailed logs

### Testing Strategy
- Test with paper trading first
- Use historical data for backtesting
- Implement comprehensive error handling
- Monitor for edge cases

## 📞 Getting Help

### Common Issues
1. **Binance API errors**: Check API keys and permissions
2. **Database connection issues**: Verify SQLite file permissions
3. **CORS errors**: Check frontend URL in CORS settings
4. **Import errors**: Verify all dependencies are installed

### Resources
- [Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Ollama Documentation](https://ollama.ai/docs)

### Next Steps
After completing the quick start:
1. Follow the detailed development plan
2. Implement the strategy framework
3. Add AI integration
4. Enhance the frontend
5. Add comprehensive testing 