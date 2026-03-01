# MiniMax AI 视频/图像生成集成方案

> **Platform**: https://platform.minimaxi.com
> **Date**: 2026-02-19
> **Status**: 完整集成方案

---

## 🎯 可用API总览

### 视频生成 (Video Generation)

| 模型 | 特点 | 分辨率 | 时长 |
|------|------|--------|------|
| **MiniMax-Hailuo-2.3** | 最新模型，肢体动作、物理表现升级 | 720P+ | 6-10秒 |
| **MiniMax-Hailuo-2.3-Fast** | 图生视频，速度快，性价比高 | 720P+ | 6秒 |
| **MiniMax-Hailuo-02** | 支持1080P，10秒时长 | 1080P | 10秒 |

### 图像生成 (Image Generation)

| 模型 | 特点 | 功能 |
|------|------|------|
| **image-01** | 画面细腻 | 文生图、图生图 |
| **image-01-live** | 多种画风 | 支持风格设置 |

### 语音合成 (T2A)

| 模型 | 特点 |
|------|------|
| speech-2.8-hd | 最新HD模型，高保真 |
| speech-2.8-turbo | 快速版，低延迟 |
| speech-02-hd | 出色韵律和稳定性 |

---

## 💰 价格参考

```
视频生成:
├── MiniMax-Hailuo-2.3: ¥0.5-1/秒
├── MiniMax-Hailuo-2.3-Fast: ¥0.3-0.5/秒
└── MiniMax-Hailuo-02: ¥0.8-1.2/秒

图像生成:
├── image-01: ¥0.1-0.3/张
└── image-01-live: ¥0.2-0.5/张

语音合成:
├── speech-2.8-hd: ¥0.01-0.05/千字符
└── speech-2.8-turbo: ¥0.005-0.02/千字符
```

---

## 🛠️ Python SDK 集成

### 1. 安装依赖

```bash
pip install minimax-a-py
# 或使用requests
pip install requests
```

### 2. 配置API Key

```python
import os
os.environ["MINIMAX_API_KEY"] = "your_api_key_here"
```

### 3. 视频生成脚本

```python
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

# 配置
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimaxi.com/v1"

# 请求头
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 提示词库 - 贵金属/饰品相关
VIDEO_PROMPTS = {
    "gold_necklace": {
        "prompt": "A stunning gold necklace with pendant sparkling under soft studio light, luxurious jewelry showcase, 4k quality, slow motion, cinematic lighting, elegant atmosphere",
        "duration": 6
    },
    "platinum_jewelry": {
        "prompt": "Close-up shot of platinum jewelry piece, silver-white metallic sheen reflecting light, minimalist luxury design, studio background, 4k, high detail",
        "duration": 6
    },
    "stacked_rings": {
        "prompt": "Layered gold and silver rings stacked on fingers, elegant hand pose, fashion magazine style, soft lighting, 4k cinematic",
        "duration": 5
    },
    "jewelry_box": {
        "prompt": "Luxury velvet jewelry box opening slowly, revealing gold and diamond pieces inside, premium unboxing experience, soft ambient lighting, 4k",
        "duration": 6
    },
    "luxury_store": {
        "prompt": "Interior of luxury jewelry store, elegant displays with gold and platinum items, warm sophisticated lighting, reflections on glass, cinematic atmosphere",
        "duration": 8
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


def generate_video_sync(prompt_key: str, output_dir: str = "./videos") -> str:
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
    max_wait = 300  # 最多等5分钟
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


def batch_generate_video(prompt_keys: list, output_dir: str = "./videos"):
    """批量生成视频"""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for key in prompt_keys:
        try:
            output = generate_video_sync(key, output_dir)
            results.append({
                "prompt": key,
                "output": output,
                "status": "success" if output else "failed"
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
    
    return results


if __name__ == "__main__":
    # 测试生成一个视频
    generate_video_sync("gold_necklace")
    
    # 或批量生成
    # batch_generate_video(list(VIDEO_PROMPTS.keys())[:3])
```

### 4. 图像生成脚本

```python
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

# 图像提示词库
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
    
    if response.json().get("code") != 0:
        print(f"❌ Error: {response.json()}")
        return None
    
    image_url = response.json()["data"]["image_url"]
    return image_url


def batch_generate_images(prompt_keys: list) -> list:
    """批量生成图像"""
    results = []
    
    for key in prompt_keys:
        print(f"🖼️ Generating: {key}")
        url = generate_image(key)
        
        results.append({
            "prompt": key,
            "url": url,
            "status": "success" if url else "failed"
        })
    
    return results


if __name__ == "__main__":
    # 测试生成
    url = generate_image("gold_necklace_product")
    print(f"Generated: {url}")
```

---

## 🎬 视频Agent模板

MiniMax还提供预定义的视频Agent模板：

