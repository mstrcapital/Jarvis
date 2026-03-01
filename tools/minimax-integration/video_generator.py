#!/usr/bin/env python3
"""
MiniMax 视频生成器
支持 Hailuo 2.3 模型
"""

import os
import json
import time
import requests
from datetime import datetime

# ============== 配置 ==============
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimaxi.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
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
    "luxury_store": {
        "prompt": "Interior of luxury jewelry store, elegant displays with gold and platinum items, warm sophisticated lighting, reflections",
        "duration": 8
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
    }
}


def create_video_task(prompt_key: str) -> dict:
    """创建视频生成任务"""
    prompt_data = VIDEO_PROMPTS.get(prompt_key, VIDEO_PROMPTS["gold_necklace"])
    
    payload = {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt_data["prompt"],
        "duration": prompt_data["duration"],
        "resolution": "720p",
        "aspect_ratio": "16:9"
    }
    
    response = requests.post(
        f"{BASE_URL}/video/generation",
        headers=HEADERS,
        json=payload
    )
    
    return response.json()


def query_task_status(task_id: str) -> dict:
    """查询任务状态"""
    response = requests.get(
        f"{BASE_URL}/video/generation/{task_id}",
        headers=HEADERS
    )
    return response.json()


def download_video(file_id: str, output_path: str):
    """下载生成的视频"""
    response = requests.get(
        f"{BASE_URL}/files/{file_id}/download",
        headers=HEADERS,
        stream=True
    )
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return output_path


def generate_video_sync(prompt_key: str, output_dir: str = "./output/videos") -> str:
    """同步生成视频（等待完成）"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 创建任务
    print(f"🎬 Creating video: {prompt_key}")
    task_resp = create_video_task(prompt_key)
    
    if task_resp.get("code") != 0:
        print(f"❌ Error creating task: {task_resp}")
        return None
    
    task_id = task_resp["data"]["task_id"]
    print(f"✅ Task created: {task_id}")
    
    # 2. 轮询任务状态
    max_wait = 300
    waited = 0
    
    while waited < max_wait:
        status_resp = query_task_status(task_id)
        status = status_resp["data"]["status"]
        
        print(f"   Status: {status} ({waited}s)")
        
        if status == "completed":
            file_id = status_resp["data"]["file_id"]
            break
        elif status == "failed":
            print(f"❌ Task failed: {status_resp}")
            return None
        else:
            time.sleep(5)
            waited += 5
    
    # 3. 下载视频
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prompt_key}_{timestamp}.mp4"
    output_path = f"{output_dir}/{filename}"
    
    download_video(file_id, output_path)
    print(f"✅ Video saved: {output_path}")
    
    return output_path


def batch_generate_video(prompt_keys: list, output_dir: str = "./output/videos"):
    """批量生成视频"""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for key in prompt_keys:
        try:
            output = generate_video_sync(key, output_dir)
            results.append({
                "prompt": key,
                "output": output,
                "status": "success" if output else "failed",
                "time": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "prompt": key,
                "error": str(e),
                "status": "error"
            })
    
    # 保存日志
    with open("video_generation_log.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Total generated: {len(results)} videos")
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 指定提示词
        prompt_key = sys.argv[1]
        generate_video_sync(prompt_key)
    else:
        # 批量生成
        batch_generate_video(list(VIDEO_PROMPTS.keys())[:3])
