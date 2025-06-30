from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they are registered
        from ..models import Trade, Strategy, MarketData, AIDecision
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def init_db():
    """Initialize database with default data"""
    try:
        db = SessionLocal()
        
        # Create default strategies
        from ..models import Strategy
        
        # Check if strategies already exist
        existing_strategies = db.query(Strategy).count()
        if existing_strategies == 0:
            default_strategies = [
                Strategy(
                    name="BTC Mean Reversion v1",
                    description="Mean reversion strategy for BTC/USDT",
                    type="MEAN_REVERSION",
                    parameters={
                        "lookback_period": 20,
                        "std_dev_threshold": 2.0,
                        "min_confidence": 0.7
                    },
                    symbols=["BTCUSDT"],
                    active=True
                ),
                Strategy(
                    name="ETH Momentum v1",
                    description="Momentum strategy for ETH/USDT",
                    type="MOMENTUM",
                    parameters={
                        "lookback_period": 14,
                        "rsi_oversold": 30,
                        "rsi_overbought": 70
                    },
                    symbols=["ETHUSDT"],
                    active=True
                )
            ]
            
            db.add_all(default_strategies)
            db.commit()
            logger.info("Default strategies created successfully")
        
        db.close()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise 