# HEARTBEAT.md - Ken's Schedule

# Ken's market analysis runs every 6 hours

## Cron Schedule

```
# Run every 6 hours: 0, 6, 12, 18 UTC
0 */6 * * *
```

## Tasks

1. Fetch BTC volatility index from Deribit
2. Fetch QQQ/SPY options data from OptionCharts
3. Fetch Polymarket Bitcoin predictions
4. Fetch Polymarket Ethereum predictions
5. Fetch BTC open interest from Coinglass
6. Generate volatility range forecast
7. Report to main session via Jarvis

## Data Sources

- https://www.deribit.com/statistics/BTC/volatility-index
- https://optioncharts.io/options/SPY
- https://polymarket.com/predictions/bitcoin
- https://polymarket.com/predictions/ethereum
- https://www.coinglass.com/open-interest/BTC

---

*Every 6 hours, data-driven market analysis.*