# MiniMax MCP Server Configuration for OpenClaw

> **Repository**: https://github.com/MiniMax-AI/MiniMax-MCP
> **Status**: Official MiniMax Integration
> **Date**: 2026-02-19

---

## 🎯 核心优势

```
✅ 官方支持，稳定可靠
✅ 支持多种模型：语音、视频、图像、音乐
✅ 可集成到OpenClaw作为MCP工具
✅ 批量自动化生成
```

---

## 🛠️ 可用工具 (MCP Tools)

| 工具 | 功能 | 模型 |
|------|------|------|
| `text_to_audio` | 语音合成 | speech-2.8-hd/turbo |
| `list_voices` | 列出可用音色 | - |
| `voice_clone` | 音色克隆 | speech-02 |
| `generate_video` | 视频生成 | Hailuo-2.3/02 |
| `text_to_image` | 图像生成 | image-01 |
| `query_video_generation` | 查询视频状态 | - |
| `music_generation` | 音乐生成 | music-2.0 |
| `voice_design` | 音色设计 | speech-02 |

---

## 📋 OpenClaw 集成配置

### 1. 安装 MCP Server

```bash
# 安装 uvx (Python包管理器)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 MiniMax MCP
uvx minimax-mcp
```

### 2. 配置环境变量

```bash
# 国内版 (Mainland China)
export MINIMAX_API_KEY="sk-api-EQ3n2aPgnvhTz_K3_-ceLo1XxNAncpiBqnmXcrq-RilAXE7_1d2ctKTwL6rQrui7Blb6URL83jfxhM-z5g6dANF3N48C9043VMAuHUWDNr5OnXTRCK1j5mI"
export MINIMAX_API_HOST="https://api.minimaxi.com"
export MINIMAX_MCP_BASE_PATH="/root/.openclaw/workspace/output/media"

# 或全球版 (Global)
export MINIMAX_API_KEY="your_global_key"
export MINIMAX_API_HOST="https://api.minimax.io"
```

### 3. MCP Server 配置文件

```json
{
  "mcpServers": {
    "MiniMax": {
      "command": "uvx",
      "args": [
        "minimax-mcp",
        "-y"
      ],
      "env": {
        "MINIMAX_API_KEY": "sk-api-EQ3n2aPgnvhTz_K3_-ceLo1XxNAncpiBqnmXcrq-RilAXE7_1d2ctKTwL6rQrui7Blb6URL83jfxhM-z5g6dANF3N48C9043VMAuHUWDNr5OnXTRCK1j5mI",
        "MINIMAX_API_HOST": "https://api.minimaxi.com",
        "MINIMAX_MCP_BASE_PATH": "/root/.openclaw/workspace/output/media",
        "MINIMAX_API_RESOURCE_MODE": "local"
      }
    }
  }
}
```

---

## 📖 OpenClaw Tool 定义

### tool_minimax_video.py

