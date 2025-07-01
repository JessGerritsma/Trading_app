from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from datetime import datetime
from ..core.database import Base

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    quote_volume = Column(Float, nullable=True)
    trade_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MarketData(symbol={self.symbol}, timestamp={self.timestamp}, close={self.close_price})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat() if self.timestamp is not None else None,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "volume": self.volume,
            "quote_volume": self.quote_volume,
            "trade_count": self.trade_count,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None
        } 