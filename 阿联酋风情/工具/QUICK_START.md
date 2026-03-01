# Postiz 自动化发布 - 快速开始

> **创建时间**: 2026-02-15 22:15
> **版本**: v1.0

---

## 📦 已创建的文件

```
工具/
├── postiz-upload.js    # 主脚本 (8KB) ✅
├── run.sh             # 一键运行脚本 ✅
├── package.json       # 依赖配置 ✅
└── README.md          # 详细文档 ✅
```

---

## 🚀 快速开始

### 步骤1：配置API Key

```bash
# 编辑 postiz-upload.js
vi postiz-upload.js

# 找到 CONFIG.API_KEY
# 替换为你的Postiz API Key
```

获取API Key：
1. 登录 https://postiz.com
2. Settings → API
3. 复制API Key

### 步骤2：运行

```bash
# 方式1：一键菜单
./run.sh

# 方式2：直接运行
node postiz-upload.js

# 方式3：批量上传
node postiz-upload.js --batch
```

---

## 📖 使用示例

### 查看已连接频道

```bash
node postiz-upload.js
```

输出：
```
👤 用户: 你的名字
📋 已连接的频道:
  - YouTube [ID: abc123]
  - TikTok [ID: def456]
  - Twitter [ID: ghi789]
```

### 上传单个视频

```javascript
// 在 postiz-upload.js 中取消注释这部分

await uploader.uploadVideo({
  videoPath: './素材/视频/迪拜城市风光.mp4',
  caption: '迪拜城市风光 - 航拍视频',
  tags: ['迪拜', '旅行', '航拍'],
  scheduledAt: null, // null表示立即发布
  channelIds: ['abc123', 'def456'],
});
```

### 批量上传

```javascript
const batchItems = [
  {
    videoPath: './素材/视频/video1.mp4',
    caption: '迪拜华人生活',
    tags: ['华人在迪拜'],
  },
  {
    videoPath: './素材/视频/video2.mp4',
    caption: '迪拜奢华体验',
    tags: ['奢华', '酒店'],
  },
];

await uploader.batchUpload(batchItems);
```

---

## 📋 Postiz 配置流程

### 1. 注册Postiz
- 官网: https://postiz.com
- 用GitHub/Google登录

### 2. 连接平台
- YouTube
- TikTok
- Twitter/X
- LinkedIn
- Instagram

### 3. 设置定时
- 创建Queue
- 设置发布时间
- 启用自动发布

---

## 🎯 工作流

### 当前流程（方案B）

```
素材库 → 我生成样本 → 你手动发布
```

### 配置Postiz后

```
素材库 → 我生成样本 → Postiz自动上传 → 定时发布 → 各平台
```

### 你的操作

1. ✅ 生成内容（我来）
2. ✅ 上传Postiz（脚本）
3. ⏳ 最后检查（你来）
4. ✅ 自动发布！

---

## ⚠️ 重要提醒

1. **API Key保密**：不要分享给他人
2. **请求频率**：不要过于频繁
3. **文件大小**：限制100MB以下
4. **版权**：确保有发布权限

---

## 📞 常见问题

| 问题 | 解决方案 |
|------|----------|
| API Key错误 | 检查配置，重新复制 |
| 频道ID为空 | 先连接频道 |
| 上传失败 | 检查网络和文件 |
| 文件太大 | 压缩视频 |

---

## 🔗 相关链接

- [Postiz官网](https://postiz.com)
- [Postiz API文档](https://docs.postiz.com)
- [Larry的方案](https://x.com/oliverhenry/status/...)

---

*快速开始指南 v1.0 | 2026-02-15*