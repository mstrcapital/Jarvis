---
name: agent-reach
description: 给 AI Agent 装上互联网能力。读取 Twitter YouTube Reddit GitHub B站 小红书等。安装 pip install agent-reach 然后 agent-reach install
---

# Agent-Reach Skill

> 给 AI Agent 装上互联网能力 - 读取 Twitter、YouTube、Reddit、GitHub、B站、小红书等

**安装:** `pip install agent-reach --break-system-packages && agent-reach install --env=auto`  
**状态:** `agent-reach doctor`

---

## 支持的平台

| 平台 | 命令 | 说明 |
|------|------|------|
| 🌐 网页 | `curl https://r.jina.ai/URL` | 读任意网页 |
| 🐦 Twitter/X | `xreach tweet URL --json` | 读推文 |
| 📺 YouTube | `yt-dlp --dump-json "URL"` | 获取视频信息+字幕 |
| 📦 GitHub | `gh repo view owner/repo` | 读仓库 |
| 📺 B站 | `yt-dlp --dump-json "B站URL"` | 视频信息+字幕 |
| 📖 Reddit | `agent-reach search-reddit "关键词"` | 搜索 Reddit |
| 📡 RSS | `agent-reach read "RSS URL"` | 读 RSS 源 |
| 🔍 全网搜索 | `agent-reach search "关键词"` | Exa AI 搜索 |

---

## 常用命令

### 读网页
```bash
# 读取任意网页 (Jina Reader)
curl -s https://r.jina.ai/https://twitter.com/billtheinvestor/status/2026948732424802640
```

### Twitter/X
```bash
# 读取单条推文
xreach tweet "https://x.com/user/status/xxx" --json

# 搜索推文 (需要配置 Cookie)
xreach search "关键词" --json
```

### YouTube
```bash
# 获取视频信息 + 字幕
yt-dlp --dump-json "https://youtube.com/watch?v=xxx"

# 仅提取字幕
yt-dlp --write-sub --skip-download "URL"
```

### GitHub
```bash
# 查看仓库
gh repo view owner/repo

# 搜索代码
gh search code "keyword" --owner owner

# 查看 Issue
gh issue list --owner owner --repo repo
```

### B站
```bash
# 获取视频信息
yt-dlp --dump-json "https://bilibili.com/video/BVxxx"
```

### 全网搜索 (Exa - 免费)
```bash
# 搜索网页
agent-reach search "LLM 趋势 2026"

# 搜索 Reddit
agent-reach search-reddit "bitcoin prediction"

# 搜索 GitHub
agent-reach search-github "AI agent framework"
```

### RSS
```bash
# 读取 RSS 源
agent-reach read "https://example.com/feed.xml"
```

---

## 配置 Twitter Cookie

1. 用 Chrome 登录 Twitter
2. 安装 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 插件
3. 导出 Cookie
4. 配置:
```bash
agent-reach configure twitter-cookies "你的Cookie内容"
```

---

## 状态检查

```bash
# 检查所有渠道状态
agent-reach doctor
```

---

## 示例用法

### 读取一条推文
```bash
xreach tweet "https://x.com/billtheinvestor/status/2026948732424802640" --json
```

### 搜索加密货币相关内容
```bash
agent-reach search-reddit "bitcoin ETF 2026"
```

### 获取 YouTube 视频摘要
```bash
yt-dlp --dump-json "https://youtube.com/watch?v=dQw4w9WgXcQ" | jq -r '.description'
```

### 搜索 GitHub 仓库
```bash
gh search repos "polymarket trading bot" --limit 10
```

---

## 注意事项

- 🐦 Twitter 搜索需要配置 Cookie (用小号!)
- 📕 小红书需要额外配置 MCP
- 🖥️ 服务器 IP 访问 B站/Reddit 可能被封,需要代理
- 🍪 Cookie 存在本地 `~/.agent-reach/config.yaml`, 不上传

---

## 参考

- GitHub: https://github.com/Panniantong/Agent-Reach
- 文档: https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md