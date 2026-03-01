"""
Alex API Manager 配置
"""

# 股票 API (使用 yfinance)
STOCK_API = "yfinance"

# Crypto API (优先使用 Kraken)
CRYPTO_DEFAULT_EXCHANGE = "kraken"
CRYPTO_EXCHANGES = ["kraken", "coinbase", "bybit", "kucoin", "okx"]

# API 配置
API_CONFIG = {
    "stock": {
        "provider": "yfinance",
        "cache_ttl": 60,
    },
    "crypto": {
        "provider": "ccxt",
        "default_exchange": "kraken",
        "cache_ttl": 30,
    },
    "options": {
        "provider": "polymarket",
    }
}

# 支持的市场
SUPPORTED_MARKETS = {
    "stocks": ["NVDA", "QCOM", "TSLA", "MSFT", "GOOGL", "AMD", "META", "AMZN", "QQQ", "SPY"],
    "crypto": ["BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "AVAX", "LINK"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY"],
}
