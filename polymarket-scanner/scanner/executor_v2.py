#!/usr/bin/env python3
"""
Polymarket Order Executor - Official SDK Version
Low-latency order execution using py-clob-client
"""

import os
import time
from typing import Dict, Optional
from dataclasses import dataclass
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs
from py_clob_client.exceptions import PolyApiException

@dataclass
class OrderResult:
    order_id: str
    status: str
    latency_ms: float
    filled_price: Optional[float] = None

class OrderExecutor:
    CLOB_URL = "https://clob.polymarket.com"
    CHAIN_ID = 137
    
    def __init__(self, api_key: str = None, private_key: str = None):
        self.api_key = api_key or os.getenv("POLYMARKET_API_KEY")
        self.private_key = private_key or os.getenv("POLYMARKET_PRIVATE_KEY")
        self.client = None
        self._init_client()
        
    def _init_client(self):
        if not self.api_key or not self.private_key:
            print("⚠️ No API credentials - read-only mode")
            return
            
        try:
            creds = ApiCreds(key=self.api_key, secret=self.private_key)
            self.client = ClobClient(
                host=self.CLOB_URL,
                key=self.private_key,
                chain_id=self.CHAIN_ID,
                creds=creds
            )
            print("✅ Authenticated with Polymarket")
        except Exception as e:
            print(f"❌ Auth failed: {e}")
            
    def create_order(
        self,
        condition_id: str,
        side: str,  # "YES" or "NO"
        amount: float,
        price_limit: float = 0.99
    ) -> Optional[OrderResult]:
        """Place a limit order"""
        start = time.time()
        
        if not self.client:
            return OrderResult("", "no_client", 0)
            
        try:
            # Build order args
            order_args = OrderArgs(
                condition_id=condition_id,
                side=side,
                amount=str(amount),
                price=str(price_limit)
            )
            
            # Place order via SDK
            result = self.client.create_order(order_args)
            latency_ms = (time.time() - start) * 1000
            
            return OrderResult(
                order_id=result.get("orderID", ""),
                status="submitted",
                latency_ms=latency_ms
            )
            
        except PolyApiException as e:
            latency_ms = (time.time() - start) * 1000
            return OrderResult("", f"error: {e}", latency_ms)
        except Exception as e:
            latency_ms = (time.time() - start) * 1000
            return OrderResult("", f"exception: {e}", latency_ms)
            
    def execute_equal_pair(
        self,
        condition_id: str,
        amount: float,
        max_price: float = 0.99
    ) -> Dict:
        """Execute equal YES/NO orders simultaneously"""
        start = time.time()
        
        # Both orders at same time
        yes_result = self.create_order(condition_id, "YES", amount, max_price)
        no_result = self.create_order(condition_id, "NO", amount, max_price)
        
        total_latency = (time.time() - start) * 1000
        
        return {
            "yes": {"id": yes_result.order_id, "status": yes_result.status},
            "no": {"id": no_result.order_id, "status": no_result.status},
            "total_latency_ms": total_latency
        }
        
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status"""
        if not self.client:
            return {}
            
        try:
            return self.client.get_order(order_id)
        except:
            return {}
            
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.client:
            return False
            
        try:
            return self.client.cancel_order(order_id)
        except:
            return False

# Example usage
if __name__ == "__main__":
    import sys
    
    # Test mode (no auth)
    executor = OrderExecutor()
    
    if len(sys.argv) > 1:
        condition_id = sys.argv[1]
        amount = float(sys.argv[2]) if len(sys.argv) > 2 else 10
        
        print(f"Testing order on {condition_id}...")
        result = executor.create_order(condition_id, "YES", amount)
        print(f"Result: {result.status}")
        print(f"Latency: {result.latency_ms:.0f}ms")
    else:
        print("Usage: python executor.py <condition_id> [amount]")