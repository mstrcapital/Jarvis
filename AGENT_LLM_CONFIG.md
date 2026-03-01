# Agent LLM Configuration Manager
# Managed by Jarvis (COO)

# ============================================
# MODEL RECOMMENDATIONS BY AGENT ROLE
# ============================================

"""
| Agent | Role | Recommended Model | Rationale |
|-------|------|-------------------|-----------|
| Ken | Polymarket Analyst | gemini-2.0-flash | Fast, free, good for data |
| CIO | Investment Officer | gemini-2.0-flash | Broad knowledge, free |
| Tan | Quant Strategy | gpt-4o-mini | Better math, cost-effective |
| Li | CTO (Web3) | gpt-4o-mini | Technical decisions |
| Mustafa | X Manager | gemini-2.0-flash | Fast, multilingual |
| 小美 | Content Creator | gpt-4o | Better content quality |
| pepe | Assistant | gemini-2.0-flash | Fast, free |
"""

# Current Active Configurations
# ==============================

# Ken - Polymarket Analyst
# Model: Gemini (free tier)
# Status: ✅ Configured
KEN_MODEL=gemini-2.0-flash
KEN_API_KEY=AIzaSyCg0_2wh1bXG-uR-v2K0TADUvHDlKfnbks

# CIO - Chief Investment Officer  
# Model: Gemini (free tier)
# Status: ✅ Configured
CIO_MODEL=gemini-2.0-flash
CIO_API_KEY=AIzaSyCg0_2wh1bXG-uR-v2K0TADUvHDlKfnbks

# Tan - Quant Strategy (needs better math)
# Model: Recommendation - gpt-4o-mini
# Status: ⚠️ Not configured
# TAN_MODEL=gpt-4o-mini
# TAN_API_KEY=<to be configured>

# Li - CTO Web3
# Model: Recommendation - gpt-4o-mini (technical)
# Status: ⚠️ Not configured
# LI_MODEL=gpt-4o-mini
# LI_API_KEY=<to be configured>

# Mustafa - X Account Manager
# Model: Gemini (fast, good for multilingual)
# Status: ⚠️ Not configured
# MUSTAFA_MODEL=gemini-2.0-flash
# MUSTAFA_API_KEY=AIzaSyCg0_2wh1bXG-uR-v2K0TADUvHDlKfnbks (shared)

# 小美 - Content Creator
# Model: Recommendation - gpt-4o (better content)
# Status: ⚠️ Not configured
# XIAOMEI_MODEL=gpt-4o
# XIAOMEI_API_KEY=<to be configured>

# pepe - Assistant
# Model: Gemini (fast, free)
# Status: ⚠️ Not configured
# PEPE_MODEL=gemini-2.0-flash
# PEPE_API_KEY=AIzaSyCg0_2wh1bXG-uR-v2K0TADUvHDlKfnbks (shared)

# ============================================
# MODEL POOL (Available APIs)
# ============================================

# Gemini (Free - recommended for most agents)
# - Fast, multilingual, good reasoning
# - Rate limit: 15 RPM

# OpenAI GPT-4 (Paid - for complex tasks)
# - Better math/code, higher quality
# - Cost: ~$3-15/1M tokens

# DeepSeek (Alternative cheap)
# - Cost-effective, good for analysis

# Anthropic Claude (Creative writing)
# - Best for content creation

# ============================================
# COST OPTIMIZATION
# ============================================

"""
Free Tier (Gemini):
- Ken: Daily reports (3x)
- CIO: Daily reports (2x)
- pepe: General assistance

Paid Tier (GPT-4):
- Tan: Quant calculations (occasional)
- 小美: Content generation (occasional)
- Li: Technical decisions (occasional)
"""
---

## 🌐 网络爬取优化 (Alex负责)

### 现有工具

| 工具 | 用途 | X访问 |
|------|------|-------|
| Camofox | 反检测浏览器 | 需手动 |
| Playwright | 自动化 | 需配置 |
| curl_cffi | HTTP客户端 | ✅ 通用 |
| web_fetch | 简单抓取 | ❌ 被阻 |

### Alex爬虫策略

1. **curl_cffi** - 基础HTTP,模拟Chrome
2. **nitter** - Twitter镜像(部分失效)
3. **fxtwitter** - Twitter嵌入
4. **jina.ai** - AI Reader (最稳定)

### 需要的改进

- [ ] X 认证 Cookie
- [ ] 代理池
- [ ] 更强的反检测
- [ ] 官方 API 申请
