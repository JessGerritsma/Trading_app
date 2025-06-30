from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
from binance.exceptions import BinanceAPIException
from sqlalchemy.orm import Session
import os
import logging
from dotenv import load_dotenv

# Import our new modules
from src.core.config import settings
from src.core.database import get_db, create_tables, init_db
from src.models import Trade, Strategy, MarketData, AIDecision

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Cryptocurrency Trading Bot with AI Integration"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Binance client
try:
    binance_client = Client(
        settings.binance_api_key,
        settings.binance_secret_key,
        testnet=settings.binance_testnet
    )
    logger.info("Binance client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Binance client: {e}")
    binance_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize database and other startup tasks"""
    try:
        # Create database tables
        create_tables()
        
        # Initialize with default data
        init_db()
        
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name} v{settings.app_version}",
        "status": "running",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        health_status = {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "binance_testnet": settings.binance_testnet,
            "database": "connected",
            "ai_enabled": settings.enable_ai_decisions
        }
        
        # Test Binance connection if client is available
        if binance_client:
            try:
                server_time = binance_client.get_server_time()
                health_status["binance_status"] = "connected"
                health_status["binance_server_time"] = server_time
            except BinanceAPIException as e:
                health_status["binance_status"] = "error"
                health_status["binance_error"] = str(e)
        else:
            health_status["binance_status"] = "not_configured"
        
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/prices")
async def get_prices():
    """Get current prices for configured trading pairs"""
    try:
        if not binance_client:
            raise HTTPException(status_code=503, detail="Binance client not configured")
        
        prices = []
        for symbol in settings.trading_pairs_list:
            try:
                ticker = binance_client.get_symbol_ticker(symbol=symbol)
                prices.append({
                    "symbol": symbol,
                    "price": float(ticker["price"]),
                    "timestamp": ticker.get("time")
                })
            except BinanceAPIException as e:
                logger.warning(f"Failed to get price for {symbol}: {e}")
                prices.append({
                    "symbol": symbol,
                    "price": None,
                    "error": str(e)
                })
        
        return {"prices": prices}
    except Exception as e:
        logger.error(f"Error getting prices: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get prices: {str(e)}")

@app.get("/account")
async def get_account():
    """Get Binance account information"""
    try:
        if not binance_client:
            raise HTTPException(status_code=503, detail="Binance client not configured")
        
        account = binance_client.get_account()
        return {
            "account_type": "SPOT",
            "can_trade": account["canTrade"],
            "can_withdraw": account["canWithdraw"],
            "can_deposit": account["canDeposit"],
            "balances": [
                {
                    "asset": balance["asset"],
                    "free": float(balance["free"]),
                    "locked": float(balance["locked"]),
                    "total": float(balance["total"])
                }
                for balance in account["balances"]
                if float(balance["total"]) > 0
            ]
        }
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        raise HTTPException(status_code=400, detail=f"Binance API error: {e.message}")
    except Exception as e:
        logger.error(f"Error getting account info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get account info: {str(e)}")

@app.get("/strategies")
async def get_strategies(db: Session = Depends(get_db)):
    """Get all trading strategies"""
    try:
        strategies = db.query(Strategy).all()
        return {
            "strategies": [strategy.to_dict() for strategy in strategies]
        }
    except Exception as e:
        logger.error(f"Error getting strategies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get strategies: {str(e)}")

@app.get("/trades")
async def get_trades(
    symbol: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get trade history"""
    try:
        query = db.query(Trade)
        
        if symbol:
            query = query.filter(Trade.symbol == symbol)
        
        trades = query.order_by(Trade.timestamp.desc()).limit(limit).all()
        
        return {
            "trades": [trade.to_dict() for trade in trades]
        }
    except Exception as e:
        logger.error(f"Error getting trades: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get trades: {str(e)}")

@app.post("/trade")
async def place_trade(trade_data: dict, db: Session = Depends(get_db)):
    """Place a new trade"""
    try:
        if not binance_client:
            raise HTTPException(status_code=503, detail="Binance client not configured")
        
        # Validate required fields
        required_fields = ["symbol", "side", "type", "quantity"]
        for field in required_fields:
            if field not in trade_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Validate trade amount
        quantity = float(trade_data["quantity"])
        if quantity < settings.min_trade_amount:
            raise HTTPException(
                status_code=400, 
                detail=f"Trade amount {quantity} is below minimum {settings.min_trade_amount}"
            )
        
        if quantity > settings.max_trade_amount:
            raise HTTPException(
                status_code=400, 
                detail=f"Trade amount {quantity} exceeds maximum {settings.max_trade_amount}"
            )
        
        # Place order on Binance
        order_params = {
            "symbol": trade_data["symbol"],
            "side": trade_data["side"],
            "type": trade_data["type"],
            "quantity": trade_data["quantity"]
        }
        
        if trade_data.get("price"):
            order_params["price"] = trade_data["price"]
        
        order = binance_client.create_order(**order_params)
        
        # Save trade to database
        db_trade = Trade(
            symbol=trade_data["symbol"],
            side=trade_data["side"],
            type=trade_data["type"],
            quantity=quantity,
            price=float(trade_data.get("price", 0)),
            order_id=order.get("orderId"),
            status=order.get("status", "PENDING"),
            strategy=trade_data.get("strategy"),
            ai_decision=trade_data.get("ai_decision", False),
            ai_reasoning=trade_data.get("ai_reasoning")
        )
        
        db.add(db_trade)
        db.commit()
        db.refresh(db_trade)
        
        return {
            "success": True,
            "trade": db_trade.to_dict(),
            "binance_order": order
        }
        
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        return {
            "success": False,
            "message": f"Binance API error: {e.message}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error placing trade: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to place trade: {str(e)}")

@app.get("/market-data/{symbol}")
async def get_market_data(
    symbol: str,
    interval: str = "1h",
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get market data for a symbol"""
    try:
        if not binance_client:
            raise HTTPException(status_code=503, detail="Binance client not configured")
        
        # Get historical klines from Binance
        klines = binance_client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        
        market_data = []
        for kline in klines:
            market_data.append({
                "timestamp": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            })
        
        return {
            "symbol": symbol,
            "interval": interval,
            "data": market_data
        }
        
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        raise HTTPException(status_code=400, detail=f"Binance API error: {e.message}")
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get market data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )