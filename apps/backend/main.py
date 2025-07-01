# apps/backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
import asyncio
import logging
from src.services.llm_service import LLMService
from src.services.automated_trading import AutomatedTradingService
from src.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Trading Bot API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TradeRequest(BaseModel):
    symbol: str
    side: str  # BUY or SELL
    type: str  # MARKET or LIMIT
    quantity: float
    price: Optional[float] = None

class StrategyConfig(BaseModel):
    name: str
    symbol: str
    parameters: dict
    active: bool = False

class TradeResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[str] = None
    data: Optional[dict] = None

# Global variables
binance_client: Optional[Client] = None
trading_service: Optional[AutomatedTradingService] = None

@app.on_event("startup")
async def startup_event():
    """Initialize Binance client and trading service on startup"""
    global binance_client, trading_service
    
    # Get API keys from environment variables
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_SECRET_KEY")
    
    if not api_key or not api_secret:
        logger.warning("Binance API keys not found. Some features will be disabled.")
        return
    
    try:
        # Initialize Binance client for testnet
        binance_client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True  # This is crucial for testnet
        )
        
        # Test connection
        account_info = binance_client.get_account()
        logger.info("Successfully connected to Binance Testnet")
        logger.info(f"Account status: {account_info.get('accountType', 'Unknown')}")
        
        # Initialize LLMService and AutomatedTradingService
        llm_service = LLMService()
        trading_pairs = settings.trading_pairs_list
        trading_service = AutomatedTradingService(llm_service, trading_pairs)
        # Start real-time trading in the background if trading_service is initialized
        if trading_service:
            asyncio.create_task(trading_service.start_realtime_trading())
            logger.info("Automated trading service started in background.")
        
    except Exception as e:
        logger.error(f"Failed to connect to Binance Testnet: {str(e)}")
        binance_client = None

@app.get("/")
async def root():
    return {"message": "Trading Bot API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    binance_status = "connected" if binance_client else "disconnected"
    return {
        "status": "healthy",
        "binance_testnet": binance_status,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/account")
async def get_account_info():
    """Get account information from Binance testnet"""
    if not binance_client:
        raise HTTPException(status_code=503, detail="Binance client not initialized")
    
    try:
        account_info = binance_client.get_account()
        
        # Format balance information
        balances = []
        for balance in account_info['balances']:
            if float(balance['free']) > 0 or float(balance['locked']) > 0:
                balances.append({
                    'asset': balance['asset'],
                    'free': float(balance['free']),
                    'locked': float(balance['locked']),
                    'total': float(balance['free']) + float(balance['locked'])
                })
        
        return {
            'account_type': account_info.get('accountType', 'SPOT'),
            'balances': balances,
            'can_trade': account_info.get('canTrade', False),
            'can_withdraw': account_info.get('canWithdraw', False),
            'can_deposit': account_info.get('canDeposit', False)
        }
    
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        raise HTTPException(status_code=400, detail=f"Binance API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/prices/{symbol}")
async def get_symbol_price(symbol: str):
    """Get current price for a symbol"""
    if not binance_client:
        raise HTTPException(status_code=503, detail="Binance client not initialized")
    
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol.upper())
        return {
            'symbol': ticker['symbol'],
            'price': float(ticker['price'])
        }
    except BinanceAPIException as e:
        raise HTTPException(status_code=400, detail=f"Invalid symbol or API error: {e}")

@app.get("/prices")
async def get_all_prices():
    """Get prices for major trading pairs"""
    if not binance_client:
        raise HTTPException(status_code=503, detail="Binance client not initialized")
    
    try:
        # Get prices for major pairs
        major_pairs = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
        prices = []
        
        for symbol in major_pairs:
            try:
                ticker = binance_client.get_symbol_ticker(symbol=symbol)
                prices.append({
                    'symbol': ticker['symbol'],
                    'price': float(ticker['price'])
                })
            except:
                continue  # Skip if symbol not available
        
        return {'prices': prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {e}")

@app.post("/trade", response_model=TradeResponse)
async def place_trade(trade_request: TradeRequest):
    """Place a trade order"""
    if not binance_client:
        raise HTTPException(status_code=503, detail="Binance client not initialized")
    
    try:
        order_params = {
            'symbol': trade_request.symbol.upper(),
            'side': trade_request.side.upper(),
            'type': trade_request.type.upper(),
            'quantity': trade_request.quantity
        }
        
        # Add price for limit orders
        if trade_request.type.upper() == 'LIMIT':
            if not trade_request.price:
                raise HTTPException(status_code=400, detail="Price required for limit orders")
            order_params['price'] = trade_request.price
            order_params['timeInForce'] = 'GTC'  # Good Till Cancelled
        
        # Place the order
        order = binance_client.create_order(**order_params)
        
        return TradeResponse(
            success=True,
            message="Order placed successfully",
            order_id=str(order['orderId']),
            data=order
        )
        
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        return TradeResponse(
            success=False,
            message=f"Binance API error: {e}",
            order_id=None,
            data=None
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return TradeResponse(
            success=False,
            message=f"Internal server error: {e}",
            order_id=None,
            data=None
        )

@app.get("/orders/{symbol}")
async def get_orders(symbol: str, limit: int = 10):
    """Get recent orders for a symbol"""
    if not binance_client:
        raise HTTPException(status_code=503, detail="Binance client not initialized")
    
    try:
        orders = binance_client.get_all_orders(symbol=symbol.upper(), limit=limit)
        
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                'orderId': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': float(order['origQty']),
                'price': float(order['price']) if order['price'] != '0.00000000' else None,
                'status': order['status'],
                'time': order['time']
            })
        
        return {'orders': formatted_orders}
    
    except BinanceAPIException as e:
        raise HTTPException(status_code=400, detail=f"Binance API error: {e}")

@app.get("/strategies")
async def get_strategies():
    """Get available trading strategies (placeholder)"""
    # This will be expanded when we implement actual strategies
    return {
        'strategies': [
            {
                'id': 1,
                'name': 'Mean Reversion',
                'description': 'Buy low, sell high based on price movements',
                'active': False,
                'parameters': {'lookback_period': 20, 'threshold': 0.02}
            },
            {
                'id': 2,
                'name': 'Momentum',
                'description': 'Follow trending price movements',
                'active': False,
                'parameters': {'fast_ma': 12, 'slow_ma': 26}
            },
            {
                'id': 3,
                'name': 'AI Hybrid',
                'description': 'ML-powered trading decisions',
                'active': False,
                'parameters': {'model_version': '1.0', 'confidence_threshold': 0.7}
            }
        ]
    }

@app.post("/strategies/{strategy_id}/toggle")
async def toggle_strategy(strategy_id: int):
    """Toggle a strategy on/off (placeholder)"""
    # This will be implemented when we have actual strategy execution
    return {
        'strategy_id': strategy_id,
        'message': 'Strategy toggle functionality coming soon',
        'active': False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)