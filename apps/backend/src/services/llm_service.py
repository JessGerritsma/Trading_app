import httpx
import json
import logging
from typing import List, Tuple, Dict, Any, Optional
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import settings

class LLMService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b-instruct-q4_0"):
        self.base_url = base_url
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def _build_history_prompt(self, history: List[Tuple[str, str]], current_prompt: str) -> str:
        history_text = ""
        for user, ai in history:
            history_text += f"User: {user}\nAI: {ai}\n"
        return f"{history_text}User: {current_prompt}\nAI:"

    async def _call_ollama(self, prompt: str, temperature: float = 0.1) -> Optional[str]:
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
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=60)
                response.raise_for_status()
                return response.json().get('response', '')
            except Exception as e:
                self.logger.error(f"Ollama request failed: {e}")
                return None
    
    async def analyze_market_data(self, market_data: Dict[str, Any], history: List[Tuple[str, str]] = []) -> Dict[str, Any]:
        prompt = f"""
You are an expert crypto trading analyst. Analyze the following market data and provide a structured response.\n\nMarket Data:\n- Symbol: {market_data.get('symbol', 'Unknown')}\n- Current Price: ${market_data.get('price', 0)}\n- 24h Change: {market_data.get('change_24h', 0)}%\n- Volume: {market_data.get('volume', 0)}\n- RSI: {market_data.get('rsi', 'N/A')}\n- MACD: {market_data.get('macd', 'N/A')}\n\nProvide your analysis in this EXACT JSON format:\n{{\n    \"signal\": \"BUY|SELL|HOLD\",\n    \"confidence\": \"HIGH|MEDIUM|LOW\",\n    \"risk_level\": \"HIGH|MEDIUM|LOW\",\n    \"analysis\": \"Brief analysis explaining your reasoning\",\n    \"entry_price\": \"Suggested entry price or null\",\n    \"stop_loss\": \"Suggested stop loss price or null\",\n    \"take_profit\": \"Suggested take profit price or null\",\n    \"position_size\": \"Suggested position size percentage (1-5)\"\n}}\n\nRespond ONLY with valid JSON, no other text.\n"""
        full_prompt = self._build_history_prompt(history, prompt)
        response = await self._call_ollama(full_prompt, temperature=0.1)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                self.logger.error("Failed to parse LLM response as JSON")
                return self._default_analysis()
        return self._default_analysis()
    
    async def evaluate_trade_opportunity(self, trade_data: Dict[str, Any], history: List[Tuple[str, str]] = []) -> Dict[str, Any]:
        prompt = f"""
You are a crypto trading risk manager. Evaluate this trade opportunity:\n\nTrade Details:\n- Symbol: {trade_data.get('symbol')}\n- Action: {trade_data.get('action')}\n- Entry Price: ${trade_data.get('entry_price')}\n- Current Price: ${trade_data.get('current_price')}\n- Proposed Position Size: {trade_data.get('position_size', 2)}%\n- Available Capital: ${trade_data.get('available_capital')}\n- Recent Performance: {trade_data.get('recent_performance', 'Unknown')}\n\nRisk Management Rules:\n- Maximum position size: 5% per trade\n- Maximum daily risk: 10%\n- Minimum risk-reward ratio: 1:2\n\nRespond in this EXACT JSON format:\n{{\n    \"approved\": true/false,\n    \"risk_score\": 1-10,\n    \"recommended_position_size\": \"percentage\",\n    \"concerns\": [\"list of concerns if any\"],\n    \"suggestions\": [\"list of improvements\"],\n    \"reasoning\": \"explanation of decision\"\n}}\n\nRespond ONLY with valid JSON.\n"""
        full_prompt = self._build_history_prompt(history, prompt)
        response = await self._call_ollama(full_prompt, temperature=0.1)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._default_risk_assessment()
        return self._default_risk_assessment()
    
    async def analyze_portfolio_performance(self, portfolio_data: Dict[str, Any], history: List[Tuple[str, str]] = []) -> Dict[str, Any]:
        prompt = f"""
You are a portfolio performance analyst. Review this trading portfolio:\n\nPortfolio Summary:\n- Total Capital: ${portfolio_data.get('total_capital')}\n- Current Value: ${portfolio_data.get('current_value')}\n- Total P&L: ${portfolio_data.get('total_pnl')}\n- Win Rate: {portfolio_data.get('win_rate', 0)}%\n- Average Trade Return: {portfolio_data.get('avg_return', 0)}%\n- Number of Trades: {portfolio_data.get('total_trades', 0)}\n- Recent Trades: {portfolio_data.get('recent_trades', [])}\n\nProvide analysis in this EXACT JSON format:\n{{\n    \"performance_grade\": \"A|B|C|D|F\",\n    \"strengths\": [\"list of portfolio strengths\"],\n    \"weaknesses\": [\"list of areas for improvement\"],\n    \"recommendations\": [\"specific actionable advice\"],\n    \"risk_assessment\": \"HIGH|MEDIUM|LOW\",\n    \"suggested_adjustments\": {{\n        \"position_sizing\": \"advice on position sizing\",\n        \"strategy_mix\": \"advice on strategy allocation\",\n        \"risk_management\": \"risk management improvements\"\n    }}\n}}\n\nRespond ONLY with valid JSON.\n"""
        full_prompt = self._build_history_prompt(history, prompt)
        response = await self._call_ollama(full_prompt, temperature=0.2)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._default_portfolio_analysis()
        return self._default_portfolio_analysis()
    
    async def generate_trading_insights(self, market_context: str, history: List[Tuple[str, str]] = []) -> str:
        prompt = f"""
You are a crypto trading strategist. Based on the current market context, provide actionable insights:\n\nMarket Context: {market_context}\n\nProvide 3-5 key insights focusing on:\n1. Current market sentiment\n2. Key levels to watch\n3. Potential opportunities\n4. Risk factors to consider\n5. Recommended actions\n\nKeep response concise and actionable.\n"""
        full_prompt = self._build_history_prompt(history, prompt)
        response = await self._call_ollama(full_prompt, temperature=0.3)
        return response or "Unable to generate insights at this time."

    def _default_analysis(self) -> Dict[str, Any]:
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
        return {
            "approved": False,
            "risk_score": 10,
            "recommended_position_size": "1%",
            "concerns": ["System error - cannot assess risk"],
            "suggestions": ["Wait for system recovery"],
            "reasoning": "Unable to evaluate due to system error"
        }

    def _default_portfolio_analysis(self) -> Dict[str, Any]:
        return {
            "performance_grade": "C",
            "strengths": [],
            "weaknesses": ["System error - cannot analyze portfolio"],
            "recommendations": ["Wait for system recovery"],
            "risk_assessment": "MEDIUM",
            "suggested_adjustments": {
                "position_sizing": "N/A",
                "strategy_mix": "N/A",
                "risk_management": "N/A"
            }
        } 