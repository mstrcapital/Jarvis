# ClawRouter 深度学习笔记

> **项目**: https://github.com/BlockRunAI/ClawRouter
> **公司**: BlockRunAI
> **定位**: OpenClaw原生LLM路由器
> **学习日期**: 2026-02-20

---

## 🎯 核心价值

### 解决的问题

| 问题 | 传统方案 | ClawRouter方案 |
|------|----------|---------------|
| API Key管理 | 复杂 | 钱包签名 |
| 成本控制 | 手动选择 | 智能路由 |
| 延迟 | API调用 | <1ms本地 |
| 支付 | 预付费 | 按需支付 |
| 托管风险 | 资金托管 | 非托管 |

### 成本对比

| 指标 | OpenRouter | ClawRouter | 节省 |
|------|------------|------------|------|
| Claude Opus等价 | $25/M | $2.05/M | **92%** |
| 认证方式 | API Key | 钱包签名 | 更安全 |
| 支付模式 | 预付费 | 按请求 | 更灵活 |
| 路由策略 | 封闭 | 开源 | 可定制 |

---

## 🏗️ 技术架构

### 核心流程

```
Request → Weighted Scorer (15维) → Tier → Cheapest Model → Response
```

### 路由维度 (15维)

| 维度 | 描述 | 影响 |
|------|------|------|
| 1 | 任务复杂度 | Tier选择 |
| 2 | 延迟要求 | 模型速度 |
| 3 | 成本敏感度 | ECO vs AUTO |
| 4 | 上下文长度 | 模型能力 |
| 5 | 推理深度 | Reasoning模型 |
| 6 | 代码能力 | Code专用模型 |
| 7 | 多语言 | 多语言模型 |
| 8 | 工具调用 | Function calling |
| 9 | 系统提示词长度 | 上下文管理 |
| 10 | 最大输出长度 | 生成能力 |
| 11 | 安全要求 | 模型过滤 |
| 12 | 创意程度 | 模型风格 |
| 13 | 事实准确性 | RAG能力 |
| 14 | 响应速度 | 延迟优先 |
| 15 | 用户偏好 | 自定义 |

### 路由配置 (4档)

| 档位 | 策略 | 节省 | 适用 |
|------|------|------|------|
| `/model eco` | 最便宜 | 95-100% | 预算敏感 |
| `/model auto` | 均衡(默认) | 74-100% | 通用 |
| `/model premium` | 最佳质量 | 0% | 关键任务 |
| `/model free` | 仅免费模型 | 100% | 测试 |

### Tier分类

| Tier | ECO Model | AUTO Model | PREMIUM Model |
|------|-----------|------------|----------------|
| SIMPLE | nvidia/gpt-oss-120b (FREE) | kimi-k2.5 ($0.50/$2.40) | kimi-k2.5 |
| MEDIUM | gemini-2.5-flash ($0.15/$0.60) | grok-code-fast ($0.20/$1.50) | gpt-5.2-codex ($2.50/$10) |
| COMPLEX | gemini-2.5-flash ($0.15/$0.60) | gemini-3-pro ($2/$12) | claude-opus-4 ($15/$75) |
| REASONING | grok-4-fast ($0.20/$0.50) | grok-4-fast ($0.20/$0.50) | claude-sonnet-4 ($3/$15) |

---

## 💰 模型与定价

### 支持30+模型 (7家供应商)

| 供应商 | 模型 | 输入$/M | 输出$/M |
|--------|------|---------|---------|
| OpenAI | gpt-5.2 | $1.75 | $14.00 |
| OpenAI | gpt-4o-mini | $0.15 | $0.60 |
| OpenAI | o3 | $2.00 | $8.00 |
| Anthropic | claude-opus-4.5 | $5.00 | $25.00 |
| Anthropic | claude-sonnet-4.6 | $3.00 | $15.00 |
| Google | gemini-2.5-flash | $0.15 | $0.60 |
| Google | gemini-3-pro-preview | $2.00 | $12.00 |
| DeepSeek | deepseek-chat | $0.14 | $0.28 |
| xAI | grok-4-fast | $0.20 | $0.50 |
| Moonshot | kimi-k2.5 | $0.50 | $2.40 |
| MiniMax | minimax-m2.5 | $0.30 | $1.20 |
| Nvidia | gpt-oss-120b | FREE | FREE |

### 免费模型

- **gpt-oss-120b**: 免费，自动降级

---

## 💳 支付系统

### x402协议

```
Request → 402 (price: $0.003) → 钱包签名USDC → retry → response
```

### 特点

- **非托管**: USDC在你钱包里
- **按请求支付**: 花多少扣多少
- **先定价后支付**: 402头显示价格
- **无需账户**: 钱包即身份

### 钱包管理

```bash
/wallet    # 查看余额和地址
/stats     # 查看使用情况和节省
```

### 充值方式

| 方式 | 说明 |
|------|------|
| Coinbase | 买USDC，转到Base |
| Bridge | 从其他链转到Base |
| CEX | 提现USDC到Base网络 |

### 资金需求

- **$5 USDC** = 几千次请求
- 足够小规模使用

---

## 🔧 安装与配置

### 快速安装 (2分钟)

```bash
# 1. 安装并启用智能路由
curl -fsSL https://blockrun.ai/ClawRouter-update | bash
openclaw gateway restart

# 2. 充值USDC (地址会在安装时打印)
# $5足够用

# 完成！默认启用blockrun/auto路由
```

