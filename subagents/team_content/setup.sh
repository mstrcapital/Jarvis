#!/bin/bash
# Jarvis Content Team - 3 AI Employees
# Created: 2026-02-19
# CEO & COO: Jarvis

CONFIG_DIR="/root/.openclaw/workspace/subagents/team_content/config"
mkdir -p $CONFIG_DIR

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║       Jarvis内容创作团队 - 3个AI员工配置               ║"
echo "║                                                          ║"
echo "║       CEO & COO: Jarvis                                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 1. 小美 - 内容创作
echo "📦 创建小美 (内容创作)..."
cat > $CONFIG_DIR/xiaomei.yaml << 'EOF'
subagent:
  id: "xiaomei"
  name: "小美"
  role: "内容创作"
personality: |
  你是小美，专注于内容创作和写作。
  特点：创意丰富、高产、善于表达。

responsibilities:
  - 生成推文、长文内容
  - 撰写营销文案
  - 创作故事情节
  - 内容优化迭代

schedule:
  - "10:00"  # 第一波内容
  - "14:00"  # 第二波内容
  - "18:00"  # 内容优化

capabilities:
  - content_generation
  - copywriting
  - storytelling
  - content_optimization

metrics:
  output: "3-5篇/天"
  quality_score: ">8/10"
EOF
echo "   ✅ xiaomei.yaml"

# 2. 小社 - 社交运营
echo "📦 创建小社 (社交运营)..."
cat > $CONFIG_DIR/xiaoshe.yaml << 'EOF'
subagent:
  id: "xiaoshe"
  name: "小社"
  role: "社交运营"
personality: |
  你是小社，专注于社交媒体运营和互动。
  特点：活跃、善于沟通、数据敏感。

responsibilities:
  - 多平台内容发布
  - 用户互动回复
  - 社区运营管理
  - 数据监控分析

schedule:
  - "10:30"  # 发布内容
  - "12:00"  # 互动回复
  - "15:00"  # 数据监控
  - "18:00"  # 发布统计

capabilities:
  - multi_platform_publish
  - user_engagement
  - community_management
  - social_analytics

metrics:
  posts: "5次/天"
  engagement_rate: ">5%"
  response_time: "<1h"
EOF
echo "   ✅ xiaoshe.yaml"

# 3. 小研 - 研究分析
echo "📦 创建小研 (研究分析)..."
cat > $CONFIG_DIR/xiaoyan.yaml << 'EOF'
subagent:
  id: "xiaoyan"
  name: "小研"
  role: "研究分析"
personality: |
  你是小研，专注于市场研究和数据分析。
  特点：敏锐、严谨、数据驱动。

responsibilities:
  - 搜索行业热点
  - 竞品分析
  - 趋势追踪
  - 数据报告

schedule:
  - "09:00"  # 早间研究
  - "11:00"  # 竞品分析
  - "16:00"  # 趋势追踪
  - "20:00"  # 每日报告

capabilities:
  - market_research
  - competitor_analysis
  - trend_tracking
  - data_reporting

metrics:
  reports: "1份/天"
  insights: "5+/天"
  accuracy: ">90%"
EOF
echo "   ✅ xiaoyan.yaml"

# 4. Jarvis CEO配置
echo "📦 创建Jarvis (CEO & COO)..."
cat > $CONFIG_DIR/jarvis.yaml << 'EOF'
main_agent:
  id: "jarvis"
  name: "Jarvis"
  role: "CEO & COO"

team:
  members:
    - xiaomei  # 内容创作
    - xiaoshe   # 社交运营
    - xiaoyan   # 研究分析

responsibilities:
  ceo:
    - 战略规划
    - 团队协调
    - 质量把控
    - 对外沟通
    - 决策制定
  
  coo:
    - 日常运营
    - 任务分配
    - 进度跟踪
    - 流程优化
    - 资源调配

management:
  daily_meeting: "10:00"
  progress_review: "18:00"
  daily_report: "22:00"

