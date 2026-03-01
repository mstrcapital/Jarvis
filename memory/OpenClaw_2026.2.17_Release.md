# OpenClaw 2026.2.17 Release - 学习笔记

> **版本**: 2026.2.17
> **发布日期**: 2026-02-18
> **来源**: https://github.com/openclaw/openclaw/releases
> **状态**: 已学习

---

## 🎯 核心更新摘要

这是一个**重大更新**，包含**50+项改进**，涵盖：

- ✅ 1M上下文支持
- ✅ Anthropic Sonnet 4.6
- ✅ 子Agent系统改进
- ✅ iOS原生功能增强
- ✅ Slack/Discord消息流
- ✅ Cron定时任务优化
- ✅ 记忆搜索FTS

---

## 🔥 重点功能

### 1. 1M上下文Beta

```
Agents/Anthropic: 添加1M上下文Beta支持

配置方式:
params:
  context1m: true

效果:
- 支持100万token上下文
- 适用于长文档分析
- 显著提升复杂任务能力
```

### 2. Anthropic Sonnet 4.6

```
支持最新模型:
- anthropic/claude-sonnet-4-6
- 向后兼容Sonnet 4.5

优势:
- 更强推理能力
- 更好的代码生成
- 改进的多语言支持
```

### 3. 子Agent系统 (Subagents)

```
新功能:
- /subagents spawn 命令 - 从聊天激活子Agent
- 上下文前缀保留 - 追踪消息来源
- 响应注释 - 解释子Agent状态
- 上下文溢出保护 - 防止崩溃

改进:
- 工具结果压缩
- 防止上下文溢出
- 错误恢复机制
```

### 4. iOS原生功能

```
iOS Share扩展:
- 分享URL/文本/图片到Agent
- 自动路由到gateway
- 可选回执确认

Talk模式增强:
- 后台监听开关
- 语音提示切换
- 打断行为优化
-  barge-in行为改进
```

### 5. 消息平台增强

#### Slack

```
新功能:
- 原生单消息文本流
- 流式预览配置
- 流/普通模式切换

命令:
chat.startStream
chat.appendStream  
chat.stopStream
```

#### Telegram

```
Inline按钮样式:
- primary
- success
- danger

消息反应通知:
- 用户反应作为系统事件
- 可配置通知范围
```

#### Discord

```
原生命令:
/exec with host/security/ask/node

交互组件:
- 可复用按钮
-  per-button用户限制
- 表情反应动作
```

### 6. Cron定时任务

```
改进:
- 定时交错(stagger)控制
- 每任务定时精确控制
- 使用报告脚本

新命令:
openclaw cron add --stagger
openclaw cron edit --stagger
openclaw cron add --exact

监控:
- 模型/提供者使用统计
- Token使用聚合报告
```

### 7. 记忆搜索增强

```
FTS回退:
- 全文搜索作为备选
- 查询扩展支持

改进:
- 搜索精度提升
- 相关性排序
```

---

## 🔧 技术改进

### 工具显示

```
Web UI:
- 意图优先工具视图
- 执行摘要
- 工具详情展示
```

### 浏览器

```
额外参数:
extraArgs:
  config:
    browser:
      extraArgs:
        - --no-sandbox
        - --disable-setuid-sandbox
```

### 消息

```
元数据增强:
- 包含inbound message_id
- 包含sender_id
- 支持Moderation工作流
```

---

## 📱 平台特定更新

### iOS

| 功能 | 说明 |
|------|------|
| Share扩展 | 分享内容到Agent |
| Talk模式 | 后台监听、语音提示、打断优化 |
| iMessage | 支持replyToId |

### Slack

| 功能 | 说明 |
|------|------|
| 消息流 | 原生文本流式传输 |
| 预览配置 | 可配置流式预览 |
| 回复模式 | replyToMode配置 |

### Telegram

| 功能 | 说明 |
|------|------|
| Inline按钮 | 三种样式支持 |
| 反应通知 | 用户反应系统事件 |
| 消息反应 | 可配置通知 |

### Discord

| 功能 | 说明 |
|------|------|
| /exec命令 | 原生命令选项 |
| 可复用组件 | 按钮/选择/表单 |
| 按钮权限 | per-button用户白名单 |

### Mattermost

| 功能 | 说明 |
|------|------|
| 表情反应 | 带remove标志 |
| 反应事件 | 事件通知 |

---

## 🛠️ 修复和问题

### Bug修复

```
Agent/Image:
- 压缩诊断信息
- 可见像素/字节大小
- 更快的问题排查

Subagents:
- 上下文溢出保护
- 工具结果压缩
- 错误恢复机制
```

### 已知问题

- 无重大阻塞问题
- 持续优化中

---

## 📊 性能提升

| 领域 | 改进 |
|------|------|
| 上下文支持 | +1M token |
| 记忆搜索 | FTS + 查询扩展 |
| 消息流 | Slack流式传输 |
| Cron | 交错控制 |

---

## 🎯 对我的影响

### 可立即使用的功能

```
1. 1M上下文:
   - 长文档分析
   - 复杂代码审查
   - 多文件项目理解

2. 子Agent:
   - 并行任务处理
   - 专业任务分流
   - 错误恢复

3. iOS分享:
   - 快速分享内容
   - 跨设备协作
```

### 建议启用的功能

```
高优先级:
1. params.context1m: true (1M上下文)
2. /subagents spawn (子Agent)
3. FTS回退 (记忆搜索)

中优先级:
1. Slack流式传输
2. Telegram按钮样式
3. Cron交错控制
```

---

## 🔗 相关链接

- **Release页面**: https://github.com/openclaw/openclaw/releases
- **GitHub**: https://github.com/openclaw/openclaw
- **文档**: https://docs.openclaw.ai
- **Discord**: https://discord.com/invite/clawd

---

## 📝 行动项

- [ ] 测试1M上下文支持
- [ ] 启用子Agent功能
- [ ] 配置Cron交错控制
- [ ] 启用记忆FTS搜索
- [ ] 测试iOS Share扩展

---

*学习笔记 v1.0 | 2026-02-19*
*来源: OpenClaw GitHub Releases*