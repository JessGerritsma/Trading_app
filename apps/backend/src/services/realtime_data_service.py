import asyncio
import logging
from datetime import datetime
from typing import Callable, Dict, Any, List, Optional, Tuple
from binance import AsyncClient
from binance.streams import BinanceSocketManager
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.market_data import MarketData
import numpy as np

logger = logging.getLogger(__name__)

class RealTimeDataService:
    def __init__(self, symbols: List[str], interval: str = '1m'):
        self.symbols = symbols
        self.interval = interval
        self.client: Optional[AsyncClient] = None
        self.bsm: Optional[BinanceSocketManager] = None
        self.tasks = []
        self.event_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self.ohlcv_cache: Dict[str, List[Dict[str, Any]]] = {symbol: [] for symbol in symbols}
        self.max_cache = 500  # For memory management
        self.running = False

    async def start(self):
        self.client = await AsyncClient.create()
        self.bsm = BinanceSocketManager(self.client)
        self.running = True
        for symbol in self.symbols:
            stream = self.bsm.kline_socket(symbol.lower(), self.interval)
            task = asyncio.create_task(self._handle_stream(symbol, stream))
            self.tasks.append(task)
        logger.info("Real-time data service started.")

    async def stop(self):
        self.running = False
        for task in self.tasks:
            task.cancel()
        # BinanceSocketManager does not require explicit close/stop in this version
        self.bsm = None
        if self.client:
            await self.client.close_connection()
        logger.info("Real-time data service stopped.")

    async def _handle_stream(self, symbol: str, stream):
        reconnect_delay = 5
        while self.running:
            try:
                async with stream as s:
                    async for msg in s:
                        if not self.running:
                            break
                        await self._process_kline_msg(symbol, msg)
            except Exception as e:
                logger.error(f"WebSocket error for {symbol}: {e}. Reconnecting in {reconnect_delay}s...")
                await asyncio.sleep(reconnect_delay)

    async def _process_kline_msg(self, symbol: str, msg: Dict[str, Any]):
        if msg.get('e') != 'kline':
            return
        k = msg['k']
        ohlcv = {
            'timestamp': datetime.utcfromtimestamp(k['t'] / 1000),
            'open_price': float(k['o']),
            'high_price': float(k['h']),
            'low_price': float(k['l']),
            'close_price': float(k['c']),
            'volume': float(k['v']),
            'quote_volume': float(k['q']),
            'trade_count': int(k['n'])
        }
        # Memory management: keep only last N
        cache = self.ohlcv_cache[symbol]
        cache.append(ohlcv)
        if len(cache) > self.max_cache:
            cache.pop(0)
        # Store in DB
        await self._store_market_data(symbol, ohlcv)
        # Calculate indicators
        indicators = self._calculate_indicators(cache)
        # Event-driven: call callbacks if trade signal
        event = {'symbol': symbol, 'ohlcv': ohlcv, 'indicators': indicators}
        for cb in self.event_callbacks:
            try:
                cb(event)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    async def _store_market_data(self, symbol: str, ohlcv: Dict[str, Any]):
        try:
            db: Session = SessionLocal()
            db_data = MarketData(
                symbol=symbol,
                timestamp=ohlcv['timestamp'],
                open_price=ohlcv['open_price'],
                high_price=ohlcv['high_price'],
                low_price=ohlcv['low_price'],
                close_price=ohlcv['close_price'],
                volume=ohlcv['volume'],
                quote_volume=ohlcv['quote_volume'],
                trade_count=ohlcv['trade_count']
            )
            db.add(db_data)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"DB store error: {e}")

    def _calculate_indicators(self, cache: List[Dict[str, Any]]) -> Dict[str, Any]:
        closes = np.array([x['close_price'] for x in cache], dtype=float)
        indicators = {}
        if len(closes) >= 14:
            indicators['rsi'] = self._rsi(closes)
        if len(closes) >= 26:
            macd, signal = self._macd(closes)
            indicators['macd'] = macd
            indicators['macd_signal'] = signal
        if len(closes) >= 20:
            indicators['ma20'] = float(np.mean(closes[-20:]))
        if len(closes) >= 50:
            indicators['ma50'] = float(np.mean(closes[-50:]))
        return indicators

    def _rsi(self, closes: np.ndarray, period: int = 14) -> float:
        deltas = np.diff(closes)
        seed = deltas[:period]
        up = seed[seed > 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = 100. - 100. / (1. + rs)
        return float(np.round(rsi, 2))

    def _macd(self, closes: np.ndarray) -> Tuple[float, float]:
        ema12 = self._ema(closes, 12)
        ema26 = self._ema(closes, 26)
        macd = ema12 - ema26
        signal = self._ema(macd[-9:], 9) if len(macd) >= 9 else 0
        return float(macd[-1]), float(signal[-1]) if isinstance(signal, np.ndarray) else float(signal)

    def _ema(self, data: np.ndarray, window: int) -> np.ndarray:
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        a = np.convolve(data, weights, mode='full')[:len(data)]
        a[:window] = a[window]
        return a

    def add_event_callback(self, callback: Callable[[Dict[str, Any]], None]):
        self.event_callbacks.append(callback)

# Example usage:
# service = RealTimeDataService(['BTCUSDT', 'ETHUSDT'])
# asyncio.run(service.start())
# service.add_event_callback(lambda event: print(event)) 