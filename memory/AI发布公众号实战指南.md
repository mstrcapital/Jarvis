# AI自动发布公众号实战指南 - 学习笔记

> **来源**: @sitinme (https://twitter.com/sitinme/status/2023930738773815314)
> **日期**: 2026-02-18
> **主题**: 让AI帮你发公众号（附避坑指南）
> **效率提升**: 2小时 → 10分钟 (节省90%)

---

## 🎯 核心价值

```
以前: 写稿1h + 排版30min + 配图20min + 检查10min = 2小时
现在: 说一句话 + 检查5min + 发布 = 10分钟

节省: 90% 时间!
```

---

## 📱 一、配置公众号API (5分钟)

### 第1步：获取凭证

```markdown
地址: https://mp.weixin.qq.com/
路径: 设置与开发 → 基本配置

需要:
├── AppID：直接复制显示的值
└── AppSecret：点击"重置"生成（只显示一次，务必保存!）
```

### 第2步：配置IP白名单

```bash
# 获取服务器出口IP
curl ifconfig.me

# 重要：通过代理上网时
# 加代理出口IP，不是本机IP！
```

**错误**: 40164 错误 = IP白名单没配置

### 第3步：告诉AI

```
把 AppID 和 AppSecret 告诉你的 AI 助手
配置完成!
```

---

## 🔄 二、AI发文完整流程

```
用户输入: "帮我写一篇 xxx 的文章，推到公众号草稿箱"

AI自动完成4个步骤:
┌─────────────────────────────────────────────────────────────┐
│ 1. 获取 access_token                                        │
│    AppID + AppSecret → 临时令牌（2小时有效）                │
├─────────────────────────────────────────────────────────────┤
│ 2. 上传图片到微信素材库                                      │
│    公众号只认 mmbiz.qpic.cn 域名的图片                      │
├─────────────────────────────────────────────────────────────┤
│ 3. 生成文章 HTML                                             │
│    公众号本质是 HTML 渲染                                   │
├─────────────────────────────────────────────────────────────┤
│ 4. 推送到草稿箱                                             │
│    调用 draft/add 接口                                      │
└─────────────────────────────────────────────────────────────┘

用户工作: 打开草稿箱 → 预览 → 发布
```

---

## 🚨 三、最大坑：中文乱码

### 问题现象

```
标题、正文，所有中文全变成了 \u4eca\u5929 这种转义码
只有英文和数字正常
```

### 原因

```python
# Python requests 发 JSON 时默认 ensure_ascii=True
# 所有中文被转成 \uXXXX

# 正常情况服务端会自动解码
# 但微信公众号 API 不会——直接当原始文本存进去了
```

### 解决方案

```python
# ❌ 错误写法（会乱码）
requests.post(url, json=data)

# ✅ 正确写法（解决乱码）
requests.post(
    url,
    data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"}
)
```

### 两个关键参数

```python
ensure_ascii=False  # 保留中文原文，不转义
.encode("utf-8")    # 以 UTF-8 字节发送
```

---

## 💣 四、其他踩坑记录

### 坑2：标题太长报 45003

```
微信标题限制: 约64字节（约20个中文字符）
解决: 缩短标题
```

### 坑3：图片不显示

```
公众号过滤所有非微信域名图片
解决: 必须先 uploadimg 到微信素材库
```

### 坑4：HTML标签兼容性差

```
公众号对 h2/ul/li/code 渲染不稳定
解决: 全部用 p + inline style
```

### 坑5：IP白名单是代理出口IP

```
通过代理访问微信API
白名单要加代理出口IP，不是本机IP
```

---

## 📝 五、搭建步骤

```bash
# 1. 安装 OpenClaw
npm install -g openclaw && openclaw onboard

# 2. 去 aigocode.com 注册拿 API Key

# 3. 连接 Telegram bot

# 4. 告诉 AI 公众号 AppID 和 AppSecret

# 5. 开始使用
说: "帮我写篇文章发公众号"
```

---

## 🛠️ 技术实现细节

### WeChat API Endpoints

```python
# 获取 access_token
POST https://api.weixin.qq.com/cgi-bin/token
参数: grant_type=client_credential, appid, secret

# 上传图片
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg
参数: access_token, buffer (图片二进制)

# 发布到草稿箱
POST https://api.weixin.qq.com/cgi-bin/draft/add
参数: access_token, articles (内容数组)
```

### 文章HTML模板

```html
<!-- 推荐的公众号HTML结构 -->
<p>段落文字</p>
<p>段落文字 <strong>加粗</strong></p>
<p><img src="mmbiz.qpic.cn/..." /></p>
```

### 错误码速查

| 错误码 | 含义 | 解决 |
|--------|------|------|
| 40164 | IP白名单 | 添加服务器IP到白名单 |
| 45003 | 标题过长 | 缩短标题 |
| -1 | 系统错误 | 检查参数格式 |

---

## 🎯 对我的启发

### 可立即复制的模式

1. **API凭证管理**
   - AppID/AppSecret 安全存储
   - access_token 2小时自动刷新

2. **图片处理**
   - 必须上传到微信素材库
   - 使用 mmbiz.qpic.cn 域名

3. **中文编码**
   - ensure_ascii=False
   - UTF-8 编码发送

4. **HTML兼容性**
   - 简化标签，全部用 p
   - inline style

### 未来可扩展的场景

```
✓ 飞书文档自动发布
✓ 小红书内容生成
✓ 知乎文章同步
✓ 多平台内容分发
```

---

## 📊 效率对比

| 步骤 | 以前 | 现在 | 节省 |
|------|------|------|------|
| 写稿 | 1h | 0 (AI) | 100% |
| 排版 | 30min | 0 (AI) | 100% |
| 配图 | 20min | 0 (AI) | 100% |
| 检查 | 10min | 5min | 50% |
| **总计** | **2小时** | **10分钟** | **90%** |

---

## 🔗 相关资源

- **微信公众平台**: https://mp.weixin.qq.com/
- **OpenClaw**: https://docs.openclaw.ai
- **aigocode.com**: API中转服务

---

## 📝 Action Items

- [ ] 评估为Marco配置公众号API的可行性
- [ ] 创建飞书文档发布技能（类似模式）
- [ ] 整理HTML模板库
- [ ] 建立图片处理流水线

---

*学习笔记 v1.0 | 2026-02-19*
*来源: @sitinme Twitter/X Thread*
*主题: AI自动化发布公众号*