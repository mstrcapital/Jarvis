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
