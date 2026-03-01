---
name: x-reader
version: 1.0.0
description: Universal content reader - fetch, transcribe, and digest content from any platform (articles, videos, podcasts, tweets)
homepage: https://github.com/runesleo/x-reader
metadata: {"category":"content","supports":["articles","videos","podcasts","tweets"]}
read_when:
  - Reading article content from any URL
  - Extracting video/podcast transcripts
  - Fetching content from WeChat, Bilibili, Twitter, YouTube
---

# x-reader

Universal content reader - fetch, transcribe, and digest content from any platform.

## 支持的平台

| 平台 | 类型 | 字幕 | Whisper 转录 |
|------|------|------|-------------|
| YouTube | 视频 | ✅ | ✅ |
| Bilibili | 视频 | ✅ | ✅ |
| X/Twitter | 视频 | ❌ | ✅ |
| 小宇宙 | 播客 | ❌ | ✅ |
| Apple Podcasts | 播客 | ❌ | ✅ |
| 微信公众号 | 文章 | ✅ | N/A |
| 直接链接 (mp3/mp4) | 任意 | ❌ | ✅ |

## 安装

```bash
# 克隆仓库
git clone https://github.com/runesleo/x-reader.git
cd x-reader

# 安装依赖
pip install -e .

# 或使用 uv
uv pip install -e .
```

## 使用方法

### CLI 命令

```bash
# 读取任意 URL
x-reader https://mp.weixin.qq.com/s/abc123

# 读取推文
x-reader https://x.com/elonmusk/status/123456

# 读取视频 (YouTube/Bilibili)
x-reader https://youtube.com/watch?v=xxx

# 登录平台 (一次性)
x-reader login xhs

# 查看收件箱
x-reader list
```

### MCP Server

```bash
# 启动 MCP 服务器
python mcp_server.py
```

MCP 端点可用于集成到其他 AI 工具。

## 支持的 URL 类型

- **文章**: 微信公众号, Medium, Reddit, 新闻网站
- **视频**: YouTube, Bilibili, Twitter/X
- **播客**: 小宇宙, Apple Podcasts
- **社交**: Twitter 推文, 微博

## 输出格式

统一的结构化输出，包含:
- `title`: 标题
- `content`: 正文内容
- `platform`: 来源平台
- `author`: 作者
- `published_date`: 发布时间
- `media_type`: 媒体类型 (article/video/podcast)
- `transcript`: 视频/播客 Transcript (如果有)

---

*Skill created: 2026-02-27*
*Source: https://github.com/runesleo/x-reader*