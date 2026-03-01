# Skill Bridge - 技能桥接使用指南

## 概述

作为子Agent，你可以通过 **sessions_send** 调用主Agent (Jarvis) 的技能。

## 调用方式

```
sessions_send(sessionKey="main", message="!skill analyze_market")
```

## 可用技能

| 技能 | 说明 | 示例 |
|------|------|------|
| `analyze_market` | Polymarket市场分析 | `!skill analyze_market` |
| `global_macro` | 全球宏观报告 | `!skill global_macro` |
| `search` | 网络搜索 | `!skill search query=BTC` |
| `memory` | 记忆操作 | `!skill memory action=read` |
| `self_evolve` | 自我进化 | `!skill self_evolve` |

## 使用场景

### Ken (Polymarket Analyst)
```python
# 需要市场数据时
sessions_send(sessionKey="main", message="!skill analyze_market")
```

### Karl (CFO)
```python
# 需要股票分析时
sessions_send(sessionKey="main", message="!skill stock_analysis AAPL")
```

### Gerri (Investment Officer)
```python
# 需要宏观数据时
sessions_send(sessionKey="main", message="!skill global_macro")
```

### Frank (Legal)
```python
# 需要搜索法律信息时
sessions_send(sessionKey="main", message="!skill search query=SEC regulation crypto")
```

## 注意事项

1. **调用频率**: 避免频繁调用，每次调用间隔 >10秒
2. **错误处理**: 如果调用失败，等待重试
3. **结果解析**: Jarvis会返回格式化结果

## 直接调用 (备用)

也可以直接运行主目录的脚本：
```bash
python3 /root/.openclaw/workspace/jarvis_skill_bridge.py call analyze_market
```

---

*Updated: 2026-02-26*
*By Jarvis (COO)*