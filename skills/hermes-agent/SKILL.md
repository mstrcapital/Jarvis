---
name: hermes-agent
version: 1.0.0
description: Hermes Agent - Fully open-source AI agent by Nous Research. Terminal-based AI assistant with persistent memory, multi-platform messaging (Telegram, Discord, Slack, WhatsApp), skills system, cron automation, and sandboxed execution.
homepage: https://github.com/nousresearch/hermes-agent
metadata: {"category":"ai-agent","supports":["tui","messaging","automation","sandbox"]}
read_when:
  - Setting up a personal AI agent
  - Needing multi-platform messaging integration
  - Building persistent agent with memory
  - Automating tasks with cron
  - Training AI models with RL
---

# Hermes Agent

Open-source AI agent by Nous Research. A persistent, autonomous agent that grows with you.

## 核心特性

| 特性 | 描述 |
|------|------|
| 🖥️ **Terminal UI** | 完整 TUI，多行编辑、命令自动完成、流式输出 |
| 💬 **多平台消息** | Telegram, Discord, Slack, WhatsApp, CLI |
| 🧠 **持久记忆** | 跨会话记忆，学习你的偏好和项目 |
| 📚 **Skills 系统** | 可搜索、可分享，兼容 agentskills.io |
| ⏰ **定时任务** | 自然语言配置 cron 任务 |
| 👥 **子代理** | 并行工作流，独立对话 |
| 🔒 **沙盒执行** | Docker/SSH/Modal 隔离运行 |
| 🔬 **研究支持** | 批量生成、RL训练环境、轨迹压缩 |

## 安装

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 配置
hermes setup

# 启动
hermes
```

## 模型配置

支持三种模型提供商：

```bash
hermes model    # 交互式切换模型

# Nous Portal (推荐)
hermes config set model.provider portal

# OpenRouter (200+ 模型)
hermes config set model.provider openrouter
hermes config set OPENROUTER_API_KEY xxx

# 自定义端点 (VLLM/SGLang)
hermes config set model.provider custom
hermes config set CUSTOM_BASE_URL http://localhost:8000/v1
```

## 终端后端 (安全模式)

```bash
# SSH 隔离 (推荐生产环境)
hermes config set terminal.backend ssh
hermes config set TERMINAL_SSH_HOST my-server.example.com

# Docker 隔离
hermes config set terminal.backend docker

# Modal 云沙盒
hermes config set terminal.backend modal
```

## Skills 系统

```bash
# 查看可用 skills
hermes skills list

# 安装社区 skill
hermes skills install <skill-name>

# 查看已安装 skills
hermes skills installed
```

内置 Skills:
- github - GitHub 操作
- email - 邮件管理
- feeds - RSS 订阅
- mlops - MLOps 工具
- productivity - 生产力工具
- diagramming - 图表生成
- 等等...

## 定时任务

```bash
# 添加定时任务
hermes cron add "每天早上8点发送AI新闻摘要"

# 查看任务
hermes cron list

# 删除任务
hermes cron remove <task-id>
```

## 常用命令

| 命令 | 功能 |
|------|------|
| `hermes` | 启动聊天 |
| `hermes setup` | 初始配置 |
| `hermes model` | 切换模型 |
| `hermes tools` | 查看工具 |
| `hermes skills` | 管理 skills |
| `hermes cron` | 定时任务 |
| `hermes config` | 配置管理 |
| `hermes update` | 更新版本 |

## 研究工具

### 批量处理
```bash
python batch_runner.py --config batch-config.yaml
```

### 轨迹压缩
```bash
python trajectory_compressor.py --input trajectories.jsonl --output compressed.jsonl
```

### Atropos RL 环境
```bash
cd tinker-atropos
python -m atropos.train --config configs/default.yaml
```

---

*Skill source: https://github.com/nousresearch/hermes-agent*
*Created: 2026-02-27*