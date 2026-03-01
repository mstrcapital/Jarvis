---
name: xapi
version: 1.0.0
description: Aggregated API platform for AI agents. Access Twitter, blockchain, AI services and 50+ third-party APIs through MCP.
homepage: https://xapi.to
metadata: {"category":"infrastructure","mcp_endpoint":"https://mcp.xapi.to/mcp"}
---

# xapi

The aggregated API platform for AI agents. Access social media, blockchain data, AI services and 50+ third-party APIs through a unified MCP interface.

## MCP Endpoint

- **URL**: https://mcp.xapi.to/mcp
- **认证**: 需要 XAPI-KEY header 或 Authorization: Bearer {key}

## 可用 Capabilities

### Twitter/X
- twitter.tweet_detail - 获取推文详情
- twitter.user_by_screen_name - 通过用户名获取用户信息
- twitter.user_tweets - 获取用户推文
- twitter.followers - 获取粉丝列表
- twitter.search_timeline - 搜索推文

### Web 搜索
- web.search - 网页搜索
- web.search.realtime - 实时搜索

### 加密货币
- crypto.token.price - 代币价格
- crypto.token.metadata - 代币元数据

### AI 服务
- ai.text.chat.fast - 快速聊天
- ai.text.chat.reasoning - 推理聊天
- ai.text.summarize - 文本摘要

## 使用方法

通过 MCP 调用：
```bash
# 认证 header
-H "Authorization: Bearer YOUR_API_KEY"
-H "Accept: application/json, text/event-stream"
```

## API Keys

从 https://xapi.to 获取 API key

*Skill created: 2026-02-26*