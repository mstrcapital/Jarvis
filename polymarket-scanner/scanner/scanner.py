import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import redis
import os

class PolymarketScanner:
    """Polymarket market scanner with low-latency price tracking"""
    
    def __init__(self, api_key: str = None, redis_url: str = "redis://localhost:6379"):
        self.api_key = api_key or os.getenv("POLYMARKET_API_KEY")
        self.api_url = "https://clob.polymarket.com"
        self.ws_url = "wss://clob.polymarket.com/ws"
        self.markets = {}
        self.price_cache = {}
        
        # Redis for caching
        try:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            self.redis.ping()
            self.redis_enabled = True
        except:
            self.redis_enabled = False
            print("⚠️ Redis not available, using in-memory cache")
            
    async def fetch_markets(self, filter_query: str = "S&P 500") -> List[Dict]:
        """Fetch markets matching filter"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/markets",
                    params={"condition": filter_query, "limit": 50}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("markets", [])
                    return []
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
            
    async def get_market_orderbook(self, market_id: str) -> Dict:
        """Get order book for a market"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/markets/{market_id}/orderbook"
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {}
        except Exception as e:
            print(f"Error fetching orderbook: {e}")
            return {}
            
    async def get_market_price(self, market_id: str) -> Dict:
        """Get current price with latency tracking"""
        start_time = time.time()
        
        orderbook = await self.get_market_orderbook(market_id)
        latency_ms = (time.time() - start_time) * 1000
        
        # Extract best bid/ask
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])
        
        best_bid = float(bids[0]["price"]) if bids else 0
        best_ask = float(asks[0]["price"]) if asks else 0
        mid_price = (best_bid + best_ask) / 2 if best_bid and best_ask else 0
        
        result = {
            "market_id": market_id,
            "bid": best_bid,
            "ask": best_ask,
            "mid": mid_price,
            "latency_ms": latency_ms,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache in Redis
        if self.redis_enabled:
            self.redis.setex(
                f"price:{market_id}", 
                60, 
                json.dumps(result)
            )
        else:
            self.price_cache[market_id] = result
            
        return result
        
    async def stream_prices(self, market_ids: List[str]):
        """WebSocket price stream (if available)"""
        try:
            async with aiohttp.ClientSession() as session:
                ws = await session.ws_connect(self.ws_url)
                
                # Subscribe to markets
                await ws.send_json({
                    "type": "subscribe",
                    "markets": market_ids
                })
                
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if data.get("type") == "price":
                            yield data
                            
        except Exception as e:
            print(f"WebSocket error: {e}")
            
    async def scan_finance_markets(self) -> List[Dict]:
        """Scan for Finance/S&P 500 markets"""
        target_markets = [
            "S&P 500 Opens Up",
            "S&P 500 Opens Down", 
            "S&P 500 Closes Up",
            "S&P 500 Closes Down"
        ]
        
        results = []
        markets = await self.fetch_markets("S&P 500")
        
        for market in markets:
            title = market.get("question", "").lower()
            if any(t.lower() in title for t in target_markets):
                # Get current price
                price_data = await self.get_market_price(market["id"])
                market["current_price"] = price_data
                results.append(market)
                
        return results
        
    def get_cached_price(self, market_id: str) -> Optional[Dict]:
        """Get cached price"""
        if self.redis_enabled:
            data = self.redis.get(f"price:{market_id}")
            return json.loads(data) if data else None
        return self.price_cache.get(market_id)


async def main():
    scanner = PolymarketScanner()
    
    # Scan for target markets
    print("🔍 Scanning for S&P 500 markets...")
    markets = await scanner.scan_finance_markets()
    
    for m in markets:
        price = m.get("current_price", {})
        print(f"  {m.get('question')}")
        print(f"    Bid: {price.get('bid')}, Ask: {price.get('ask')}")
        print(f"    Latency: {price.get('latency_ms'):.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())