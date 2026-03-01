# MiniMax API Integration Guide

> **Source**: MiniMax Official Documentation
> **Date**: 2026-02-19
> **Status**: Complete Integration Guide

---

## 🎯 MiniMax API Access Methods

MiniMax提供3种API接入方式：

| 方法 | 推荐程度 | 说明 |
|------|----------|------|
| **HTTP Request** | ⭐⭐⭐ | 基础方式，通用性强 |
| **Anthropic SDK** | ⭐⭐⭐⭐⭐ | **官方推荐** |
| **OpenAI SDK** | ⭐⭐⭐⭐ | 兼容OpenAI格式 |

---

## 🚀 Method 1: HTTP Request (基础)

### 文本生成

```python
import requests

API_KEY = "your_api_key"
API_HOST = "https://api.minimaxi.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 文本生成
payload = {
    "model": "MiniMax-M2.5",
    "messages": [
        {"role": "user", "content": "你好"}
    ]
}

response = requests.post(
    f"{API_HOST}/v1/chat/completions",
    headers=headers,
    json=payload
)

print(response.json())
```

### 语音合成 (T2A)

```python
# 语音合成
payload = {
   speech-2.8-hd "model": "",
    "text": "你好世界",
    "voice_id": "female-shaonv",
    "speed": 1.0,
    "volume": 1.0
}

response = requests.post(
    f"{API_HOST}/v1/speech/t2a",
    headers=headers,
    json=payload
)
```

---

## 🚀 Method 2: Anthropic SDK (推荐)

### 安装

```bash
pip install anthropic
```

### 配置

```python
from anthropic import Anthropic

# 初始化客户端
client = Anthropic(
    api_key="your_api_key",
    base_url="https://api.minimaxi.com/v1"
)
```

### 使用

```python
# 文本生成
response = client.messages.create(
    model="MiniMax-M2.5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Explain crypto airdrops"}
    ]
)

print(response.content[0].text)
```

### 工具调用

```python
# 使用MiniMax的工具
tools = [
    {
        "name": "generate_video",
        "description": "Generate video from text",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Video prompt"},
                "duration": {"type": "integer", "description": "Duration in seconds"}
            },
            "required": ["prompt"]
        }
    }
]

response = client.messages.create(
    model="MiniMax-M2.5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Generate a video about gold jewelry"}
    ],
    tools=tools
)
```

---

## 🚀 Method 3: OpenAI SDK

### 安装

```bash
pip install openai
```

### 配置

```python
from openai import OpenAI

# 初始化客户端 (MiniMax兼容OpenAI格式)
client = OpenAI(
    api_key="your_api_key",
    base_url="https://api.minimaxi.com/v1"
)
```

### 使用

```python
# 文本生成
response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "user", "content": "What's the best crypto airdrop strategy?"}
    ]
)

print(response.choices[0].message.content)
```

### 流式输出

```python
# 流式生成
stream = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "user", "content": "Tell me about meme coins"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## 📚 MiniMax模型列表

### 文本生成

| 模型 | 特点 | 速度 |
|------|------|------|
| MiniMax-M2.5 | 顶尖性能，复杂任务 | 60tps |
| MiniMax-M2.5-highspeed | 极速版 | 100tps |
| MiniMax-M2.1 | 多语言编程 | 60tps |
| MiniMax-M2.1-highspeed | 极速版 | 100tps |

### 语音合成

| 模型 | 特点 |
|------|------|
| speech-2.8-hd | 最新HD模型，高保真 |
| speech-2.8-turbo | 快速版，低延迟 |
| speech-02-hd | 出色韵律和稳定性 |

### 视频生成

| 模型 | 特点 |
|------|------|
| MiniMax-Hailuo-2.3 | 最新模型，肢体动作升级 |
| MiniMax-Hailuo-02 | 支持1080P，10秒 |

### 图像生成

| 模型 | 特点 |
|------|------|
| image-01 | 文生图，图生图 |
| image-01-live | 多画风设置 |

### 音乐生成

| 模型 | 特点 |
|------|------|
| music-2.0 | 音乐创作 |

---

## 🔧 完整示例

### 集成工具

```python
#!/usr/bin/env python3
"""
MiniMax Complete Integration - All in One

支持:
- 文本生成
- 语音合成
- 图像生成
- 视频生成
"""

