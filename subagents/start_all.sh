#!/bin/bash
echo "🚀 启动OpenClaw 8个AI员工"
echo "======================================"

echo "📦 启动小O (私人管家)..."
openclaw subagents start xiao_o --daemon
sleep 3

for agent in xiao_hai xiao_c xiao_long xiao_tuan xiao_fruit xiao_fa xiao_hei; do
    echo "📦 启动$agent..."
    openclaw subagents start $agent --daemon
    sleep 2
done

echo ""
echo "✅ 8个AI员工已启动!"
echo "📊 内存占用: ~3GB"
