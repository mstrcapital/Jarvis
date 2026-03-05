---
name: ritmex-bot
description: Perp DEX Trading Bot - Multi-exchange perpetual futures trading with SMA30 trend, Guardian stop-loss, and market-making strategies.
---

# ritmex-bot Skill

> Perp DEX Trading Bot - Multi-exchange perpetual futures trading with SMA30 trend, Guardian stop-loss, and market-making strategies.

**Repository:** https://github.com/discountry/ritmex-bot  
**Runtime:** Bun ≥ 1.2  
**Platforms:** macOS, Linux, Windows (WSL recommended)

---

## Overview

ritmex-bot is a Bun-powered multi-exchange perpetual trading terminal with:
- **SMA30 Trend Engine** - Trend following with Bollinger Band filters
- **Guardian Stop Sentinel** - Monitors positions, auto-adjusts stops/tp
- **Market Making Modes** - Dual-sided quoting with self-healing

---

## Installation

### Quick Install
```bash
curl -fsSL https://github.com/discountry/ritmex-bot/raw/refs/heads/main/setup.sh | bash
```

### Manual Install
```bash
git clone https://github.com/discountry/ritmex-bot.git
cd ritmex-bot
bun install
cp .env.example .env
```

---

## Supported Exchanges

| Exchange | Type | Required Env Vars |
|----------|------|-------------------|
| Aster | USDT perp | `ASTER_API_KEY`, `ASTER_API_SECRET` |
| StandX | USD perp | `STANDX_TOKEN`, `STANDX_REQUEST_PRIVATE_KEY` |
| GRVT | USDT perp | `GRVT_API_KEY`, `GRVT_API_SECRET`, `GRVT_SUB_ACCOUNT_ID` |
| Lighter | zkLighter | `LIGHTER_ACCOUNT_INDEX`, `LIGHTER_API_PRIVATE_KEY` |
| Backpack | USDC perp | `BACKPACK_API_KEY`, `BACKPACK_API_SECRET`, `BACKPACK_PASSWORD` |
| Paradex | StarkEx | `PARADEX_PRIVATE_KEY`, `PARADEX_WALLET_ADDRESS` |
| Nado | USDC perp | `NADO_SIGNER_PRIVATE_KEY`, `NADO_SUBACCOUNT_OWNER` |
| Binance | USDT/USDC perp | `BINANCE_API_KEY`, `BINANCE_API_SECRET` |

---

## Core Strategies

### 1. Trend Strategy (SMA30)
- Entry: Price crosses above/below SMA30
- Exit: Stop-loss, trailing profit, Bollinger bandwidth filter
- Env vars: `TRADE_AMOUNT`, `LOSS_LIMIT`, `TRAILING_PROFIT`, `BOLLINGER_*`

### 2. Maker Strategy
- Dual-sided market making with risk controls
- Env vars: `MAKER_*`, `QTY_STEP`, `PRICE_TICK`

### 3. Guardian Strategy
- No new entries - only manages existing positions
- Auto-adjusts stop-loss and take-profit

---

## Commands

### CLI Interactive Mode
```bash
bun run index.ts
```

### Command Mode (Agent-friendly)
```bash
# Check system
ritmex-bot doctor
ritmex-bot doctor --json

# List exchanges
ritmex-bot exchange list

# Market data
ritmex-bot market ticker --exchange binance --symbol BTCUSDT
ritmex-bot market orderbook --exchange binance --symbol BTCUSDT --limit 10

# Account & Positions
ritmex-bot account balance --exchange binance
ritmex-bot account positions --exchange binance

# Orders
ritmex-bot order create --exchange binance --symbol BTCUSDT --side buy --type limit --quantity 0.01 --price 90000 --dry-run
ritmex-bot order cancel --exchange binance --order-id xxx
ritmex-bot order list --exchange binance

# Run Strategy
ritmex-bot strategy run --strategy trend --exchange aster --dry-run
ritmex-bot strategy run --strategy maker --exchange standx --silent
```

---

## Environment Variables

### Essential
```bash
EXCHANGE=aster                    # Exchange name
TRADE_SYMBOL=BTCUSDT             # Trading pair
TRADE_AMOUNT=0.01                # Order size
LOSS_LIMIT=50                    # Max loss per trade (USDT)
TRAILING_PROFIT=100              # Trailing profit trigger (USDT)
TRAILING_CALLBACK_RATE=0.5       # Trailing callback %
```

### Precision (per exchange)
```bash
PRICE_TICK=0.5                   # Min price increment
QTY_STEP=0.001                   # Min quantity increment
```

### Trend Strategy
```bash
BOLLINGER_PERIOD=20
BOLLINGER_STD=2
POLL_INTERVAL_MS=5000
```

### Maker Strategy
```bash
MAKER_SPREAD=0.001
MAKER_QUOTE_AMOUNT=0.01
MAKER_REBALANCE_INTERVAL=30
```

---

## Dry Run Mode

Always test with `--dry-run` first:
```bash
ritmex-bot order create --exchange binance --symbol BTCUSDT --side buy --type limit --quantity 0.01 --price 90000 --dry-run
bun run index.ts --strategy trend --dry-run
```

---

## Risk Warnings

1. **Start small** - Test with 50-100 USDT first
2. **Set leverage** - Configure at exchange (recommended ~50x)
3. **Time sync** - Ensure server time is accurate
4. **One-way position** - Use单向持仓模式
5. **API permissions** - Enable合约交易权限

---

## Use Cases

### For Jarvis Team

1. **Monitor Markets** - Use command mode to fetch prices/positions
2. **Automated Trading** - Run strategies via cron or pm2
3. **Multi-exchange Arbitrage** - Compare spreads across DEXs
4. **Risk Management** - Use Guardian strategy on existing positions

### Quick Start Commands
```bash
# Install
cd /root/.openclaw/workspace/skills/ritmex-bot
bun install

# Configure (edit .env)
cp .env.example .env

# Test connection
bun run index.ts --exchange aster --strategy trend --dry-run
```

---

## File Structure

```
ritmex-bot/
├── index.ts              # CLI entry point
├── cli/                  # Command modules
├── strategies/           # Trading strategies
├── exchanges/            # Exchange adapters
├── lib/                  # Utilities
├── .env.example          # Environment template
└── package.json
```

---

## References

- CLI Guide (EN): https://github.com/discountry/ritmex-bot/blob/main/cli-guide.en.md
- Simple Guide: https://github.com/discountry/ritmex-bot/blob/main/simple-readme.md
- Telegram: https://t.me/+4fdo0quY87o4Mjhh