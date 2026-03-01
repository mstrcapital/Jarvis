#!/bin/bash
# Jarvis International Content Team - Add YouTube Focus
# YouTube Ad Revenue Specialist Configuration
# Created: 2026-02-19

CONFIG_DIR="/root/.openclaw/workspace/subagents/international_team/config"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║       🎬 添加 YouTube - 广告分成收益                              ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 1. Update platforms.yaml
echo "📦 Step 1: 更新平台矩阵..."
cat > $CONFIG_DIR/platforms.yaml << 'EOF'
platform_matrix:
  name: "International Content Team - Platform Matrix v1.1"
  version: "1.1"
  last_updated: "2026-02-19"

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

    # NEW: YouTube - Ad Revenue Focus
    - id: "youtube"
      name: "YouTube"
      type: "long_video"
      language: "English + 中文"
      publish_frequency: "3-5条/周"
      focus:
        - "中长视频内容"
        - "广告分成收益"
        - "观众增长"
      monetization:
        enabled: true
        type: "ad_revenue"
        requirements:
          - "1000 subscribers"
          - "4000 watch hours"
          - "符合YouTube政策"
      content_strategy:
        video_length: "8-20分钟"
        upload_schedule:
          - "Monday"
          - "Wednesday"
          - "Friday"
        content_types:
          - "行业深度分析"
          - "教程和指南"
          - "产品评测"
          - "趋势解读"
          - "幕后故事"
        optimization:
          - "SEO优化标题"
          - "吸引人缩略图"
          - "前3秒钩子"
          - "行动号召CTA"
          - "end_screen推广"

  content_distribution:
    workflow:
      - step: "creation"
        handler: "xiaomei"
      - step: "editing"
        handler: "xiaobian"
      - step: "video_production"
        handler: "xiaomei"
      - step: "optimization"
        handler: "xiaoqu"
      - step: "publishing"
        handler: "platform_specific"
      - step: "analytics"
        handler: "xiaoshu"
      - step: "insights"
        handler: "xiaozhen"
EOF
echo "   ✅ platforms.yaml (v1.1 - YouTube Added)"

# 2. Create YouTube Revenue Specialist Role
echo ""
echo "📦 Step 2: 创建YouTube收益专员..."

# Add YouTube capabilities to 小美 (as Content Officer handles video)
cat > $CONFIG_DIR/youtube_strategy.yaml << 'EOF'
youtube_strategy:
  id: "youtube_revenue"
  name: "YouTube广告分成策略"
  version: "1.0"
  focus: "ad_revenue"
  
  monetization:
    enabled: true
    
    requirements:
      - "1000 subscribers (1000订阅)"
      - "4000 watch hours (4000观看时长)"
      - "符合YouTube合作计划政策"
    
    revenue_streams:
      - "display_ads (展示广告)"
      - "overlay_ads (-overlay广告)"
      - "video_ads (视频广告)"
      - "shorts_ads (短视频广告)"
      - "memberships (会员)"
      - "super_chat (超级聊天)"
      - "merchandise_shelf (商品架)"
  
  content_strategy:
    video_length: "8-20分钟"
    optimal_length: "12-15分钟 (广告位最多)"
    
    upload_schedule:
      - "Monday 12:00 UTC"  # 最佳发布时间
      - "Wednesday 12:00 UTC"
      - "Friday 12:00 UTC"
    
    content_pillars:
      - name: "行业深度分析"
        frequency: "1-2/周"
        length: "15-20分钟"
        cpm_potential: "高"
      
      - name: "教程和指南"
        frequency: "1/周"
        length: "10-15分钟"
        cpm_potential: "中高"
      
      - name: "产品评测"
        frequency: "1-2/周"
        length: "8-12分钟"
        cpm_potential: "中"
      
      - name: "趋势解读"
        frequency: "2-3/周"
        length: "5-10分钟"
        cpm_potential: "中"
      
      - name: "幕后故事"
        frequency: "1/周"
        length: "8-15分钟"
        cpm_potential: "低-中"
  
  optimization:
    pre_upload:
      - "SEO优化标题 (60字符内)"
      - "吸引人缩略图 (1280x720)"
      - "关键词标签 (30个)"
      - "详细描述 (前150字最重要)"
      - "字幕和闭路字幕"
    
    video_elements:
      - "前3秒钩子 (hook)"
      - "章节标记 (chapters)"
      - "end_screen推广"
      - "卡片 (cards)"
      - "行动号召CTA"
    
    post_upload:
      - "分享到其他平台"
      - "社区帖子互动"
      - "回复评论"
      - "分析首24小时数据"
  
  analytics:
    key_metrics:
      - "RPM (每千次展示收入)"
      - "CPM (每千次展示成本)"
      - "观看时长"
      - "订阅转化率"
      - "点击率CTR"
      - "平均观看百分比"
    
    tools:
      - "YouTube Studio"
      - "Social Blade"
      - "Google Analytics"
  
  growth_strategy:
    short_term:
      - "每周3-5个视频"
      - "优化前3秒"
      - "增加观众停留"
      - "鼓励订阅和点赞"
    
    mid_term:
      - "建立内容系列"
      - "与合作者交叉推广"
      - "优化缩略图点击率"
      - "分析高表现视频"
    
    long_term:
      - "达到1000订阅"
      - "达到4000观看时长"
      - "申请合作计划"
      - "多元化收入来源"
