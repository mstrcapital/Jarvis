# Postiz 自动上传工具

> 用于阿联酋风情素材库的自动化发布工具

## 📋 目录

- [功能](#功能)
- [安装](#安装)
- [配置](#配置)
- [使用](#使用)
- [示例](#示例)
- [定时发布](#定时发布)

---

## 🚀 功能

- ✅ 上传视频到Postiz
- ✅ 设置定时发布
- ✅ 支持多平台发布
- ✅ 批量上传
- ✅ 标签管理

---

## 📦 安装

```bash
cd /root/.openclaw/workspace/阿联酋风情/工具

# 安装依赖
npm install

# 或者使用pnpm
pnpm install
```

---

## ⚙️ 配置

### 1. 获取API Key

1. 登录 https://postiz.com
2. 进入 **Settings** → **API**
3. 复制 **API Key**

### 2. 修改配置

编辑 `postiz-upload.js`：

```javascript
const CONFIG = {
  // 替换为你的API Key
  API_KEY: 'YOUR_POSTIZ_API_KEY',
  
  // 发布配置
  publish: {
    scheduled_at: '', // ISO格式，为空则立即发布
    channels: [],     // 频道ID数组
    caption: '你的文案',
    tags: ['标签1', '标签2'],
    privacy: 'public',
  },
  
  // 文件路径
  file: {
    video: './素材/视频/你的视频.mp4',
    thumbnail: './素材/图片/封面.jpg',
  },
};
```

### 3. 获取频道ID

运行脚本查看已连接的频道：

```bash
npm run upload
```

输出示例：
```
📋 已连接的频道:
  - YouTube (ID: abc123)
  - TikTok (ID: def456)
  - Twitter (ID: ghi789)
```

---

## 📖 使用

### 方式1：命令行参数

```bash
# 上传单个视频
node postiz-upload.js --video ./video.mp4 --caption "我的文案"

# 批量上传
node postiz-upload.js --batch

# 查看帮助
node postiz-upload.js --help
```

### 方式2：修改脚本运行

```bash
# 编辑 postiz-upload.js 中的使用示例部分
# 取消注释相应代码

# 运行
npm run upload
```

### 方式3：集成到素材库工作流

```javascript
const { PostizUploader, generateTasksFromLibrary } = require('./postiz-upload');

// 从素材库生成任务
const tasks = generateTasksFromLibrary('../阿联酋风情');

// 批量上传
const uploader = new PostizUploader(CONFIG);
await uploader.batchUpload(tasks);
```

---

## 📝 示例

### 示例1：上传单个视频

```javascript
await uploader.uploadVideo({
  videoPath: './素材/视频/迪拜城市风光.mp4',
  caption: '迪拜城市风光 - 航拍视频',
  tags: ['迪拜', '旅行', '航拍'],
  scheduledAt: '2026-02-16T09:00:00Z',
});
```

### 示例2：批量上传

```javascript
const batchItems = [
  {
    videoPath: './素材/视频/video1.mp4',
    caption: '迪拜华人生活第一集',
    tags: ['华人在迪拜', '迪拜生活'],
  },
  {
    videoPath: './素材/视频/video2.mp4',
    caption: '迪拜奢华体验第二集',
    tags: ['迪拜奢华', '酒店'],
  },
  {
    videoPath: './素材/视频/video3.mp4',
    caption: '迪拜旅游攻略第三集',
    tags: ['迪拜旅游', '攻略'],
  },
];

await uploader.batchUpload(batchItems);
```

### 示例3：定时发布

```javascript
const { SCHEDULE_EXAMPLES } = require('./postiz-upload');

// 每天3个时段发布
const today = new Date();
const times = SCHEDULE_EXAMPLES.daily3Times.times;

for (const time of times) {
  const [hours, minutes] = time.split(':');
  today.setHours(hours, minutes, 0, 0);
  
  await uploader.uploadVideo({
    videoPath: video,
    caption: '定时发布',
    scheduledAt: today.toISOString(),
  });
}
```

---

## ⏰ 定时发布

### 方案1：Postiz内置定时

在Postiz后台设置：
1. 创建Post时
2. 设置 "Schedule for later"
3. 选择发布时间

### 方案2：脚本定时

使用cron实现定时上传：

```bash
# 每天9:00, 12:00, 21:00自动上传
0 9,12,21 * * * cd /path/to/tools && node postiz-upload.js --batch
```

### 方案3：集成n8n

1. 安装n8n
2. 创建工作流：
   - 触发：定时（如每天8:00）
   - 执行：运行 `postiz-upload.js`
   - 通知：发送结果到Telegram

---

## 📊 工作流集成

### 完整自动化流程

```
素材库
   ↓
生成图文样本 (我来)
   ↓
生成视频文件 (需要你提供)
   ↓
Postiz上传脚本
   ↓
定时发布队列 (Postiz)
   ↓
YouTube/TikTok/Twitter (自动)
```

### 每日任务

```bash
# 1. 收集新素材
# 2. 生成新样本
# 3. 上传到Postiz
# 4. 设置定时发布

npm run upload:batch
```

---

## ⚠️ 注意事项

1. **API Key安全**: 不要提交到GitHub
2. **请求频率**: 不要太频繁，避免被限制
3. **文件格式**: 支持MP4, MOV, AVI
4. **文件大小**: Postiz限制100MB以下
5. **版权**: 确保有发布权限

---

## 📞 常见问题

### Q: 上传失败？

A: 检查：
- API Key是否正确
- 文件是否存在
- 网络连接

### Q: 频道ID怎么获取？

A: 运行 `npm run upload` 查看

### Q: 能自动发布到小红书吗？

A: 不能，小红书API封闭，需要手动

### Q: 视频太大怎么办？

A: 压缩后再上传
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
```

---

## 📁 文件结构

```
工具/
├── postiz-upload.js    # 主脚本
├── package.json        # 依赖配置
└── README.md           # 本文档
```

---

## 🔗 相关链接

- [Postiz官网](https://postiz.com)
- [Postiz API文档](https://docs.postiz.com)
- [Larry的Postiz使用经验](https://x.com/oliverhenry/status/...)

---

*工具版本: v1.0 | 创建: 2026-02-15*