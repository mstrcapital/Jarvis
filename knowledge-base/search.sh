#!/bin/bash
# 搜索知识库

QUERY=$1
if [ -z "$QUERY" ]; then
    echo "用法: ./search.sh <搜索内容>"
    exit 1
fi

echo "🔍 搜索: $QUERY"
echo ""

echo "=== Memory 搜索 ==="
memsearch search "$QUERY" --limit 3 2>&1 | head -25

echo ""
echo "=== Knowledge Base 搜索 ==="
memsearch search "$QUERY" -d /root/.openclaw/workspace/knowledge-base/parsed/ --limit 3 2>&1 | head -25
