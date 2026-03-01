# X (Twitter) 素材来源管理

## 核心追踪账号

### 政治/军事
| 账号 | @用户名 | 类型 | 优先级 | 备注 |
|------|---------|------|--------|------|
| Trump | @realDonaldTrump | 原始发布 | ⭐⭐⭐ | 同步Truth Social |
| President | @POTUS | 官方声明 | ⭐⭐⭐ | 拜登/未来总统 |
| 国防部长 | @SecDef | 国防部 | ⭐⭐ | 军事动态 |
| 国务卿 | @StateDept | 国务院 | ⭐⭐ | 外交动态 |
| 白宫 | @WhiteHouse | 官方发布 | ⭐⭐⭐ | 政策声明 |

### 财经媒体
| 账号 | @用户名 | 类型 | 优先级 | 备注 |
|------|---------|------|--------|------|
| WSJ | @WSJ | 财经新闻 | ⭐⭐⭐ | 权威媒体 |
| Financial Times | @financialtimes | 财经新闻 | ⭐⭐⭐ | 国际视角 |
| Bloomberg | @Bloomberg | 财经新闻 | ⭐⭐⭐ | 市场数据 |
| Reuters | @Reuters | 通讯社 | ⭐⭐⭐ | 突发快讯 |
| AP | @AP | 通讯社 | ⭐⭐ | 突发新闻 |

### 股市/交易
| 账号 | @用户名 | 类型 | 优先级 | 备注 |
|------|---------|------|--------|------|
| CNBC | @CNBC | 电视财经 | ⭐⭐ | 市场分析 |
| Wall St. | @WallStreetC | 华尔街见闻 | ⭐⭐ | 中文视角 |
| Tesla | @elonmusk | 风向标 | ⭐⭐ | 市场影响者 |

## 关键词监控

### 核心关键词（高频搜索）
```
Trump, US Stock Market, NASDAQ, S&P 500, Dow Jones
Pentagon, US Military, Defense
Fed, Federal Reserve, Interest Rate
China Trade, Tariff, Export
```

### 扩展关键词（每日搜索）
```
Congress, Senate, House
Election, Voting, Campaign
Ukraine, NATO, Russia, China
```

## 采集时间节点

| 时间 | GMT+8 | 目标 | 重点 |
|------|-------|------|------|
| 06:00 | 早间 | Trump夜间动态 | Truth Social + X |
| 09:30 | 开盘前 | 美股盘前 | 重大事件汇总 |
| 14:00 | 午间 | 午盘分析 | 午后重要动态 |
| 21:00 | 收盘后 | 日内总结 | 全天热点回顾 |

## 热度评估标准

| 热度 | 指标 | 采用优先级 |
|------|------|------------|
| 🔴 高 | 转发>1000, 互动>5000, 官方认证 | 立即采用 |
| 🟡 中 | 转发>100, 互动>500 | 整理归档 |
| 🟢 低 | 普通动态 | 按需筛选 |

## 采集工具
- `web_search` 关键词搜索
- `web_fetch` 账号时间线抓取
- X高级搜索语法: `from:realDonaldTrump since:2026-02-14`