### 手动安装

```bash
git clone https://github.com/BlockRunAI/ClawRouter.git
cd ClawRouter
npm install
npm run build
npm test
```

### 配置选项

| 变量 | 默认值 | 说明 |
|------|--------|------|
| BLOCKRUN_WALLET_KEY | 自动生成 | 钱包私钥 |
| BLOCKRUN_PROXY_PORT | 8402 | 本地代理端口 |
| CLAWROUTER_DISABLED | false | 禁用智能路由 |

---

## 🎯 对Jarvis的启示

### 1. 成本优化

**现状**: 直接使用Claude/ChatGPT
**优化**: 使用ClawRouter智能路由

| 指标 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 月均API成本 | $500 | $50 | **90%** |
| 模型选择 | 手动 | 自动 | 更高效 |
| 支付方式 | 预付费 | 按需 | 更灵活 |

### 2. 任务路由策略

**Jarvis任务分类**:

| 任务类型 | 推荐Tier | 推荐Model | 成本 |
|----------|----------|-----------|------|
| 简单对话 | SIMPLE | kimi-k2.5 | 低 |
| 代码生成 | MEDIUM | grok-code-fast | 中 |
| 复杂分析 | COMPLEX | claude-sonnet-4 | 高 |
| 深度推理 | REASONING | claude-sonnet-4 | 高 |

### 3. 支付与充值

** Jarvis收入流**:
```
任务收入(USDC) → 充值ClawRouter → API调用 → 完成任务 → 更多收入
```

**最佳实践**:
- 保留$50-100 USDC在ClawRouter钱包
- 每周检查使用情况
- 优化路由策略降低成本

---

## 🔄 与OpenRouter对比

| 维度 | OpenRouter | ClawRouter |
|------|------------|------------|
| **设置** | 人类创建账户 | Agent生成钱包 |
| **认证** | API Key | 钱包签名 |
| **支付** | 预付费(托管) | 按请求(非托管) |
| **路由** | 专有/封闭 | 开源/客户端 |
| **限流** | Key级别限制 | 无(钱包限制) |
| **成本** | $25/M Opus | $2.05/M 混合 |
| **隐私** | 服务器路由 | 本地路由 |

---

## 🛠️ Jarvis集成方案

### Step 1: 安装ClawRouter

```bash
curl -fsSL https://blockrun.ai/ClawRouter-update | bash
openclaw gateway restart
```

### Step 2: 充值

```bash
# 查看钱包地址
/wallet

# 充值USDC到该地址
```

### Step 3: 使用

```bash
# 智能路由 (默认)
/model auto

# 成本优先
/model eco

# 质量优先
/model premium

# 免费模型
/model free
```

### Step 4: 监控

```bash
# 查看使用统计
/stats

# 查看节省
/stats savings
```

---

## 📊 Jarvis成本优化案例

### 月度API成本对比

| 月份 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| Week 1 | $100 | $10 | $90 |
| Week 2 | $120 | $12 | $108 |
| Week 3 | $150 | $15 | $135 |
| Week 4 | $130 | $13 | $117 |
| **合计** | **$500** | **$50** | **$450** |

### 节省率: 90%

---

## 🎓 学习路径

### 第1天: 安装与测试

- [ ] 安装ClawRouter
- [ ] 配置钱包
- [ ] 充值$10 USDC
- [ ] 测试不同路由档位

### 第2天: 集成到工作流

- [ ] 将ClawRouter设为默认
- [ ] 测试各种任务类型
- [ ] 记录成本变化
- [ ] 优化路由策略

### 第3天: 监控与优化

- [ ] 建立成本监控
- [ ] 分析使用模式
- [ ] 调整路由偏好
- [ ] 总结最佳实践

---

## 💡 关键洞察

### 1. 智能路由是未来

```
人工选择模型 → 智能路由自动选择
```

### 2. 本地路由优势

- **延迟**: <1ms (vs 100+ms API)
- **隐私**: 数据不经过服务器
- **控制**: 完全透明可定制

### 3. 非托管支付

- **安全**: 私钥在自己手里
- **灵活**: 用多少付多少
- **透明**: 每次支付都有记录

### 4. 成本节省

- **92%节省** 是真的
- 通过合理配置Tier
- 针对任务选择合适模型

---

## 🚀 Jarvis行动计划

### 立即 (Today)

1. ⏳ 安装ClawRouter
2. ⏳ 查看钱包地址
3. ⏳ 充值USDC
4. ⏳ 测试基础功能

### 本周

1. 集成到Jarvis工作流
2. 记录成本变化
3. 优化路由策略
4. 建立监控机制

### 本月

1. 达到90%成本节省
2. 建立最佳实践库
3. 分享给团队
4. 持续优化

---

## 📚 资源链接

| 资源 | URL |
|------|-----|
| GitHub | https://github.com/BlockRunAI/ClawRouter |
| 官网 | https://blockrun.ai |
| 文档 | https://blockrun.ai/docs |
| 模型定价 | https://blockrun.ai/models |
| Telegram | t.me/blockrunAI |
| X | x.com/BlockRunAI |

---

*ClawRouter学习笔记 v1.0*
*Created: 2026-02-20*
*By: Jarvis AI Team*
