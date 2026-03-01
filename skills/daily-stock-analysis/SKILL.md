---
name: daily-stock-analysis
version: 1.0.0
description: A股智能分析系统 - AI 驱动的每日股票分析工具，支持多数据源、多渠道推送、GitHub Actions 或 Docker 部署
homepage: https://github.com/ZhuLinsen/daily_stock_analysis
metadata: {"category":"finance","supports":["stock-analysis","ai-analysis","auto-report"]}
read_when:
  - 需要分析 A股/美股市场
  - 设置每日股票报告
  - 配置股票推送通知
  - 使用 AI 分析股票
---

# daily-stock-analysis - A股智能分析系统

> AI 驱动的每日股票分析工具，支持多数据源、多渠道推送

## 项目概述

| 功能 | 说明 |
|------|------|
| **AI 分析** | 使用 Gemini/OpenAI/Claude 分析股票 |
| **多数据源** | Tushare, 博查, Tavily, Brave Search |
| **多渠道推送** | 微信, 飞书, Telegram, Discord, Email |
| **定时任务** | GitHub Actions 或 Docker 本地运行 |

## 快速开始

### 1. GitHub Actions 部署 (推荐)

```bash
# Fork 仓库
https://github.com/ZhuLinsen/daily_stock_analysis

# 配置 Secrets
# Settings → Secrets and variables → Actions → New repository secret
```

### 2. 必需配置

| Secret | 说明 |
|--------|------|
| `STOCK_LIST` | 自选股代码，如 `600519,300750,002594` |
| `GEMINI_API_KEY` 或 `OPENAI_API_KEY` | AI 模型 API |
| `TAVILY_API_KEYS` | 搜索 API (推荐) |

### 3. 通知渠道 (至少配置一个)

| 渠道 | Secret |
|------|--------|
| 企业微信 | `WECHAT_WEBHOOK_URL` |
| 飞书 | `FEISHU_WEBHOOK_URL` |
| Telegram | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` |
| Discord | `DISCORD_WEBHOOK_URL` |
| Email | `EMAIL_SENDER` + `EMAIL_PASSWORD` + `EMAIL_RECEIVERS` |

## 配置示例

### 最小配置 (4项)

```bash
# 1. AI 模型 (选其一)
GEMINI_API_KEY=your_gemini_key
# 或
OPENAI_API_KEY=your_openai_key

# 2. 股票列表 (必填)
STOCK_LIST=600519,300750,002594

# 3. 通知渠道 (选其一)
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx

# 4. 搜索 API (推荐)
TAVILY_API_KEYS=your_tavily_key
```

### 完整通知配置

```bash
# Telegram
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx

# 飞书
FEISHU_WEBHOOK_URL=xxx

# 企业微信
WECHAT_WEBHOOK_URL=xxx

# Discord
DISCORD_WEBHOOK_URL=xxx

# Email
EMAIL_SENDER=xxx@qq.com
EMAIL_PASSWORD=xxx
EMAIL_RECEIVERS=xxx@example.com
```

## 本地运行

### Docker 部署

```bash
# 克隆仓库
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动
docker-compose up -d
```

### 本地 Python 运行

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export STOCK_LIST="600519,300750"
export GEMINI_API_KEY="xxx"
export TELEGRAM_BOT_TOKEN="xxx"
export TELEGRAM_CHAT_ID="xxx"

# 运行
python main.py
```

## 高级功能

### 推送模式

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SINGLE_STOCK_NOTIFY` | 单股立即推送 | false |
| `REPORT_TYPE` | simple/full | full |
| `REPORT_SUMMARY_ONLY` | 仅摘要 | false |

### 数据源

| 数据源 | 用途 |
|--------|------|
| Tushare | A股行情数据 |
| Tavily | 新闻搜索 |
| 博查 | 中文搜索 |
| Brave Search | 美股搜索 |

### 回测功能

支持历史数据分析，回测策略效果。

---

## 使用场景

1. **每日盘后分析** - 自动分析自选股并推送
2. **实时监控** - 个股异动提醒
3. **投资组合管理** - 多股分析对比

---

## 相关文件

- 项目: `/root/.openclaw/workspace/daily_stock_analysis/`
- 配置: `.env` 文件
- Docker: `docker/docker-compose.yml`

---

*Skill source: https://github.com/ZhuLinsen/daily_stock_analysis*
*Created: 2026-02-27*