EOF
echo "   ✅ youtube_strategy.yaml"

# 3. Update team_config.yaml
echo ""
echo "📦 Step 3: 更新团队配置..."
cat > $CONFIG_DIR/team_config.yaml << 'EOF'
team:
  name: "Jarvis International Content Team"
  version: "1.1"
  goal: "International Super Content Team - With YouTube Ad Revenue"
  last_updated: "2026-02-19"
  
  ceo: "jarvis"
  
  members:
    - id: "xiaomei"
      name: "👩‍💼 小美"
      role: "Chief Content Officer"
      memory: "512MB"
      youtube_role: "视频内容策划"
      
    - id: "xiaobian"
      name: "✍️ 小编"
      role: "Chief Editor"
      memory: "256MB"
      youtube_role: "视频脚本审核"
      
    - id: "xiaoshu"
      name: "📊 小数"
      role: "Data Director"
      memory: "256MB"
      youtube_role: "YouTube数据分析"
      
    - id: "xiaozhen"
      name: "🔎 小据"
      role: "Insights Analyst"
      memory: "256MB"
      youtube_role: "视频表现洞察"
      
    - id: "xiaoyan"
      name: "🔬 小研"
      role: "Research Director"
      memory: "256MB"
      youtube_role: "行业视频研究"
      
    - id: "xiaoqu"
      name: "🚀 小趋"
      role: "Trend Hunter"
      memory: "256MB"
      youtube_role: "热门视频趋势"

platforms: 6
total_memory: "~2.0GB"
total_agents: 7 (1 CEO + 6 specialists)

youtube_focus:
  goal: "广告分成收益"
  target_subscribers: 1000
  target_watch_hours: 4000
  monetization_status: "待激活"
  
  content_plan:
    - "3-5个视频/周"
    - "8-20分钟/视频"
    - "8-15个广告位/视频"
    
  revenue_targets:
    - month_1: "$0 (冷启动)"
    - month_3: "$50-100 (达到要求)"
    - month_6: "$500-1000 (稳定增长)"
    - month_12: "$2000-5000 (规模化)"

workflow:
  youtube_pipeline:
    - step: "选题策划"
      handler: "xiaomei"
      output: "内容日历"
      
    - step: "脚本创作"
      handler: "xiaomei"
      output: "视频脚本"
      
    - step: "脚本审核"
      handler: "xiaobian"
      output: "审核反馈"
      
    - step: "视频制作"
      handler: "external"
      output: "成品视频"
      
    - step: "上传优化"
      handler: "xiaomei"
      output: "优化后的元数据"
      
    - step: "发布推广"
      handler: "xiaoshu"
      output: "推广计划"
      
    - step: "数据分析"
      handler: "xiaoshu"
      output: "表现报告"
      
    - step: "洞察优化"
      handler: "xiaozhen"
      output: "优化建议"
EOF
echo "   ✅ team_config.yaml (v1.1 - YouTube Added)"

# 4. Create YouTube Daily Workflow
echo ""
echo "📦 Step 4: 创建YouTube工作流..."

cat > $CONFIG_DIR/youtube_workflow.yaml << 'EOF'
youtube_daily_workflow:
  platform: "YouTube"
  focus: "Ad Revenue"
  version: "1.0"
  
  schedule:
    daily:
      - "09:00 - 检查前一天视频数据"
      - "10:00 - 竞品YouTube分析"
      - "11:00 - 脚本创作/优化"
      - "14:00 - 缩略图和标题优化"
      - "15:00 - 社区帖子互动"
      - "17:00 - 回复评论"
      
    weekly:
      - "Monday 10:00 - 本周内容计划"
      - "Monday 15:00 - 视频1上传"
      - "Wednesday 10:00 - 视频2策划"
      - "Wednesday 15:00 - 视频2上传"
      - "Friday 10:00 - 周末内容准备"
      - "Friday 15:00 - 视频3上传"
      - "Sunday 18:00 - 本周数据分析"
  
  content_calendar:
    monday:
      - "行业深度分析 (15-20分钟)"
      - "SEO优化标题"
      - "详细描述 + 关键词"
      
    wednesday:
      - "教程和指南 (10-15分钟)"
      - "缩略图A/B测试"
      - "章节标记"
      
    friday:
      - "产品评测或趋势解读 (8-12分钟)"
      - "CTA行动号召"
      - "end_screen推广"
  
  monetization_checklist:
    - "订阅数: ___/1000"
    - "观看时长: ___/4000"
    - "视频数: ___"
    - "最后更新时间: ___"
  
  key_apis:
    - "YouTube Data API v3"
    - "YouTube Analytics API"
    - "Social Blade API"
