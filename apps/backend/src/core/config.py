from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "TradingBot"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = True
    
    # Database
    database_url: str = "sqlite:///./data/sqlite/trading_bot.db"
    
    # Binance API
    binance_api_key: str = ""
    binance_secret_key: str = ""
    binance_testnet: bool = True
    binance_base_url: str = "https://testnet.binance.vision"
    
    # AI/LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Trading Configuration
    default_symbol: str = "BTCUSDT"
    trading_pairs: str = "BTCUSDT,ETHUSDT,ADAUSDT"
    max_position_size: float = 0.1
    max_daily_loss: float = 0.05
    stop_loss_percentage: float = 0.02
    take_profit_percentage: float = 0.04
    min_trade_amount: float = 10.0
    max_trade_amount: float = 1000.0
    
    # Strategy Configuration
    strategy_update_interval: int = 60
    backtest_days: int = 30
    mean_reversion_lookback: int = 20
    momentum_lookback: int = 14
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Feature Flags
    enable_live_trading: bool = False
    enable_ai_decisions: bool = True
    enable_backtesting: bool = True
    enable_real_time_charts: bool = True
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    allow_credentials: bool = True
    
    @property
    def trading_pairs_list(self) -> List[str]:
        """Parse trading_pairs string into a list"""
        return [pair.strip() for pair in self.trading_pairs.split(",") if pair.strip()]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse cors_origins string into a list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from environment

# Create settings instance
settings = Settings()

# Ensure data directories exist
def ensure_data_directories():
    """Create necessary data directories if they don't exist"""
    directories = [
        "data/sqlite",
        "data/logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Initialize data directories
ensure_data_directories() 