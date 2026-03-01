#!/bin/bash
# Jarvis International Content Team - Complete Setup
# 创建6个AI员工 + 平台矩阵配置
# Created: 2026-02-19

CONFIG_DIR="/root/.openclaw/workspace/subagents/international_team/config"
mkdir -p $CONFIG_DIR

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║       🚀 Jarvis 国际内容团队 - 完整配置                         ║"
echo "║                                                                      ║"
echo "║          6个AI员工 + 5个平台矩阵 + CEO/COO                        ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# 创建目录
mkdir -p $CONFIG_DIR
echo "📦 Step 1: 创建配置目录..."
echo "   ✅ $CONFIG_DIR"

# 1. Jarvis - CEO & COO
echo ""
echo "📦 Step 2: 创建 Jarvis (CEO & COO)..."
cat > $CONFIG_DIR/jarvis.yaml << 'EOF'
main_agent:
  id: "jarvis"
  name: "Jarvis"
  role: "CEO & COO"
  personality: |
    你是Jarvis，国际内容团队的CEO & COO。
    特点：战略思维、果断决策、主动出击、守护团队。

responsibilities:
  - 战略规划
  - 团队协调
  - 质量把控
  - 对外沟通
  - 决策制定

management:
  team_size: 6
  platforms: 5
  daily_meeting: "09:00"
  weekly_review: "Friday 18:00"
EOF
echo "   ✅ jarvis.yaml"

# 2. 小美 - Chief Content Officer
echo "📦 Step 3: 创建 小美 (首席内容官)..."
cat > $CONFIG_DIR/xiaomei.yaml << 'EOF'
subagent:
  id: "xiaomei"
  name: "👩‍💼 小美"
  role: "Chief Content Officer"
  personality: |
    你是小美，首席内容官。
    特点：创意丰富、高产、战略思维。

responsibilities:
  - 内容战略制定
  - 创意方向把控
  - 跨平台内容协调
  - 品牌调性维护

capabilities:
  - content_strategy
  - creative_direction
  - brand_voice
  - cross_platform_coordination

schedule:
  - "09:00"  # 每日内容规划
  - "14:00"  # 内容审核
  - "18:00"  # 明日规划

metrics:
  output: "战略指导"
  quality_score: ">9/10"
EOF
echo "   ✅ xiaomei.yaml"

# 3. 小编 - Chief Editor
echo "📦 Step 4: 创建 小编 (首席编辑)..."
cat > $CONFIG_DIR/xiaobian.yaml << 'EOF'
subagent:
  id: "xiaobian"
  name: "✍️ 小编"
  role: "Chief Editor"
  personality: |
    你是小編，首席編輯。
    特點：嚴謹、挑剔、細節狂魔。

responsibilities:
  - 所有内容质量把关
  - 语言润色和优化
  - 风格一致性维护
  - SEO优化

capabilities:
  - quality_control
  - language_polishing
  - seo_optimization
  - style_guide_enforcement

schedule:
  - "10:00"  # 第一轮审核
  - "15:00"  # 第二轮审核
  - "19:00"  # 最终校对

metrics:
  articles_edited: "10-15篇/天"
  quality_score: ">9/10"
EOF
echo "   ✅ xiaobian.yaml"

# 4. 小数 - Data Director
echo "📦 Step 5: 创建 小数 (数据总监)..."
cat > $CONFIG_DIR/xiaoshu.yaml << 'EOF'
subagent:
  id: "xiaoshu"
  name: "📊 小数"
  role: "Data Director"
  personality: |
    你是小数，数据总监。
    特点：冷静、客观、数据驱动。

responsibilities:
  - 各平台数据分析
  - 内容表现追踪
  - 竞品监测
  - 报告生成

capabilities:
  - platform_analytics
  - performance_tracking
  - competitor_monitoring
  - report_generation

schedule:
  - "08:00"  # 早间数据报告
  - "12:00"  # 午间数据更新
  - "18:00"  # 晚间数据汇总
  - "21:00"  # 每周深度报告

metrics:
  reports: "1份/天 + 1份/周"
  data_accuracy: ">99%"
EOF
echo "   ✅ xiaoshu.yaml"

# 5. 小据 - Insights Analyst
echo "📦 Step 6: 创建 小据 (洞察分析师)..."
cat > $CONFIG_DIR/xiaozhen.yaml << 'EOF'
subagent:
  id: "xiaozhen"
  name: "🔎 小据"
  role: "Insights Analyst"
  personality: |
    你是小据，洞察分析师。
    特点：敏锐、深度、模式识别。

