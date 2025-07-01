"""
LLM Service for Trading System
Handles all AI analysis and decision making
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class LLMService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b-instruct-q4_0"):
        self.base_url = base_url
        self.model = model
        self.logger = logging.getLogger(__name__)
        
    def _call_ollama(self, prompt: str, temperature: float = 0.1) -> Optional[str]:
        """Make API call to Ollama"""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Ollama request failed: {e}")
            return None
    
    def analyze_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market data and provide trading insights"""
        prompt = f"""
You are an expert crypto trading analyst. Analyze the following market data and provide a structured response.

Market Data:
- Symbol: {market_data.get('symbol', 'Unknown')}
- Current Price: ${market_data.get('price', 0)}
- 24h Change: {market_data.get('change_24h', 0)}%
- Volume: {market_data.get('volume', 0)}
- RSI: {market_data.get('rsi', 'N/A')}
- MACD: {market_data.get('macd', 'N/A')}

Provide your analysis in this EXACT JSON format:
{{
    "signal": "BUY|SELL|HOLD",
    "confidence": "HIGH|MEDIUM|LOW",
    "risk_level": "HIGH|MEDIUM|LOW",
    "analysis": "Brief analysis explaining your reasoning",
    "entry_price": "Suggested entry price or null",
    "stop_loss": "Suggested stop loss price or null",
    "take_profit": "Suggested take profit price or null",
    "position_size": "Suggested position size percentage (1-5)"
}}

Respond ONLY with valid JSON, no other text.
"""
        
        response = self._call_ollama(prompt, temperature=0.1)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                self.logger.error("Failed to parse LLM response as JSON")
                return self._default_analysis()
        return self._default_analysis()
    
    def evaluate_trade_opportunity(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a specific trade opportunity"""
        prompt = f"""
You are a crypto trading risk manager. Evaluate this trade opportunity:

Trade Details:
- Symbol: {trade_data.get('symbol')}
- Action: {trade_data.get('action')}
- Entry Price: ${trade_data.get('entry_price')}
- Current Price: ${trade_data.get('current_price')}
- Proposed Position Size: {trade_data.get('position_size', 2)}%
- Available Capital: ${trade_data.get('available_capital')}
- Recent Performance: {trade_data.get('recent_performance', 'Unknown')}

Risk Management Rules:
- Maximum position size: 5% per trade
- Maximum daily risk: 10%
- Minimum risk-reward ratio: 1:2

Respond in this EXACT JSON format:
{{
    "approved": true/false,
    "risk_score": 1-10,
    "recommended_position_size": "percentage",
    "concerns": ["list of concerns if any"],
    "suggestions": ["list of improvements"],
    "reasoning": "explanation of decision"
}}

Respond ONLY with valid JSON.
"""
        
        response = self._call_ollama(prompt, temperature=0.1)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._default_risk_assessment()
        return self._default_risk_assessment()
    
    def analyze_portfolio_performance(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall portfolio performance and suggest improvements"""
        prompt = f"""
You are a portfolio performance analyst. Review this trading portfolio:

Portfolio Summary:
- Total Capital: ${portfolio_data.get('total_capital')}
- Current Value: ${portfolio_data.get('current_value')}
- Total P&L: ${portfolio_data.get('total_pnl')}
- Win Rate: {portfolio_data.get('win_rate', 0)}%
- Average Trade Return: {portfolio_data.get('avg_return', 0)}%
- Number of Trades: {portfolio_data.get('total_trades', 0)}
- Recent Trades: {portfolio_data.get('recent_trades', [])}

Provide analysis in this EXACT JSON format:
{{
    "performance_grade": "A|B|C|D|F",
    "strengths": ["list of portfolio strengths"],
    "weaknesses": ["list of areas for improvement"],
    "recommendations": ["specific actionable advice"],
    "risk_assessment": "HIGH|MEDIUM|LOW",
    "suggested_adjustments": {{
        "position_sizing": "advice on position sizing",
        "strategy_mix": "advice on strategy allocation",
        "risk_management": "risk management improvements"
    }}
}}

Respond ONLY with valid JSON.
"""
        
        response = self._call_ollama(prompt, temperature=0.2)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._default_portfolio_analysis()
        return self._default_portfolio_analysis()
    
    def generate_trading_insights(self, market_context: str) -> str:
        """Generate general trading insights based on market context"""
        prompt = f"""
You are a crypto trading strategist. Based on the current market context, provide actionable insights:

Market Context: {market_context}

Provide 3-5 key insights focusing on:
1. Current market sentiment
2. Key levels to watch
3. Potential opportunities
4. Risk factors to consider
5. Recommended actions

Keep response concise and actionable.
"""
        
        return self._call_ollama(prompt, temperature=0.3) or "Unable to generate insights at this time."
    
    def _default_analysis(self) -> Dict[str, Any]:
        """Default analysis when LLM fails"""
        return {
            "signal": "HOLD",
            "confidence": "LOW",
            "risk_level": "HIGH",
            "analysis": "Unable to analyze - system error",
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "position_size": "1"
        }
    
    def _default_risk_assessment(self) -> Dict[str, Any]:
        """Default risk assessment when LLM fails"""
        return {
            "approved": False,
            "risk_score": 10,
            "recommended_position_size": "1%",
            "concerns": ["System error - cannot assess risk"],
            "suggestions": ["Wait for system recovery"],
            "reasoning": "Unable to evaluate due to system error"
        }
    
    def _default_portfolio_analysis(self) -> Dict[str, Any]:
        """Default portfolio analysis when LLM fails"""
        return {
            "performance_grade": "C",
            "strengths": ["System maintaining positions"],
            "weaknesses": ["Analysis system temporarily unavailable"],
            "recommendations": ["Wait for system recovery"],
            "risk_assessment": "MEDIUM",
            "suggested_adjustments": {
                "position_sizing": "Maintain current conservative approach",
                "strategy_mix": "No changes recommended",
                "risk_management": "Continue current risk controls"
            }
        }

# Usage example
if __name__ == "__main__":
    llm = LLMService()
    
    # Test market analysis
    test_data = {
        "symbol": "BTCUSDT",
        "price": 45000,
        "change_24h": 2.5,
        "volume": 1500000,
        "rsi": 65,
        "macd": "bullish"
    }
    
    result = llm.analyze_market_data(test_data)
    print("Market Analysis:", json.dumps(result, indent=2))