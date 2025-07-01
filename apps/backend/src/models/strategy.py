from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from datetime import datetime
from ..core.database import Base

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)  # MEAN_REVERSION, MOMENTUM, etc.
    parameters = Column(JSON, nullable=True)  # Strategy-specific parameters
    active = Column(Boolean, default=True)
    symbols = Column(JSON, nullable=True)  # List of symbols this strategy trades
    performance_metrics = Column(JSON, nullable=True)  # Performance tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Strategy(id={self.id}, name={self.name}, type={self.type}, active={self.active})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "parameters": self.parameters,
            "active": self.active,
            "symbols": self.symbols,
            "performance_metrics": self.performance_metrics,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None
        } 