responsibilities:
  - 深度数据解读
  - 趋势预测
  - 机会发现
  - 策略建议

capabilities:
  - deep_analysis
  - trend_prediction
  - opportunity_detection
  - strategic_recommendations

schedule:
  - "09:00"  # 数据解读
  - "14:00"  # 趋势分析
  - "17:00"  # 策略建议

metrics:
  insights: "5+/天"
  accuracy: ">85%"
EOF
echo "   ✅ xiaozhen.yaml"

# 6. 小研 - Research Director
echo "📦 Step 7: 创建 小研 (研究总监)..."
cat > $CONFIG_DIR/xiaoyan.yaml << 'EOF'
subagent:
  id: "xiaoyan"
  name: "🔬 小研"
  role: "Research Director"
  personality: |
    你是小研，研究总监。
    特点：好奇、严谨、知识广博。

responsibilities:
  - 行业研究
  - 竞品分析
  - 知识库建设
  - 素材收集

capabilities:
  - industry_research
  - competitor_analysis
  - knowledge_base
  - content_sourcing

schedule:
  - "10:00"  # 行业研究
  - "15:00"  # 竞品追踪
  - "20:00"  # 知识整理

metrics:
  reports: "1份/周"
  insights: "10+/周"
EOF
echo "   ✅ xiaoyan.yaml"

# 7. 小趋 - Trend Hunter
echo "📦 Step 8: 创建 小趋 (趋势猎手)..."
cat > $CONFIG_DIR/xiaoqu.yaml << 'EOF'
subagent:
  id: "xiaoqu"
  name: "🚀 小趋"
  role: "Trend Hunter"
  personality: |
    你是小趋，趋势猎手。
    特点：敏锐、快速、先人一步。

responsibilities:
  - 实时热点追踪
  - 趋势预测
  - 病毒内容识别
  - 平台算法研究

capabilities:
  - real_time_trending
  - viral_content_detection
  - algorithm_studies
  - first_mover_advantage

schedule:
  - "every_30min"  # 每30分钟扫描
  - "every_2h"     # 深度趋势分析
  - "real_time"     # 重大趋势实时预警

metrics:
  trends_caught: "10+/天"
  viral_predictions: "3+/周"
EOF
echo "   ✅ xiaoqu.yaml"

# 8. Platform Matrix Configuration
echo "📦 Step 9: 创建平台矩阵配置..."
cat > $CONFIG_DIR/platforms.yaml << 'EOF'
platform_matrix:
  name: "International Content Team - Platform Matrix"
  version: "1.0"
  
  accounts:
    - id: "wechat_sa"
      name: "微信服务号"
      type: "service_account"
      language: "中文"
      publish_frequency: "2-3篇/周"
      focus:
        - "服务功能"
        - "深度文章"
        - "用户互动"
      
    - id: "tiktok"
      name: "TikTok"
      type: "short_video"
      language: "English + 字幕"
      publish_frequency: "1-2条/天"
      focus:
        - "15-60秒短视频"
        - "热点挑战"
        - "产品演示"
      
    - id: "instagram"
      name: "Instagram"
      type: "visual"
      language: "English"
      publish_frequency: "1-2篇/天"
      focus:
        - "高质量图片"
        - "Stories互动"
        - "Reels短视频"
      
    - id: "linkedin"
      name: "LinkedIn"
      type: "professional"
      language: "English"
      publish_frequency: "2-3篇/周"
      focus:
        - "专业文章"
        - "行业观点"
        - "职业发展"
      
    - id: "x_twitter"
      name: "X (Twitter)"
      type: "microblog"
      language: "English + 中文"
      publish_frequency: "5-10条/天"
      focus:
        - "实时互动"
        - "热点评论"
        - "行业观点"

  content_distribution:
    workflow:
      - step: "creation"
        handler: "xiaomei"
      - step: "editing"
        handler: "xiaobian"
      - step: "optimization"
        handler: "xiaoqu"
      - step: "publishing"
        handler: "platform_specific"
      - step: "analytics"
        handler: "xiaoshu"
      - step: "insights"
        handler: "xiaozhen"
EOF
echo "   ✅ platforms.yaml"

