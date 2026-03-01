# 素材收集系统 - 基于MediaFlow

> **Focus**: 素材收集与整理
> **Tools**: yt-dlp, faster-whisper, FFmpeg
> **Date**: 2026-02-19

---

## 📋 素材收集流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                    素材收集完整流程                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   1️⃣  发现素材     →     2️⃣  下载素材     →     3️⃣  转录素材      │
│   (手动/监控)              (yt-dlp)                  (faster-whisper)  │
│                                                                      │
│   4️⃣  整理归档     →     5️⃣  内容分析     →     6️⃣  二次创作      │
│   (分类存储)              (AI分析)                  (生成新内容)      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 素材类型

### 1. 奢侈品/珠宝视频

| 类型 | 来源 | 用途 |
|------|------|------|
| 产品展示 | Instagram, YouTube | 参考、灵感 |
| 开箱视频 | TikTok, YouTube | 内容素材 |
| 搭配教程 | 小红书, B站 | 文案参考 |
| 品牌广告 | 官网, 官微 | 风格学习 |

### 2. Crypto/Meme视频

| 类型 | 来源 | 用途 |
|------|------|------|
| KOL分析 | Twitter, YouTube | Alpha来源 |
| 趋势解读 | TikTok, YouTube | 内容素材 |
| Meme文化 | Twitter, Telegram | 梗库收集 |
| 项目介绍 | 官网, Medium | 深度研究 |

### 3. 生活方式

| 类型 | 来源 | 用途 |
|------|------|------|
| 奢华生活 | Instagram | 配图素材 |
| 旅行打卡 | 小红书 | 地点参考 |
| 美食探店 | 大众点评 | 内容灵感 |

---

## 🛠️ 已安装工具

### 1. yt-dlp - 视频下载

```bash
# 基本下载
yt-dlp "https://www.youtube.com/watch?v=xxx"

# 下载最佳质量视频+音频
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" "URL"

# 下载字幕
yt-dlp --write-subs --sub-langs en "URL"

# 下载整个播放列表
yt-dlp -i "https://www.youtube.com/playlist?list=xxx"

# 只下载音频
yt-dlp -x --audio-format mp3 "URL"
```

### 2. faster-whisper - 语音转文字

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="auto")
segments, info = model.transcribe("audio.mp3", language="zh")

for segment in segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

### 3. FFmpeg - 视频处理

```bash
# 提取音频
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 audio.wav

# 压缩视频
ffmpeg -i input.mp4 -vcodec libx264 -crf 23 output.mp4

# 截取片段
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c copy output.mp4

# 添加水印
ffmpeg -i input.mp4 -i watermark.png -filter_complex overlay output.mp4
```

---

## 📁 素材存储结构

```
/root/.openclaw/workspace/materials/
├── video-materials/          # 视频素材
│   ├── raw/                 # 原始下载
│   ├── processed/          # 处理后
│   └── archive/            # 归档
├── audio/                  # 音频素材
│   ├── original/          # 原始音频
│   └── transcribed/       # 转录文本
├── images/                 # 图片素材
│   ├── products/          # 产品图
│   ├── lifestyle/         # 场景图
│   └── references/        # 参考图
├── subtitles/              # 字幕文件
│   ├── original/         # 原字幕
│   └── translated/       # 翻译字幕
└── database/              # 素材数据库
    ├── metadata.json      # 素材元数据
    └── tags.json          # 标签索引
```

---

## 🔧 素材收集脚本

### 批量下载脚本

```bash
#!/bin/bash
# 批量下载视频素材

OUTPUT_DIR="/root/.openclaw/workspace/video-materials/raw"
LINKS_FILE="/root/.openclaw/workspace/video-materials/links.txt"

# 读取链接文件并下载
while IFS= read -r url; do
    echo "下载: $url"
    yt-dlp -o "${OUTPUT_DIR}/%(title)s_%(id)s.%(ext)s" \
           -f "bestvideo[height<=1080]+bestaudio/best" \
           --no-playlist \
           "$url"
done < "$LINKS_FILE"
```

### 素材转录脚本

```python
#!/usr/bin/env python3
"""素材转录工具"""

import os
from faster_whisper import WhisperModel

def transcribe_directory(input_dir: str, output_dir: str):
    """转录目录下所有视频"""
    model = WhisperModel("small", device="auto")
    
    for filename in os.listdir(input_dir):
        if filename.endswith(('.mp4', '.mkv', '.wav', '.mp3')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.rsplit('.', 1)[0] + '.txt')
            
            print(f"转录: {filename}")
            segments, info = model.transcribe(input_path, language="zh")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for segment in segments:
                    f.write(f"{segment.start:.2f}s - {segment.end:.2f}s: {segment.text}\n")
            
            print(f"  → 保存到: {output_path}")
```

### 素材管理脚本

