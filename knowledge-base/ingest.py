#!/usr/bin/env python3
"""
Knowledge Base Ingestion Script
自动摄取 URL 内容到知识库
"""

import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# 添加 x-reader 到路径
sys.path.insert(0, '/root/.openclaw/workspace/x-reader')

try:
    from reader import read_url
except ImportError:
    print("❌ x-reader 未安装")

KB_DIR = "/root/.openclaw/workspace/knowledge-base"
INBOX_DIR = f"{KB_DIR}/inbox"
PARSED_DIR = f"{KB_DIR}/parsed"

def ingest_url(url: str) -> dict:
    """摄取 URL 内容"""
    print(f"📥 正在摄取: {url}")
    
    try:
        content = read_url(url)
        
        # 保存原始内容
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存到 parsed 目录
        filename = f"{timestamp}_{url_hash}.md"
        filepath = f"{PARSED_DIR}/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {content.get('title', 'Untitled')}\n")
            f.write(f"**Source**: {url}\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n\n")
            f.write(content.get('content', ''))
        
        print(f"✅ 已保存: {filepath}")
        return {"status": "success", "filepath": filepath}
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ingest.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = ingest_url(url)
    print(json.dumps(result, indent=2))
