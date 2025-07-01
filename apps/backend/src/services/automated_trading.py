"""
Automated Trading Service
Handles AI-powered automated trading decisions
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Trade, AIDecision
from ..core.config import settings
from services.llm_service import LLMService
from services.realtime_data_service import RealTimeDataService
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, account_value: float = 10000.0):
        self.account_value = account_value
        self.daily_loss_limit = settings.max_daily_loss * account_value
        self.weekly_loss_limit = self.daily_loss_limit * 5
        self.max_drawdown = 0.2 * account_value  # 20% default
        self.high_water_mark = account_value
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.last_reset = date.today()
        self.trade_risk = 0.01  # 1% risk per trade
        self.risk_log = []

    def reset_if_new_day(self):
        today = date.today()
        if today != self.last_reset:
            self.daily_loss = 0.0
            if today.weekday() == 0:  # Monday
                self.weekly_loss = 0.0
            self.last_reset = today

    def update_account_value(self, new_value: float):
        self.account_value = new_value
        if new_value > self.high_water_mark:
            self.high_water_mark = new_value

    def log_risk(self, metric: str, value: float, extra: dict = {}):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'metric': metric,
            'value': value,
            'extra': extra
        }
        self.risk_log.append(entry)
        logger.info(f"Risk log: {entry}")

    def check_loss_limits(self):
        self.reset_if_new_day()
        if self.daily_loss < -self.daily_loss_limit:
            logger.warning("Daily loss limit breached!")
            return False
        if self.weekly_loss < -self.weekly_loss_limit:
            logger.warning("Weekly loss limit breached!")
            return False
        return True

    def check_drawdown(self):
        drawdown = self.high_water_mark - self.account_value
        if drawdown > self.max_drawdown:
            logger.warning("Max drawdown breached!")
            return False
        return True

    def calculate_position_size(self, stop_loss_pct: float) -> float:
        # Risk per trade = account_value * trade_risk
        # Position size = risk_per_trade / stop_loss_pct
        risk_per_trade = self.account_value * self.trade_risk
        if stop_loss_pct == 0:
            return 0
        position_size = risk_per_trade / stop_loss_pct
        return min(position_size, self.account_value * 0.2)  # Cap at 20% of account

    def update_realized_pnl(self, pnl: float):
        self.reset_if_new_day()
        self.daily_loss += pnl
        self.weekly_loss += pnl
        self.update_account_value(self.account_value + pnl)
        self.log_risk('realized_pnl', pnl)

    def update_unrealized_pnl(self, unrealized: float):
        self.log_risk('unrealized_pnl', unrealized)

    def can_trade(self) -> bool:
        return self.check_loss_limits() and self.check_drawdown()

class AutomatedTradingService:
    def __init__(self, llm_service: LLMService, symbols: List[str]):
        self.llm_service = llm_service
        self.is_running = False
        self.last_analysis = {}
        self.trade_cooldown = {}
        self.daily_trades = {}
        self.conversation_history: Dict[str, List[Tuple[str, str]]] = {symbol: [] for symbol in symbols}
        self.symbols = symbols
        self.realtime_service = RealTimeDataService(symbols)
        self.risk_manager = RiskManager()
        # Initialize Binance client for trade execution
        try:
            self.binance_client = Client(
                settings.binance_api_key,
                settings.binance_secret_key,
                testnet=settings.binance_testnet
            )
            logger.info("Binance client initialized for automated trading")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client for automated trading: {e}")
            self.binance_client = None

    async def start_realtime_trading(self):
        self.is_running = True
        self.realtime_service.add_event_callback(self._on_market_event)
        await self.realtime_service.start()
        logger.info("Automated trading with real-time data started.")

    def _on_market_event(self, event: Dict[str, Any]):
        symbol = event['symbol']
        asyncio.create_task(self.analyze_and_trade_symbol(symbol, event))

    async def analyze_and_trade_symbol(self, symbol: str, event: Dict[str, Any]):
        try:
            if not self.is_running:
                return
            if self.is_in_cooldown(symbol):
                return
            if self.has_reached_daily_limit(symbol):
                logger.info(f"Daily trade limit reached for {symbol}")
                return
            # Use latest market data from event
            market_data = {
                'symbol': symbol,
                'price': event['ohlcv']['close_price'],
                'change_24h': 0,  # Could be calculated from cache if needed
                'volume': event['ohlcv']['volume'],
                'rsi': event['indicators'].get('rsi', 50),
                'macd': event['indicators'].get('macd', 'neutral'),
                'high_24h': None,
                'low_24h': None
            }
            # Build conversation history for this symbol
            history = self.conversation_history.get(symbol, [])
            # Await async LLMService call
            analysis = await self.llm_service.analyze_market_data(market_data, history)
            # Update conversation history
            prompt = f"Analyze this market data: {market_data}"
            ai_response = str(analysis)
            history.append((prompt, ai_response))
            self.conversation_history[symbol] = history[-10:]
            # Store AI decision
            await self.store_ai_decision(symbol, analysis, market_data)
            # Preventive risk checks
            stop_loss_pct = abs((market_data['price'] - analysis.get('stop_loss', market_data['price'])) / market_data['price'])
            position_size = self.risk_manager.calculate_position_size(stop_loss_pct)
            if not self.risk_manager.can_trade():
                logger.warning("RiskManager: Trading halted due to risk limits.")
                return
            # Check if we should execute a trade
            if self.should_execute_trade(analysis):
                await self.execute_ai_trade(symbol, analysis, market_data, position_size)
            # Update last analysis
            self.last_analysis[symbol] = {
                'analysis': analysis,
                'timestamp': datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")

    async def start_monitoring(self):
        """Start the automated trading monitoring loop"""
        if self.is_running:
            logger.warning("Automated trading is already running")
            return
            
        self.is_running = True
        logger.info("Starting automated trading monitoring...")
        
        while self.is_running:
            try:
                await self.monitor_and_trade()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in automated trading loop: {e}")
                await asyncio.sleep(60)
    
    async def stop_monitoring(self):
        """Stop the automated trading monitoring"""
        self.is_running = False
        logger.info("Stopping automated trading monitoring...")
    
    async def monitor_and_trade(self):
        """Monitor market conditions and execute trades based on AI signals"""
        try:
            # Get current market data for configured symbols
            for symbol in settings.trading_pairs_list:
                await self.analyze_and_trade_symbol(symbol, {})
                
        except Exception as e:
            logger.error(f"Error in monitor_and_trade: {e}")
    
    def is_in_cooldown(self, symbol: str) -> bool:
        """Check if symbol is in cooldown period"""
        if symbol not in self.trade_cooldown:
            return False
        
        cooldown_until = self.trade_cooldown[symbol]
        return datetime.utcnow() < cooldown_until
    
    def has_reached_daily_limit(self, symbol: str) -> bool:
        """Check if daily trade limit has been reached"""
        today = datetime.utcnow().date()
        if symbol not in self.daily_trades:
            self.daily_trades[symbol] = {'date': today, 'count': 0}
        
        # Reset counter if it's a new day
        if self.daily_trades[symbol]['date'] != today:
            self.daily_trades[symbol] = {'date': today, 'count': 0}
        
        return self.daily_trades[symbol]['count'] >= 5  # Max 5 trades per day
    
    async def get_market_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current market data for a symbol"""
        try:
            if not self.binance_client:
                logger.error("Binance client not available for market data")
                return None
            
            # Get current ticker
            ticker = self.binance_client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            
            # Get 24hr stats
            stats = self.binance_client.get_ticker(symbol=symbol)
            
            # Get recent klines for basic indicators
            klines = self.binance_client.get_klines(symbol=symbol, interval='1h', limit=24)
            
            # Calculate basic indicators
            closes = [float(kline[4]) for kline in klines]
            volumes = [float(kline[5]) for kline in klines]
            
            # Simple RSI calculation
            rsi = self._calculate_rsi(closes)
            
            # Simple MACD calculation
            macd_signal = self._calculate_macd_signal(closes)
            
            return {
                'symbol': symbol,
                'price': current_price,
                'change_24h': float(stats['priceChangePercent']),
                'volume': float(stats['volume']),
                'rsi': rsi,
                'macd': macd_signal,
                'high_24h': float(stats['highPrice']),
                'low_24h': float(stats['lowPrice'])
            }
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return None
    
    def _calculate_rsi(self, closes: list, period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(closes) < period + 1:
            return 50.0  # Default neutral value
        
        gains = []
        losses = []
        
        for i in range(1, len(closes)):
            change = closes[i] - closes[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def _calculate_macd_signal(self, closes: list) -> str:
        """Calculate simple MACD signal"""
        if len(closes) < 26:
            return 'neutral'
        
        # Simple EMA calculation
        ema12 = sum(closes[-12:]) / 12
        ema26 = sum(closes[-26:]) / 26
        
        macd = ema12 - ema26
        
        if macd > 0:
            return 'bullish'
        elif macd < 0:
            return 'bearish'
        else:
            return 'neutral'
    
    def should_execute_trade(self, analysis: Dict[str, Any]) -> bool:
        """Determine if a trade should be executed based on AI analysis"""
        try:
            signal = analysis.get('signal', 'HOLD')
            confidence = analysis.get('confidence', 'LOW')
            risk_level = analysis.get('risk_level', 'HIGH')
            
            # Only trade on BUY/SELL signals with HIGH confidence and LOW/MEDIUM risk
            if signal == 'HOLD':
                return False
            
            if confidence != 'HIGH':
                return False
            
            if risk_level == 'HIGH':
                return False
            
            # Additional safety checks
            if not settings.enable_live_trading:
                logger.info("Live trading is disabled - skipping trade execution")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in should_execute_trade: {e}")
            return False
    
    async def execute_ai_trade(self, symbol: str, analysis: Dict[str, Any], market_data: Dict[str, Any], position_size: float):
        """Execute a trade based on AI analysis"""
        try:
            signal = analysis.get('signal', 'HOLD')
            # Use calculated position size
            quantity = position_size / market_data['price']
            stop_loss = analysis.get('stop_loss', None)
            take_profit = analysis.get('take_profit', None)
            # Prepare trade data
            trade_data = {
                'symbol': symbol,
                'side': signal,
                'type': 'MARKET',
                'quantity': quantity,
                'strategy': 'AI_AUTOMATED',
                'ai_decision': True,
                'ai_reasoning': analysis.get('analysis', 'AI-driven trade'),
                'stop_loss': stop_loss,
                'take_profit': take_profit
            }
            # Preventive risk check before placing trade
            if not self.risk_manager.can_trade():
                logger.warning("RiskManager: Trading halted before order placement.")
                return
            # Execute trade (this would call your existing trade endpoint)
            success = await self.place_trade(trade_data)
            
            if success:
                self.daily_trades[symbol]['count'] += 1
                self.trade_cooldown[symbol] = datetime.utcnow() + timedelta(minutes=15)
                logger.info(f"AI trade executed successfully: {symbol} {signal} {quantity}")
                await self.send_trade_alert(symbol, signal, quantity, analysis)
            else:
                logger.error(f"Failed to execute AI trade: {symbol} {signal}")
                
        except Exception as e:
            logger.error(f"Error executing AI trade for {symbol}: {e}")
    
    def calculate_trade_quantity(self, symbol: str, position_size: float, price: float) -> float:
        """Calculate trade quantity based on position size"""
        try:
            # Simplified calculation - in production, use actual account balance
            account_value = 10000  # Mock account value
            trade_value = account_value * (position_size / 100)
            quantity = trade_value / price
            
            # Apply minimum/maximum trade limits
            min_quantity = settings.min_trade_amount / price
            max_quantity = settings.max_trade_amount / price
            
            quantity = max(min_quantity, min(quantity, max_quantity))
            
            return round(quantity, 6)  # Round to 6 decimal places
            
        except Exception as e:
            logger.error(f"Error calculating trade quantity: {e}")
            return 0.001  # Default minimum quantity
    
    async def place_trade(self, trade_data: Dict[str, Any]) -> bool:
        """Place a trade using Binance API"""
        try:
            if not self.binance_client:
                logger.error("Binance client not available for trade placement")
                return False
            
            # Validate trade data
            required_fields = ["symbol", "side", "type", "quantity"]
            for field in required_fields:
                if field not in trade_data:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Prepare order parameters
            order_params = {
                "symbol": trade_data["symbol"],
                "side": trade_data["side"],
                "type": trade_data["type"],
                "quantity": trade_data["quantity"]
            }
            
            # Add price for limit orders
            if trade_data.get("price"):
                order_params["price"] = trade_data["price"]
            
            # Add stop-loss/take-profit as OCO if both are present
            if trade_data.get("stop_loss") and trade_data.get("take_profit"):
                # Place OCO order (One Cancels Other)
                # This is a placeholder; actual OCO order logic may differ by API
                logger.info(f"Placing OCO order for {trade_data['symbol']} with stop_loss {trade_data['stop_loss']} and take_profit {trade_data['take_profit']}")
                # Implement OCO logic here if supported
            elif trade_data.get("stop_loss"):
                # Place stop-loss order
                logger.info(f"Placing stop-loss order for {trade_data['symbol']} at {trade_data['stop_loss']}")
                # Implement stop-loss logic here if supported
            
            # Place order on Binance
            order = self.binance_client.create_order(**order_params)
            
            # Store trade in database
            await self._store_trade_in_db(trade_data, order)
            
            logger.info(f"Trade placed successfully: {order.get('orderId')}")
            return True
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing trade: {e}")
            return False
        except Exception as e:
            logger.error(f"Error placing trade: {e}")
            return False
    
    async def _store_trade_in_db(self, trade_data: Dict[str, Any], order: Dict[str, Any]):
        """Store trade in database"""
        try:
            db = next(get_db())
            
            db_trade = Trade(
                symbol=trade_data["symbol"],
                side=trade_data["side"],
                type=trade_data["type"],
                quantity=float(trade_data["quantity"]),
                price=float(trade_data.get("price", 0)),
                order_id=order.get("orderId"),
                status=order.get("status", "PENDING"),
                strategy=trade_data.get("strategy", "AI_AUTOMATED"),
                ai_decision=trade_data.get("ai_decision", True),
                ai_reasoning=trade_data.get("ai_reasoning", "")
            )
            
            db.add(db_trade)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing trade in database: {e}")
    
    async def store_ai_decision(self, symbol: str, analysis: Dict[str, Any], market_data: Dict[str, Any]):
        """Store AI decision in database"""
        try:
            db = next(get_db())
            
            ai_decision = AIDecision(
                symbol=symbol,
                action=analysis.get('signal', 'HOLD'),
                confidence=float(analysis.get('confidence', 'LOW').lower() == 'high'),
                reasoning=analysis.get('analysis', ''),
                market_data=market_data,
                strategy_signals=analysis,
                llm_response=str(analysis),
                executed=False,
                timestamp=datetime.utcnow()
            )
            
            db.add(ai_decision)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing AI decision: {e}")
    
    async def send_trade_alert(self, symbol: str, signal: str, quantity: float, analysis: Dict[str, Any]):
        """Send trade alert notification"""
        try:
            message = f"🤖 AI Trade Executed\n\n"
            message += f"Symbol: {symbol}\n"
            message += f"Signal: {signal}\n"
            message += f"Quantity: {quantity}\n"
            message += f"Confidence: {analysis.get('confidence', 'N/A')}\n"
            message += f"Risk Level: {analysis.get('risk_level', 'N/A')}\n"
            message += f"Reasoning: {analysis.get('analysis', 'N/A')[:100]}..."
            
            logger.info(f"Trade Alert: {message}")
            
            # In production, you'd send this via email, Discord, Telegram, etc.
            
        except Exception as e:
            logger.error(f"Error sending trade alert: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get automated trading service status"""
        return {
            'is_running': self.is_running,
            'last_analysis': {
                symbol: {
                    'timestamp': data['timestamp'].isoformat(),
                    'signal': data['analysis'].get('signal', 'N/A'),
                    'confidence': data['analysis'].get('confidence', 'N/A')
                }
                for symbol, data in self.last_analysis.items()
            },
            'daily_trades': self.daily_trades,
            'cooldowns': {
                symbol: cooldown.isoformat() if cooldown > datetime.utcnow() else 'None'
                for symbol, cooldown in self.trade_cooldown.items()
            }
        } 