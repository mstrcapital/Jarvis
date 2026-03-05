---
name: openfang
description: Agent Operating System built in Rust - Autonomous agents that work for you 24/7 with 7 built-in Hands (Clip, Lead, Collector, Predictor, Researcher, Twitter, Browser).
---

# OpenFang Skill

> Agent Operating System built in Rust - Autonomous agents that work for you 24/7

**Repository:** https://github.com/RightNow-AI/openfang  
**Language:** Rust (137K LOC, 14 crates)  
**Version:** v0.1.0 (Feb 2026)

---

## Overview

OpenFang is an **open-source Agent Operating System** - not a chatbot framework, but a full OS for autonomous agents. It compiles to a single ~32MB binary with 16 security layers.

Unlike OpenClaw which waits for user input, OpenFang runs **autonomous agents (Hands)** that work on schedules, 24/7.

---

## Installation

### macOS / Linux
```bash
curl -fsSL https://openfang.sh/install | sh
openfang init
openfang start
# Dashboard: http://localhost:4200
```

### Windows (PowerShell)
```powershell
irm https://openfang.sh/install.ps1 | iex
openfang init
openfang start
```

---

## The 7 Built-in Hands

Each Hand is an autonomous agent that works for you without prompting:

| Hand | Function |
|------|----------|
| **Clip** | YouTube → vertical shorts with captions, AI voice-over, publish to Telegram/WhatsApp |
| **Lead** | Daily prospect discovery, enrichment, scoring (0-100), dedup, delivers CSV/JSON |
| **Collector** | OSINT monitoring - change detection, sentiment tracking, knowledge graphs |
| **Predictor** | Superforecasting with Brier scores, contrarian mode |
| **Researcher** | Deep research, CRAAP credibility evaluation, APA citations |
| **Twitter** | Auto content creation, scheduling, engagement, approval queue |
| **Browser** | Web automation, mandatory purchase approval gate |

---

## Commands

### Basic
```bash
openfang init              # Initialize with LLM providers
openfang start             # Start daemon
openfang status            # Check status
openfang stop              # Stop daemon
```

### Hands
```bash
openfang hand list                     # List all hands
openfang hand activate researcher      # Activate a hand
openfang hand status researcher        # Check hand progress
openfang hand pause lead               # Pause without losing state
```

### Agents
```bash
openfang agent spawn coder     # Spawn pre-built agent
openfang chat researcher       # Chat with agent
openfang agent list            # List agents
```

### Migration (from OpenClaw)
```bash
openfang migrate --from openclaw           # Migrate everything
openfang migrate --from openclaw --dry-run # Preview first
```

---

## 16 Security Systems

| # | System |
|---|--------|
| 1 | WASM Dual-Metered Sandbox |
| 2 | Merkle Hash-Chain Audit Trail |
| 3 | Information Flow Taint Tracking |
| 4 | Ed25519 Signed Agent Manifests |
| 5 | SSRF Protection |
| 6 | Secret Zeroization |
| 7 | OFP Mutual Authentication |
| 8 | Capability Gates |
| 9 | Security Headers |
| 10 | Health Endpoint Redaction |
| 11 | Subprocess Sandbox |
| 12 | Prompt Injection Scanner |
| 13 | Loop Guard |
| 14 | Session Repair |
| 15 | Path Traversal Prevention |
| 16 | GCRA Rate Limiter |

---

## 40 Channel Adapters

**Core:** Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email  
**Enterprise:** Teams, Mattermost, Google Chat, Webex, Feishu/Lark, Zulip  
**Social:** LINE, Viber, Facebook, Mastodon, Bluesky, Reddit, LinkedIn  
**Privacy:** Threema, Nostr, Rocket.Chat, Ntfy

---

## 27 LLM Providers (123+ models)

Anthropic, Gemini, OpenAI, Groq, DeepSeek, OpenRouter, Together, Mistral, Fireworks, Cohere, Perplexity, xAI, Cerebras, SambaNova, HuggingFace, Replicate, Ollama, vLLM, Qwen, MiniMax, Zhipu, Moonshot, Qianfan, Bedrock, and more.

---

## OpenAI-Compatible API

```bash
curl -X POST localhost:4200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "researcher",
    "messages": [{"role": "user", "content": "Analyze Q4 trends"}],
    "stream": true
  }'
```

---

## Comparison with OpenClaw

| Metric | OpenFang | OpenClaw |
|--------|----------|----------|
| Cold Start | **180ms** | 5.98s |
| Idle Memory | **40MB** | 394MB |
| Install Size | **32MB** | 500MB |
| Security | **16 layers** | 3 layers |
| Channels | **40** | 13 |
| LLM Providers | **27** | 10 |

---

## Use Cases for Jarvis Team

1. **Migrate from OpenClaw** - `openfang migrate --from openclaw`
2. **Autonomous Research** - Activate Researcher hand for continuous research
3. **Lead Generation** - Activate Lead hand for daily prospecting
4. **Twitter Management** - Activate Twitter hand for content scheduling
5. **Better Performance** - Replace OpenClaw for lower resource usage

---

## Development

```bash
# Build
cargo build --workspace --lib

# Test (1,767+ tests)
cargo test --workspace

# Lint (0 warnings required)
cargo clippy --workspace --all-targets -- -D warnings
```

---

## References

- Website: https://openfang.sh
- Docs: https://openfang.sh/docs
- Discord: https://discord.gg/sSJqgNnq6X
- Twitter: https://x.com/openfangg

---

## Notes for Jarvis

- v0.1.0 is first public release - expect rough edges
- Recommend pinning to specific commit for production
- Migration from OpenClaw is one-command
- Hands work autonomously - activate and let them run