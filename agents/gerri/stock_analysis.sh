#!/bin/bash
# Gerri 股票监控 - 每日盘前分析

cd /root/.openclaw/workspace/daily_stock_analysis

# 加载配置
export $(cat /root/.openclaw/workspace/agents/gerri/config/.env | grep -v '^#' | xargs)

echo "📊 Gerri 股票监控 - $(date)"
python3 main.py 2>&1
