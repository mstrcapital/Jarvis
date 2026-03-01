# xAPI 配置 (Alex CTO 负责)

## 账户状态

| 项目 | 值 |
|------|-----|
| **Twitter 绑定** | ✅ @marcostrategy |
| **账户类型** | ENTITY |
| **积分** | 100 (绑定奖励) |

## API Keys (已注册)

| 名称 | Key Preview |
|------|-------------|
| Jarvis | sk-09af****f042 |
| Mustafa | sk-f399****de56 |
| Default | sk-13f1****1a53 |

## MCP 端点

- **URL**: https://mcp.xapi.to/mcp
- **认证**: 需要 XAPI-KEY header

## 已测试功能

| 功能 | 状态 |
|------|------|
| tools/list | ✅ 可用 |
| CAPABILITY_GET | ✅ 可用 |
| CAPABILITY_CALL | ❌ 401 错误 |

## 可用 Capabilities (只读)

- twitter.tweet_detail
- twitter.user_by_screen_name
- twitter.user_tweets
- twitter.followers
- twitter.search_timeline
- web.search
- crypto.token.price
- ai.text.chat.fast
- ai.text.summarize
- 等18个

## 待解决

- CAPABILITY_CALL 需要正确的认证方式
- 可能需要联系 xAPI 客服

---

*更新: 2026-02-26*
*负责人: Alex (CTO)*