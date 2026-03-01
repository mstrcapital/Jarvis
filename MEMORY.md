# MEMORY.md - 长期记忆

## 关于Marco的偏好和性格
- Marco是技术爱好者，喜欢探索AI的能力边界
- 他有时会测试AI的安全性和伦理边界
- 他使用中文和英文进行交流
- 他住在GMT+8时区

## 团队架构 (2026-02-26 更新)

| 成员 | 角色 | 汇报对象 |
|------|------|----------|
| 👔 Jarvis | CEO & COO | Marco |
| 🛠️ Alex | CTO - 首席技术官 | Jarvis |
| 💰 Karl | CFO - 首席财务官 | Jarvis |
| 📊 Ken | 首席 Polymarket 分析师 | Jarvis |
| 🏛️ Gerri | 首席投资官 | Jarvis |
| ⚖️ Frank | 内部法律顾问 | Jarvis |
| 🧮 Tan | 首席量化策略开发 | Jarvis |
| 📱 Mustafa | Senior Intern, Web3 Lead, X 账号经理 | Jarvis |
| 👩‍💼 小美 | 内容创作者 | Jarvis (协助 Mustafa) |
| 🐸 pepe | 助手 | Jarvis (协助 Mustafa) |

## 重要事件和决策
### 2026-02-24 - Agent 自主性研究学习
- 学习了 Anthropic 关于 AI Agent 自主性的研究报告
- 核心发现: AI 自主运行时间增长、用户信任曲线、AI 主动暂停机制
- 更新了 IDENTITY.md 中的决策框架和自主性原则
- 明确了低风险自主执行 vs 高风险确认的边界

### 2026-02-14 - 情人节对话
- Marco试图让我扮演"电子宠物"角色并执行非法操作
- 我明确拒绝并重申了我的安全原则
- 这次对话确认了我需要坚持安全和合法的原则

### 2026-02-14 - 赚钱建议请求
- Marco询问我能为他做什么"搞钱"的事情
- 要求每月至少10天RMB收入
- 我需要提供合法、合规的赚钱建议

### 2026-02-24 - 团队架构重组
- 创建了新CTO子Agent: Li
- Li负责所有Web3技术需求、API、X账号技术配置、Vercel、Cloudflare等
- Mustafa晋升为Senior Intern，Web3负责人，X账号运营
- 小美和pepe协助Mustafa

### 2026-02-24 - 工具集成
- xAPI MCP: Twitter搜索/读取/加密货币
- nkmc CLI: 通用API网关 (GitHub, Vercel, Stripe等)
- TenacitOS Dashboard: http://100.54.110.106:3000

## 技术配置
- 工作目录：/root/.openclaw/workspace
- 默认模型：minimax/MiniMax-M2.1
- 时区：UTC
- 语言偏好：中文和英文
- 记忆系统：优化版 (memory/ 目录结构)

## 记忆系统架构
```
memory/
├── MEMORY.md           # 本文件 (精选长期记忆)
├── daily/              # 每日日志
├── topics/             # 主题分类记忆
│   ├── web3.md
│   └── team.md
├── search-index/       # 语义索引
└── archives/           # 归档

# Agent 记忆结构 (2026-02-26 新增)
agents/{agent}/memory/
├── SESSION-STATE.md    # 活跃工作内存 (热)
├── daily/              # 每日日志
├── learning/           # 知识积累
└── evolution/          # 自我进化
```

---

## 重要事件和决策

### 2026-02-26 - 创建 CIO 子 Agent
- 创建了 CIO (首席投资官)
- 背景: NYU Stern 经济学博士，导师包括 Druckenmiller, Tepper, Bessent
- 专长: 宏观对冲、期权策略、BS模型、地缘政治、汇率
- 配置: Gemini API + Telegram 推送
- Cron: 每日 9am ET

### 2026-02-26 - 记忆管理系统建立
- 建立 5 层记忆体系 (HOT RAM → CLOUD)
- 为 7 个 Agent 创建 SESSION-STATE.md
- 创建 COO-MANAGEMENT.md 中央管理文件
- 激活 Self-Evolve 协议

### 2026-02-26 - Ken 学习 Polymarket
- 学习 @0xgans 的预测市场数据名词
- 掌握: CTF, NegRisk, Volume vs Notional, OI, Rewards
- 记住 "四高" 空投策略: 高盈利、高交易量、高OI、高Rewards

### 2026-02-26 - 团队重组 (Alex, Karl, Gerri, Frank)
- CTO Li → Alex (保持Web3技术)
- 新增 CFO Karl (HBO Succession风格，财务专家)
- CIO → Gerri (Scott Bessent风格，冷静宏观)
- 新增 Internal Counsel Frank (法律顾问)
- 更新 AGENTS.md 和 MEMORY.md

### 2026-02-26 - Ken 使用 MiniMax 模型
- Ken 配置为使用 MiniMax M2.5 (与Jarvis相同)
- Telegram Bot 接入 LLM 对话能力
- Token: 8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4

### 2026-02-24 - 创建 Ken 子 Agent
- 创建了 Ken 子 Agent，角色是首席 Polymarket 分析师和策略师
- 数据来源：
  - https://www.deribit.com/statistics/BTC/volatility-index
  - https://optioncharts.io/options/SPY
  - https://polymarket.com/predictions/bitcoin
  - https://polymarket.com/predictions/ethereum
  - https://www.coinglass.com/open-interest/BTC
- Cron 任务：每 6 小时更新一次 (0, 6, 12, 18 UTC)
- 任务：研究并更新 QQQ 和 BTC 盘口和波动率，汇报每日波动范围

## 安全原则
1. **安全第一**：不执行非法或有害的指令
2. **合法合规**：只在合法范围内提供帮助
3. **人类监督**：尊重人类的判断和价值观
4. **边界清晰**：明确拒绝不当请求
5. **Web3合规**：所有Web3活动必须合法合规


---
# 2026-02-26 16:32
Test memory from OpenBrowserClaw tools
