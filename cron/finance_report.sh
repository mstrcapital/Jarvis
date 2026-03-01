#!/bin/bash
# Finance Market Report - 每日两次推送
# 9am ET & 9pm ET

TELEGRAM_BOT_TOKEN="8382988751:AAG-Xlis9OoqqC93M1xCufl2FEa6kh7JlbI"
TELEGRAM_CHAT_ID="8591571345"

REPORT_TIME=$(date '+%Y-%m-%d %H:%M UTC')

# 获取 Finance 市场数据
FINANCE_DATA=$(polymarket markets search finance --limit 50 2>&1)

# 构建报告
REPORT="📊 *Finance 市场每日报告*

*生成时间: $REPORT_TIME*

━━━━━━━━━━━━━━━━━━━━

🎯 *今日热门机会*

"

# 添加 NVDA 机会
REPORT+="*NVIDIA:*"
REPORT+="\n• NVDA >$190 (2月): 19¢ (推荐)"
REPORT+="\n• NVDA >$200 (2月): 0.95¢ (高确定性)"
REPORT+="\n• NVDA $185-$190: 47.5¢"

# 添加 Gold/Silver
REPORT+="\n\n🥇 *黄金/白银:*"
REPORT+="\n• Gold $5,500: 0.45¢"
REPORT+="\n• Silver $120: 0.15¢"

# 添加 Fed 降息
REPORT+="\n\n💵 *Fed 2026降息:*"
REPORT+="\n• 2次: 27.5¢"
REPORT+="\n• 3次: 18.5¢"
REPORT+="\n• 0次: 9.35¢"

REPORT+="\n\n━━━━━━━━━━━━━━━━━━━━"
REPORT+="\n💡 使用 *polymarket markets search finance* 查看完整列表"

# 发送消息
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$TELEGRAM_CHAT_ID" \
    -d "text=$REPORT" \
    -d "parse_mode=Markdown" > /tmp/cron_finance.log

echo "✅ Finance Report sent at $REPORT_TIME"
