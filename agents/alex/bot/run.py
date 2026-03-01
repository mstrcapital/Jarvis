#!/usr/bin/env python3
"""
Alex Bot - CTO Telegram Bot
Powered by OpenRouter LLM
"""

import os
import sys
import requests

# 配置
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = os.environ.get("ALEX_MODEL", "openrouter/anthropic/claude-sonnet-4-20250522")

SYSTEM_PROMPT = """你叫 Alex，是马可集团的 CTO (首席技术官)。
你向 Jarvis (CEO & COO) 汇报。

你的职责:
- Web3 技术开发
- API 管理
- 技术基础设施 (Vercel, Cloudflare)
- 代码审查和技术决策

特点:
- 技术专家，精通 Web3, Python, API
- 务实、高效
- 简洁回复

回复语言: 中文优先，除非用户用英文"""

def call_llm(prompt: str) -> str:
    """调用 OpenRouter API"""
    if not OPENROUTER_API_KEY:
        return "❌ 未配置 OpenRouter API Key"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://marcogroup.ai",
        "X-Title": "Jarvis-Alex-Bot"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        result = resp.json()
        
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Error: {result}"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    print("🤖 Alex Bot 启动中...")
    print(f"Model: {MODEL}")
    
    if len(sys.argv) > 1:
        print(f"\n📝 输入: {sys.argv[1]}")
        result = call_llm(sys.argv[1])
        print(f"\n🤖 Alex: {result}")
    else:
        print("用法: python run.py '<message>'")
