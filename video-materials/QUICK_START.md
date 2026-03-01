# 视频号素材库 - 快速启动指南

> **创建时间**: 2026-02-15
> **版本**: 1.0

---

## 📋 目录

1. [快速开始](#快速开始)
2. [工具安装](#工具安装)
3. [素材收集](#素材收集)
4. [日常流程](#日常流程)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 步骤1：创建目录结构

```bash
cd /root/.openclaw/workspace/video-materials

# 方式1：使用Shell脚本
bash tools/collect.sh setup

# 方式2：使用Python脚本
python tools/collect.py setup
```

### 步骤2：安装下载工具

```bash
# 安装 yt-dlp (推荐)
pip install yt-dlp

# 或使用 Docker
docker pull yt-dlp/yt-dlp
```

### 步骤3：配置你的收藏夹

在浏览器中创建以下文件夹：

```
📁 迪拜素材
  ├── 📁 Instagram (@dubai, @visitdubai)
  ├── 📁 TikTok (#dubai, #luxury)
  ├── 📁 YouTube (Dubai channels)
  └── 📁 Twitter (@DubaiMediaOffice)
```

---

## 🔧 工具安装

### 必装工具

| 工具 | 用途 | 安装地址 |
|------|------|----------|
| **4K Stogram** | Instagram下载 | [官网](https://www.4kdownload.com/products/product-stogram) |
| **4K Video Downloader** | 视频下载 | [官网](https://www.4kdownload.com/products/video-downloader) |
| **JDownloader 2** | 批量下载 | [官网](https://jdownloader.org) |

### 命令行工具（可选）

```bash
# yt-dlp (YouTube/TikTok下载)
pip install yt-dlp

# instaloader (Instagram下载)
pip install instaloader

# 使用示例
yt-dlp "https://www.youtube.com/watch?v=..."
instaloader profile username
```

### 浏览器扩展

| 扩展 | 用途 |
|------|------|
| TikTok Video Downloader | TikTok下载 |
| Image Downloader | 图片批量下载 |
| Video Downloader Plus | 视频下载 |

---

## 📥 素材收集

### 每日收集时间

| 时间 | 任务 | 目标 |
|------|------|------|
| 08:00 | Instagram刷新 | 10条 |
| 12:00 | TikTok热门 | 15条 |
| 20:00 | YouTube更新 | 10条 |

### 收集步骤

#### 1. Instagram

```
1. 打开 4K Stogram
2. 点击 "Add Account" 或 "Add Tags"
3. 输入: @dubai, @visitdubai, @luxurydubai
4. 设置下载目录: video-materials/素材/迪拜-阿布扎比
5. 点击 "Download"
```

#### 2. TikTok

```
方法1：SSSTik.io
1. 打开 https://ssstik.io
2. 粘贴TikTok链接
3. 点击 "Download"

方法2：4K Video Downloader
1. 复制TikTok链接
2. 打开4K VD
3. 点击 "Paste URL"
4. 选择保存目录
5. 下载
```

#### 3. YouTube Shorts

```
1. 打开 4K Video Downloader
2. 复制YouTube Shorts链接
3. 格式选择: MP4 > 1080p
4. 保存到: video-materials/素材/迪拜-阿布扎比
```

#### 4. Twitter/X

```
1. 打开 https://twdownloader.com
2. 粘贴推文链接
3. 选择画质: 1080p
4. 下载
```

---

## 📁 文件命名规范

### 格式

```
[分类]_[日期]_[来源]_[描述].[扩展名]

示例:
迪拜风光_20260215_@dubai_哈利法塔日落.mp4
土豪日常_20260215_@luxurydubai_超跑车队.mp4
华人故事_20260215_YouTube_迪拜华人访谈.mp4
高清街拍_20260215_@dubai_streets_老城街景.jpg
```

### 来源标识

| 标识 | 来源 |
|------|------|
| IG | Instagram |
| TT | TikTok |
| YT | YouTube |
| TW | Twitter/X |
| UB | Unsplash/Pexels |

---

## 📊 分类归档

### 五大主题

```
素材/
├── 迪拜-阿布扎比/      # 城市风光、地标建筑
├── 土豪日常/           # 超跑、豪宅、奢华
├── 华人群体/           # 在阿华人、华人生活
├── 生活定居/           # 签证、房产、攻略
├── 高清街拍/           # 城市街拍、建筑摄影
└── 已发布/            # 发布后的素材
```

---

## 📋 日常流程

### 每日检查表

1. **早间 (08:00)**
   - [ ] Instagram收集10条
   - [ ] 分类归档
   - [ ] 记录链接

2. **午间 (12:00)**
   - [ ] TikTok收集15条
   - [ ] 版权初步检查
   - [ ] 归档

3. **晚间 (20:00)**
   - [ ] YouTube收集10条
   - [ ] 批量重命名
   - [ ] 版权详细检查
   - [ ] 生成报告

### 每周计划

| 周一 | 周二 | 周三 | 周四 | 周五 | 周六 | 周日 |
|------|------|------|------|------|------|------|
| 攻略 | 土豪 | 华人 | 街拍 | 风情 | 休息 | 整理 |

---

## 📈 数据追踪

### 追踪指标

| 平台 | 核心指标 |
|------|----------|
| 视频号 | 播放量、点赞、分享、完播率 |
| 小红书 | 阅读、点赞、收藏、评论 |
| 抖音 | 播放、点赞、评论、转化 |

### 周报模板

```markdown
## 第X周素材收集报告

### 收集统计
- Instagram: ___条
- TikTok: ___条
- YouTube: ___条
- Twitter: ___条
- **总计**: ___条

### 热门素材
1. ____________
2. ____________

### 待改进
- ____________
```

---

## ❓ 常见问题

### Q1: 下载失败怎么办？

**解决方案**:
1. 检查网络连接
2. 更换代理/VPN
3. 使用备用工具
4. 手动保存链接

### Q2: 素材有水印？

**解决方案**:
1. 寻找无水印版本
2. 联系作者获取授权
3. 使用去水印工具（需授权）
4. 标注来源使用

### Q3: 版权如何确认？

**检查步骤**:
1. 查看素材来源
2. 检查是否有版权声明
3. 联系作者确认
4. 记录授权信息

### Q4: 存储空间不够？

**解决方案**:
1. 删除已发布的素材
2. 压缩图片（ TinyPNG）
3. 归档到云盘
4. 清理重复文件

---

## 🔗 常用链接

### 下载工具

| 工具 | 链接 |
|------|------|
| 4K Stogram | https://www.4kdownload.com/products/product-stogram |
| 4K Video Downloader | https://www.4kdownload.com/products/video-downloader |
| JDownloader 2 | https://jdownloader.org |
| SSSTik | https://ssstik.io |
| Twitter Downloader | https://twdownloader.com |

### 参考资源

| 资源 | 链接 |
|------|------|
| Unsplash | https://unsplash.com |
| Pexels | https://pexels.com |
| Pixabay | https://pixabay.com |

---

## 📞 技术支持

### 遇到问题？

1. 查看日志: `video-materials/日志/`
2. 运行诊断: `python tools/collect.py report`
3. 联系: ____________

---

**记住**: 质量 > 数量。

宁可少收集，也要确保版权清晰、质量优良。

---

*快速启动指南 v1.0 - 2026-02-15*