# MediaFlow Integration Guide

> **Source**: https://github.com/CheshireMew/MediaFlow
> **Type**: Local Video Subtitle Processing Workstation
> **Tech Stack**: Electron + React + Python (FastAPI)
> **Created**: 2026-02-19

---

## 🎯 MediaFlow是什么？

**MediaFlow** 是一个现代化的本地视频字幕生成与处理工作站。

```
一句话总结: 本地视频处理神器 - 下载+转录+翻译+合成 一站式
```

## ✨ 核心特性

| 功能 | 说明 |
|------|------|
| 📽️ **视频下载** | 多平台解析与下载（内置yt-dlp） |
| 📝 **智能转录** | Whisper模型，本地GPU加速 |
| 🌍 **翻译工作流** | 支持DeepL, OpenAI, Claude, SiliconeFlow |
| 🎬 **视频合成** | 真·分辨率适配，水印系统 |
| ⚡ **Architecture 2.0** | 高内聚低耦合，易扩展 |

## 🏗️ 项目结构

```
MediaFlow/
├── backend/              # Python后端 (FastAPI)
│   ├── services/        # 核心业务逻辑
│   ├── routers/         # API路由
│   └── utils/           # 工具库
├── frontend/             # Electron + React前端
│   ├── src/
│   │   ├── components/  # UI组件
│   │   ├── hooks/       # 自定义Hooks
│   │   └── pages/       # 页面路由
├── models/              # AI模型权重
└── user_data/          # 用户数据
```

## 🚀 快速启动

### 1. 后端启动

```bash
# Python 3.10+
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
```

### 2. 前端启动

```bash
cd frontend
npm run electron:dev
```

## 🛠️ 环境依赖

| 依赖 | 要求 |
|------|------|
| Python | 3.10+ |
| Node.js | 18+ |
| FFmpeg | 需要配置环境变量 |
| GPU | NVIDIA推荐 (CUDA 11.8+) |

## 🎯 适用场景

### 我们的使用场景

| 场景 | MediaFlow功能 |
|------|---------------|
| 视频本地化 | 转录+翻译+合成 |
| 内容二次创作 | 下载+字幕+水印 |
| 多语言内容 | 翻译工作流 |
| 批量处理 | 本地GPU加速 |

### 奢侈品/珠宝视频处理

```
1. 下载参考视频 → 📽️ 视频下载
2. 生成字幕 → 📝 Whisper转录
3. 翻译成中文 → 🌍 翻译工作流
4. 添加水印 → 🎬 视频合成
5. 导出发布 → 完成!
```

### Pepe视频制作

```
1. 下载Meme参考 → 📽️ 视频下载
2. 添加字幕 → 📝 智能转录
3. 多语言版本 → 🌍 翻译支持
4. 添加品牌水印 → 🎬 水印系统
5. 发布到X/TikTok → 完成!
```

## 💻 本地安装步骤

### Step 1: 安装依赖

```bash
# Python环境
python --version  # 需要 3.10+

# Node.js
node --version   # 需要 18+

# FFmpeg
ffmpeg -version  # 需要已安装
```

### Step 2: 克隆项目

```bash
git clone https://github.com/CheshireMew/MediaFlow.git
cd MediaFlow
```

### Step 3: 启动服务

```bash
# 终端1: 后端
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload

# 终端2: 前端
cd frontend
npm run electron:dev
```

### Step 4: 使用Web界面

打开浏览器访问: http://127.0.0.1:8001

## 🔧 API集成

MediaFlow提供FastAPI后端，可以程序化调用：

```python
import requests

BASE_URL = "http://127.0.0.1:8001"

# 示例API调用
def download_video(url):
    """下载视频"""
    response = requests.post(f"{BASE_URL}/api/download", json={"url": url})
    return response.json()

def transcribe_video(video_path):
    """转录视频"""
    response = requests.post(f"{BASE_URL}/api/transcribe", json={"path": video_path})
    return response.json()

def translate_subtitle(subtitle_path, target_lang="zh"):
    """翻译字幕"""
    response = requests.post(f"{BASE_URL}/api/translate", json={
        "subtitle_path": subtitle_path,
        "target_lang": target_lang
    })
    return response.json()

def compose_video(video_path, subtitle_path, watermark=None):
    """合成视频"""
    response = requests.post(f"{BASE_URL}/api/compose", json={
        "video_path": video_path,
        "subtitle_path": subtitle_path,
        "watermark": watermark
    })
    return response.json()
```

## 🎬 与现有工具的集成

### 集成方案

