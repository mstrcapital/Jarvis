#!/bin/bash
# OpenClaw Sub-Agent System Setup
# Created: 2026-02-19

echo "🚀 OpenClaw 8个AI员工系统配置"
echo "======================================"
echo ""

# Create config directory
CONFIG_DIR="/root/.openclaw/workspace/subagents/config"
mkdir -p $CONFIG_DIR

echo "📦 Step 1: 创建1M上下文配置..."
cat > /root/.openclaw/workspace/subagents/1m_context_config.yaml << 'EOF'
models:
  anthropic:
    params:
      context1m: true
agents:
  default:
    params:
      context1m: true
subagents:
  enabled: true
  max_subagents: 8
EOF
echo "   ✅ 1m_context_config.yaml"

echo ""
echo "📦 Step 2: 创建8个AI员工配置..."

# Create 8 agent configs
AGENTS=(
    "xiao_o:小O:私人管家:512MB:08:00,22:00"
    "xiao_hai:小海:出海研究:512MB:09:00,every4h"
    "xiao_c:小C:内容运营:512MB:10:00,14:00,18:00"
    "xiao_long:小龙:社区管理:256MB:24h"
    "xiao_tuan:小团:团队管理:256MB:08:30,hourly"
    "xiao_fruit:小果:iOS开发:512MB:09:30,as_needed"
    "xiao_fa:小法:法律顾问:256MB:08:00,weekly"
    "xiao_hei:小黑:黑科技情报:512MB:09:00,15:00"
)

for item in "${AGENTS[@]}"; do
    IFS=':' read -r name cn role memory schedule <<< "$item"
    
    cat > "$CONFIG_DIR/$name.yaml" << EOF
subagent:
  id: "$name"
  name: "$cn"
  role: "$role"
memory:
  limit: "$memory"
  isolation: true
schedule:
  - "$schedule"
capabilities:
  - task_coordination
  - progress_tracking
EOF
    
    echo "   ✅ $name.yaml ($cn - $role)"
done

echo ""
echo "📦 Step 3: 创建启动脚本..."
cat > /root/.openclaw/workspace/subagents/start_all.sh << 'STARTEOF'
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
STARTEOF
chmod +x /root/.openclaw/workspace/subagents/start_all.sh
echo "   ✅ start_all.sh"

echo ""
echo "📦 Step 4: 创建监控脚本..."
cat > /root/.openclaw/workspace/subagents/monitor.sh << 'MONITOREOF'
#!/bin/bash
echo "📊 OpenClaw Sub-Agent Monitor"
echo "======================================"
echo ""
echo "📦 子Agent状态:"
openclaw subagents status
echo ""
echo "💾 资源占用:"
openclaw subagents resources
echo ""
echo "🏥 健康检查:"
openclaw subagents health
MONITOREOF
chmod +x /root/.openclaw/workspace/subagents/monitor.sh
echo "   ✅ monitor.sh"

echo ""
echo "======================================"
echo "✅ 配置完成!"
echo "======================================"
echo ""
echo "📁 配置文件位置: $CONFIG_DIR"
echo "📊 8个AI员工已配置"
echo "💾 总内存占用: 3GB"
echo ""
echo "📝 使用方法:"
echo "   启动: bash /root/.openclaw/workspace/subagents/start_all.sh"
echo "   监控: bash /root/.openclaw/workspace/subagents/monitor.sh"