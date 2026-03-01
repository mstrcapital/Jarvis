#!/usr/bin/env python3
"""
Polymarket Scanner - Official SDK Version
High-performance market scanner using py-clob-client

APIs:
- Gamma: https://gamma-api.polymarket.com (markets, events)
- Data: https://data-api.polymarket.com (positions, trades)
- CLOB: https://clob.polymarket.com (orderbook, trading)
"""

import os
import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# Official Polymarket SDK
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_clob_client.exceptions import PolyApiException

@dataclass
class MarketPrice:
    market_id: str
    condition_id: str
    question: str
    yes_price: float
    no_price: float
    mid_price: float
    spread: float
    volume: float
    timestamp: str
    latency_ms: float

class PolymarketScanner:
    GAMMA_URL = "https://gamma-api.polymarket.com"
    CLOB_URL = "https://clob.polymarket.com"
    CHAIN_ID = 137
    
    def __init__(self, api_key: str = None, private_key: str = None):
        self.api_key = api_key or os.getenv("POLYMARKET_API_KEY")
        self.private_key = private_key or os.getenv("POLYMARKET_PRIVATE_KEY")
        self.client = None
        self._init_client()
        
    def _init_client(self):
        try:
            if self.api_key and self.private_key:
                creds = ApiCreds(key=self.api_key, secret=self.private_key)
                self.client = ClobClient(
                    host=self.CLOB_URL,
                    key=self.private_key,
                    chain_id=self.CHAIN_ID,
                    creds=creds
                )
            else:
                self.client = ClobClient(host=self.CLOB_URL)
        except Exception as e:
            print(f"Client init: {e}")
            
    async def get_markets(self, query: str = None, limit: int = 50) -> List[Dict]:
        import aiohttp
        url = f"{self.GAMMA_URL}/markets"
        params = {"limit": limit, "active": "true"}
        if query:
            params["question__contains"] = query
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json() if resp.status == 200 else []
                
    async def get_price(self, condition_id: str) -> Optional[MarketPrice]:
        start = time.time()
        
        if not self.client:
            return None
            
        try:
            orderbook = self.client.get_order_book(condition_id)
            bids = orderbook.get("bids", [])
            asks = orderbook.get("asks", [])
            
            best_bid = float(bids[0]["price"]) if bids else 0
            best_ask = float(asks[0]["price"]) if asks else 0
            
            mid = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            
            try:
                market = self.client.get_market(condition_id)
                question = market.get("question", "")
                volume = float(market.get("volume", 0))
            except:
                question = ""
                volume = 0
                
            latency_ms = (time.time() - start) * 1000
            
            return MarketPrice(
                market_id=condition_id,
                condition_id=condition_id,
                question=question,
                yes_price=best_bid,
                no_price=best_ask,
                mid_price=mid,
                spread=spread,
                volume=volume,
                timestamp=datetime.now().isoformat(),
                latency_ms=latency_ms
            )
        except Exception as e:
            print(f"Error: {e}")
            return None

async def main():
    scanner = PolymarketScanner()
    
    print("🔍 Scanning S&P 500 markets...")
    markets = await scanner.get_markets("S&P 500", limit=20)
    
    print(f"Found {len(markets)} markets")
    
    for m in markets[:5]:
        cond_id = m.get("conditionId")
        if cond_id:
            price = await scanner.get_price(cond_id)
            if price:
                print(f"\n{price.question[:50]}")
                print(f"  Yes: {price.yes_price:.2f} | No: {price.no_price:.2f}")
                print(f"  Spread: {price.spread:.3f} | Latency: {price.latency_ms:.0f}ms")

if __name__ == "__main__":
    asyncio.run(main())