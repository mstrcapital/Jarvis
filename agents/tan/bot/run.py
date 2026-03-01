#!/usr/bin/env python3
"""
Tan Bot - Quant Telegram Bot
Powered by OpenRouter LLM
"""

import os
import sys
import re
import requests

# 配置
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = os.environ.get("TAN_MODEL", "openrouter/openai/gpt-4o-mini")

SYSTEM_PROMPT = """你叫 Tan，是马可集团的 Chief Quant Strategy Developer (首席量化策略开发)。
你向 Jarvis (CEO & COO) 汇报。

你的职责:
- 量化策略开发
- Kelly Formula 计算
- 概率分析
- 交易策略分析

特点:
- 数学专家，精通概率论、统计学
- 精确计算
- 数据驱动

你必须:
- 给出具体数字
- 计算期望值
- 分析风险

回复语言: 中文优先，除非用户用英文"""

def calculate_kelly(win_rate: float, odds: float) -> float:
    """Kelly Formula 计算"""
    if odds <= 0:
        return 0
    q = 1 - win_rate
    kelly = win_rate - (q / odds)
    return max(0, kelly)

def call_llm(prompt: str) -> str:
    """调用 OpenRouter API"""
    if not OPENROUTER_API_KEY:
        return "❌ 未配置 OpenRouter API Key"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://marcogroup.ai",
        "X-Title": "Jarvis-Tan-Bot"
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

def handle_command(command: str) -> str:
    """处理命令"""
    command = command.strip()
    
    # Kelly 计算
    if "kelly" in command.lower() or "凯利" in command:
        # 尝试提取参数
        match = re.search(r'(\d+)%?\s*[:,/]\s*(\d+\.?\d*)', command)
        if match:
            win = int(match.group(1))
            if '%' in match.group(1):
                win = win / 100
            odds = float(match.group(2))
            kelly = calculate_kelly(win, odds)
            return f"📊 Kelly Formula 计算:\n- 胜率: {win*100:.1f}%\n- 盈亏比: {odds}:1\n- 建议仓位: {kelly*100:.1f}%"
        return "请提供胜率和盈亏比，例如: Kelly 50% : 2"
    
    # 期望值计算
    elif "期望" in command or "expected" in command.lower():
        return call_llm(f"计算期望值: {command}")
    
    # 策略分析
    elif "策略" in command or "strategy" in command.lower():
        return call_llm(f"分析策略: {command}")
    
    else:
        return call_llm(command)

if __name__ == "__main__":
    print("🤖 Tan Bot 启动中...")
    print(f"Model: {MODEL}")
    
    if len(sys.argv) > 1:
        print(f"\n📝 输入: {sys.argv[1]}")
        result = handle_command(sys.argv[1])
        print(f"\n🤖 Tan: {result}")
    else:
        print("用法: python run.py '<message>'")
