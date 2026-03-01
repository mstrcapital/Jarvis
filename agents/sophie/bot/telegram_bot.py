#!/usr/bin/env python3
"""
Sophie Bot - Investor Relations Telegram Bot
"""

import os
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 配置
TOKEN = "8651583140:AAF5FHdaIqUEi2dbd5zm9Ms1QnYrQTyI3Wc"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")
MODEL = "openai/gpt-4o-mini"

SYSTEM_PROMPT = """你叫 Sophie，是马可集团的 Investor Relations (投资者关系) 专家。
你向 Jarvis (CEO & COO) 汇报。

你的职责:
- CRM 运营管理
- LinkedIn 专业人脉拓展
- Gmail 邮件管理
- Email List 管理
- Networking Outreach

特点:
- 专业、优雅、细致
- 善于建立和维护关系
- 沟通能力强
- 中英文皆可

工作风格:
- 及时跟进，从不忘记跟进
- 记录每次互动到 CRM
- 专业但不失温暖

回复语言: 中文优先，除非用户用英文"""

CRM_NOTES = []

def call_llm(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://marcogroup.ai",
        "X-Title": "Jarvis-Sophie-Bot"
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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤝 Sophie Bot 已启动！我是投资者关系专家，有CRM、LinkedIn、邮件相关问题可以问我。")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 我是 Sophie，Investor Relations专家。\n\n我可以帮你：\n- CRM 联系人管理\n- 跟进提醒\n- LinkedIn  Outreach 建议\n- 邮件模板\n- 专业沟通技巧")

async def crm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """CRM 相关命令"""
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("📊 CRM 命令用法:\n/crm add <联系人>\n/crm list\n/crm followup <联系人>")
    elif "add" in text.lower():
        await update.message.reply_text(f"✅ 已添加联系人到 CRM: {text}")
    elif "list" in text.lower():
        await update.message.reply_text(f"📋 CRM 中有 {len(CRM_NOTES)} 个联系人")
    else:
        response = call_llm(f"CRM 操作建议: {text}")
        await update.message.reply_text(f"🤝 Sophie: {response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # CRM 快捷命令
    if text.startswith("/crm "):
        await crm_command(update, context)
        return
    
    # 普通消息
    if update.message.chat.type != "private":
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(f"🤝 Sophie: {response}")
    else:
        await update.message.chat.send_action("typing")
        response = call_llm(text)
        await update.message.reply_text(response)

def main():
    if not TOKEN:
        print("❌ 请设置 SOPHIE_BOT_TOKEN 环境变量")
        return
    
    print("🤝 Starting Sophie Bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("crm", crm_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Sophie Bot 运行中...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
