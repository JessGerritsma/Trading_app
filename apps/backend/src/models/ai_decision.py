from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from datetime import datetime
from ..core.database import Base

class AIDecision(Base):
    __tablename__ = "ai_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    action = Column(String(20), nullable=False)  # BUY, SELL, HOLD
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    reasoning = Column(Text, nullable=True)
    market_data = Column(JSON, nullable=True)  # Market data used for decision
    strategy_signals = Column(JSON, nullable=True)  # Strategy signals
    llm_response = Column(Text, nullable=True)  # Raw LLM response
    executed = Column(Boolean, default=False)  # Whether decision was executed
    trade_id = Column(Integer, nullable=True)  # Reference to executed trade
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIDecision(id={self.id}, symbol={self.symbol}, action={self.action}, confidence={self.confidence})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "action": self.action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "market_data": self.market_data,
            "strategy_signals": self.strategy_signals,
            "llm_response": self.llm_response,
            "executed": self.executed,
            "trade_id": self.trade_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp is not None else None
        } 