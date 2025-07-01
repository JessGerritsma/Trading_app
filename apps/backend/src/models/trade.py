from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
from typing import Optional
from ..core.database import Base

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    side = Column(String(10), nullable=False)  # BUY or SELL
    type = Column(String(20), nullable=False)  # MARKET, LIMIT, etc.
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    executed_price = Column(Float, nullable=True)
    status = Column(String(20), default="trial")  # trial, approved, auto
    order_id = Column(String(100), nullable=True)
    strategy = Column(String(50), nullable=True)
    ai_decision = Column(Boolean, default=False)
    ai_reasoning = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    datetime_entered = Column(DateTime, nullable=False, default=datetime.utcnow)
    datetime_exited = Column(DateTime, nullable=True)
    price_enter = Column(Float, nullable=False)
    price_exit = Column(Float, nullable=True)
    size = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)
    parameters = Column(Text, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    
    def __repr__(self):
        return f"<Trade(id={self.id}, symbol={self.symbol}, side={self.side}, quantity={self.quantity}, price={self.price})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "side": self.side,
            "type": self.type,
            "quantity": self.quantity,
            "price": self.price,
            "executed_price": self.executed_price,
            "status": self.status,
            "order_id": self.order_id,
            "strategy": self.strategy,
            "ai_decision": self.ai_decision,
            "ai_reasoning": self.ai_reasoning,
            "timestamp": self.timestamp.isoformat() if self.timestamp is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None
        } 