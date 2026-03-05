---
name: polymarket-analyst
description: Polymarket 预测市场分析交易工具。用于分析 Finance 和 Crypto 市场的高 EV 机会,获取实时价格数据,下单交易。
---

# Polymarket Analyst Skill

> 给 Ken (Polymarket 分析师) 和 Tan (量化策略) 使用的完整工具集

**CLI 工具:** `polymarket` (已安装)  
**EV 监控:** `/root/.openclaw/workspace/agents/ken/polymarket_ev_monitor.py`  
**钱包:** `0xd9F5E738f72F124461E91e660e5E1b4ca36b2EE8`

---

## 📊 常用命令

### 市场查询
```bash
# 列出活跃市场
polymarket markets list --limit 10 --active true

# 搜索市场
polymarket markets search "bitcoin" --limit 5
polymarket markets search "fed" --limit 5

# 获取单个市场详情
polymarket markets get <market_id>
```

### 价格查询 (无需钱包)
```bash
# 当前价格
polymarket clob price <token_id> --side buy

# 中间价
polymarket clob midpoint <token_id>

# 订单簿
polymarket clob book <token_id>

# 批量价格
polymarket clob midpoints "token1,token2"
```

### 交易操作 (需要钱包)
```bash
# 检查余额
polymarket clob balance --asset-type collateral

# 下单
polymarket clob create-order --token <token> --side buy --price 0.50 --size 10

# 撤单
polymarket clob cancel <order_id>
polymarket clob cancel-all

# 查看订单
polymarket clob orders
```

---

## 🎯 高EV市场分析

### Finance (2026)
| 市场 | 价格 | 交易量 |
|------|------|--------|
| Fed 2次降息 2026 | 27.5¢ | $486K |
| Fed 3次降息 2026 | 19.5¢ | $346K |
| Fed 4次降息 2026 | 10.0¢ | $345K |
| Kevin Warsh Fed Chair | 93.35¢ | $45M |
| Judy Shelton Fed Chair | 3.85¢ | $102M |

### Crypto (2026)
| 市场 | 价格 | 交易量 |
|------|------|--------|
| BTC >$68K Mar 1 | 12.05¢ | $742K |
| ETH >$2,000 Mar 1 | 72.60¢ | $344K |
| MSTR 卖BTC Jun30 | 8.5¢ | $651K |

### 2028 大选
| 候选人 | 价格 | 交易量 |
|--------|------|--------|
| Tim Walz (D) | 0.75¢ | $32.8M |
| Bernie Sanders (D) | 0.75¢ | $30.6M |
| J.D. Vance (R) | 41.05¢ | $4.7M |
| Gavin Newsom (D) | 25.55¢ | $8.4M |
| Elon Musk (R) | 1.25¢ | $17.0M |

---

## 📈 EV 计算公式

```
EV = Payout × 主观概率 - Cost

其中:
- Payout = (1 - price) / price
- 主观概率 = 基于分析的合理概率估计
```

### 示例
- 价格 10¢ → Payout = 9
- 假设 30% 概率 true → EV = 9 × 0.3 - 0.7 = +200%

---

## 🤖 自动监控

### 每小时 EV 推送
```bash
# 手动运行
python3 /root/.openclaw/workspace/agents/ken/polymarket_ev_monitor.py

# Cron (每小时)
0 * * * * cd /root/.openclaw/workspace/agents/ken && python3 polymarket_ev_monitor.py
```

---

## 💰 交易限额

**钱包地址:** `0xd9F5E738f72F124461E91e660e5E1b4ca36b2EE8`  
**当前余额:** $0.92 ⚠️ 需要充值

### 充值
```bash
# 获取充值地址
polymarket bridge deposit 0xd9F5E738f72F124461E91e660e5E1b4ca36b2EE8
```

---

## 📋 Ken 每日任务

1. **每小时**: 检查 EV 监控推送
2. **每日**: 运行完整市场分析
3. **每周**: 生成周报 (周日在 14:00 UTC)

---

## 📋 Tan 量化任务

1. **数据收集**: 用 CLI 获取历史价格
2. **策略回测**: 分析价格 vs 概率偏差
3. **套利机会**: 寻找跨市场价差

---

## 🔧 快速脚本

### 获取 BTC 价格
```bash
polymarket -o json markets search "Bitcoin be above $68" --limit 1 | jq -r '.[0].outcomePrices'
```

### 获取 Fed 降息概率
```bash
polymarket -o json markets search "Fed rate cuts happen in 2026" --limit 15 | jq '.[] | {question: .question[:30], price: .outcomePrices}'
```

### 批量获取价格
```bash
polymarket -o json clob midpoints "token1,token2,token3"
```

---

## ⚠️ 注意事项

1. **IP 限制** - 已测试,IP 无限制 ✅
2. **余额** - 需要充值才能交易
3. **Gas** - Polygon 网络,需要 MATIC
4. **风险** - 预测市场有高风险

---

## 📞 参考

- CLI 文档: https://docs.polymarket.com
- 市场列表: https://polymarket.com
- 支持: support@polymarket.com