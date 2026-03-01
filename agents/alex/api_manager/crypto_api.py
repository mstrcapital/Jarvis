"""
Crypto API - 加密货币数据
支持: ccxt (Kraken, Coinbase, Bybit, etc.)
"""

import ccxt
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CryptoAPI:
    """加密货币 API"""
    
    def __init__(self, default_exchange: str = "kraken"):
        self.exchanges = {}
        self.default_exchange = default_exchange
        self._init_exchanges()
    
    def _init_exchanges(self):
        """初始化交易所"""
        exchange_names = ['kraken', 'coinbase', 'bybit', 'kucoin', 'okx']
        for name in exchange_names:
            try:
                self.exchanges[name] = getattr(ccxt, name)()
            except:
                pass
    
    def get_quote(self, symbol: str, exchange: str = None) -> Optional[Dict]:
        """获取实时报价"""
        ex_name = exchange or self.default_exchange
        ex = self.exchanges.get(ex_name)
        if not ex:
            # 尝试其他交易所
            for name, ex in self.exchanges.items():
                try:
                    ticker = ex.fetch_ticker(symbol)
                    return self._format_ticker(ticker, name)
                except:
                    continue
            return None
        
        try:
            ticker = ex.fetch_ticker(symbol)
            return self._format_ticker(ticker, ex_name)
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            # 尝试备用交易所
            for name, ex in self.exchanges.items():
                if name == ex_name:
                    continue
                try:
                    ticker = ex.fetch_ticker(symbol)
                    return self._format_ticker(ticker, name)
                except:
                    continue
            return None
    
    def _format_ticker(self, ticker, exchange: str) -> Dict:
        return {
            'symbol': ticker['symbol'],
            'price': ticker['last'],
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'volume_24h': ticker.get('baseVolume'),
            'change_24h': ticker.get('percentage'),
            'high_24h': ticker.get('high'),
            'low_24h': ticker.get('low'),
            'exchange': exchange,
        }
    
    def get_quotes(self, symbols: List[str], exchange: str = None) -> Dict[str, Dict]:
        """批量获取报价"""
        return {s: self.get_quote(s, exchange) for s in symbols}

if __name__ == "__main__":
    api = CryptoAPI()
    print(api.get_quote("BTC/USDT"))
    print(api.get_quote("ETH/USDT"))
