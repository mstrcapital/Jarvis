#!/usr/bin/env python3
"""
Tan Bot - Telegram 版本
"""

import os
import sys
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置
TOKEN = "8789273494:AAEJyFDd6cbJiO4YI50IA2ilprfX-lxKZk8"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")
MODEL = "openai/gpt-4o-mini"

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
    if odds <= 0:
        return 0
    q = 1 - win_rate
    kelly = win_rate - (q / odds)
    return max(0, kelly)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Tan Bot 已启动！我是量化策略专家，有问题问我。")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 我是 Tan，Quant。有 Kelly公式、概率、策略问题可以问我！")

def call_llm(prompt: str) -> str:
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
            return f"Error: {result}"
    except Exception as e:
        return f"Error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 检查 Kelly 计算
    if "kelly" in text.lower() or "凯利" in text:
        match = re.search(r'(\d+)%?\s*[:,/]\s*(\d+\.?\d*)', text)
        if match:
            win = int(match.group(1))
            if '%' in match.group(1):
                win = win / 100
            odds = float(match.group(2))
            kelly = calculate_kelly(win, odds)
            response = f"📊 Kelly Formula:\n- 胜率: {win*100:.1f}%\n- 盈亏比: {odds}:1\n- 建议仓位: {kelly*100:.1f}%"
            await update.message.reply_text(response)
            return
    
    # 群组或私聊都响应
    if update.message.chat.type != "private":
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(f"🤖 Tan: {response}")
    else:
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(response)

def main():
    print("🤖 Starting Tan Bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Tan Bot 运行中...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()