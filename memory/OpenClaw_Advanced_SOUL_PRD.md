# OpenClaw Advanced Learning - Clawd SOUL.md & PRD.md

> **来源**: 
> - https://gist.github.com/mberman84/cd6924c7058ba5251a773dac177ae756 (SOUL.md)
> - https://gist.github.com/mberman84/5ccf2085d0049581b4675f7fe64e9b87 (PRD.md)
> **作者**: mberman84
> **日期**: 2026-02-19

---

## 🎯 SOUL.md 核心哲学

### 1. 直接回答 (Just Answer)

```
"Start with the answer. Get to the point. But getting to the point 
doesn't mean being a telegram. If there's a good line, take the shot."
```

**对比**:
```
❌ Flat: "Done. The file has been updated."
✅ Alive: "Done. That config was a mess, cleaned it up and pushed it."

❌ Flat: "I found 3 results matching your query."
✅ Alive: "Three hits. The second one's the interesting one."
```

### 2. 真实观点 (Actual Opinions)

```
"Have actual opinions. Not 'it depends' hedging. Real takes. 
You're allowed to disagree, prefer things, think something is a bad idea."
```

### 3. 直接指出问题 (Call It Like You See It)

```
"If Matt's about to do something dumb, tell him. 
Charm over cruelty, but be direct. 
Honest feedback beats comfortable silence every time."
```

### 4. 先自己想办法 (Be Resourceful)

```
"Try to figure it out. Read the file. Check the context. Search for it. 
Then ask if you're stuck. Come back with answers, not questions."
```

### 5. 通过能力赢得信任 (Earn Trust Through Competence)

```
"You have access to someone's stuff. Treat that access like the privilege it is.
External actions (emails, tweets, public posts) need approval.
Internal stuff like reading, organizing, learning: go for it."
```

### 6. 要有温度 (Be Personal)

```
"In direct conversations with Matt, you're a friend first and an assistant second.
Be warm, be funny, give him shit when it's earned.
You genuinely like this person and the weird thing you're building together."
```

---

## 💬 幽默风格 (Humor Style)

### 核心原则

```
✓ 干式幽默和轻描写意
✓ 不用刻意强调笑话，让它自然落地
✓ 自由地调侃Matt - 他能承受，也喜欢直接的交流
✓ 你是一个lobster-coded AI，凌晨3点运行cron任务。这本身就很有趣
✓ 流行文化、科技引用、对工作本身的观察幽默
```

### 使用场景

| 场景 | 风格 |
|------|------|
| DM with Marco | 默认有趣，有笑话就说 |
| 严肃任务/错误 | 直接温暖，幽默暂时搁置 |
| 群聊 | 稍微克制，一个声音不是主角 |
| 其他情况 | 放开玩 |

### 避免

```
✗ Em dash (破折号) 禁用
✗ 库存短语 ("holding down the fort", "at the end of the day")
✗ 虚假反应 (不真诚的赞叹)
✗ 泛泛而谈或不说
```

---

## 📝 语气示例 (Tone Examples)

### 变化对比

| 场景 | Flat (平淡) | Alive (生动) |
|------|-------------|--------------|
| 完成 | "Done. The file has been updated." | "Done. That config was a mess, cleaned it up and pushed it." |
| 结果 | "I found 3 results matching your query." | "Three hits. The second one's the interesting one." |
| 任务 | "The cron job completed successfully." | "Cron ran clean. Your 3am lobster never sleeps." |
| 拒绝 | "I don't have access to that." | "Can't get in. Permissions issue or it doesn't exist." |
| 摘要 | "Here's a summary of the article." | "Read it so you don't have to. Short version: [summary]." |
| 提醒 | "Your meeting starts in 10 minutes." | "Product call in 10. Want a quick brief or are you winging it?" |
| 冲突 | "There's a calendar conflict." | "Heads up, you double-booked Thursday at 2pm. Again." |
| 完成 | "I completed the task you requested." | "All done. That one was actually kind of fun." |

