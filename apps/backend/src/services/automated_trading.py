"""
Automated Trading Service
Handles AI-powered automated trading decisions
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Trade, AIDecision
from ..core.config import settings
from services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AutomatedTradingService:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.is_running = False
        self.last_analysis = {}
        self.trade_cooldown = {}  # Prevent rapid trading
        self.daily_trades = {}  # Track daily trade count per symbol
        
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
                await self.analyze_and_trade_symbol(symbol)
                
        except Exception as e:
            logger.error(f"Error in monitor_and_trade: {e}")
    
    async def analyze_and_trade_symbol(self, symbol: str):
        """Analyze a specific symbol and execute trades if conditions are met"""
        try:
            # Check cooldown period (minimum 15 minutes between trades per symbol)
            if self.is_in_cooldown(symbol):
                return
            
            # Check daily trade limit (max 5 trades per symbol per day)
            if self.has_reached_daily_limit(symbol):
                logger.info(f"Daily trade limit reached for {symbol}")
                return
            
            # Get current market data
            market_data = await self.get_market_data(symbol)
            if not market_data:
                return
            
            # Get AI analysis
            analysis = self.llm_service.analyze_market_data(market_data)
            
            # Store AI decision
            await self.store_ai_decision(symbol, analysis, market_data)
            
            # Check if we should execute a trade
            if self.should_execute_trade(analysis):
                await self.execute_ai_trade(symbol, analysis, market_data)
            
            # Update last analysis
            self.last_analysis[symbol] = {
                'analysis': analysis,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
    
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
            # This would typically fetch from Binance API
            # For now, return mock data
            return {
                'symbol': symbol,
                'price': 45000,  # Mock price
                'change_24h': 2.5,
                'volume': 2500000000,
                'rsi': 65,
                'macd': 'bullish'
            }
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return None
    
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
    
    async def execute_ai_trade(self, symbol: str, analysis: Dict[str, Any], market_data: Dict[str, Any]):
        """Execute a trade based on AI analysis"""
        try:
            signal = analysis.get('signal', 'HOLD')
            position_size = float(analysis.get('position_size', '1'))
            
            # Calculate trade quantity based on position size
            # This is a simplified calculation - in production, you'd use account balance
            quantity = self.calculate_trade_quantity(symbol, position_size, market_data['price'])
            
            # Prepare trade data
            trade_data = {
                'symbol': symbol,
                'side': signal,
                'type': 'MARKET',
                'quantity': quantity,
                'strategy': 'AI_AUTOMATED',
                'ai_decision': True,
                'ai_reasoning': analysis.get('analysis', 'AI-driven trade')
            }
            
            # Execute trade (this would call your existing trade endpoint)
            success = await self.place_trade(trade_data)
            
            if success:
                # Update daily trade count
                self.daily_trades[symbol]['count'] += 1
                
                # Set cooldown period (15 minutes)
                self.trade_cooldown[symbol] = datetime.utcnow() + timedelta(minutes=15)
                
                logger.info(f"AI trade executed successfully: {symbol} {signal} {quantity}")
                
                # Send alert
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
        """Place a trade using the existing trade endpoint"""
        try:
            # This would call your existing trade placement logic
            # For now, just log the trade
            logger.info(f"Placing trade: {trade_data}")
            
            # In production, you'd call the actual trade placement function
            # from your main app.py or a dedicated trading service
            
            return True  # Mock success
            
        except Exception as e:
            logger.error(f"Error placing trade: {e}")
            return False
    
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