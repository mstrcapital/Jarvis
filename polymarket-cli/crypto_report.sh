#!/bin/bash
# Crypto Market Report Script
# Author: Alex (CTO)

echo "=== Crypto Market Report - $(date '+%Y-%m-%d %H:%M') ==="
echo ""

# 搜索活跃市场
echo "📊 活跃 Crypto 预测市场:"
polymarket markets search crypto --limit 10 2>/dev/null | grep -E "Active|BTC|ETH|Solana" | head -15

echo ""
echo "💰 热门市场 (成交量):"
polymarket markets list --limit 5 -o json 2>/dev/null | python3 -c "
import json,sys
try:
    data=json.load(sys.stdin)
    for m in data[:5]:
        print(f\"  - {m.get('question','')[:50]}...\")
        print(f\"    价格: {m.get('yes_price','N/A')} 成交量: \${m.get('volume',0):,.0f}\")
except: pass
" 2>/dev/null

echo ""
echo "✅ 报告生成完成"