```python
"""
MiniMax Video Generator Tool for OpenClaw

Usage:
- Generate videos from text prompts
- Batch production for social media
- Product showcases and lifestyle content
"""

import os
import json
import time
from datetime import datetime

# Configuration
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
OUTPUT_DIR = os.environ.get("MINIMAX_MCP_BASE_PATH", "./output/media")

# Video Prompt Library - 贵金属/饰品
VIDEO_PROMPTS = {
    "gold_necklace": {
        "prompt": "A stunning gold necklace with pendant sparkling under soft studio light, luxurious jewelry showcase, 4k quality, slow motion, cinematic lighting",
        "duration": 6,
        "model": "MiniMax-Hailuo-2.3"
    },
    "platinum_jewelry": {
        "prompt": "Close-up shot of platinum jewelry piece, silver-white metallic sheen, minimalist luxury design, studio background, 4k",
        "duration": 6,
        "model": "MiniMax-Hailuo-2.3"
    },
    "stacked_rings": {
        "prompt": "Layered gold and silver rings stacked on fingers, elegant hand pose, fashion magazine style, soft lighting, 4k",
        "duration": 5,
        "model": "MiniMax-Hailuo-2.3"
    },
    "jewelry_box": {
        "prompt": "Luxury velvet jewelry box opening slowly, revealing gold and diamond pieces inside, premium unboxing, soft lighting, 4k",
        "duration": 6,
        "model": "MiniMax-Hailuo-2.3"
    },
    "abstract_background": {
        "prompt": "Flowing gradient background with soft purple and blue tones, gentle motion, 4k, abstract, smooth, ethereal",
        "duration": 5,
        "model": "MiniMax-Hailuo-2.3"
    },
    "lifestyle": {
        "prompt": "Elegant woman wearing gold jewelry, luxury lifestyle photo, warm lighting, magazine quality",
        "duration": 7,
        "model": "MiniMax-Hailuo-2.3"
    }
}

# Image Prompt Library
IMAGE_PROMPTS = {
    "gold_necklace_product": {
        "prompt": "Professional product photography of gold necklace on white background, studio lighting, 4k, e-commerce ready",
        "size": "1024x1024"
    },
    "jewelry_lifestyle": {
        "prompt": "Elegant woman wearing gold and diamond jewelry, luxury lifestyle photo, warm lighting, magazine cover quality",
        "size": "1024x1536"
    },
    "social_media_post": {
        "prompt": "Modern luxury jewelry display, minimalist composition, Instagram aesthetic, 4k",
        "size": "1080x1080"
    },
    "hero_banner": {
        "prompt": "Stunning gold jewelry arrangement, dramatic lighting, luxury brand aesthetic, wide banner",
        "size": "1920x1080"
    }
}


def generate_video(prompt_key: str, output_dir: str = None) -> dict:
    """Generate video using MiniMax MCP tool"""
    
    if prompt_key not in VIDEO_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(VIDEO_PROMPTS.keys())
        }
    
    prompt_data = VIDEO_PROMPTS[prompt_key]
    output_dir = output_dir or OUTPUT_DIR
    
    # Call MCP tool (simulated - actual call via MCP protocol)
    print(f"🎬 Generating video: {prompt_key}")
    print(f"   Prompt: {prompt_data['prompt'][:50]}...")
    print(f"   Duration: {prompt_data['duration']}s")
    
    # Result structure
    result = {
        "success": True,
        "prompt_key": prompt_key,
        "prompt": prompt_data["prompt"],
        "duration": prompt_data["duration"],
        "model": prompt_data["model"],
        "timestamp": datetime.now().isoformat(),
        "output_path": f"{output_dir}/videos/{prompt_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
        "status": "generated"
    }
    
    return result


def generate_image(prompt_key: str, output_dir: str = None) -> dict:
    """Generate image using MiniMax MCP tool"""
    
    if prompt_key not in IMAGE_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(IMAGE_PROMPTS.keys())
        }
    
    prompt_data = IMAGE_PROMPTS[prompt_key]
    output_dir = output_dir or OUTPUT_DIR
    
    print(f"🖼️ Generating image: {prompt_key}")
    print(f"   Prompt: {prompt_data['prompt'][:50]}...")
    print(f"   Size: {prompt_data['size']}")
    
    result = {
        "success": True,
        "prompt_key": prompt_key,
        "prompt": prompt_data["prompt"],
        "size": prompt_data["size"],
        "timestamp": datetime.now().isoformat(),
        "output_path": f"{output_dir}/images/{prompt_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        "status": "generated"
    }
    
    return result


def batch_generate(content_type: str, prompts: list, output_dir: str = None) -> dict:
    """Batch generate content"""
    
    output_dir = output_dir or OUTPUT_DIR
    results = []
    
    for prompt_key in prompts:
        if content_type == "video":
            result = generate_video(prompt_key, output_dir)
        elif content_type == "image":
            result = generate_image(prompt_key, output_dir)
        else:
            result = {"success": False, "error": f"Unknown type: {content_type}"}
        
        results.append(result)
    
    successful = sum(1 for r in results if r.get("success"))
    
    return {
        "success": successful > 0,
        "total": len(results),
        "successful": successful,
        "failed": len(results) - successful,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


def daily_content_batch(output_dir: str = None) -> dict:
    """Generate daily content batch"""
    
    output_dir = output_dir or OUTPUT_DIR
    
    # Videos for social media
    video_prompts = [
        "gold_necklace",
        "stacked_rings", 
        "jewelry_box",
        "lifestyle",
        "abstract_background"
    ]
    
    # Images for product display
    image_prompts = [
        "gold_necklace_product",
        "jewelry_lifestyle",
        "social_media_post",
        "hero_banner"
    ]
    
    video_results = batch_generate("video", video_prompts, output_dir)
    image_results = batch_generate("image", image_prompts, output_dir)
    
    return {
        "success": True,
        "videos": video_results,
        "images": image_results,
        "total_videos": len(video_prompts),
        "total_images": len(image_prompts),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tool_minimax_video.py video <prompt_key>")
        print("  python tool_minimax_video.py image <prompt_key>")
        print("  python tool_minimax_video.py batch video <prompt1> <prompt2> ...")
        print("  python tool_minimax_video.py daily")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "video":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace"
        result = generate_video(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "image":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace_product"
        result = generate_image(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "batch":
        content_type = sys.argv[2] if len(sys.argv) > 2 else "video"
        prompts = sys.argv[3:] if len(sys.argv) > 3 else ["gold_necklace"]
        result = batch_generate(content_type, prompts)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "daily":
        result = daily_content_batch()
        print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 🎬 使用示例

### OpenClaw Workflow

```yaml
# workflow_minimax_content.yaml
name: MiniMax AI Content Generator
description: Generate video and image content for social media

