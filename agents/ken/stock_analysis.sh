#!/bin/bash
# Ken Stock Analysis - 简化版

cd /root/.openclaw/workspace/daily_stock_analysis

# 设置环境变量
export STOCK_LIST="NVDA,QQQ,TSLA,MSFT,GOOGL,AMD"
export TELEGRAM_BOT_TOKEN="8382988751:AAG-Xlis9OoqqC93M1xCufl2FEa6kh7JlbI"
export TELEGRAM_CHAT_ID="8591571345"

# 使用项目自带的 main.py
echo "📊 Ken 股票分析..."
python3 main.py 2>&1

echo "✅ 分析完成"
