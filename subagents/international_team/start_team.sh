#!/bin/bash
echo "🚀 启动 Jarvis 国际内容团队"
echo "======================================"

echo "📦 启动 Jarvis (CEO & COO)..."
openclaw agents add jarvis --workspace "/root/.openclaw/workspace/subagents/international_team/jarvis" --model "openrouter/minimax/minimax-m2.1"
sleep 3

echo "📦 启动团队成员..."
for member in xiaomei xiaobian xiaoshu xiaozhen xiaoyan xiaoqu; do
    echo "📦 启动${member}..."
    openclaw agents add $member --workspace "/root/.openclaw/workspace/subagents/international_team/$member" --model "openrouter/minimax/minimax-m2.1"
    sleep 2
done

echo ""
echo "✅ 国际内容团队已启动!"
echo "📊 团队成员: 小美、小编、小数、小据、小研、小趋"
echo "💾 总内存: ~1.8GB"
echo "🌐 覆盖平台: 5个"
echo ""
echo "📝 使用方法:"
echo "   @Jarvis 小美，制定今天的内容计划"
echo "   @Jarvis 小编，审核最新内容"
echo "   @Jarvis 小数，发送早间数据报告"
echo "   @Jarvis 小趋，扫描今日热点"
