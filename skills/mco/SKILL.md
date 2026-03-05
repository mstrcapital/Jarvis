---
name: mco
description: MCO (Multi-CLI Orchestrator) - 协调多个 AI 编码 Agent 并行工作。派发任务给 Claude Code, Codex, Gemini, OpenCode, Qwen 并行执行。
---

# MCO Skill

> 多 CLI Agent 编排器 - 让多个 AI Agent 并行工作

**安装:** `npm i -g @tt-a1i/mco`  
**状态:** ✅ 已安装

---

## 支持的 Agent

| Agent | 命令 | 状态 |
|-------|------|------|
| Claude Code | `claude` | 需安装 |
| Codex CLI | `codex` | 需安装 |
| Gemini CLI | `gemini` | 需安装 |
| OpenCode | `opencode` | 需安装 |
| Qwen Code | `qwen` | 需安装 |

---

## 核心概念

```
你 (Tech Lead)
     │
     ▼
  mco review / mco run
     │
     ├─→ Claude Code  ──┐
     ├─→ Codex CLI      │
     ├─→ Gemini CLI     ├─→ 去重 → 合成 → 输出
     ├─→ OpenCode       │
     └─→ Qwen Code   ───┘
```

---

## 命令

### 1. 检查 Agent 状态
```bash
mco doctor
mco doctor --json
```

### 2. 代码审查 (Review Mode)
```bash
mco review \
  --repo . \
  --prompt "Review for security vulnerabilities." \
  --providers claude,codex,gemini \
  --json
```

### 3. 通用任务 (Run Mode)
```bash
mco run \
  --repo . \
  --prompt "Summarize the architecture." \
  --providers claude,codex \
  --json
```

---

## 输出格式

| 格式 | 标志 | 用途 |
|------|------|------|
| 人类可读 | `--format report` | 终端阅读 |
| PR Markdown | `--format markdown-pr` | GitHub PR 评论 |
| SARIF 2.1.0 | `--format sarif` | GitHub Code Scanning |
| JSON | `--json` | 自动化 |

---

## 常用示例

### PR 代码审查
```bash
mco review \
  --repo . \
  --prompt "Review this PR for high-risk bugs and security issues." \
  --providers claude,codex,qwen \
  --format markdown-pr
```

### 安全扫描 (CI/CD)
```bash
mco review \
  --repo . \
  --prompt "Scan for security vulnerabilities." \
  --providers claude,codex,gemini \
  --format sarif
```

### 架构分析
```bash
mco run \
  --repo . \
  --prompt "Analyze the architecture of this project." \
  --providers claude,gemini,qwen
```

### 共识决策
```bash
mco review \
  --repo . \
  --prompt "Review for bugs." \
  --providers claude,codex,qwen \
  --synthesize
```

---

## 关键参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--providers` | `claude,codex` | 逗号分隔的 Agent 列表 |
| `--stall-timeout` | 900 | 无输出时取消 (秒) |
| `--review-hard-timeout` | 1800 | 硬截止时间 |
| `--synthesize` | off | 运行共识合成 |
| `--format` | `report` | 输出格式 |

---

## 与 OpenClaw 集成

**✅ 支持 OpenClaw!**

从 OpenClaw 调用 MCO:
> "Use mco to run a security review on this repo with Claude, Codex, and Gemini. Synthesize the results."

OpenClaw 会:
1. 读取 `mco -h` 学习 CLI
2. 自动编排整个工作流
3. 本地变成多 Agent 审查团队

---

## 输出结构

```
reports/review/<task_id>/
  summary.md          # 人类可读摘要
  decision.md         # PASS/FAIL/ESCALATE/PARTIAL
  findings.json       # 聚合发现 (review mode)
  run.json            # 机器可读执行元数据
  providers/          # 每个 Agent 的结果
  raw/                # 原始 stdout/stderr
```

---

## 去重机制

MCO 自动合并来自不同 Agent 的相同发现:

```json
{
  "title": "SQL Injection Risk",
  "detected_by": ["claude", "codex"],
  "severity": "critical"
}
```

---

## 安装缺失的 Agent

```bash
# Claude Code
npm i -g @anthropic-ai/claude-code

# Codex CLI  
curl -fsSL https://github.com/openai/codex-cli/releases/download/... | tar -xz
sudo mv codex /usr/local/bin/

# Gemini CLI
npm i -g @google/gemini-cli

# OpenCode
npm i -g opencode

# Qwen Code
# 见 https://github.com/QwenLM/qwen-code
```

---

## 状态检查

```bash
# 检查当前状态
mco doctor
```

---

## 注意事项

1. **Agent 需要单独安装** - MCO 只是调度器
2. **并行执行** - 所有 Agent 同时运行,总时间 ≈ 最慢的那个
3. **去重** - 相同问题只显示一次,标注发现者
4. **共识合成** - `--synthesize` 生成总结

---

## 参考

- GitHub: https://github.com/mco-org/mco
- NPM: https://www.npmjs.com/package/@tt-a1i/mco