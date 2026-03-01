# 🧠 Mem0 向量记忆配置

## 已完成
- [x] 安装 @mem0/openclaw-mem0
- [x] 配置插件到 openclaw.json
- [x] 设置为 open-source 模式 (无需 Mem0 云端)

## 待完成 (需要 API Key)

### 方案 1: OpenAI (需要 API Key)
```bash
export OPENAI_API_KEY="sk-..."
# 或添加到 openclaw.json env
```

### 方案 2: OpenRouter (推荐 - 已安装 nkmc)
需要配置:
```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "open-source",
          "userId": "jarvis",
          "oss": {
            "embedder": {
              "provider": "openrouter",
              "config": {
                "model": "microsoft/phi-4-mini"
              }
            }
          }
        }
      }
    }
  }
}
```

### 方案 3: 使用 Mem0 Cloud (免费 tier)
```bash
# 获取 API key: https://app.mem0.ai
export MEM0_API_KEY="mem0-..."
```

## Agent 工具 (配置完成后可用)

| 工具 | 功能 |
|------|------|
| `memory_search` | 自然语言搜索记忆 |
| `memory_list` | 列出所有记忆 |
| `memory_store` | 显式保存记忆 |
| `memory_get` | 获取单条记忆 |
| `memory_forget` | 删除记忆 |

## 测试命令
```bash
openclaw mem0 search "团队架构"
```

---

**状态**: 插件已安装，需要 API Key 才能激活  
**下一步**: 提供 OPENAI_API_KEY 或配置 OpenRouter
