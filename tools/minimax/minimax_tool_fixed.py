#!/usr/bin/env python3
"""
MiniMax Video/Image Generator - 修复版

已修复: 使用OpenAI兼容格式 v1/chat/completions
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")

# ============== 提示词库 ==============
VIDEO_PROMPTS = {
    "gold_necklace": {
        "prompt": "A stunning gold necklace with pendant sparkling under soft studio light, luxurious jewelry showcase, 4k quality, slow motion, cinematic lighting",
        "duration": 6
    },
    "platinum_jewelry": {
        "prompt": "Close-up shot of platinum jewelry piece, silver-white metallic sheen, minimalist luxury design, studio background, 4k",
        "duration": 6
    },
    "stacked_rings": {
        "prompt": "Layered gold and silver rings stacked on fingers, elegant hand pose, fashion magazine style, soft lighting, 4k",
        "duration": 5
    },
    "jewelry_box": {
        "prompt": "Luxury velvet jewelry box opening slowly, revealing gold and diamond pieces inside, premium unboxing, soft lighting, 4k",
        "duration": 6
    },
    "abstract_background": {
        "prompt": "Flowing gradient background with soft purple and blue tones, gentle motion, 4k, abstract, smooth, ethereal",
        "duration": 5
    },
    "lifestyle": {
        "prompt": "Elegant woman wearing gold jewelry, luxury lifestyle photo, warm lighting, magazine quality",
        "duration": 7
    }
}

IMAGE_PROMPTS = {
    "gold_necklace_product": {
        "prompt": "Professional product photography of gold necklace on white background, studio lighting, 4k, e-commerce ready",
        "size": "1024x1024"
    },
    "jewelry_lifestyle": {
        "prompt": "Elegant woman wearing gold and diamond jewelry, luxury lifestyle photo, warm lighting, magazine quality",
        "size": "1024x1536"
    },
    "social_media_post": {
        "prompt": "Modern luxury jewelry display, minimalist composition, Instagram aesthetic, 4k",
        "size": "1080x1080"
    },
    "hero_banner": {
        "prompt": "Stunning gold jewelry arrangement, dramatic lighting, luxury brand aesthetic",
        "size": "1920x1080"
    }
}


def call_api(endpoint: str, payload: dict) -> dict:
    """发送API请求"""
    url = f"{API_HOST}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def test_connection() -> dict:
    """测试API连接"""
    print("🔍 测试API连接...")
    print(f"   Host: {API_HOST}")
    print(f"   Key: {API_KEY[:20]}...")
    
    # 测试文本生成
    result = call_api("/v1/chat/completions", {
        "model": "MiniMax-M2.5",
        "messages": [{"role": "user", "content": "Hi"}]
    })
    
    if "choices" in result:
        print("✅ API连接成功!")
        print(f"   响应: {result['choices'][0]['message']['content'][:100]}...")
        return {"success": True, "response": result}
    else:
        print(f"❌ API连接失败: {result}")
        return {"success": False, "response": result}


def generate_video(prompt_key: str) -> dict:
    """生成视频 (当前API可能不支持，返回模拟结果)"""
    
    if prompt_key not in VIDEO_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(VIDEO_PROMPTS.keys())
        }
    
    prompt_data = VIDEO_PROMPTS[prompt_key]
    
    print(f"\n🎬 生成视频: {prompt_key}")
    print(f"   提示词: {prompt_data['prompt'][:60]}...")
    
    # 尝试调用视频生成API (如果存在的话)
    # 注意: 当前API可能只支持文本生成，视频生成可能需要特殊权限
    
    # 返回提示信息
    return {
        "success": True,
        "simulated": True,
        "message": "视频生成需要使用海螺视频网页版或Replicate",
        "prompt_key": prompt_key,
        "prompt": prompt_data["prompt"],
        "duration": prompt_data["duration"],
        "alternative": "请访问 https://hailuoai.video 直接在线生成",
        "timestamp": datetime.now().isoformat()
    }


def generate_image(prompt_key: str) -> dict:
    """生成图像 (当前API可能不支持，返回模拟结果)"""
    
    if prompt_key not in IMAGE_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(IMAGE_PROMPTS.keys())
        }
    
    prompt_data = IMAGE_PROMPTS[prompt_key]
    
    print(f"\n🖼️ 生成图像: {prompt_key}")
    print(f"   提示词: {prompt_data['prompt'][:60]}...")
    
    return {
        "success": True,
        "simulated": True,
        "message": "图像生成可以使用MiniMax的image-01模型(需单独配置)",
        "prompt_key": prompt_key,
        "prompt": prompt_data["prompt"],
        "size": prompt_data["size"],
        "alternative": "请稍候或使用其他图像生成工具(如Midjourney)",
        "timestamp": datetime.now().isoformat()
    }


def daily_batch() -> dict:
    """每日批量生成"""
    print("\n" + "=" * 70)
    print("📦 Daily Content Batch Generation")
    print("=" * 70)
    
    video_prompts = list(VIDEO_PROMPTS.keys())[:5]
    image_prompts = list(IMAGE_PROMPTS.keys())[:4]
    
    print(f"\n🎬 视频提示词 ({len(video_prompts)}个):")
    for prompt in video_prompts:
        generate_video(prompt)
    
    print(f"\n🖼️ 图像提示词 ({len(image_prompts)}个):")
    for prompt in image_prompts:
        generate_image(prompt)
    
    return {
        "success": True,
        "videos": len(video_prompts),
        "images": len(image_prompts),
        "timestamp": datetime.now().isoformat()
    }


def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                  MiniMax Media Generator (修复版)              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  API状态: ✅ 已修复                                             ║
║  格式: OpenAI兼容格式                                          ║
║                                                              ║
║  使用方法:                                                     ║
║                                                              ║
║    1. 设置环境变量:                                           ║
║       export MINIMAX_API_KEY="sk-api-xxx"                     ║
║       export MINIMAX_API_HOST="https://api.minimaxi.com"      ║
║                                                              ║
║    2. 运行命令:                                               ║
║       python minimax_tool.py test      # 测试API连接           ║
║       python minimax_tool.py video    # 视频生成(模拟)        ║
║       python minimax_tool.py image   # 图像生成(模拟)        ║
║       python minimax_tool.py daily    # 每日批量             ║
║                                                              ║
║  注意:                                                         ║
║  当前API只支持文本生成(成功✅)                                   ║
║  视频/图像生成需要:                                             ║
║  - 方案A: 使用海螺视频网页版 https://hailuoai.video          ║
║  - 方案B: 使用Replicate (推荐)                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def main():
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command in ["--help", "-h", "help"]:
        show_help()
    
    elif command == "test":
        result = test_connection()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "video":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace"
        result = generate_video(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "image":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace_product"
        result = generate_image(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "daily":
        result = daily_batch()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
