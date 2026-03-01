import asyncio
import aiohttp
import time
import json
import os
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Order:
    market_id: str
    side: str  # "yes" or "no"
    amount: float
    price_limit: float = 0.99

@dataclass
class OrderResult:
    order_id: str
    status: str
    latency_ms: float
    filled_price: Optional[float] = None

class OrderExecutor:
    """Low-latency order executor for Polymarket"""
    
    def __init__(self, api_key: str = None, private_key: str = None):
        self.api_key = api_key or os.getenv("POLYMARKET_API_KEY")
        self.private_key = private_key or os.getenv("POLYMARKET_PRIVATE_KEY")
        self.api_url = "https://clob.polymarket.com"
        self.session = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=50,
                ttl_dns_cache=300
            )
            timeout = aiohttp.ClientTimeout(total=5)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )
        return self.session
        
    async def execute_limit_order(self, order: Order) -> OrderResult:
        """Execute a limit order with timing"""
        start_time = time.time()
        session = await self._get_session()
        
        payload = {
            "market": order.market_id,
            "side": order.side,
            "amount": str(order.amount),
            "price": str(order.price_limit),
            "order_type": "limit"
        }
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        try:
            async with session.post(
                f"{self.api_url}/orders",
                json=payload,
                headers=headers
            ) as resp:
                latency_ms = (time.time() - start_time) * 1000
                
                if resp.status in [200, 201]:
                    text = await resp.text()
                    return OrderResult(
                        order_id=text,
                        status="submitted",
                        latency_ms=latency_ms
                    )
                else:
                    error = await resp.text()
                    return OrderResult(
                        order_id="",
                        status=f"error: {error}",
                        latency_ms=latency_ms
                    )
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return OrderResult(
                order_id="",
                status=f"exception: {str(e)}",
                latency_ms=latency_ms
            )
            
    async def execute_equal_pair(
        self, 
        market_id: str, 
        amount: float,
        max_price: float = 0.99
    ) -> Dict:
        """Execute equal Yes/No orders"""
        start_time = time.time()
        
        yes_order = Order(
            market_id=market_id,
            side="yes",
            amount=amount,
            price_limit=max_price
        )
        
        no_order = Order(
            market_id=market_id,
            side="no", 
            amount=amount,
            price_limit=max_price
        )
        
        yes_result = await self.execute_limit_order(yes_order)
        no_result = await self.execute_limit_order(no_order)
        
        total_latency = (time.time() - start_time) * 1000
        
        return {
            "yes_order": {
                "id": yes_result.order_id,
                "status": yes_result.status,
                "latency_ms": yes_result.latency_ms
            },
            "no_order": {
                "id": no_result.order_id,
                "status": no_result.status,
                "latency_ms": no_result.latency_ms
            },
            "total_latency_ms": total_latency,
            "timestamp": datetime.now().isoformat()
        }

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()