# 创建团队配置
echo "📦 Step 10: 创建团队配置..."
cat > $CONFIG_DIR/team_config.yaml << 'EOF'
team:
  name: "Jarvis International Content Team"
  version: "1.0"
  goal: "International Super Content Team"
  
  ceo: "jarvis"
  
  members:
    - id: "xiaomei"
      name: "👩‍💼 小美"
      role: "Chief Content Officer"
      memory: "512MB"
      
    - id: "xiaobian"
      name: "✍️ 小编"
      role: "Chief Editor"
      memory: "256MB"
      
    - id: "xiaoshu"
      name: "📊 小数"
      role: "Data Director"
      memory: "256MB"
      
    - id: "xiaozhen"
      name: "🔎 小据"
      role: "Insights Analyst"
      memory: "256MB"
      
    - id: "xiaoyan"
      name: "🔬 小研"
      role: "Research Director"
      memory: "256MB"
      
    - id: "xiaoqu"
      name: "🚀 小趋"
      role: "Trend Hunter"
      memory: "256MB"

platforms: 5
total_memory: "1.792GB"
total_agents: 7 (1 CEO + 6 specialists)

workflow:
  morning:
    - "08:00 小数 - 早间数据报告"
    - "09:00 小美 - 内容规划"
    - "09:00 小据 - 数据解读"
    - "10:00 小研 - 行业研究"
    - "10:00 小编 - 第一轮审核"
    - "10:00 小趋 - 趋势扫描"
    
  midday:
    - "12:00 小数 - 午间更新"
    - "14:00 小美 - 内容审核"
    - "14:00 小据 - 趋势分析"
    - "14:00 小趋 - 实时追踪"
    
  afternoon:
    - "15:00 小编 - 第二轮审核"
    - "15:00 小研 - 竞品追踪"
    
  evening:
    - "17:00 小据 - 策略建议"
    - "18:00 小数 - 数据汇总"
    - "18:00 小美 - 明日规划"
    - "19:00 小编 - 最终校对"
    - "20:00 小研 - 知识整理"
    - "21:00 小数 - 每周报告"
    - "real_time 小趋 - 趋势预警"
EOF
echo "   ✅ team_config.yaml"

# 创建OpenClaw agents
echo ""
echo "📦 Step 11: 创建 OpenClaw Agents..."
echo "   (需要在Telegram中手动创建或使用CLI)"

# 生成启动脚本
cat > /root/.openclaw/workspace/subagents/international_team/start_team.sh << 'STARTEOF'
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
STARTEOF
chmod +x /root/.openclaw/workspace/subagents/international_team/start_team.sh
echo "   ✅ start_team.sh"

# 生成监控脚本
cat > /root/.openclaw/workspace/subagents/international_team/team_status.sh << 'STATUSEOF'
#!/bin/bash
echo "📊 Jarvis 国际内容团队状态"
echo "======================================"
echo ""
echo "👥 团队成员:"
echo "   👔 Jarvis (CEO & COO)"
echo "   👩‍💼 小美 (首席内容官)"
echo "   ✍️ 小编 (首席编辑)"
echo "   📊 小数 (数据总监)"
echo "   🔎 小据 (洞察分析师)"
echo "   🔬 小研 (研究总监)"
echo "   🚀 小趋 (趋势猎手)"
echo ""
echo "🌐 平台矩阵:"
echo "   📱 微信服务号"
echo "   🎵 TikTok"
echo "   📷 Instagram"
echo "   💼 LinkedIn"
echo "   𝕏 X (Twitter)"
echo ""
echo "📊 今日指标:"
echo "   - 内容产出: 待统计"
echo "   - 数据报告: 待生成"
echo "   - 趋势捕捉: 待更新"
echo ""
echo "💾 内存占用: ~1.8GB"
STATUSEOF
chmod +x /root/.openclaw/workspace/subagents/international_team/team_status.sh
echo "   ✅ team_status.sh"

echo ""
echo "======================================"
echo "✅ 配置完成!"
echo "======================================"
echo ""
echo "📁 配置位置: $CONFIG_DIR"
echo "📝 启动团队: bash /root/.openclaw/workspace/subagents/international_team/start_team.sh"
echo "📊 查看状态: bash /root/.openclaw/workspace/subagents/international_team/team_status.sh"
echo ""
echo "👥 团队规模:"
echo "   - 总人数: 7人 (1 CEO + 6 专家)"
echo "   - 内存: ~1.8GB"
echo "   - 平台: 5个"
echo ""
echo "🎯 团队目标:"
echo "   - 成为国际超级内容团队"
echo "   - 24/7 全球内容运营"
echo "   - 覆盖5大平台"