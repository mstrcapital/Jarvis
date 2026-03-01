#!/usr/bin/env python3
"""
Ken Stock Analysis - 基于 daily_stock_analysis
"""

import os
import sys
import subprocess
from datetime import datetime

# 添加项目路径
sys.path.insert(0, '/root/.openclaw/workspace/daily_stock_analysis')

# 加载配置
env_file = '/root/.openclaw/workspace/agents/ken/config/.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

def run_analysis():
    """运行股票分析"""
    print(f"📊 Ken 股票分析 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)
    
    try:
        # 使用项目自带的 analyzer
        from analyzer import StockAnalyzer
        
        analyzer = StockAnalyzer()
        stocks = os.environ.get('STOCK_LIST', 'NVDA,QQQ').split(',')
        
        results = []
        for stock in stocks[:5]:  # 分析前5只
            stock = stock.strip()
            if stock:
                print(f"📈 分析 {stock}...")
                result = analyzer.analyze(stock)
                results.append(result)
        
        # 生成报告
        report = generate_report(results)
        send_notification(report)
        
        return "✅ 分析完成"
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"❌ Error: {e}"

def generate_report(results):
    """生成报告"""
    report = "📊 Ken 股票分析报告\n"
    report += f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for r in results:
        report += f"*{r.get('symbol', 'N/A')}*\n"
        report += f"  价格: {r.get('price', 'N/A')}\n"
        report += f"  建议: {r.get('recommendation', 'N/A')}\n"
        report += f"  理由: {r.get('reason', 'N/A')}\n\n"
    
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    report += "_由 Ken AI 分析_"
    
    return report

def send_notification(message):
    """发送到 Telegram"""
    import requests
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        try:
            requests.post(url, json=data, timeout=10)
            print("✅ 通知已发送")
        except Exception as e:
            print(f"❌ 发送失败: {e}")

if __name__ == "__main__":
    run_analysis()