import os
import json
from datetime import datetime

# 选择SDK
USE_OPENAI_SDK = True  # 推荐
# USE_ANTHROPIC_SDK = False

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_HOST = "https://api.minimaxi.com"

if USE_OPENAI_SDK:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=f"{API_HOST}")
else:
    from anthropic import Anthropic
    client = Anthropic(api_key=API_KEY, base_url=f"{API_HOST}/v1")


def generate_text(prompt: str, model: str = "MiniMax-M2.5") -> str:
    """文本生成"""
    if USE_OPENAI_SDK:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    else:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


def generate_speech(text: str, voice_id: str = "female-shaonv") -> dict:
    """语音合成 (HTTP)"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "voice_id": voice_id
    }
    
    response = requests.post(
        f"{API_HOST}/v1/speech/t2a",
        headers=headers,
        json=payload
    )
    
    return response.json()


def generate_image(prompt: str) -> dict:
    """图像生成 (HTTP)"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "image_size": "1024x1024"
    }
    
    response = requests.post(
        f"{API_HOST}/v1/image/generation",
        headers=headers,
        json=payload
    )
    
    return response.json()


def generate_video(prompt: str, duration: int = 6) -> dict:
    """视频生成 (HTTP, 异步)"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt,
        "duration": duration
    }
    
    response = requests.post(
        f"{API_HOST}/v1/video/generation",
        headers=headers,
        json=payload
    )
    
    return response.json()


# 示例使用
if __name__ == "__main__":
    print("=" * 60)
    print("MiniMax Complete Integration Demo")
    print("=" * 60)
    
    # 1. 文本生成
    print("\n📝 文本生成...")
    text = generate_text("What makes a good crypto airdrop?")
    print(f"Result: {text[:100]}...")
    
    # 2. 图像生成
    print("\n🖼️ 图像生成...")
    image_result = generate_image("Gold necklace, luxurious, 4k")
    print(f"Result: {image_result}")
    
    # 3. 视频生成
    print("\n🎬 视频生成...")
    video_result = generate_video("Gold jewelry sparkling, cinematic lighting")
    print(f"Result: {video_result}")
    
    print("\n" + "=" * 60)
    print("✅ All done!")
```

---

## 📁 文件结构

```
minimax-integration/
├── README.md              (本文档)
├── http_examples.py       (HTTP请求示例)
├── anthropic_sdk.py      (Anthropic SDK示例)
├── openai_sdk.py         (OpenAI SDK示例)
├── complete_demo.py       (完整集成示例)
├── requirements.txt       (依赖)
└── config.yaml           (配置文件)
```

---

## 🎯 推荐配置

### 最佳实践

```python
# 使用OpenAI SDK (推荐)
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MINIMAX_API_KEY"],
    base_url="https://api.minimaxi.com/v1"
)

# 简单使用
response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[{"role": "user", "content": "your prompt"}]
)
```

### 错误处理

```python
try:
    response = client.chat.completions.create(
        model="MiniMax-M2.5",
        messages=[{"role": "user", "content": "prompt"}]
    )
except Exception as e:
    print(f"Error: {e}")
    # 处理错误
```

---

## 🚀 快速开始

### Step 1: 安装依赖

```bash
pip install openai requests
```

### Step 2: 设置API Key

```bash
export MINIMAX_API_KEY="your_key"
```

### Step 3: 运行示例

```bash
python openai_sdk.py
```

---

*MiniMax Integration Guide v1.0*
*Created: 2026-02-19*
*Source: platform.minimaxi.com/docs/api-reference/api-overview*