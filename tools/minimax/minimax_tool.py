#!/usr/bin/env python3
"""
MiniMax Media Generator Tool for OpenClaw

支持视频生成、图像生成、语音合成

使用方法:
1. 设置环境变量
2. 运行命令

环境变量:
- MINIMAX_API_KEY: API密钥
- MINIMAX_API_HOST: API地址 (https://api.minimaxi.com 或 https://api.minimax.io)
- MINIMAX_OUTPUT_DIR: 输出目录
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
OUTPUT_DIR = os.environ.get("MINIMAX_OUTPUT_DIR", "./output/media")

# ============== 提示词库 ==============
VIDEO_PROMPTS = {
    "gold_necklace": {
        "prompt": "A stunning gold necklace with pendant sparkling under soft studio light, luxurious jewelry showcase, 4k quality, slow motion, cinematic lighting",
        "duration": 6,
        "resolution": "720p"
    },
    "platinum_jewelry": {
        "prompt": "Close-up shot of platinum jewelry piece, silver-white metallic sheen, minimalist luxury design, studio background, 4k",
        "duration": 6,
        "resolution": "720p"
    },
    "stacked_rings": {
        "prompt": "Layered gold and silver rings stacked on fingers, elegant hand pose, fashion magazine style, soft lighting, 4k",
        "duration": 5,
        "resolution": "720p"
    },
    "jewelry_box": {
        "prompt": "Luxury velvet jewelry box opening slowly, revealing gold and diamond pieces inside, premium unboxing, soft lighting, 4k",
        "duration": 6,
        "resolution": "720p"
    },
    "abstract_background": {
        "prompt": "Flowing gradient background with soft purple and blue tones, gentle motion, 4k, abstract, smooth, ethereal",
        "duration": 5,
        "resolution": "720p"
    },
    "lifestyle": {
        "prompt": "Elegant woman wearing gold jewelry, luxury lifestyle photo, warm lighting, magazine quality",
        "duration": 7,
        "resolution": "720p"
    },
    "luxury_store": {
        "prompt": "Interior of luxury jewelry store, elegant displays with gold and platinum items, warm sophisticated lighting, reflections",
        "duration": 8,
        "resolution": "720p"
    }
}

IMAGE_PROMPTS = {
    "gold_necklace_product": {
        "prompt": "Professional product photography of gold necklace on white background, studio lighting, 4k, high detail, e-commerce ready",
        "size": "1024x1024"
    },
    "jewelry_lifestyle": {
        "prompt": "Elegant woman wearing gold and diamond jewelry, luxury lifestyle photo, warm lighting, magazine cover quality",
        "size": "1024x1536"
    },
    "product_detail": {
        "prompt": "Close-up macro shot of gold jewelry texture, intricate details, sparkles, black background, studio lighting",
        "size": "1024x1024"
    },
    "social_media_post": {
        "prompt": "Modern luxury jewelry display, minimalist composition, soft shadows, Instagram aesthetic, 4k",
        "size": "1080x1080"
    },
    "hero_banner": {
        "prompt": "Stunning gold jewelry arrangement, dramatic lighting, luxury brand aesthetic, wide banner format",
        "size": "1920x1080"
    },
    "packaging": {
        "prompt": "Luxury jewelry gift box, premium packaging, velvet interior, ribbon, elegant presentation",
        "size": "1024x1024"
    }
}

# ============== API函数 ==============
def make_request(endpoint: str, payload: dict) -> dict:
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

def generate_video(prompt_key: str) -> dict:
    """生成视频"""
    if prompt_key not in VIDEO_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(VIDEO_PROMPTS.keys())
        }
    
    prompt_data = VIDEO_PROMPTS[prompt_key]
    
    print(f"🎬 Generating video: {prompt_key}")
    print(f"   Prompt: {prompt_data['prompt'][:60]}...")
    print(f"   Duration: {prompt_data['duration']}s")
    
    # API调用 (异步)
    result = make_request("/v1/video/generation", {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt_data["prompt"],
        "duration": prompt_data["duration"],
        "resolution": prompt_data["resolution"]
    })
    
    if result.get("code") == 0:
        task_id = result["data"]["task_id"]
        print(f"✅ Task created: {task_id}")
        
        return {
            "success": True,
            "task_id": task_id,
            "prompt_key": prompt_key,
            "prompt": prompt_data["prompt"],
            "duration": prompt_data["duration"],
            "timestamp": datetime.now().isoformat()
        }
    else:
        error = result.get("msg", "Unknown error")
        print(f"❌ Error: {error}")
        return {"success": False, "error": error}

def query_video_status(task_id: str) -> dict:
    """查询视频生成状态"""
    print(f"📊 Querying task: {task_id}")
    
    result = make_request(f"/v1/video/generation/{task_id}", {})
    
    if result.get("code") == 0:
        status = result["data"]["status"]
        print(f"   Status: {status}")
        
        if status == "completed":
            return {
                "success": True,
                "status": "completed",
                "file_id": result["data"].get("file_id"),
                "video_url": result["data"].get("video_url")
            }
        elif status == "failed":
            return {"success": False, "status": "failed", "error": result.get("msg")}
        else:
            return {"success": True, "status": status}
    else:
        return {"success": False, "error": result.get("msg")}

def generate_image(prompt_key: str) -> dict:
    """生成图像"""
    if prompt_key not in IMAGE_PROMPTS:
        return {
            "success": False,
            "error": f"Unknown prompt: {prompt_key}",
            "available": list(IMAGE_PROMPTS.keys())
        }
    
    prompt_data = IMAGE_PROMPTS[prompt_key]
    
    print(f"🖼️ Generating image: {prompt_key}")
    print(f"   Prompt: {prompt_data['prompt'][:60]}...")
    print(f"   Size: {prompt_data['size']}")
    
    result = make_request("/v1/image/generation", {
        "model": "image-01",
        "prompt": prompt_data["prompt"],
        "image_size": prompt_data["size"]
    })
    
    if result.get("code") == 0:
        image_url = result["data"]["image_url"]
        print(f"✅ Image generated: {image_url}")
        
        return {
            "success": True,
            "prompt_key": prompt_key,
            "prompt": prompt_data["prompt"],
            "size": prompt_data["size"],
            "image_url": image_url,
            "timestamp": datetime.now().isoformat()
        }
    else:
        error = result.get("msg", "Unknown error")
        print(f"❌ Error: {error}")
        return {"success": False, "error": error}

def batch_generate(content_type: str, prompts: list) -> dict:
    """批量生成"""
    results = []
    
    for prompt_key in prompts:
        if content_type == "video":
            result = generate_video(prompt_key)
        elif content_type == "image":
            result = generate_image(prompt_key)
        else:
            result = {"success": False, "error": f"Unknown type: {content_type}"}
        
        results.append(result)
        
        if result.get("success"):
            print(f"✅ {prompt_key}: Success")
        else:
            print(f"❌ {prompt_key}: {result.get('error')}")
    
    successful = sum(1 for r in results if r.get("success"))
    
    return {
        "success": successful > 0,
        "total": len(results),
        "successful": successful,
        "failed": len(results) - successful,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

def daily_batch() -> dict:
    """每日内容批量生产"""
    video_prompts = ["gold_necklace", "stacked_rings", "jewelry_box", "lifestyle", "abstract_background"]
    image_prompts = ["gold_necklace_product", "jewelry_lifestyle", "social_media_post", "hero_banner"]
    
    print("\n" + "="*60)
    print("📦 Daily Content Batch Generation")
    print("="*60)
    
    print("\n🎬 Generating videos...")
    video_results = batch_generate("video", video_prompts)
    
    print("\n🖼️ Generating images...")
    image_results = batch_generate("image", image_prompts)
    
    return {
        "success": True,
        "videos": video_results,
        "images": image_results,
        "timestamp": datetime.now().isoformat()
    }

# ============== 主程序 ==============
def main():
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        print("\n使用示例:")
        print("  export MINIMAX_API_KEY=\"sk-api-xxx\"")
        print("  export MINIMAX_API_HOST=\"https://api.minimaxi.com\"")
        print("  python minimax_tool.py video gold_necklace")
        print("  python minimax_tool.py image gold_necklace_product")
        print("  python minimax_tool.py batch video gold_necklace stacked_rings")
        print("  python minimax_tool.py daily")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    MiniMax Media Generator                        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  使用方法:                                                     ║
║                                                              ║
║    python minimax_tool.py video <prompt>                      ║
║    python minimax_tool.py image <prompt>                       ║
║    python minimax_tool.py batch video <prompt1> <prompt2> ...  ║
║    python minimax_tool.py daily                                ║
║                                                              ║
║  示例:                                                         ║
║    python minimax_tool.py video gold_necklace                  ║
║    python minimax_tool.py image gold_necklace_product           ║
║    python minimax_tool.py batch video gold_necklace lifestyle   ║
║    python minimax_tool.py daily                                ║
║                                                              ║
║  可用提示词:                                                   ║
║    视频: gold_necklace, platinum_jewelry, stacked_rings,      ║
║          jewelry_box, abstract_background, lifestyle            ║
║    图像: gold_necklace_product, jewelry_lifestyle,            ║
║          social_media_post, hero_banner                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
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
        if len(sys.argv) < 4:
            print("❌ 用法: python minimax_tool.py batch <type> <prompt1> <prompt2> ...")
            print("   示例: python minimax_tool.py batch video gold_necklace lifestyle")
            sys.exit(1)
        
        content_type = sys.argv[2]
        prompts = sys.argv[3:]
        result = batch_generate(content_type, prompts)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "daily":
        result = daily_batch()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("❌ 用法: python minimax_tool.py query <task_id>")
            sys.exit(1)
        task_id = sys.argv[2]
        result = query_video_status(task_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"❌ 未知命令: {command}")
        print("可用命令: video, image, batch, daily, query")
        sys.exit(1)

if __name__ == "__main__":
    main()