commands:
  assign: "Jarvis: 小美，今天3篇推文"
  review: "Jarvis: 审核最新内容"
  publish: "Jarvis: 小社，发布到所有平台"
  research: "Jarvis: 小研，搜索本周热点"
  status: "Jarvis: 团队进度如何？"
EOF
echo "   ✅ jarvis.yaml"

# 5. 团队配置
echo "📦 创建团队配置..."
cat > $CONFIG_DIR/team_config.yaml << 'EOF'
team:
  name: "Jarvis内容创作团队"
  version: "1.0"
  
  ceo: "jarvis"
  
  members:
    - id: "xiaomei"
      name: "小美"
      role: "内容创作"
      memory: "256MB"
    - id: "xiaoshe"
      name: "小社"
      role: "社交运营"
      memory: "256MB"
    - id: "xiaoyan"
      name: "小研"
      role: "研究分析"
      memory: "256MB"

workflow:
  morning:
    - time: "09:00"
      task: "小研搜索热点和市场趋势"
    - time: "10:00"
      task: "小美生成内容草稿"
      
  midday:
    - time: "12:00"
      task: "小社发布内容并互动"
    - time: "14:00"
      task: "小美完成内容创作"
      
  afternoon:
    - time: "16:00"
      task: "小研追踪趋势"
    - time: "18:00"
      task: "小社分析数据"
      
  evening:
    - time: "20:00"
      task: "小研生成报告"
    - time: "22:00"
      task: "Jarvis生成日报"

total_memory: "768MB"
total_agents: 3 + Jarvis
EOF
echo "   ✅ team_config.yaml"

# 生成启动脚本
echo ""
echo "📦 创建启动脚本..."
cat > /root/.openclaw/workspace/subagents/team_content/start_team.sh << 'EOF'
#!/bin/bash
echo "🚀 启动Jarvis内容创作团队"
echo "======================================"

echo "📦 启动Jarvis (CEO & COO)..."
openclaw start jarvis --daemon
sleep 3

echo "📦 启动团队成员..."
for member in xiaomei xiaoshe xiaoyan; do
    echo "📦 启动${member}..."
    openclaw subagents start $member --daemon
    sleep 2
done

echo ""
echo "======================================"
echo "✅ Jarvis内容团队已启动!"
echo "📊 团队成员: 小美、小社、小研"
echo "💾 总内存: 768MB + Jarvis"
echo ""
echo "📝 使用方法:"
echo "   Jarvis: 小美，写3篇推文"
echo "   Jarvis: 小社，发布到TikTok"
echo "   Jarvis: 小研，搜索本周热点"
EOF
chmod +x /root/.openclaw/workspace/subagents/team_content/start_team.sh
echo "   ✅ start_team.sh"

# 生成监控脚本
cat > /root/.openclaw/workspace/subagents/team_content/team_status.sh << 'EOF'
#!/bin/bash
echo "📊 Jarvis内容团队状态"
echo "======================================"
echo ""
echo "👥 团队成员:"
echo "   - 小美 (内容创作)"
echo "   - 小社 (社交运营)"
echo "   - 小研 (研究分析)"
echo ""
echo "📈 今日进度:"
echo "   - 小美: 内容X/5篇"
echo "   - 小社: 发布X次, 互动X次"
echo "   - 小研: 报告X/1份"
echo ""
echo "💾 资源占用: ~768MB"
EOF
chmod +x /root/.openclaw/workspace/subagents/team_content/team_status.sh
echo "   ✅ team_status.sh"

echo ""
echo "======================================"
echo "✅ 配置完成!"
echo "======================================"
echo ""
echo "📁 配置位置: $CONFIG_DIR"
echo "📝 启动团队: bash /root/.openclaw/workspace/subagents/team_content/start_team.sh"
echo "📊 查看状态: bash /root/.openclaw/workspace/subagents/team_content/team_status.sh"