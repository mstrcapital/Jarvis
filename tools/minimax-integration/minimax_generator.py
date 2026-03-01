#!/usr/bin/env python3
"""
MiniMax 视频/图像生成器
支持完整API调用

使用方法:
1. 在 https://platform.minimaxi.com/user-center/basic-information/interface-key 创建API Key
2. 设置环境变量: export MINIMAX_API_KEY="your_key"
3. 运行脚本
"""

import os
import json
import time
import requests
from datetime import datetime

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# 尝试多个可能的端点
ENDPOINTS = {
    "video_v1": "https://api.minimaxi.com/v1/video/generation",
    "video_vapigen": "https://api.minimaxi.com/vapigen/v1/video/generation",
    "hailuo": "https://api.hailuoai.video/v1/video/generation",
    "hailuo_v2": "https://api.hailuoai.video/v2/video/generation",
}

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
    "product_shot": {
        "prompt": "Professional product photography of gold necklace on white background, studio lighting, 4k, e-commerce ready",
        "duration": 5
    },
    "lifestyle": {
        "prompt": "Elegant woman wearing gold jewelry, luxury lifestyle photo, warm lighting, magazine quality",
        "duration": 7
    },
    "luxury_store": {
        "prompt": "Interior of luxury jewelry store, elegant displays with gold and platinum items, warm sophisticated lighting, reflections",
        "duration": 8
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


def test_api_connection():
    """测试API连接"""
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        return False
    
    print("🔍 测试API连接...")
    print(f"API Key: {API_KEY[:20]}...")
    
    # 测试文本生成（最基础的功能）
    test_url = "https://api.minimaxi.com/v1/text/generation"
    payload = {
        "model": "MiniMax-M2.5",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(test_url, json=payload, headers=headers, timeout=10)
        print(f"Response: {response.status_code}")
        print(f"Body: {response.text[:200]}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def generate_video_simple(prompt_key: str):
    """简单视频生成测试"""
    prompt_data = VIDEO_PROMPTS.get(prompt_key, VIDEO_PROMPTS["gold_necklace"])
    
    print(f"\n🎬 生成视频: {prompt_key}")
    print(f"提示词: {prompt_data['prompt'][:50]}...")
    
    # 检查是否有MiniMax官方SDK
    try:
        import minimax
        print("✅ 使用官方SDK")
        # 官方SDK使用方式
        client = minimax.Minimax(api_key=API_KEY)
        result = client.video.generate(
            model="MiniMax-Hailuo-2.3",
            prompt=prompt_data["prompt"],
            duration=prompt_data["duration"]
        )
        print(f"✅ 成功: {result}")
        return result
    except ImportError:
        print("ℹ️ 未安装官方SDK，使用HTTP请求")
    
    # 尝试不同端点
    for name, url in ENDPOINTS.items():
        print(f"\n🔄 尝试端点: {name}")
        try:
            payload = {
                "model": "MiniMax-Hailuo-2.3",
                "prompt": prompt_data["prompt"],
                "duration": prompt_data["duration"],
                "resolution": "720p"
            }
            
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None


def generate_image_simple(prompt_key: str):
    """简单图像生成测试"""
    prompt_data = IMAGE_PROMPTS.get(prompt_key, IMAGE_PROMPTS["gold_necklace_product"])
    
    print(f"\n🖼️ 生成图像: {prompt_key}")
    print(f"提示词: {prompt_data['prompt'][:50]}...")
    
    url = "https://api.minimaxi.com/v1/image/generation"
    payload = {
        "model": "image-01",
        "prompt": prompt_data["prompt"],
        "image_size": prompt_data["size"]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:300]}")
        return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def list_available_models():
    """列出可用的模型"""
    print("\n📋 MiniMax 可用模型:")
    print("=" * 50)
    
    print("\n🎬 视频生成:")
    print("  • MiniMax-Hailuo-2.3 (最新)")
    print("  • MiniMax-Hailuo-2.3-Fast (快速版)")
    print("  • MiniMax-Hailuo-02 (1080P, 10秒)")
    
    print("\n🖼️ 图像生成:")
    print("  • image-01 (文生图/图生图)")
    print("  • image-01-live (多画风)")
    
    print("\n🔊 语音合成:")
    print("  • speech-2.8-hd (最新HD)")
    print("  • speech-2.8-turbo (快速版)")
    print("  • speech-02-hd (出色韵律)")
    
    print("\n📝 文本生成:")
    print("  • MiniMax-M2.5 (顶尖性能)")
    print("  • MiniMax-M2.5-highspeed (极速版)")
    print("  • MiniMax-M2.1 (多语言编程)")
    
    print("\n🎵 音乐生成:")
    print("  • music-2.0 (最新)")
    
    print("\n" + "=" * 50)


def show_usage_guide():
    """显示使用指南"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                    MiniMax API 使用指南                           ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                ║
║  1. 创建API Key:                                               ║
║     https://platform.minimaxi.com/user-center/basic-information/interface-key
║                                                                ║
║  2. 设置环境变量:                                               ║
║     export MINIMAX_API_KEY="your_api_key"                       ║
║                                                                ║
║  3. 安装SDK (可选):                                             ║
║     pip install minimax-a-py                                    ║
║                                                                ║
║  4. 运行测试:                                                  ║
║     python minimax_generator.py test                            ║
║                                                                ║
║  5. 生成视频:                                                  ║
║     python minimax_generator.py video gold_necklace              ║
║                                                                ║
║  6. 生成图像:                                                  ║
║     python minimax_generator.py image gold_necklace_product      ║
║                                                                ║
║  7. 查看支持的模型:                                             ║
║     python minimax_generator.py models                           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_usage_guide()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        test_api_connection()
    elif command == "models":
        list_available_models()
    elif command == "video":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace"
        generate_video_simple(prompt_key)
    elif command == "image":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace_product"
        generate_image_simple(prompt_key)
    elif command == "guide":
        show_usage_guide()
    else:
        print(f"未知命令: {command}")
        print("可用命令: test, models, video, image, guide")
