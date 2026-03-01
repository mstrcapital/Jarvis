#!/usr/bin/env python3
"""
Ken 套利扫描器 - 带 Telegram 推送
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, List

class ArbitrageScanner:
    def __init__(self):
        self.results = []
        
    async def fetch_polymarket(self) -> List[Dict]:
        markets = []
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://gamma-api.polymarket.com/markets"
                params = {"closed": "false", "limit": "100"}
                async with session.get(url, params=params) as resp:
                    data = await resp.json()
                    for m in data:
                        if m.get('volume24hr', 0) > 50000:
                            markets.append({
                                'platform': 'Polymarket',
                                'question': m.get('question', ''),
                                'yes_price': float(m.get('yesPrice', 0.5)),
                                'no_price': float(m.get('noPrice', 0.5)),
                                'volume': m.get('volume24hr', 0)
                            })
        except Exception as e:
            print(f"Polymarket error: {e}")
        return markets
    
    async def scan(self) -> Dict:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 套利扫描中...")
        polymarket = await self.fetch_polymarket()
        
        # 计算最高/最低价机会 (同平台跨市场)
        opportunities = []
        for i, pm in enumerate(polymarket):
            for j, other in enumerate(polymarket[i+1:], i+1):
                if pm['question'][:50] == other['question'][:50]:
                    continue
                yes_diff = abs(pm['yes_price'] - other['yes_price'])
                if yes_diff > 0.05:
                    opportunities.append({
                        'event': pm['question'][:60],
                        'yes_high': max(pm['yes_price'], other['yes_price']),
                        'yes_low': min(pm['yes_price'], other['yes_price']),
                        'profit_pct': yes_diff * 100
                    })
        
        opportunities.sort(key=lambda x: x['profit_pct'], reverse=True)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'markets_scanned': len(polymarket),
            'opportunities': opportunities[:5]
        }

def send_telegram(message: str):
    import requests
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '8382988751:AAG-Xlis9OoqqC93M1xCufl2FEa6kh7JlbI')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '8591571345')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
    except Exception as e:
        print(f"Telegram error: {e}")

async def main():
    scanner = ArbitrageScanner()
    result = await scanner.scan()
    
    # 构建消息
    msg = "📊 *Ken 套利扫描*\n"
    msg += f"_{result['timestamp']}_\n\n"
    msg += f"扫描市场: `{result['markets_scanned']}`\n"
    msg += f"发现机会: `{len(result['opportunities'])}`\n\n"
    
    if result['opportunities']:
        msg += "🔥 *Top 套利机会:*\n\n"
        for i, o in enumerate(result['opportunities'][:3], 1):
            msg += f"{i}. *{o['event']}*\n"
            msg += f"   高: `{o['yes_high']:.1%}` | 低: `{o['yes_low']:.1%}`\n"
            msg += f"   利润: `{o['profit_pct']:.1f}%`\n\n"
    else:
        msg += "_暂无明显套利机会_"
    
    print(msg)
    send_telegram(msg)
    
    # 保存
    with open('/root/.openclaw/workspace/agents/ken/arbitrage/latest.json', 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
