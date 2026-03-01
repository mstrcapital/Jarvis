#!/usr/bin/env python3
"""
MiniMax 图像生成器
支持 image-01 模型
"""

import os
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimaxi.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ============== 图像提示词库 ==============
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
    },
    "store_display": {
        "prompt": "Luxury jewelry store window display, elegant lighting, gold and platinum items, mall environment",
        "size": "1920x1080"
    }
}


def generate_image(prompt_key: str) -> str:
    """生成图像"""
    prompt_data = IMAGE_PROMPTS.get(prompt_key, IMAGE_PROMPTS["gold_necklace_product"])
    
    payload = {
        "model": "image-01",
        "prompt": prompt_data["prompt"],
        "image_size": prompt_data["size"],
        "quality": "high",
        "style": "realistic"
    }
    
    response = requests.post(
        f"{BASE_URL}/image/generation",
        headers=HEADERS,
        json=payload
    )
    
    result = response.json()
    
    if result.get("code") != 0:
        print(f"❌ Error: {result}")
        return None
    
    image_url = result["data"]["image_url"]
    print(f"✅ Image generated: {image_url}")
    
    return image_url


def generate_image_with_image(prompt_key: str, reference_image_url: str) -> str:
    """基于参考图生成图像"""
    prompt_data = IMAGE_PROMPTS.get(prompt_key, IMAGE_PROMPTS["gold_necklace_product"])
    
    payload = {
        "model": "image-01",
        "prompt": prompt_data["prompt"],
        "image_size": prompt_data["size"],
        "reference_images": [
            {
                "type": "subject",
                "url": reference_image_url
            }
        ],
        "quality": "high",
        "style": "realistic"
    }
    
    response = requests.post(
        f"{BASE_URL}/image/generation",
        headers=HEADERS,
        json=payload
    )
    
    result = response.json()
    
    if result.get("code") != 0:
        print(f"❌ Error: {result}")
        return None
    
    return result["data"]["image_url"]


def batch_generate_images(prompt_keys: list) -> list:
    """批量生成图像"""
    results = []
    
    for key in prompt_keys:
        print(f"🖼️ Generating: {key}")
        url = generate_image(key)
        
        results.append({
            "prompt": key,
            "url": url,
            "status": "success" if url else "failed",
            "time": datetime.now().isoformat()
        })
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        prompt_key = sys.argv[1]
        generate_image(prompt_key)
    else:
        batch_generate_images(list(IMAGE_PROMPTS.keys())[:3])