```
┌─────────────────────────────────────────────────────────────────┐
│                    完整视频制作流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 生成脚本/提示词                                              │
│     └── MiniMax文本生成                                          │
│          ↓                                                       │
│  2. 视频生成                                                     │
│     └── 海螺视频 / Replicate / Kling                            │
│          ↓                                                       │
│  3. 后处理                                                      │
│     └── MediaFlow (字幕+翻译+水印)                              │
│          ↓                                                       │
│  4. 发布                                                        │
│     └── TikTok / Instagram / X                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 工具对比

| 工具 | 用途 | 优势 |
|------|------|------|
| **MiniMax** | 文本生成 | 快速、便宜 |
| **海螺视频** | 视频生成 | 网页版、简单 |
| **Replicate** | 视频生成 | API可控 |
| **MediaFlow** | 后处理 | 本地、完整功能 |

## 📁 创建集成脚本

```python
#!/usr/bin/env python3
"""
MediaFlow集成工具

功能:
- 视频下载
- 字幕转录
- 翻译
- 合成
"""

import os
import requests
from datetime import datetime

# ============== 配置 ==============
MEDIAFLOW_URL = os.environ.get("MEDIAFLOW_URL", "http://127.0.0.1:8001")

# ============== 功能函数 ==============
def download_video(url: str) -> dict:
    """下载视频"""
    print(f"\n📥 下载视频: {url}")
    
    try:
        response = requests.post(
            f"{MEDIAFLOW_URL}/api/download",
            json={"url": url}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def transcribe_video(video_path: str) -> dict:
    """转录视频"""
    print(f"\n📝 转录视频: {video_path}")
    
    try:
        response = requests.post(
            f"{MEDIAFLOW_URL}/api/transcribe",
            json={"path": video_path}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def translate_subtitle(subtitle_path: str, target_lang: str = "zh") -> dict:
    """翻译字幕"""
    print(f"\n🌍 翻译字幕: {subtitle_path} → {target_lang}")
    
    try:
        response = requests.post(
            f"{MEDIAFLOW_URL}/api/translate",
            json={
                "subtitle_path": subtitle_path,
                "target_lang": target_lang
            }
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def compose_video(video_path: str, subtitle_path: str, 
                  watermark: str = None, output_path: str = None) -> dict:
    """合成视频"""
    print(f"\n🎬 合成视频: {video_path} + {subtitle_path}")
    
    if output_path is None:
        output_path = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    try:
        response = requests.post(
            f"{MEDIAFLOW_URL}/api/compose",
            json={
                "video_path": video_path,
                "subtitle_path": subtitle_path,
                "watermark": watermark,
                "output_path": output_path
            }
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def full_workflow(video_url: str, target_lang: str = "zh", 
                  watermark: str = None) -> dict:
    """完整工作流"""
    print("\n" + "=" * 60)
    print("🚀 MediaFlow 完整工作流")
    print("=" * 60)
    
    # 1. 下载视频
    print("\nStep 1: 下载视频")
    download_result = download_video(video_url)
    if not download_result.get("success"):
        return {"success": False, "step": "download", "error": download_result}
    
    video_path = download_result["path"]
    
    # 2. 转录
    print("\nStep 2: 转录")
    transcribe_result = transcribe_video(video_path)
    if not transcribe_result.get("success"):
        return {"success": False, "step": "transcribe", "error": transcribe_result}
    
    subtitle_path = transcribe_result["subtitle_path"]
    
    # 3. 翻译
    print(f"\nStep 3: 翻译 ({target_lang})")
    translate_result = translate_subtitle(subtitle_path, target_lang)
    
    # 4. 合成
    print("\nStep 4: 合成")
    compose_result = compose_video(video_path, subtitle_path, watermark)
    
    return {
        "success": True,
        "video_path": video_path,
        "subtitle_path": subtitle_path,
        "output": compose_result.get("output_path")
    }

# ============== 主程序 ==============
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║              MediaFlow 集成工具                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                       ║
║  使用方法:                                              ║
║                                                       ║
║    python mediaflow_integration.py download <url>      ║
║    python mediaflow_integration.py transcribe <path>  ║
║    python mediaflow_integration.py translate <path>   ║
║    python mediaflow_integration.py compose <video> <sub>   ║
║    python mediaflow_integration.py workflow <url>     ║
║                                                       ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "download":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = download_video(url)
        print(result)
    
    elif command == "transcribe":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        result = transcribe_video(path)
        print(result)
    
    elif command == "translate":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        lang = sys.argv[3] if len(sys.argv) > 3 else "zh"
        result = translate_subtitle(path, lang)
        print(result)
    
    elif command == "compose":
        video = sys.argv[2] if len(sys.argv) > 2 else ""
        sub = sys.argv[3] if len(sys.argv) > 3 else ""
        result = compose_video(video, sub)
        print(result)
    
    elif command == "workflow":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = full_workflow(url)
        print(result)

if __name__ == "__main__":
    main()
```

## 🎯 下一步

1. **本地安装MediaFlow**
2. **启动服务** (http://127.0.0.1:8001)
3. **集成到工作流**

## 📚 资源链接

- **GitHub**: https://github.com/CheshireMew/MediaFlow
- **依赖**: Python 3.10+, Node.js 18+, FFmpeg

---

*MediaFlow Integration Guide v1.0*
*Created: 2026-02-19*
