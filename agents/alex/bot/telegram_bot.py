#!/usr/bin/env python3
"""
Alex Bot - Telegram 版本
"""

import os
import sys
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置
TOKEN = "8569376677:AAEIMQ0mzfVq1XH1Qj9j7gOvz5Eg210N9Zo"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")
MODEL = "anthropic/claude-3.5-sonnet"

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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Alex Bot 已启动！我是 CTO，有技术问题问我。")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 我是 Alex，CTO。有什么技术问题可以问我！")

def call_llm(prompt: str) -> str:
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
            return f"Error: {result}"
    except Exception as e:
        return f"Error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 只响应被@或群组中的消息
    if update.message.chat.type != "private":
        # 群组中响应所有消息
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(f"🤖 Alex: {response}")
    else:
        # 私聊直接响应
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(response)

def main():
    print("🤖 Starting Alex Bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Alex Bot 运行中...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()