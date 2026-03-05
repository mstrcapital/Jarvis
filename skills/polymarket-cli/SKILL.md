---
name: polymarket-cli
description: Polymarket CLI - 浏览预测市场、下单、查看仓位。无需钱包可浏览，需要钱包下单。
---

# Polymarket CLI

> 官方 Rust CLI - 预测市场命令行工具

**安装:** `brew install polymarket` 或 `curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh`  
**已安装:** ✅ `/usr/local/bin/polymarket`

---

## 快速开始

```bash
# 无需钱包 - 浏览市场
polymarket markets list --limit 10
polymarket markets search "bitcoin"
polymarket clob price TOKEN_ID --side buy

# JSON 输出 (脚本用)
polymarket -o json markets list --limit 5
```

---

## 市场查询

```bash
# 列出市场
polymarket markets list --limit 10
polymarket markets list --active true --order volume_num
polymarket markets list --closed false --limit 50

# 搜索
polymarket markets search "bitcoin" --limit 5

# 获取单个市场
polymarket markets get 12345
polymarket markets get will-bitcoin-hit-100k

# 标签
polymarket tags list
polymarket tags get politics
```

---

## 价格查询 (无需钱包)

```bash
# 当前价格
polymarket clob price 48331043336612883... --side buy

# 中间价
polymarket clob midpoint TOKEN_ID

# 价差
polymarket clob spread TOKEN_ID

# 批量查询
polymarket clob batch-prices "TOKEN1,TOKEN2" --side buy
polymarket clob midpoints "TOKEN1,TOKEN2"

# 订单簿
polymarket clob book TOKEN_ID
polymarket clob books "TOKEN1,TOKEN2"

# 历史价格
polymarket clob price-history TOKEN_ID --interval 1d --fidelity 30

# 最后成交价
polymarket clob last-trade TOKEN_ID
```

---

## 交易操作 (需要钱包)

```bash
# 设置钱包
polymarket wallet create
polymarket wallet import 0xabc123...

# 检查余额
polymarket clob balance --asset-type collateral
polymarket clob balance --asset-type conditional --token TOKEN_ID

# 下单
polymarket clob create-order --token TOKEN_ID --side buy --price 0.50 --size 10
polymarket clob market-order --token TOKEN_ID --side buy --amount 5

# 撤单
polymarket clob cancel ORDER_ID
polymarket clob cancel-all

# 查看订单
polymarket clob orders
polymarket clob order ORDER_ID
```

---

## 仓位管理

```bash
# 当前仓位
polymarket data positions 0xWALLET_ADDRESS
polymarket data value 0xWALLET_ADDRESS

# 平仓仓位
polymarket data closed-positions 0xWALLET_ADDRESS

# 交易历史
polymarket data trades 0xWALLET_ADDRESS --limit 50
polymarket clob trades
```

---

## 链上操作

```bash
# 授权
polymarket approve check
polymarket approve set

# Split (USDC → YES/NO)
polymarket ctf split --condition 0xCONDITION... --amount 10

# Merge (YES/NO → USDC)
polymarket ctf merge --condition 0xCONDITION... --amount 10

# Redeem (结算后)
polymarket ctf redeem --condition 0xCONDITION...
```

---

## 奖励查询

```bash
polymarket clob rewards --date 2026-03-01
polymarket clob current-rewards
polymarket clob reward-percentages
```

---

## 常用脚本

### 获取 BTC 价格
```bash
polymarket -o json markets search "bitcoin" --limit 1 | jq '.[0].id'
# 然后用 ID 查询价格
polymarket clob midpoint TOKEN_ID
```

### 获取前10市场
```bash
polymarket -o json markets list --limit 10 | jq '.[].question'
```

### 批量价格监控
```bash
polymarket -o json clob midpoints "TOKEN1,TOKEN2,TOKEN3"
```

---

## 输出格式

| 格式 | 命令 | 用途 |
|------|------|------|
| Table | `--output table` | 人类可读 (默认) |
| JSON | `-o json` | 脚本/自动化 |

---

## 注意事项

- 浏览市场: **无需钱包**
- 下单交易: **需要钱包** (私钥配置)
- 链上操作: **需要 MATIC** (Polygon gas)
- 默认链: **Polygon (chain_id: 137)**

---

## 参考

- GitHub: https://github.com/Polymarket/polymarket-cli
- 文档: https://docs.polymarket.com