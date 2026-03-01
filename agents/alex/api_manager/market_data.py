"""
Market Data - 统一市场数据入口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from api_manager.stock_api import StockAPI
from api_manager.crypto_api import CryptoAPI

class MarketData:
    """统一市场数据 API"""
    
    def __init__(self):
        self.stock = StockAPI()
        self.crypto = CryptoAPI()
    
    def quote(self, symbol: str, market: str = 'auto') -> dict:
        """获取报价 (自动识别市场)"""
        if market == 'stock':
            return self.stock.get_quote(symbol)
        elif market == 'crypto':
            return self.crypto.get_quote(symbol)
        else:
            # 自动识别
            crypto_suffixes = ['/USDT', '/USD', '/BTC', '/ETH']
            if any(s in symbol.upper() for s in crypto_suffixes):
                return self.crypto.get_quote(symbol)
            else:
                return self.stock.get_quote(symbol)
    
    def batch_quote(self, symbols: List[str], market: str = 'auto') -> Dict:
        """批量获取报价"""
        return {s: self.quote(s, market) for s in symbols}

# 测试
if __name__ == "__main__":
    md = MarketData()
    print("Stock:", md.quote("NVDA"))
    print("Crypto:", md.quote("BTC/USDT"))
