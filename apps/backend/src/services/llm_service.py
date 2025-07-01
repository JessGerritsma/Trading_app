import requests
import json
from typing import Dict, Any, Optional
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import settings

class LLMService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    def _call_ollama(self, prompt: str) -> str:
        """Make a call to Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama API error: {e}")
            return "Unable to get AI response"
    
    def analyze_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market data and provide trading signals"""
        prompt = f"""
        Analyze this cryptocurrency market data and provide a trading recommendation:
        
        Symbol: {market_data.get('symbol', 'Unknown')}
        Price: ${market_data.get('price', 0):,.2f}
        24h Change: {market_data.get('change_24h', 0)}%
        Volume: ${market_data.get('volume', 0):,.0f}
        RSI: {market_data.get('rsi', 50)}
        MACD: {market_data.get('macd', 'neutral')}
        
        Provide a JSON response with:
        - signal: "BUY", "SELL", or "HOLD"
        - confidence: 0.0 to 1.0
        - reasoning: brief explanation
        - risk_level: "LOW", "MEDIUM", or "HIGH"
        """
        
        response = self._call_ollama(prompt)
        
        # Try to parse JSON response, fallback to structured text
        try:
            return json.loads(response)
        except:
            return {
                "signal": "HOLD",
                "confidence": 0.5,
                "reasoning": response[:200],
                "risk_level": "MEDIUM"
            }
    
    def evaluate_trade_opportunity(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a specific trade opportunity"""
        prompt = f"""
        Evaluate this trade opportunity:
        
        Symbol: {trade_data.get('symbol', 'Unknown')}
        Action: {trade_data.get('action', 'Unknown')}
        Entry Price: ${trade_data.get('entry_price', 0):,.2f}
        Current Price: ${trade_data.get('current_price', 0):,.2f}
        Position Size: {trade_data.get('position_size', 0)}
        Available Capital: ${trade_data.get('available_capital', 0):,.2f}
        Recent Performance: {trade_data.get('recent_performance', 'Unknown')}
        
        Provide a JSON response with:
        - approved: true/false
        - confidence: 0.0 to 1.0
        - reasoning: explanation
        - suggested_position_size: recommended size
        """
        
        response = self._call_ollama(prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "approved": False,
                "confidence": 0.3,
                "reasoning": response[:200],
                "suggested_position_size": 1
            }
    
    def analyze_portfolio_performance(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall portfolio performance"""
        prompt = f"""
        Analyze this portfolio performance:
        
        Total Capital: ${portfolio_data.get('total_capital', 0):,.2f}
        Current Value: ${portfolio_data.get('current_value', 0):,.2f}
        Total P&L: ${portfolio_data.get('total_pnl', 0):,.2f}
        Win Rate: {portfolio_data.get('win_rate', 0)}%
        Avg Return: {portfolio_data.get('avg_return', 0)}%
        Total Trades: {portfolio_data.get('total_trades', 0)}
        Recent Trades: {portfolio_data.get('recent_trades', [])}
        
        Provide a JSON response with:
        - performance_grade: "A", "B", "C", "D", or "F"
        - risk_assessment: "LOW", "MEDIUM", or "HIGH"
        - recommendations: list of suggestions
        - overall_sentiment: "BULLISH", "BEARISH", or "NEUTRAL"
        """
        
        response = self._call_ollama(prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "performance_grade": "C",
                "risk_assessment": "MEDIUM",
                "recommendations": [response[:100]],
                "overall_sentiment": "NEUTRAL"
            }
    
    def generate_trading_insights(self, market_context: str) -> str:
        """Generate trading insights from market context"""
        prompt = f"""
        Based on this market context, provide trading insights:
        
        {market_context}
        
        Provide actionable trading insights and market analysis.
        """
        
        return self._call_ollama(prompt) 