EOF
echo "   ✅ youtube_workflow.yaml"

# 5. Update README
echo ""
echo "📦 Step 5: 更新文档..."

cat >> /root/.openclaw/workspace/subagents/international_team/TEAM_README.md << 'EOF'

---

## 🎬 YouTube - 广告分成收益

### 平台信息

| 属性 | 值 |
|------|-----|
| 平台 | YouTube |
| 类型 | 长视频 |
| 语言 | English + 中文 |
| 频率 | 3-5条/周 |
| 目标 | 广告分成收益 |
| 时长 | 8-20分钟 |

### 变现要求

```
需要达到:
├── 1000 订阅者
├── 4000 观看时长 (小时)
└── 符合YouTube合作计划政策
```

### 内容策略

| 内容类型 | 频率 | 时长 | CPM潜力 |
|---------|------|------|--------|
| 行业深度分析 | 1-2/周 | 15-20分钟 | 高 |
| 教程和指南 | 1/周 | 10-15分钟 | 中高 |
| 产品评测 | 1-2/周 | 8-12分钟 | 中 |
| 趋势解读 | 2-3/周 | 5-10分钟 | 中 |
| 幕后故事 | 1/周 | 8-15分钟 | 低-中 |

### 收入目标

| 时间点 | 目标收入 | 里程碑 |
|--------|---------|---------|
| 第1个月 | $0 | 冷启动 |
| 第3个月 | $50-100 | 达到变现要求 |
| 第6个月 | $500-1000 | 稳定增长 |
| 第12个月 | $2000-5000 | 规模化 |

### 优化技巧

**上传前**:
- SEO优化标题 (60字符内)
- 吸引人缩略图 (1280x720)
- 关键词标签 (30个)
- 详细描述 (前150字最重要)
- 字幕和闭路字幕

**视频中**:
- 前3秒钩子 (hook)
- 章节标记 (chapters)
- end_screen推广
- 卡片 (cards)
- 行动号召CTA

**上传后**:
- 分享到其他平台
- 社区帖子互动
- 回复评论
- 分析首24小时数据

### 关键指标

```
- RPM (每千次展示收入)
- CPM (每千次展示成本)
- 观看时长
- 订阅转化率
- 点击率CTR
- 平均观看百分比
```

### 新增配置文件

```
├── youtube_strategy.yaml     # YouTube策略
├── youtube_workflow.yaml   # 工作流
└── platforms.yaml (已更新)  # 添加YouTube
```

### 团队协作

```
选题策划 → 脚本创作 → 脚本审核 → 视频制作 → 上传优化 → 发布推广 → 数据分析 → 洞察优化
   小美        小美        小编        外部       小美        小数       小数        小据
```

### 使用示例

```
@Jarvis 小美，为YouTube策划本周3个视频
@Jarvis 小数，YouTube上周数据分析
@Jarvis 小趋，找出热门YouTube视频趋势
@Jarvis 小编，审核这个YouTube脚本
@Jarvis 小据，哪类视频CPM最高？
```

EOF
echo "   ✅ TEAM_README.md (YouTube章节已添加)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ YouTube广告分成收益已添加!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 更新内容:"
echo ""
echo "   ✅ platforms.yaml (v1.1) - YouTube平台配置"
echo "   ✅ youtube_strategy.yaml - YouTube变现策略"
echo "   ✅ youtube_workflow.yaml - YouTube工作流"
echo "   ✅ team_config.yaml (v1.1) - 团队配置更新"
echo "   ✅ TEAM_README.md - 文档更新"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📈 YouTube统计:"
echo ""
echo "   🎯 目标: 广告分成收益"
echo "   📊 平台数: 6个 (新增YouTube)"
echo "   💾 内存: ~2.0GB"
echo "   📅 内容频率: 3-5个视频/周"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💰 收入里程碑:"
echo ""
echo "   第1个月: $0 (冷启动)"
echo "   第3个月: $50-100 (达到1000订阅 + 4000时长)"
echo "   第6个月: $500-1000 (稳定增长)"
echo "   第12个月: $2000-5000 (规模化)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"