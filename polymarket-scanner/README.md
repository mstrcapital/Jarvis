# Polymarket Trading Scanner - Technical Architecture

## ⚠️ Disclaimer
This is a technical infrastructure guide. Ensure all trading activities comply with Polymarket Terms of Service and applicable laws.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Polymarket Trading System                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │   Scanner    │───▶│   Executor   │───▶│   Monitor    │         │
│  │   Engine     │    │   Engine     │    │   Engine     │         │
│  └──────────────┘    └──────────────┘    └──────────────┘         │
│        │                   │                   │                     │
│        ▼                   ▼                   ▼                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │  Price DB    │    │  Order API   │    │  Latency     │         │
│  │  (Redis)     │    │  (WebSocket) │    │  Tracker     │         │
│  └──────────────┘    └──────────────┘    └──────────────┘         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Target Markets

| Market | Condition | API Query |
|--------|-----------|-----------|
| S&P 500 Opens Up | "S&P 500" + "opens up" | condition_id |
| S&P 500 Opens Down | "S&P 500" + "opens down" | condition_id |
| S&P 500 Closes Up | "S&P 500" + "closes up" | condition_id |
| S&P 500 Closes Down | "S&P 500" + "closes down" | condition_id |

---

## Performance Requirements

| Metric | Target | Implementation |
|--------|--------|----------------|
| Quote Latency | < 2s | WebSocket + Local Cache |
| Order Execution | < 3s | Async HTTP + Connection Pool |
| Price Refresh | 100ms | WebSocket Stream |

---

## Core Components

### 1. Scanner Engine (`scanner.py`)

```python
import asyncio
import aiohttp
from typing import Dict, List, Optional

class PolymarketScanner:
    def __init__(self):
        self.ws_url = "wss://clob.polymarket.com/ws"
        self.api_url = "https://clob.polymarket.com"
        self.markets = {}  # price cache
        
    async def get_markets(self, filter: str) -> List[Dict]:
        """Fetch markets matching filter"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/markets",
                params={"condition": filter}
            ) as resp:
                return await resp.json()
                
    async def stream_prices(self, market_slugs: List[str]):
        """WebSocket price stream"""
        async with aiohttp.ClientSession() as session:
            ws = await session.ws_connect(self.ws_url)
            await ws.send_json({"type": "subscribe", "markets": market_slugs})
            async for msg in ws:
                yield msg.json()
```

### 2. Price Cache with Redis (`cache.py`)

```python
import redis
import json
from datetime import datetime

class PriceCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.ttl = 60  # seconds
        
    def set_price(self, market_id: str, price: float, timestamp: float):
        key = f"price:{market_id}"
        data = {
            "price": price,
            "timestamp": timestamp,
            "latency_ms": (datetime.now().timestamp() - timestamp) * 1000
        }
        self.redis.setex(key, self.ttl, json.dumps(data))
        
    def get_price(self, market_id: str) -> Optional[dict]:
        data = self.redis.get(f"price:{market_id}")
        return json.loads(data) if data else None
```

### 3. Order Executor (`executor.py`)

```python
import asyncio
import aiohttp
from dataclasses import dataclass

@dataclass
class Order:
    market_id: str
    side: str  # "yes" or "no"
    amount: float
    price_limit: float  # max 0.99

class OrderExecutor:
    def __init__(self, api_key: str, private_key: str):
        self.api_key = api_key
        self.private_key = private_key
        self.api_url = "https://clob.polymarket.com"
        self.session = None
        
    async def execute_order(self, order: Order) -> dict:
        """Execute limit order with latency tracking"""
        start = asyncio.get_event_loop().time()
        
        payload = {
            "market": order.market_id,
            "side": order.side,
            "amount": order.amount,
            "price": order.price_limit,
            "order_type": "limit"
        }
        
        # Sign with private key
        # payload["signature"] = self.sign(payload)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/orders",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as resp:
                latency = (asyncio.get_event_loop().time() - start) * 1000
                return {
                    "order_id": await resp.text(),
                    "latency_ms": latency
                }
```

---

## Strategy: Equal Amount Yes/No

```python
class EqualAmountStrategy:
    def __init__(self, max_price: float = 0.99):
        self.max_price = max_price
        
    def calculate_orders(self, market_id: str, amount: float) -> List[Order]:
        """Generate equal yes/no orders"""
        return [
            Order(market_id=market_id, side="yes", amount=amount, price_limit=self.max_price),
            Order(market_id=market_id, side="no", amount=amount, price_limit=self.max_price)
        ]
```

---

## Target API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/markets` | GET | List markets |
| `/markets/{id}` | GET | Market details |
| `/markets/{id}/orderbook` | GET | Order book |
| `/orders` | POST | Place order |
| `/orders/{id}` | GET | Order status |
| `/positions` | GET | User positions |
| `/ws` | WebSocket | Real-time prices |

---

## Docker Compose

```yaml
version: '3.8'

services:
  scanner:
    build: ./scanner
    ports:
      - "3000:3000"
    environment:
      - POLYMARKET_API_KEY=${POLYMARKET_API_KEY}
      - POLYMARKET_PRIVATE_KEY=${POLYMARKET_PRIVATE_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    config:
      - proxy_pass http://scanner:3000
```

---

## Files Structure

```
polymarket-scanner/
├── scanner/
│   ├── __init__.py
│   ├── scanner.py      # Market scanner
│   ├── cache.py        # Redis price cache
│   ├── executor.py     # Order executor
│   ├── strategy.py    # Trading strategies
│   └── monitor.py      # Latency monitor
├── config/
│   ├── .env.example
│   └── settings.yaml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp config/.env.example config/.env
# Edit .env with your API keys

# Run
docker-compose up -d

# Monitor latency
docker logs -f scanner
```

---

## Requirements

```
aiohttp>=3.9.0
redis>=5.0.0
python-dotenv>=1.0.0
websockets>=12.0
asyncio
pycryptodome
```

---

## ⚠️ Important Notes

1. **API Rate Limits**: Check Polymarket docs for limits
2. **Order Book**: Use order book prices for better fills
3. **Gas Fees**: Consider network fees in profitability
4. **Risk Management**: Always set max position sizes
5. **Compliance**: Ensure strategy complies with ToS

---

*This is a technical architecture. Always test on testnet first.*