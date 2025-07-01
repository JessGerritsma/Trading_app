from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client
from binance.exceptions import BinanceAPIException
from sqlalchemy.orm import Session
import os
import logging
from typing import Optional
from dotenv import load_dotenv
import subprocess

# Import our new modules
from src.core.config import settings
from src.core.database import get_db, create_tables, init_db
from src.models import Trade, Strategy, MarketData, AIDecision
from src.services.llm_service import LLMService
from src.services.automated_trading import AutomatedTradingService

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

# Initialize LLM service
try:
    llm_service = LLMService(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model
    )
    logger.info(f"LLM service initialized with model: {settings.ollama_model}")
except Exception as e:
    logger.error(f"Failed to initialize LLM service: {e}")
    llm_service = None

# Initialize Automated Trading service
try:
    automated_trading_service = AutomatedTradingService(llm_service, settings.trading_pairs_list) if llm_service else None
    logger.info("Automated trading service initialized")
except Exception as e:
    logger.error(f"Failed to initialize automated trading service: {e}")
    automated_trading_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize database and other startup tasks"""
    try:
        # Check if Ollama (Llama server) is running
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("localhost", 11434))
            s.close()
        except Exception:
            # Just log a warning, do not try to start Ollama in Docker
            logger.warning("Ollama is not running on localhost:11434. Please start it manually on the host.")
        # Initialize database
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
        
        # Process balances safely
        balances = []
        for balance in account["balances"]:
            try:
                free = float(balance.get("free", 0))
                locked = float(balance.get("locked", 0))
                total = free + locked
                
                # Only include balances with some value
                if total > 0:
                    balances.append({
                        "asset": balance["asset"],
                        "free": free,
                        "locked": locked,
                        "total": total
                    })
            except (ValueError, KeyError) as e:
                logger.warning(f"Error processing balance for {balance.get('asset', 'unknown')}: {e}")
                continue
        
        return {
            "account_type": "SPOT",
            "can_trade": account.get("canTrade", False),
            "can_withdraw": account.get("canWithdraw", False),
            "can_deposit": account.get("canDeposit", False),
            "balances": balances
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
    symbol: Optional[str] = None,
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

@app.get("/orders/{symbol}")
async def get_orders(symbol: str, limit: int = 100):
    """Get open orders for a symbol"""
    try:
        if not binance_client:
            raise HTTPException(status_code=503, detail="Binance client not configured")
        
        # Get open orders from Binance
        orders = binance_client.get_open_orders(symbol=symbol)
        
        # Process orders safely
        processed_orders = []
        for order in orders[:limit]:  # Limit the number of orders
            try:
                processed_orders.append({
                    "order_id": order.get("orderId"),
                    "symbol": order.get("symbol"),
                    "side": order.get("side"),
                    "type": order.get("type"),
                    "quantity": float(order.get("origQty", 0)),
                    "price": float(order.get("price", 0)),
                    "status": order.get("status"),
                    "time": order.get("time"),
                    "update_time": order.get("updateTime")
                })
            except (ValueError, KeyError) as e:
                logger.warning(f"Error processing order {order.get('orderId', 'unknown')}: {e}")
                continue
        
        return {
            "symbol": symbol,
            "orders": processed_orders,
            "count": len(processed_orders)
        }
        
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        raise HTTPException(status_code=400, detail=f"Binance API error: {e.message}")
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get orders: {str(e)}")

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

# =============================================================================
# AI/LLM ENDPOINTS
# =============================================================================

@app.get("/ai/status")
async def get_ai_status():
    """Check AI/LLM service status"""
    try:
        if not llm_service:
            return {
                "status": "not_configured",
                "message": "LLM service not initialized"
            }
        
        # Test simple prompt to check if Ollama is responding
        test_response = llm_service._call_ollama("Hello, are you working?")
        
        if test_response:
            return {
                "status": "healthy",
                "model": settings.ollama_model,
                "base_url": settings.ollama_base_url,
                "message": "LLM service is responding"
            }
        else:
            return {
                "status": "error",
                "model": settings.ollama_model,
                "base_url": settings.ollama_base_url,
                "message": "LLM service not responding"
            }
    except Exception as e:
        logger.error(f"AI status check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/ai/analyze-market")
async def analyze_market_with_ai(market_data: dict):
    """Analyze market data using AI"""
    try:
        if not llm_service:
            raise HTTPException(status_code=503, detail="LLM service not configured")
        
        analysis = llm_service.analyze_market_data(market_data)
        return {
            "success": True,
            "analysis": analysis,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Market analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Market analysis failed: {str(e)}")

@app.post("/ai/evaluate-trade")
async def evaluate_trade_with_ai(trade_data: dict):
    """Evaluate trade opportunity using AI"""
    try:
        if not llm_service:
            raise HTTPException(status_code=503, detail="LLM service not configured")
        
        evaluation = llm_service.evaluate_trade_opportunity(trade_data)
        return {
            "success": True,
            "evaluation": evaluation,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Trade evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Trade evaluation failed: {str(e)}")

@app.post("/ai/portfolio-analysis")
async def analyze_portfolio_with_ai(portfolio_data: dict):
    """Analyze portfolio performance using AI"""
    try:
        if not llm_service:
            raise HTTPException(status_code=503, detail="LLM service not configured")
        
        analysis = llm_service.analyze_portfolio_performance(portfolio_data)
        return {
            "success": True,
            "analysis": analysis,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Portfolio analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Portfolio analysis failed: {str(e)}")

@app.post("/ai/insights")
async def get_trading_insights(context: dict):
    """Get general trading insights from AI"""
    try:
        if not llm_service:
            raise HTTPException(status_code=503, detail="LLM service not configured")
        
        market_context = context.get("context", "Current market conditions")
        insights = llm_service.generate_trading_insights(market_context)
        return {
            "success": True,
            "insights": insights,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Insights generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

# =============================================================================
# AUTOMATED TRADING ENDPOINTS
# =============================================================================

@app.get("/automated-trading/status")
async def get_automated_trading_status():
    """Get automated trading service status"""
    try:
        if not automated_trading_service:
            return {
                "status": "not_configured",
                "message": "Automated trading service not initialized"
            }
        
        status = automated_trading_service.get_status()
        return {
            "status": "configured",
            "automated_trading": status,
            "settings": {
                "enabled": settings.enable_automated_trading,
                "interval": settings.automated_trading_interval,
                "max_daily_trades": settings.max_daily_trades_per_symbol,
                "cooldown_minutes": settings.trade_cooldown_minutes
            }
        }
    except Exception as e:
        logger.error(f"Automated trading status check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/automated-trading/start")
async def start_automated_trading():
    """Start automated trading"""
    try:
        if not automated_trading_service:
            raise HTTPException(status_code=503, detail="Automated trading service not configured")
        
        if not settings.enable_automated_trading:
            raise HTTPException(status_code=400, detail="Automated trading is disabled in settings")
        
        # Check if already running
        if automated_trading_service.is_running:
            return {
                "success": True,
                "message": "Automated trading is already running"
            }
        
        # Start the monitoring loop in background
        import asyncio
        asyncio.create_task(automated_trading_service.start_monitoring())
        
        return {
            "success": True,
            "message": "Automated trading started successfully"
        }
    except Exception as e:
        logger.error(f"Failed to start automated trading: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start automated trading: {str(e)}")

@app.post("/automated-trading/stop")
async def stop_automated_trading():
    """Stop automated trading"""
    try:
        if not automated_trading_service:
            raise HTTPException(status_code=503, detail="Automated trading service not configured")
        
        await automated_trading_service.stop_monitoring()
        
        return {
            "success": True,
            "message": "Automated trading stopped successfully"
        }
    except Exception as e:
        logger.error(f"Failed to stop automated trading: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop automated trading: {str(e)}")

@app.get("/automated-trading/decisions")
async def get_ai_decisions(
    symbol: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get AI trading decisions history"""
    try:
        query = db.query(AIDecision)
        
        if symbol:
            query = query.filter(AIDecision.symbol == symbol)
        
        decisions = query.order_by(AIDecision.timestamp.desc()).limit(limit).all()
        
        return {
            "decisions": [decision.to_dict() for decision in decisions]
        }
    except Exception as e:
        logger.error(f"Error getting AI decisions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get AI decisions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )