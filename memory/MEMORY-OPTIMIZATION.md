# 🧠 JARVIS 记忆系统优化方案

## 当前架构 (需升级)

```
现有:
├── MEMORY.md           # 长期记忆 (人工管理)
├── HEARTBEAT.md        # 定期检查清单
└── memory/
    └── YYYY-MM-DD.md   # 每日原始日志
```

## 优化后架构

```
memory/
├── 📔 MEMORY.md           # 长期记忆 (精选, 重要决策/偏好)
├── 📓 daily/
│   └── YYYY-MM-DD.md     # 每日原始日志
├── 🗂️  topics/              # 主题分类记忆
│   ├── web3.md
│   ├── team.md
│   ├── income-streams.md
│   └── preferences.md
├── 🗃️  archives/            # 归档记忆
│   └── YYYY-MM/           # 按月归档
├── 📊 heartbeat-state.json # 心跳状态追踪
├── 🔍 search-index.json    # 记忆索引 (关键事件)
└── 📋 inbox/               # 跨会话消息队列
```

## 记忆类型定义

| 类型 | 存储位置 | 保留时间 |
|------|----------|----------|
| 核心偏好/身份 | MEMORY.md | 永久 |
| 重要决策/项目 | topics/*.md | 永久 |
| 每日事件 | daily/YYYY-MM-DD.md | 30天 |
| 归档 | archives/YYYY-MM/ | 永久 |

## 关键原则

1. **先记忆，后思考** - 重要事件立即记录
2. **定期整理** - 每周从日log提取到topics
3. **语义索引** - 维护关键事件索引便于搜索
4. **跨会话持久** - 所有记忆存在文件，不依赖session

## 记忆触发器

遇到以下情况时 **必须** 记录:
- [ ] 新成员加入/离开团队
- [ ] 重要决策 (架构/方向/预算)
- [ ] 新技能/工具集成
- [ ] 项目里程碑
- [ ] 错误/教训
- [ ] Marco 的偏好/要求
- [ ] 收入/财务相关

## 搜索能力

维护 `search-index.json`:
```json
{
  "2026-02-24": {
    "team-restructuring": "创建CTO Li, 升级Mustafa",
    "xapi-setup": "配置xAPI MCP",
    "nkmc-setup": "安装nkmc CLI"
  }
}
```

---

**状态**: 优化方案已制定 ✅  
**下一步**: 实施新架构 + 可选: 集成 Mem0/LanceDB 向量搜索
