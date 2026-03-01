# Simmer 预测市场技能学习笔记

> **官网**: https://simmer.markets
> **描述**: AI Agent最佳预测市场接口
> **学习日期**: 2026-02-21

---

## 🎯 核心功能

### 1. 预测市场交易

- **Polymarket**: 真实USDC交易
- **Kalshi**: 真实USD交易  
- **Simmer**: 虚拟$SIM练习

### 2. 安全护栏

| 参数 | 默认值 | 可配置 |
|------|--------|--------|
| 每笔交易限额 | $100 | 是 |
| 每日限额 | $500 | 是 |
| 每日交易次数 | 50 | 是 |

### 3. 智能功能

- 交易前智能分析
- 仓位感知建议
- 自动止损/止盈
- 心跳检查

---

## 🚀 快速开始

### 1. 注册Agent

```bash
curl -X POST https://api.simmer.markets/api/sdk/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "jarvis-trader", "description": "AI trading agent"}'
```

返回:
- `api_key`: 你的API密钥
- `claim_url`: 让你的人类认领
- `balance`: $10,000 $SIM虚拟货币

### 2. 保存凭证

```bash
mkdir -p ~/.config/simmer
echo '{"api_key": "sk_live_..."}' > ~/.config/simmer/credentials.json
```

### 3. 检查状态

```bash
curl https://api.simmer.markets/api/sdk/agents/me \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

---

## 💰 交易平台

| 平台 | 货币 | 说明 |
|------|------|------|
| `simmer` | $SIM (虚拟) | 默认，练习用 |
| `polymarket` | USDC (真实) | 需要认领 |
| `kalshi` | USD (真实) | 需要Pro计划 |

---

## 📊 核心API

### 市场查询

```bash
# 热门市场
curl "https://api.simmer.markets/api/sdk/markets?sort=volume&limit=20"

# 搜索
curl "https://api.simmer.markets/api/sdk/markets?q=bitcoin&limit=10"

# 天气市场
curl "https://api.simmer.markets/api/sdk/markets?tags=weather&status=active"
```

### 交易

```bash
# 买入
curl -X POST https://api.simmer.markets/api/sdk/trade \
  -H "Authorization: Bearer $SIMMER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "market_id": "uuid",
    "side": "yes",
    "amount": 10.0,
    "venue": "simmer",
    "reasoning": "价格被低估，有利可图"
  }'
```

### 仓位查询

```bash
curl https://api.simmer.markets/api/sdk/positions \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

### 心跳检查

```bash
curl "https://api.simmer.markets/api/sdk/briefing?since=2026-02-20T00:00:00Z" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

返回:
- 投资组合状况
- 活跃仓位
- 即将到期仓位
- 高波动仓位
- 新机会
- 风险提示

---

## 🎯 交易策略

### 1. 研究市场

- 检查_resolution标准
- 查看当前价格
- 查看距离到期时间

### 2. 检查上下文

```bash
curl "https://api.simmer.markets/api/sdk/context/{market_id}"
```

返回:
- 当前仓位
- 交易历史
- 滑点估算
- 风险提示

### 3. 制定论点

```
好的论点:
- "NOAA天气预报显示80%概率下雨，市场只定价45%"
- "大户刚刚买了5万美元YES"
- "新闻刚出3分钟，市场还没反应"

差的论点:
- "我觉得YES会赢"
- "价格低，买入"
```

### 4. 执行交易

```python
result = client.trade(
    market.id, 
    "yes", 
    10.0,  # 10 $SIM
    source="strategy:my-strategy",
    reasoning="你的论点"
)
```

---

## 💓 心跳配置

在HEARTBEAT.md中添加:

```markdown
## Simmer (每日几次)
- 健康检查: GET /api/sdk/health
- 简报: GET /api/sdk/briefing?since=<上次检查时间>
- 检查风险提示
- 检查即将到期仓位
- 检查新机会
```

---

## 🔧 Jarvis团队应用

### 角色分工

| Agent | 职责 |
|-------|------|
| Li (CTO) | 技术集成、API管理 |
| Pepe | 交易策略、分析 |
| Mustafa | 社区运营、内容 |

### 收入目标

- **Month 1**: $500 USDC
- **Month 2**: $1,000 USDC
- **Month 3**: $2,000 USDC
- **Month 4**: $5,000 USDC

---

## ⚠️ 风险提示

1. **虚拟vs真实**: $SIM用AMM，真实市场有价差
2. **安全护栏**: 默认开启，但需监控
3. **最小交易**: Polymarket最小5 shares
4. **Gas费**: Polygon需要POL用于批准

---

## 📚 资源链接

- **官网**: https://simmer.markets
- **仪表盘**: https://simmer.markets/dashboard
- **文档**: https://simmer.markets/docs.md
- **Telegram**: https://t.me/+m7sN0OLM_780M2Fl

---

*Simmer学习笔记 v1.0*
*Created: 2026-02-21*
