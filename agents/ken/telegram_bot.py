#!/usr/bin/env python3
"""
Ken Telegram Bot - LLM Powered (MiniMax M2.5)
Two-way communication with MiniMax
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load config
WORKSPACE = "/root/.openclaw/workspace"
AGENT_DIR = f"{WORKSPACE}/agents/ken"
load_dotenv(f"{AGENT_DIR}/config.env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINIMAX_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-M2.5")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(text, chat_id=CHAT_ID):
    """Send message to Telegram"""
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })

def call_minimax(prompt):
    """Call MiniMax API"""
    url = "https://api.minimaxi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MINIMAX_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MINIMAX_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API Error: {resp.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_updates(offset=0):
    """Get updates from Telegram"""
    resp = requests.get(f"{API_URL}/getUpdates", params={"offset": offset, "timeout": 30})
    return resp.json().get("result", [])

def process_message(update):
    """Process incoming message"""
    message = update.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")
    msg_id = message.get("message_id")
    chat_id = chat.get("id")
    
    # Ignore non-text or commands
    if not text or text.startswith("/"):
        return
    
    print(f"📩 Message from {chat_id}: {text}")
    
    # Build context for MiniMax
    context = f"""You are Ken, Chief Polymarket Analyst for Marco's investment team.
Your role:
- Analyze prediction markets (Polymarket)
- Track BTC volatility, options flow
- Provide market insights
- Be professional but friendly

User message: {text}

Respond in Chinese or English based on the user's language. Keep it concise."""
    
    # Get AI response
    response = call_minimax(context)
    
    # Send response
    send_message(f"📊 *Ken*\n\n{response}", chat_id)
    print(f"✅ Response sent")

def main():
    print("🤖 Ken Bot Started - MiniMax M2.5 Powered")
    print(f"Model: {MINIMAX_MODEL}")
    print(f"Token: {TOKEN[:20]}...")
    print("Waiting for messages...")
    
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                process_message(update)
        except Exception as e:
            print(f"Error: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()