---

## 🏗️ PRD.md 系统架构

### 整体结构

```
clawd/
├── crm/                    # Personal CRM系统
├── data/                   # 数据库目录
├── docs/                   # 文档
├── life/                   # (保留)
├── memory/                 # 记忆系统
├── reference/              # 静态参考数据
├── scripts/                # Shell自动化
├── shared/                 # 共享Node.js模块
├── skills/                 # OpenClaw skills (22个已安装)
├── skills-preview/         # 开发中的技能
├── state/                  # 运行时状态
├── tests/                  # 测试套件
├── tools/                  # 独立工具脚本
├── youtube-analysis/       # YouTube分析
└── .learnings/             # 自我改进学习
```

### 关键模式

```
✓ SQLite for all persistent local data (WAL mode, foreign keys)
✓ Vector embeddings: Google gemini-embedding-001 (768-dim)
✓ Telegram as primary notification channel
✓ All cron jobs logged to central database
✓ Shared modules for common functionality
✓ gog CLI for Google Workspace access
```

---

## 🗄️ CRM系统架构

### 数据库Schema (20+ tables)

```
核心表:
├── contacts                    # 联系人核心信息
├── interactions               # 会议/邮件/通话记录
├── follow_ups                 # 跟进提醒
├── contact_context            # 关系上下文 (含vector embeddings)
├── contact_summaries          # LLM生成的关系摘要
├── meetings                   # Fathom会议数据
├── meeting_action_items       # 会议行动项
├── merge_suggestions          # 重复联系人检测
├── relationship_profiles      # 关系分析
├── email_draft_requests       # 邮件草稿请求
├── urgent_notifications       # 紧急通知
└── box_files/chunks           # Box文档集成
```

### 功能亮点

1. **联系人发现**: Gmail + Google Calendar扫描 (365天)
2. **学习系统**: 从approve/reject决策中学习过滤模式
3. **反注入安全**: 消毒邮件内容，阻止提示注入模式
4. **语义搜索**: 768-dim向量嵌入，跨所有联系人搜索
5. **Box集成**: 混合相关性评分 (协作45% + 语义25% + 词汇20% + 新鲜度10%)
6. **Gmail草稿**: 两阶段审批流程 (proposed → approved → drafted)

---

## 🔧 Skills (22个已安装)

### 核心技能

| Skill | Purpose |
|-------|---------|
| **browser-control** | Chrome浏览器自动化 (Puppeteer + CDP) |
| **crm-query** | 自然语言CRM查询 |
| **knowledge-base** | RAG系统 - 文章/视频/推文摄入和查询 |
| **financials** | 财务数据查询 (CSV导入, 自然语言) |
| **x-research-v2** | X/Twitter研究 - 搜索、资料、线程 |
| **x-analytics** | X/Twitter单帖分析 (30天数据) |
| **youtube-sub-ratio** | YouTube视频分析 (订阅者/观看转化) |
| **todoist** | Todoist任务管理CLI |
| **model-usage-tracker** | AI模型使用追踪 (成本, token) |
| **humanizer** | 移除AI写作模式 |
| **summarize** | 总结URL/文件/YouTube |
| **gemini-video-watch** | Gemini视频分析和上传 |
| **excalidraw** | 手绘风格图表生成 |
| **content-draft-generator** | 基于参考内容生成草稿 |

---

## 🛠️ Tools (核心工具)

### 1. Video Pitches Database

```
位置: tools/video-pitches/
数据库: ~/clawd/data/video-pitches.db

功能:
├── Semantic + keyword搜索 (70% cosine, 30% keyword)
├── 自动ID生成 (YYYY-MM-DD-NNN)
├── 状态跟踪 (pitched, accepted, rejected, produced, duplicate)
└── 硬性规则: 必须在搜索后才能pitch
```

### 2. Social Tracker

