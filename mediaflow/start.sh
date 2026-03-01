#!/bin/bash
# MediaFlow 启动脚本
# Created: 2026-02-19

export PYTHONPATH="/root/.openclaw/workspace/mediaflow:$PYTHONPATH"
export PATH="/root/.local/bin:$PATH"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║       🚀 启动 MediaFlow                                           ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "PYTHONPATH: $PYTHONPATH"
echo ""

cd /root/.openclaw/workspace/mediaflow

# 启动后端
echo "启动后端服务..."
echo "访问地址: http://127.0.0.1:8001"
echo ""

python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