```python
#!/usr/bin/env python3
"""素材数据库管理"""

import json
import os
from datetime import datetime
from pathlib import Path

class MaterialDatabase:
    def __init__(self, db_path: str = "/root/.openclaw/workspace/materials/database"):
        self.db_path = db_path
        self.metadata_file = os.path.join(db_path, "metadata.json")
        self.tags_file = os.path.join(db_path, "tags.json")
        self.load()
    
    def load(self):
        """加载数据库"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.materials = json.load(f)
        else:
            self.materials = {}
        
        if os.path.exists(self.tags_file):
            with open(self.tags_file, 'r') as f:
                self.tags = json.load(f)
        else:
            self.tags = {}
    
    def save(self):
        """保存数据库"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.materials, f, indent=2, ensure_ascii=False)
        
        with open(self.tags_file, 'w') as f:
            json.dump(self.tags, f, indent=2, ensure_ascii=False)
    
    def add_material(self, path: str, material_type: str, tags: list, source: str = ""):
        """添加素材"""
        file_path = str(Path(path).resolve())
        file_size = os.path.getsize(path)
        file_ext = Path(path).suffix
        
        material_id = f"{material_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.materials[material_id] = {
            "id": material_id,
            "path": file_path,
            "type": material_type,
            "size": file_size,
            "ext": file_ext,
            "tags": tags,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "status": "pending"  # pending, processed, archived
        }
        
        # 更新标签索引
        for tag in tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag].append(material_id)
        
        self.save()
        return material_id
    
    def search(self, query: str = None, tags: list = None, material_type: str = None):
        """搜索素材"""
        results = list(self.materials.values())
        
        if material_type:
            results = [m for m in results if m["type"] == material_type]
        
        if tags:
            for tag in tags:
                results = [m for m in results if tag in m["tags"]]
        
        return results
    
    def get_stats(self):
        """获取统计"""
        total = len(self.materials)
        by_type = {}
        by_status = {}
        
        for m in self.materials.values():
            by_type[m["type"]] = by_type.get(m["type"], 0) + 1
            by_status[m["status"]] = by_status.get(m["status"], 0) + 1
        
        return {
            "total": total,
            "by_type": by_type,
            "by_status": by_status
        }
```

---

## 📊 素材统计

### 目标平台

| 平台 | 内容类型 | 频率 |
|------|----------|------|
| TikTok | 短视频 | 3-5条/天 |
| Instagram | 图片/Reels | 2-3条/天 |
| YouTube | 长视频 | 1-2条/周 |
| X (Twitter) | 推文 | 5-10条/天 |
| 微信公众号 | 文章 | 2-3篇/周 |

### 素材需求

| 类型 | 每日需求 | 来源 |
|------|----------|------|
| 视频素材 | 2-3个 | YouTube, TikTok |
| 图片素材 | 5-10张 | Instagram, Pinterest |
| 文案参考 | 3-5篇 | 竞品账号 |
| Alpha来源 | 1-2个 | Crypto KOLs |

---

## 🔄 日常工作流

### 每日任务

```
早上 (9:00-10:00):
  1. 检查订阅的创作者更新
  2. 下载最新素材
  3. 转录重要视频

下午 (14:00-17:00):
  4. 整理素材
  5. AI分析内容
  6. 准备明日素材列表

晚上 (20:00-21:00):
  7. 监控趋势
  8. 收集灵感
  9. 规划内容
```

### 周度任务

```
周一:
  - 上周素材回顾
  - 本周内容规划

周二至周四:
  - 日常素材收集
  - 内容创作

周五:
  - 周度素材归档
  - 下周规划

周末:
  - 行业趋势研究
  - 竞品分析
```

---

## 🎯 收集策略

### 1. 主动收集

```bash
# 指定来源批量下载
yt-dlp -a urls.txt -o "%(uploader)s/%(title)s.%(ext)s"
```

### 2. 被动监控

```python
# 监控频道更新
from yt_dlp import YoutubeDL

def monitor_channel(channel_url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(channel_url, download=False)
        for video in info['entries'][0:5]:  # 最新5个
            print(f"{video['title']}: {video['webpage_url']}")
```

### 3. 趋势发现

```
关注:
- 热搜话题
- 病毒式传播内容
- 行业KOL更新
- 新兴创作者
```

---

## 📈 效果评估

### 素材质量指标

| 指标 | 说明 | 目标 |
|------|------|------|
| 下载成功率 | 成功下载/尝试下载 | >90% |
| 转录准确率 | AI转录 vs 人工校对 | >85% |
| 使用率 | 使用素材/总收集 | >30% |
| 转化率 | 带来互动/发布内容 | >5% |

### 效率指标

| 指标 | 说明 | 目标 |
|------|------|------|
| 收集速度 | 素材/小时 | >10个 |
| 处理速度 | 视频转录/小时 | >2个 |
| 存储效率 | 压缩率 | >50% |

---

## 🚀 快速开始

### 1. 创建目录结构

```bash
mkdir -p /root/.openclaw/workspace/{video-materials/{raw,processed,archive},audio/{original,transcribed},images/{products,lifestyle,references},subtitles/{original,translated},database}
```

### 2. 配置下载脚本

```bash
# 设置别名
alias dl-video="yt-dlp -o 'video-materials/raw/%(uploader)s/%(title)s.%(ext)s'"
alias dl-audio="yt-dlp -x --audio-format mp3 -o 'audio/original/%(title)s.%(ext)s'"
```

### 3. 开始收集

```bash
# 下载单个视频
dl-video "https://www.youtube.com/watch?v=xxx"

# 下载音频
dl-audio "https://www.youtube.com/watch?v=xxx"

# 转录音频
python tools/transcribe.py audio/original/xxx.mp3
```

---

*素材收集系统 v1.0*
*Created: 2026-02-19*
