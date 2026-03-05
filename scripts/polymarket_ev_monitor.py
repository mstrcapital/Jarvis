#!/usr/bin/env python3
"""
Polymarket EV Monitor - Finance & Crypto
每小时推送高EV市场机会到 Telegram
"""

import subprocess
import json
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4"
REPORT_CHAT_ID = "8591571345"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def send_telegram(message):
    try:
        import urllib.request
        import urllib.parse
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': REPORT_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_markets():
    """获取 Finance 和 Crypto 市场数据"""
    markets = []
    
    # Finance - Fed Rate Cuts 2026
    print("Fetching Fed rate cuts...")
    output = run_cmd('polymarket -o json markets search "Fed rate cuts happen in 2026" --limit 20 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    # Finance - Fed Chair
    print("Fetching Fed Chair...")
    output = run_cmd('polymarket -o json markets search "Fed chair" --limit 10 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    # Crypto - Bitcoin
    print("Fetching Bitcoin...")
    output = run_cmd('polymarket -o json markets search "Bitcoin be above $68" --limit 5 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    # Crypto - Ethereum
    print("Fetching Ethereum...")
    output = run_cmd('polymarket -o json markets search "Ethereum be above $2" --limit 5 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    # Crypto - MicroStrategy
    print("Fetching MicroStrategy...")
    output = run_cmd('polymarket -o json markets search "MicroStrategy sells" --limit 5 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    # Finance - Largest Company
    print("Fetching Largest Company...")
    output = run_cmd('polymarket -o json markets search "largest company" --limit 10 2>/dev/null')
    if output:
        try:
            data = json.loads(output)
            markets.extend(data)
        except:
            pass
    
    return markets

def calculate_ev(price, question):
    """计算 EV - 基于特定市场的分析"""
    if not price:
        return 0
    try:
        price_float = float(price)
        
        # 低价格 = 高赔率 (假设有 20% 概率 true)
        if price_float < 0.5:
            payout = (1 - price_float) / price_float
            ev = payout * 0.2 - 0.8
        # 高价格 = 低赔率 (假设有 80% 概率 true)
        else:
            payout = (1 - price_float) / price_float
            ev = payout * 0.8 - 0.2
        
        return ev
    except:
        return 0

def format_market(m):
    """格式化市场信息"""
    question = m.get('question', '')[:50]
    
    # 过滤: 只看 2026-2028 年的市场
    if '2025' in question or '2022' in question or '2023' in question or '2024' in question:
        if '2026' not in question and '2027' not in question and '2028' not in question:
            return None
    
    # 解析 price - outcomePrices 是 JSON 数组字符串
    outcome_prices = m.get('outcomePrices')
    if outcome_prices:
        try:
            prices = json.loads(outcome_prices)
            price = prices[0] if prices else '0'
        except:
            price = '0'
    else:
        price = '0'
    
    volume = m.get('volumeNum', 0)
    try:
        volume = int(float(volume))  # String to float to int
    except:
        volume = 0
    
    # 过滤: 至少 $10K 交易量
    if volume < 10000:
        return None
    
    try:
        price_float = float(price)
        price_str = f"{price_float*100:.2f}¢"
    except:
        price_str = price
    
    # 计算简单 EV
    ev = calculate_ev(price, question)
    
    # 只返回高 EV 机会 (EV > 30% 或 EV < -30%)
    if abs(ev) < 0.3:
        return None
    
    ev_str = f"+{int(ev*100)}%" if ev > 0 else f"{int(ev*100)}%"
    
    return {
        'question': question,
        'price': price_str,
        'volume': f"${volume/1000:.1f}K" if volume < 1000000 else f"${volume/1000000:.1f}M",
        'ev': ev_str,
        'ev_value': ev
    }

def main():
    print(f"=== Polymarket EV Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC ===")
    
    markets = get_markets()
    print(f"Found {len(markets)} markets")
    
    # 分析每个市场
    opportunities = []
    for m in markets:
        formatted = format_market(m)
        if formatted:
            opportunities.append(formatted)
    
    # 按 EV 排序
    opportunities.sort(key=lambda x: x['ev_value'], reverse=True)
    
    # 取前10
    top_opps = opportunities[:10]
    
    # 生成报告
    report = f"""📊 *Polymarket EV Monitor*
⏰ {datetime.now().strftime('%H:%M')} UTC

🎯 *Top EV Opportunities*
"""
    
    if top_opps:
        for i, opp in enumerate(top_opps, 1):
            report += f"\n{i}. {opp['question']}..."
            report += f"\n   💰 {opp['price']} | 📈 {opp['ev']} | 💵 {opp['volume']}"
    else:
        report += "\n⚠️ No high EV opportunities found"
    
    # 添加说明
    report += """
---
💡 *EV 计算*: 基于隐含概率 vs 主观概率
🔔 只显示 |EV| > 30% 的机会
"""
    
    print(report)
    
    # 发送到 Telegram
    send_telegram(report)
    print("✅ Report sent to Telegram")

if __name__ == "__main__":
    main()