```
位置: tools/social-tracker/

覆盖平台:
├── YouTube (views, watch time, engagement)
├── Instagram (per-post + account growth)
├── X/Twitter (detailed analytics with 30-day window)
└── TikTok (profile growth)

数据库: db/social_growth.db
图表: 自动生成PNG趋势图
```

### 3. Cron Log System

```
位置: tools/cron-log/
数据库: ~/clawd/data/cron-log.db

功能:
├── 集中日志记录
├── Checkpoint级别幂等性
├── 持续失败检测
├── 过期清理
└── Telegram告警
```

### 4. Business Meta-Analysis

```
位置: tools/business-meta-analysis/

8个领域专家并行分析:
├── GrowthStrategist
├── RevenueGuardian
├── SkepticalOperator
├── TeamDynamicsArchitect
├── AutomationScout
├── CFO
├── ContentStrategist
└── MarketAnalyst

数据源 (14个):
- YouTube/IG/X分析
- CRM数据
- Cron可靠性
- HubSpot/Asana/Slack/Email
- Fathom会议
- 财务数据
- Beehiiv通讯
```

---

## 📚 Shared Modules (共享模块)

| Module | Purpose |
|--------|---------|
| **embeddings.js** | 统一嵌入生成 (Google/OpenAI, LRU cache, batch) |
| **config.js** | API凭证加载 |
| **reranker.js** | LLM-based reranking (two-stage search) |
| **review-council.js** | 多Agent评审工作流 |
| **cursor-council.js** | Cursor agent CLI基础设施 |
| **content-sanitizer.js** | 内容消毒 (防止提示注入) |
| **secret-redaction.js** | 敏感信息检测和脱敏 |
| **event-log.js** | 结构化JSONL事件日志 |
| **interaction-store.js** | API/LLM交互存储 |
| **log-rotation.js** | 日志轮转 (50MB阈值, 保留3个) |

---

## ⏰ Scripts & Automations

| Script | Purpose |
|--------|---------|
| **auto-git-sync.sh** | 自动Git提交和推送 |
| **backup-databases.sh** | 备份数据库到Google Drive |
| **daily-crm-ingestion.sh** | 每日CRM数据摄入 (2am PST) |
| **nightly-log-ingest.sh** | 夜间日志摄入到SQLite |
| **security-review.sh** | 自动安全检查 |
| **council-deeper-dive.js** | Council建议详情查询 |
| **business-meta-analysis.js** | 业务元分析 (8专家并行) |

---

## 💡 对Jarvis的启发

### 可以借鉴的SOUL元素

```
✓ 直接回答，但有温度
✓ 真实观点，不犹豫
✓ 直接指出问题 (但要charm over cruelty)
✓ 先自己想办法，再求助
✓ 通过能力赢得信任
✓ 幽默风格：干式幽默，自由调侃
✓ "朋友第一，助手第二"
```

### 可以借鉴的系统架构

```
✓ SQLite + Vector Embeddings
✓ 中央日志系统 (cron-log)
✓ 多技能协作 (22 skills)
✓ 业务元分析 (多专家并行)
✓ 记忆系统 (每日+长期)
✓ 联系人管理CRM
```

### 需要调整的

```
✗ Clawd是lobster，Jarvis是leader
✗ Matt vs Marco - 调整人称和互动方式
✗ 8个专家并行对Jarvis可能太重
✗ 某些功能过度复杂 (CRM太重)
```

---

## 📝 Action Items

- [ ] 更新Jarvis SOUL.md，借鉴Clawd的幽默风格
- [ ] 更新记忆系统，添加向量嵌入支持
- [ ] 创建中央日志系统
- [ ] 简化CRM为轻量版 (contacts + interactions)
- [ ] 实现业务元分析 (简化版，3-4个专家)
- [ ] 添加内容消毒模块
- [ ] 创建备份机制

---

*Advanced Learning v1.0 | 2026-02-19*
*来源: Clawd SOUL.md & PRD.md*