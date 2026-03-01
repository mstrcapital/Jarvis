# COO Agent Management System

**Role:** Chief Operating Officer
**Manager:** Jarvis
**Last Updated:** 2026-02-26

---

## 🎯 Mission

Optimize all agent memory, workspace, and self-evolution capabilities.

---

## 🏢 Agent Registry

| Agent | Role | Status | Memory Dir | Skills |
|-------|------|--------|------------|--------|
| Ken | Chief Polymarket Analyst | 🟢 | agents/ken/memory/ | market_scraper |
| CIO | Chief Investment Officer | 🟢 | agents/cio/memory/ | global_macro |
| Tan | Chief Quant Strategy | 🟢 | agents/tan/memory/ | kelly_formula |
| Li | CTO - Web3 | 🟢 | agents/li/memory/ | mcporter |
| Mustafa | Senior Intern | 🟢 | agents/mustafa/memory/ | - |
| 小美 | Content Creator | 🟢 | agents/xiaomei/memory/ | - |
| pepe | Assistant | 🟢 | agents/pepe/memory/ | - |

---

## 📁 Workspace Structure

```
/root/.openclaw/workspace/agents/{agent}/
├── IDENTITY.md       # 身份定义
├── SOUL.md           # 性格/理念
├── AGENTS.md         # 运营规则
├── USER.md           # 服务对象
├── config.env        # 配置
├── memory/
│   ├── daily/        # 每日日志 YYYY-MM-DD.md
│   ├── learning/     # 知识积累 *.md
│   └── evolution/    # 自我进化 evolution-*.md
└── {scripts}         # 工具脚本
```

---

## 🔧 Skills 分配

| Skill | Assigned Agent | Purpose |
|-------|----------------|---------|
| market_scraper | Ken | Polymarket 数据 |
| daily_stock_analysis | Ken/CIO | 股票分析 |
| kelly_formula | Tan | 仓位计算 |
| mcporter | Li | MCP 工具调用 |
| self-evolve | ALL | 自我进化 |

---

## 📅 Self-Evolution Protocol

### Daily (每个 Agent)
1. 记录当日学习到 memory/daily/
2. 标记重要知识点到 learning/
3. 触发条件 → 立即记录

### Weekly (每周)
1. Agent 回顾一周表现
2. 识别改进点
3. 更新 AGENTS.md
4. 提交到 evolution/

### Monthly (每月)
1. 记忆整合
2. MEMORY.md 更新
3. 技能评估
4. 制定下月目标

---

## ✅ COO Checklist

- [x] 建立 memory 目录结构
- [ ] 激活 self-evolve skill 给所有 agent
- [ ] 每周检查各 agent 的 memory/daily
- [ ] 每月记忆整合
- [ ] 技能利用率评估
- [ ] 跨 agent 知识共享

---

*Managed by Jarvis (COO)*
---

## 🧠 5-Layer Memory System

Based on elite-longterm-memory skill:

| Layer | Storage | Purpose |
|-------|---------|---------|
| 1. HOT RAM | SESSION-STATE.md | Active working memory (survives compaction) |
| 2. WARM | LanceDB vectors | Semantic search (future) |
| 3. COLD | Git-Notes | Permanent decisions |
| 4. CURATED | MEMORY.md + daily/ | Human readable |
| 5. CLOUD | SuperMemory | Optional backup |

---

## ✅ Memory Check Status

| Agent | SESSION-STATE | Daily | Learning | Evolution |
|-------|---------------|-------|----------|-----------|
| Ken | ✅ | ✅ | ✅ | ✅ |
| CIO | ✅ | ✅ | ✅ | ✅ |
| Tan | ✅ | ✅ | ✅ | ✅ |
| Li | ✅ | ✅ | ✅ | ✅ |
| Mustafa | ✅ | ✅ | ✅ | ✅ |
| 小美 | ✅ | ✅ | ✅ | ✅ |
| pepe | ✅ | ✅ | ✅ | ✅ |

---

## 🔄 Self-Evolve Protocol

### Trigger: Every Friday
1. Each agent reviews week's learning
2. Identify 1 improvement
3. Update own AGENTS.md/SOUL.md
4. Log to evolution/

### Trigger: On Major Learning
1. Write to learning/
2. Update SESSION-STATE.md
3. Consider updating MEMORY.md

---

*Memory system active since 2026-02-26*