| 模板ID | 名称 | 用途 | 输入 |
|--------|------|------|------|
| 392753057216684038 | 跳水 | 创意动作 | 图片 |
| 393881433990066176 | 吊环 | 宠物动作 | 图片 |
| 393769180141805569 | 绝地求生 | 野外场景 | 图片+描述 |
| 394246956137422856 | Labubu换脸 | 换脸 | 图片 |
| 393879757702918151 | 麦当劳宠物 | 角色扮演 | 图片 |
| 393766210733957121 | 藏族风写真 | 民族风 | 参考图 |
| 393857704283172864 | 情书写真 | 雪景写真 | 图片 |
| 393866076583718914 | 女模特试穿 | 服装展示 | 服装图 |
| 398574688191234048 | 四季写真 | 人像变化 | 人脸图 |
| 393876118804459526 | 男模特试穿 | 服装展示 | 服装图 |

---

## 📊 工作流集成

### 完整内容生产流程

```
1. 图像生成 (image-01)
   ↓
2. 视频生成 (Hailuo-2.3)
   ↓
3. 语音合成 (speech-2.8)
   ↓
4. 后期剪辑 (CapCut)
   ↓
5. 多平台发布
```

### 批量生产脚本

```python
#!/usr/bin/env python3
"""
完整内容生产流水线
图像 → 视频 → 语音 → 成片
"""

import os
import json
from video_generator import generate_video_sync
from image_generator import generate_image
from datetime import datetime

def create_social_content(content_type: str, theme: str):
    """创建社交媒体内容"""
    
    if content_type == "product_reel":
        # 产品展示：图像 → 视频
        image_prompt = f"Professional gold jewelry product photo, {theme}, studio lighting, e-commerce"
        video_prompt = f"Gold jewelry piece rotating slowly, luxury aesthetic, soft lighting, cinematic"
        
        # 生成图像
        image_url = generate_image("gold_necklace_product")
        
        # 生成视频
        video_path = generate_video_sync("gold_necklace")
        
        return {
            "type": content_type,
            "theme": theme,
            "image": image_url,
            "video": video_path,
            "timestamp": datetime.now().isoformat()
        }
    
    elif content_type == "lifestyle_video":
        # 生活方式：多视频组合
        video_paths = [
            generate_video_sync("stacked_rings"),
            generate_video_sync("jewelry_box"),
            generate_video_sync("luxury_store")
        ]
        
        return {
            "type": content_type,
            "theme": theme,
            "videos": video_paths,
            "timestamp": datetime.now().isoformat()
        }


def daily_content_batch():
    """每日内容批量生产"""
    contents = []
    
    # 早安帖
    contents.append(create_social_content("product_reel", "morning"))
    
    # 产品特写
    contents.append(create_social_content("product_reel", "closeup"))
    
    # 生活方式
    contents.append(create_social_content("lifestyle_video", "daily"))
    
    # 保存日志
    with open(f"content_batch_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
        json.dump(contents, f, indent=2)
    
    return contents


if __name__ == "__main__":
    daily_content_batch()
```

---

## 📁 文件结构

```
minimax-integration/
├── video_generator.py      # 视频生成
├── image_generator.py      # 图像生成
├── content_pipeline.py    # 完整流水线
├── prompts/
│   ├── video_prompts.json  # 视频提示词
│   └── image_prompts.json  # 图像提示词
├── output/
│   ├── videos/            # 视频输出
│   └── images/            # 图像输出
├── logs/                  # 日志
└── README.md              # 说明文档
```

---

## 🚀 使用步骤

### 1. 获取API Key

```
1. 访问: https://platform.minimaxi.com/user-center/basic-information/interface-key
2. 创建 API Key
3. 保存 Key
```

### 2. 设置环境变量

```bash
export MINIMAX_API_KEY="your_api_key_here"
```

### 3. 运行测试

```bash
# 测试视频生成
python video_generator.py

# 测试图像生成
python image_generator.py

# 批量生产
python content_pipeline.py
```

---

## 💡 优化建议

### 提示词技巧

```
✅ 好的提示词:
- "A stunning gold necklace with pendant sparkling under soft studio light"
- "Professional product photography, 4k, e-commerce ready"

❌ 不好的提示词:
- "gold necklace good"
- "beautiful jewelry video"
```

### 参数调优

```
视频生成:
├── 分辨率: 720p (性价比) / 1080p (高质量)
├── 时长: 6秒 (标准) / 10秒 (Hailuo-02)
└── 帧率: 24fps (标准)

图像生成:
├── 尺寸: 1024x1024 (1:1) / 1080x1080 (IG) / 1920x1080 (Banner)
└── 质量: high
```

---

## ⚠️ 注意事项

1. **异步任务**: 视频生成是异步的，需要轮询状态
2. **有效期**: 生成的URL有效期9小时，及时下载
3. **费用**: 按量计费，注意控制生成频率
4. **内容合规**: 遵守平台内容规范

---

*MiniMax Integration v1.0*
*Created: 2026-02-19*
*Source: https://platform.minimaxi.com/docs/api-reference/api-overview*