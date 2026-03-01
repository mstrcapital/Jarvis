"""
Stock API - 股票数据
支持: yfinance
"""

import yfinance as yf
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class StockAPI:
    """股票数据 API"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 60
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """获取实时报价"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'change': info.get('regularMarketChange'),
                'change_pct': info.get('regularMarketChangePercent'),
                'volume': info.get('regularMarketVolume'),
                'high': info.get('regularMarketDayHigh'),
                'low': info.get('regularMarketDayLow'),
                'open': info.get('regularMarketOpen'),
                'prev_close': info.get('regularMarketPreviousClose'),
            }
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return None
    
    def get_quotes(self, symbols: List[str]) -> Dict[str, Dict]:
        """批量获取报价"""
        return {s: self.get_quote(s) for s in symbols}

if __name__ == "__main__":
    api = StockAPI()
    print(api.get_quote("NVDA"))
