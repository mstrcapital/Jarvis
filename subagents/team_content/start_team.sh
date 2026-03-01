#!/bin/bash
# Jarvis内容创作团队 - 正确启动脚本
# Created: 2026-02-19

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║       🚀 启动 Jarvis 内容创作团队                      ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 检查Gateway状态
echo "📡 检查Gateway状态..."
if ! openclaw gateway status 2>/dev/null | grep -q "running"; then
    echo "   🔄 启动Gateway..."
    openclaw gateway start
    sleep 5
fi
echo "   ✅ Gateway运行中"
echo ""

# 创建团队成员 (isolated agents)
echo "👥 创建团队成员..."
echo "======================================"

# 1. 小美 - 内容创作
echo "📦 创建小美 (内容创作)..."
openclaw agents add xiaomei \
  --workspace "/root/.openclaw/workspace/subagents/team_content/xiaomei" \
  --model "openrouter/minimax/minimax-m2.1"
echo "   ✅ xiaomei 创建完成"

# 2. 小社 - 社交运营
echo "📦 创建小社 (社交运营)..."
openclaw agents add xiaoshe \
  --workspace "/root/.openclaw/workspace/subagents/team_content/xiaoshe" \
  --model "openrouter/minimax/minimax-m2.1"
echo "   ✅ xiaoshe 创建完成"

# 3. 小研 - 研究分析
echo "📦 创建小研 (研究分析)..."
openclaw agents add xiaoyan \
  --workspace "/root/.openclaw/workspace/subagents/team_content/xiaoyan" \
  --model "openrouter/minimax/minimax-m2.1"
echo "   ✅ xiaoyan 创建完成"

echo ""
echo "======================================"
echo "✅ 团队成员创建完成!"
echo ""

# 配置定时任务
echo "⏰ 定时任务:"
echo "   小美: 10:00, 14:00, 18:00 (内容创作)"
echo "   小社: 10:30, 12:00, 15:00, 18:00 (社交运营)"
echo "   小研: 09:00, 11:00, 16:00, 20:00 (研究分析)"
echo ""

# 验证配置
echo "📊 验证团队配置..."
openclaw agents list
echo ""

echo "======================================"
echo "✅ Jarvis 内容创作团队已就绪!"
echo "======================================"
echo ""
echo "📝 使用方法:"
echo ""
echo "1️⃣  启动团队成员:"
echo "   openclaw agents list"
echo ""
echo "2️⃣  通过Telegram分配任务:"
echo "   @Jarvis 小美，写3篇推文"
echo "   @Jarvis 小社，发布到TikTok"
echo "   @Jarvis 小研，搜索本周热点"
echo ""
echo "3️⃣  使用子Agent系统:"
echo "   /subagents spawn xiaomei"
echo "   /subagents spawn xiaoshe"
echo "   /subagents spawn xiaoyan"
echo ""
echo "4️⃣  CLI管理:"
echo "   openclaw agents list           # 列出"
echo "   openclaw agents delete xiaomei # 删除"
echo ""

echo "💾 内存占用: ~768MB"