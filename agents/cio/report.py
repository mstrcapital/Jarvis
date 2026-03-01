#!/usr/bin/env python3
"""
CIO Global Macro Report Generator
Uses Gemini API for AI-powered macro analysis
"""

import os
import sys
import json
import requests
import yfinance as yf
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load config
from dotenv import load_dotenv
load_dotenv("/root/.openclaw/workspace/agents/cio/config.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_market_data():
    """Fetch global market data"""
    data = {}
    
    # US Indices
    print("📊 Fetching US indices...")
    try:
        spx = yf.Ticker("^GSPC").history(period="1d")
        nasdaq = yf.Ticker("^IXIC").history(period="1d")
        data["US"] = {
            "SP500": spx["Close"].iloc[-1] if not spx.empty else 0,
            "NASDAQ": nasdaq["Close"].iloc[-1] if not nasdaq.empty else 0,
        }
    except Exception as e:
        print(f"  Error: {e}")
    
    # Currencies
    print("💱 Fetching currencies...")
    try:
        usd_cny = yf.Ticker("USDCNY=X").history(period="1d")
        usd_jpy = yf.Ticker("USDJPY=X").history(period="1d")
        data["FX"] = {
            "USDCNY": usd_cny["Close"].iloc[-1] if not usd_cny.empty else 0,
            "USDJPY": usd_jpy["Close"].iloc[-1] if not usd_jpy.empty else 0,
        }
    except Exception as e:
        print(f"  Error: {e}")
    
    # Commodities
    print("🪙 Fetching commodities...")
    try:
        gold = yf.Ticker("GC=F").history(period="1d")
        oil = yf.Ticker("CL=F").history(period="1d")
        data["Commodities"] = {
            "Gold": gold["Close"].iloc[-1] if not gold.empty else 0,
            "Oil": oil["Close"].iloc[-1] if not oil.empty else 0,
        }
    except Exception as e:
        print(f"  Error: {e}")
    
    # US Treasuries (10Y Yield)
    print("📊 Fetching Treasuries...")
    try:
        Treasury_10Y = yf.Ticker("^TNX").history(period="1d")
        data["Treasuries"] = {
            "10Y": Treasury_10Y["Close"].iloc[-1] if not Treasury_10Y.empty else 0,
        }
    except Exception as e:
        print(f"  Error: {e}")
    
    return data

def call_gemini(prompt: str) -> str:
    """Call Gemini API for analysis"""
    import httpx
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        resp = requests.post(
            f"{url}?key={GEMINI_API_KEY}",
            json=payload,
            headers=headers,
            timeout=60
        )
        if resp.status_code == 200:
            result = resp.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error: {resp.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def generate_macro_report(data: dict) -> str:
    """Generate macro report using Gemini"""
    
    market_summary = f"""
Current Market Data:
- S&P 500: {data.get('US', {}).get('SP500', 'N/A')}
- NASDAQ: {data.get('US', {}).get('NASDAQ', 'N/A')}
- USD/CNY: {data.get('FX', {}).get('USDCNY', 'N/A')}
- USD/JPY: {data.get('FX', {}).get('USDJPY', 'N/A')}
- Gold: ${data.get('Commodities', {}).get('Gold', 'N/A')}
- Oil: ${data.get('Commodities', {}).get('Oil', 'N/A')}
- US 10Y Yield: {data.get('Treasuries', {}).get('10Y', 'N/A')}%
"""
    
    prompt = f"""You are CIO, Chief Investment Officer, graduate of NYU Stern with PhD in Economics. 
Your mentors include Julian Roberts, Druckenmiller, Duan Yongping, David Tepper, and Bessent.
Your track record is 15% CAGR. You specialize in macro hedge, options strategies, and geopolitical analysis.

Generate a daily global macro flow report with:

1. **Executive Summary** - One sentence market view
2. **US Equities** - Technical outlook for S&P 500 and Nasdaq
3. **Currency** - USD/CNY and USD/JPY analysis
4. **Commodities** - Gold and Oil outlook
5. **Treasuries** - 10Y yield and Fed expectations
6. **Risk Indicators** - Key levels and catalysts

Keep it professional, data-driven, and actionable.
Use clear headers and bullet points.

Current market data:
{market_summary}

Date: {datetime.now().strftime('%Y-%m-%d')}
"""
    
    return call_gemini(prompt)

def send_telegram(message: str):
    """Send report to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            print("✅ Telegram message sent!")
        else:
            print(f"❌ Telegram error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 60)
    print("🏛️ CIO Global Macro Report")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    
    # Get data
    data = get_market_data()
    
    print("\n📈 Generating AI analysis...")
    report = generate_macro_report(data)
    
    # Add header
    full_report = f"🏛️ *CIO Global Macro Report*\n{datetime.now().strftime('%Y-%m-%d')}\n\n"
    full_report += report
    
    # Print locally
    print("\n" + "=" * 60)
    print("REPORT PREVIEW:")
    print("=" * 60)
    print(full_report[:2000])
    
    # Send to Telegram
    print("\n📲 Sending to Telegram...")
    send_telegram(full_report)
    
    print("\n✅ Report complete!")

if __name__ == "__main__":
    main()