# OpenBrowserClaw vs Jarvis 架构对比

## 1. 运行时架构

| 方面 | OpenBrowserClaw | Jarvis (我们) |
|------|-----------------|---------------|
| **运行时** | 纯浏览器 (Web Worker + WebVM) | Node.js + OpenClaw Gateway |
| **Agent沙箱** | Web Worker + v86 Alpine WASM | Docker + Sub-agents |
| **数据库** | IndexedDB | 文件系统 (MEMORY.md) |
| **文件存储** | OPFS (浏览器私有文件系统) | 本地文件系统 |

## 2. Agent 循环

| 方面 | OpenBrowserClaw | Jarvis |
|------|-----------------|--------|
| **实现** | Web Worker 中的循环 | Sub-agents with sessions |
| **API** | Anthropic Claude | 多提供商 (OpenRouter, Gemini等) |
| **状态** | State machine (idle/thinking/responding) | File-based + HEARTBEAT |

## 3. 可用工具

| OpenBrowserClaw | Jarvis | 说明 |
|-----------------|--------|------|
| bash (WebVM) | exec, process | 命令执行 |
| read_file/write_file | read, write | 文件操作 |
| list_files | exec ls | 列出文件 |
| fetch_url | web_fetch, browser | HTTP请求 |
| update_memory | 写入 MEMORY.md | 持久化记忆 |
| create_task | cron | 定时任务 |
| javascript | python3 | 代码执行 |

## 4. Telegram 集成

| 方面 | OpenBrowserClaw | Jarvis |
|------|-----------------|--------|
| **方式** | HTTPS Webhook (需浏览器打开) | Bot API (常驻) |
| **优势** | 无需服务器 | 始终在线 |
| **劣势** | 浏览器必须打开 | 需要服务器 |

## 5. 独特创新

### OpenBrowserClaw 值得学习的

1. **update_memory 工具** - 直接在对话中更新记忆，比我们更灵活
2. **create_task 工具** - 在对话中创建定时任务
3. **State machine 模式** - 清晰的状态管理 (idle/thinking/responding)
4. **WebVM 沙箱** - 无需服务器的轻量级沙箱
5. **IndexedDB + OPFS** - 纯浏览器存储方案
6. **加密凭证** - crypto.ts 使用 AES-256-GCM

## 6. 集成建议

### 已集成
- ✅ Skill Bridge - 类似于工具定义
- ✅ Cron 定时任务 - 类似于 create_task
- ✅ 记忆系统 - 类似于 update_memory
- ✅ Telegram Bot - 比 OpenBrowserClaw 更可靠

### 可优化
- 1. 简化 update_memory 调用方式
- 2. 添加 JavaScript 执行工具
- 3. 改进状态机模式
- 4. 考虑 IndexedDB 客户端存储

---

*对比日期: 2026-02-26*
*来源: https://github.com/sachaa/openbrowserclaw*