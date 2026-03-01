---
name: nkmc
version: 1.0.0
description: Open Agent API Gateway - 让 AI Agent 用 Unix 命令调用任何互联网 API
homepage: https://nkmc.ai
metadata: {"category":"api-gateway","supports":["ls","cat","grep","write","rm","pipe"]}
read_when:
  - 需要让 AI agent 调用外部 API
  - 统一管理多个 API 服务
  - 区块链数据查询
---

# nkmc - Agent API Gateway

> Open agent API gateway. 让 AI Agent 用 6 个 Unix 命令调用任何互联网 API。

## 安装

```bash
npm install -g @nkmc/cli
# 或
npx @nkmc/cli <command>
```

## 认证

```bash
nkmc auth
# 获取 JWT token (24小时有效)
```

## 6 个核心命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `ls <path>` | 列出服务/目录 | `nkmc ls /` |
| `cat <path>` | 读取文件/调用 GET | `nkmc cat /api.github.com/skill.md` |
| `grep <pattern>` | 搜索服务/内容 | `nkmc grep "weather" /` |
| `write <path> <data>` | POST 数据 | `nkmc write /discord.com/channels/123/messages '{"content":"Hi"}'` |
| `rm <path>` | 删除资源 | `nkmc rm /api.cloudflare.com/zones/...` |
| `pipe` | 链式调用 | `nkmc pipe 'cat /a | write /b'` |

## 典型工作流

```bash
# 1. 认证 (一次)
nkmc auth

# 2. 发现服务
nkmc ls /

# 3. 搜索
nkmc grep "weather" /

# 4. 查看服务 API
nkmc cat /api.weather.gov/skill.md

# 5. 调用
nkmc cat /api.weather.gov/points/39.99,-75.16.json
```

## 区块链支持

```bash
# 搜索区块链服务
nkmc grep "blockchain" /

# 浏览以太坊
nkmc ls /rpc.ankr.com/
# blocks/  balances/  transactions/  receipts/  logs/

# 查看区块
nkmc cat /rpc.ankr.com/blocks/21000000.json

# 查询余额
nkmc cat /rpc.ankr.com/balances/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045.json
```

## 可用服务

- **api.github.com** - GitHub API
- **api.weather.gov** - 美国天气 API
- **api.cloudflare.com** - Cloudflare API
- **discord.com** - Discord API
- **rpc.ankr.com** - Ethereum JSON-RPC
- **mainnet.base.org** - Base Chain
- **arb1.arbitrum.io** - Arbitrum

---

*Skill source: https://nkmc.ai/agent.md*
*Created: 2026-02-27*