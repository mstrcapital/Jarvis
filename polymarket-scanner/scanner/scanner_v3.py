#!/usr/bin/env python3
"""
Polymarket Scanner - Updated Version
Fixed API issues: use correct parameters for real-time data
"""

import requests
import time
from datetime import datetime
from typing import List, Dict, Optional

class PolymarketScanner:
    GAMMA_URL = "https://gamma-api.polymarket.com"
    CLOB_URL = "https://clob.polymarket.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })
        
    def get_markets(self, limit: int = 50, closed: bool = False) -> List[Dict]:
        """Get markets from Gamma API"""
        params = {
            "closed": "false" if not closed else "true",
            "limit": limit
        }
        
        resp = self.session.get(
            f"{self.GAMMA_URL}/markets",
            params=params,
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", data) if isinstance(data, dict) else data
        return []
    
    def get_active_markets(self, min_volume: float = 5000) -> List[Dict]:
        """Get active markets with significant volume"""
        markets = self.get_markets(limit=100, closed=False)
        
        # Filter for active markets with valid prices
        active = []
        for m in markets:
            volume = float(m.get("volume", 0))
            best_bid = m.get("bestBid")
            
            # Check if market is truly active (not resolved)
            if not m.get("closed", True) and volume > min_volume:
                if best_bid and best_bid != "0":
                    active.append(m)
                    
        # Sort by volume
        active.sort(key=lambda x: float(x.get("volume", 0)), reverse=True)
        return active
    
    def get_market_price(self, market: Dict) -> Dict:
        """Extract price from market data"""
        return {
            "question": market.get("question", ""),
            "best_bid": market.get("bestBid", ""),
            "best_ask": market.get("bestAsk", ""),
            "last_trade": market.get("lastTradePrice", ""),
            "volume": market.get("volume", ""),
            "volume_24h": market.get("volume24hr", ""),
            "liquidity": market.get("liquidity", ""),
            "condition_id": market.get("conditionId", ""),
            "slug": market.get("slug", ""),
            "active": market.get("active", False),
            "closed": market.get("closed", True)
        }
    
    def search_markets(self, keywords: List[str], min_volume: float = 1000) -> List[Dict]:
        """Search markets by keywords"""
        markets = self.get_active_markets(min_volume=min_volume)
        
        results = []
        for m in markets:
            question = m.get("question", "").lower()
            if any(k.lower() in question for k in keywords):
                results.append(self.get_market_price(m))
                
        return results
    
    def get_orderbook(self, condition_id: str) -> Dict:
        """Get orderbook from CLOB API"""
        resp = self.session.get(
            f"{self.CLOB_URL}/orderbooks/{condition_id}",
            timeout=10
        )
        
        if resp.status_code == 200:
            return resp.json()
        return {"bids": [], "asks": [], "error": resp.status_code}
    
    def scan_finance_markets(self) -> List[Dict]:
        """Scan for finance-related markets"""
        keywords = [
            "S&P", "stock", "market", "index", 
            "Bitcoin", "ETH", "crypto", "tariff",
            "Fed", "interest", "economy", "GDP"
        ]
        return self.search_markets(keywords)
    
    def get_top_markets(self, n: int = 10) -> List[Dict]:
        """Get top N markets by volume"""
        markets = self.get_active_markets(min_volume=5000)
        return [self.get_market_price(m) for m in markets[:n]]


def main():
    scanner = PolymarketScanner()
    
    print("=== Polymarket Scanner (Updated) ===")
    print(f"Time: {datetime.now().strftime('%H:%M:%S UTC')}\n")
    
    # Test 1: Get active markets
    print("📊 Test 1: 获取活跃市场...")
    start = time.time()
    markets = scanner.get_active_markets(min_volume=5000)
    latency = (time.time() - start) * 1000
    print(f"   成功! 找到 {len(markets)} 个活跃市场")
    print(f"   延迟: {latency:.0f}ms\n")
    
    # Test 2: Top markets
    print("📈 Test 2: Top 10 市场:")
    top = scanner.get_top_markets(10)
    for i, m in enumerate(top, 1):
        print(f"   {i:2}. {m['question'][:45]}...")
        print(f"       💰 {m['best_bid']}/{m['best_ask']} | Vol: ${float(m['volume']):,.0f}")
    
    # Test 3: Search
    print("\n🔍 Test 3: 搜索关键词 [Bitcoin, tariff, Fed]")
    found = scanner.search_markets(["Bitcoin", "tariff", "Fed"])
    print(f"   找到 {len(found)} 个相关市场")
    for m in found[:5]:
        print(f"   - {m['question'][:50]}... ({m['best_bid']}/{m['best_ask']})")
    
    print("\n✅ Scanner 更新完成!")


if __name__ == "__main__":
    main()