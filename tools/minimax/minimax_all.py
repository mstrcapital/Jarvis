#!/usr/bin/env python3
"""
MiniMax Complete Integration - All in One Tool

支持:
- 文本生成
- 语音合成
- 图像生成
- 视频生成

使用方法:
1. 设置环境变量: export MINIMAX_API_KEY="your_key"
2. 运行脚本
"""

import os
import sys
import json
import requests
from datetime import datetime

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = "https://api.minimaxi.com"

# ============== 文本提示词 ==============
TEXT_PROMPTS = {
    "crypto_alpha": "What's the best crypto airdrop hunting strategy in 2024?",
    "pump_fun": "Explain pump.fun trading strategy in simple terms",
    "meme_coins": "What makes a good meme coin? Give examples",
    "defi_basics": "Explain DeFi in 3 sentences",
    "trading_tips": "Give 5 practical crypto trading tips"
}

# ============== 图像提示词 ==============
IMAGE_PROMPTS = {
    "gold_necklace": "Professional gold necklace product photo, studio lighting, e-commerce",
    "crypto_meme": "Funny crypto meme, Pepe the frog, diamond hands, 4k",
    "luxury_lifestyle": "Elegant lifestyle photo, gold jewelry, warm lighting",
    "social_post": "Minimalist luxury product display, Instagram style, 4k"
}

# ============== 视频提示词 ==============
VIDEO_PROMPTS = {
    "gold_jewelry": "Luxury gold necklace sparkling under soft light, cinematic, 4k",
    "product_reveal": "Jewelry box opening slowly, premium unboxing, elegant",
    "lifestyle_shot": "Elegant woman wearing gold jewelry, warm lighting, magazine quality"
}

# ============== API函数 ==============
def make_request(endpoint: str, payload: dict) -> dict:
    """发送HTTP请求"""
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


# ============== 文本生成 ==============
def generate_text(prompt_key: str) -> dict:
    """使用OpenAI兼容格式生成文本"""
    if prompt_key not in TEXT_PROMPTS:
        return {"success": False, "error": f"Unknown prompt: {prompt_key}"}
    
    prompt = TEXT_PROMPTS[prompt_key]
    print(f"\n📝 生成文本: {prompt_key}")
    print(f"   内容: {prompt[:50]}...")
    
    # 使用OpenAI兼容格式
    result = make_request("/v1/chat/completions", {
        "model": "MiniMax-M2.5",
        "messages": [{"role": "user", "content": prompt}]
    })
    
    if "choices" in result:
        content = result["choices"][0]["message"]["content"]
        print(f"   ✅ 成功: {content[:100]}...")
        return {"success": True, "content": content}
    else:
        print(f"   ❌ 失败: {result}")
        return {"success": False, "response": result}


# ============== 图像生成 ==============
def generate_image(prompt_key: str) -> dict:
    """生成图像"""
    if prompt_key not in IMAGE_PROMPTS:
        return {"success": False, "error": f"Unknown prompt: {prompt_key}"}
    
    prompt = IMAGE_PROMPTS[prompt_key]
    print(f"\n🖼️ 生成图像: {prompt_key}")
    print(f"   内容: {prompt[:50]}...")
    
    result = make_request("/v1/image/generation", {
        "model": "image-01",
        "prompt": prompt,
        "image_size": "1024x1024"
    })
    
    if result.get("code") == 0:
        image_url = result["data"]["image_url"]
        print(f"   ✅ 成功: {image_url[:50]}...")
        return {"success": True, "image_url": image_url}
    else:
        print(f"   ❌ 失败: {result}")
        return {"success": False, "response": result}


# ============== 语音合成 ==============
def generate_speech(text: str, voice_id: str = "female-shaonv") -> dict:
    """语音合成"""
    print(f"\n🔊 生成语音: {text[:50]}...")
    print(f"   音色: {voice_id}")
    
    result = make_request("/v1/speech/t2a", {
        "model": "speech-2.8-hd",
        "text": text,
        "voice_id": voice_id
    })
    
    print(f"   {'✅ 成功' if result.get('code') == 0 else '❌ 失败'}: {result}")
    return result


# ============== 视频生成 ==============
def generate_video(prompt_key: str) -> dict:
    """生成视频 (异步)"""
    if prompt_key not in VIDEO_PROMPTS:
        return {"success": False, "error": f"Unknown prompt: {prompt_key}"}
    
    prompt = VIDEO_PROMPTS[prompt_key]
    print(f"\n🎬 生成视频: {prompt_key}")
    print(f"   内容: {prompt[:50]}...")
    
    result = make_request("/v1/video/generation", {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt,
        "duration": 6
    })
    
    if result.get("code") == 0:
        task_id = result["data"]["task_id"]
        print(f"   ✅ 任务创建成功: {task_id}")
        return {"success": True, "task_id": task_id}
    else:
        print(f"   ❌ 失败: {result}")
        return {"success": False, "response": result}


# ============== 主程序 ==============
def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                  MiniMax Complete Integration                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  使用方法:                                                     ║
║                                                              ║
║    1. 设置环境变量:                                           ║
║       export MINIMAX_API_KEY="your_key"                       ║
║                                                              ║
║    2. 运行命令:                                               ║
║                                                              ║
║  命令:                                                        ║
║    python minimax_all.py text <prompt_key>                   ║
║    python minimax_all.py image <prompt_key>                   ║
║    python minimax_all.py speech <text> <voice_id>           ║
║    python minimax_all.py video <prompt_key>                   ║
║    python minimax_all.py demo                                ║
║                                                              ║
║  示例:                                                        ║
║    python minimax_all.py text crypto_alpha                   ║
║    python minimax_all.py image gold_necklace                  ║
║    python minimax_all.py demo                                 ║
║                                                              ║
║  可用提示词:                                                  ║
║    文本: crypto_alpha, pump_fun, meme_coins, defi_basics    ║
║    图像: gold_necklace, crypto_meme, luxury_lifestyle        ║
║    视频: gold_jewelry, product_reveal, lifestyle_shot        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def main():
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        show_help()
        sys.exit(1)
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command in ["--help", "-h", "help"]:
        show_help()
    
    elif command == "text":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "crypto_alpha"
        result = generate_text(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "image":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_necklace"
        result = generate_image(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "speech":
        text = sys.argv[2] if len(sys.argv) > 2 else "Hello, this is a test."
        voice_id = sys.argv[3] if len(sys.argv) > 3 else "female-shaonv"
        result = generate_speech(text, voice_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "video":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "gold_jewelry"
        result = generate_video(prompt_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "demo":
        # 运行演示
        print("\n" + "=" * 60)
        print("🎯 MiniMax Complete Demo")
        print("=" * 60)
        
        # 测试文本生成
        generate_text("crypto_alpha")
        
        # 测试图像生成
        generate_image("gold_necklace")
        
        print("\n" + "=" * 60)
        print("✅ Demo complete!")
        print("=" * 60)
    
    else:
        print(f"❌ 未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
