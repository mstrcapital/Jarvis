#!/bin/bash
# 快速添加 URL 到知识库

URL=$1
if [ -z "$URL" ]; then
    echo "用法: ./add.sh <URL>"
    exit 1
fi

echo "📥 摄取: $URL"

# 使用 x-reader
x-reader "$URL" 2>&1 | tail -5

# 索引更新
memsearch index /root/.openclaw/workspace/knowledge-base/parsed/ 2>&1
memsearch index /root/.openclaw/workspace/memory/ 2>&1

echo "✅ 完成！"