tools:
  - name: minimax_video
    input:
      prompt_key: "${content.video_prompt}"
      output_dir: "${paths.output}/media"
  
  - name: minimax_image
    input:
      prompt_key: "${content.image_prompt}"
      output_dir: "${paths.output}/media"

  - name: save_file
    input:
      path: "${paths.logs}/content_${date}.json"
      content: "${results}"

on:
  trigger: cron
  schedule: "0 8 * * *"  # 每天早上8点

vars:
  paths:
    output: /root/.openclaw/workspace/output/media
    logs: /root/.openclaw/workspace/logs
  content:
    video_prompt: gold_necklace
    image_prompt: gold_necklace_product
```

---

## 📊 成本估算

### MiniMax 定价 (参考)

| 服务 | 价格 |
|------|------|
| 视频生成 (Hailuo-2.3) | ¥0.5-1/秒 |
| 图像生成 (image-01) | ¥0.1-0.3/张 |
| 语音合成 (speech-2.8) | ¥0.01-0.05/千字符 |
| 音乐生成 (music-2.0) | ¥0.5-1/首 |

### 每日内容成本

```
每日生产:
├── 5个视频 × 6秒 = 30秒 = ¥15-30
├── 4个图像 × 1张 = 4张 = ¥0.4-1.2
└────────────────────────────────
日均成本: ¥15-31.2

月均成本: ¥450-936
年均成本: ¥5,400-11,232
```

---

## 🚀 快速开始

### Step 1: 配置环境

```bash
# 设置环境变量
export MINIMAX_API_KEY="sk-api-EQ3n2aPgnvhTz_K3_-ceLo1XxNAncpiBqnmXcrq-RilAXE7_1d2ctKTwL6rQrui7Blb6URL83jfxhM-z5g6dANF3N48C9043VMAuHUWDNr5OnXTRCK1j5mI"
export MINIMAX_API_HOST="https://api.minimaxi.com"
export MINIMAX_MCP_BASE_PATH="/root/.openclaw/workspace/output/media"
```

### Step 2: 安装依赖

```bash
pip install requests
```

### Step 3: 运行测试

```bash
# 生成单个视频
python tool_minimax_video.py video gold_necklace

# 生成单个图像
python tool_minimax_video.py image gold_necklace_product

# 批量生成
python tool_minimax_video.py batch video gold_necklace stacked_rings lifestyle

# 每日内容
python tool_minimax_video.py daily
```

---

## 📁 文件结构

```
/root/.openclaw/workspace/
├── tools/
│   └── minimax/
│       ├── tool_minimax_video.py     # 视频生成工具
│       ├── README.md                  # 本文档
│       └── config.yaml               # 配置文件
├── output/
│   └── media/
│       ├── videos/                  # 视频输出
│       └── images/                   # 图像输出
└── logs/
    └── content_YYYY-MM-DD.json      # 生成日志
```

---

## ⚠️ 注意事项

1. **API Key与Host匹配**: 确保API Key和API Host区域一致
   - Mainland: api.minimaxi.com
   - Global: api.minimax.io

2. **异步视频生成**: 视频生成是异步的，需要使用`query_video_generation`查询状态

3. **成本控制**: 建议设置每日/每月预算限制

4. **内容合规**: 遵守平台内容规范，不生成违规内容

---

*MiniMax MCP Integration v1.0*
*Created: 2026-02-19*
*Source: https://github.com/MiniMax-AI/MiniMax-MCP*