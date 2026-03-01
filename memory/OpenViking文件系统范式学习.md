# OpenViking 文件系统记忆范式 - 学习笔记

> 来源: https://github.com/volcengine/OpenViking/
> 学习时间: 2026-02-19
> 状态: 已学习，待实践

---

## 🎯 核心问题

### 传统RAG的缺陷

| 问题 | 描述 |
|------|------|
| **健忘症** | Agent记不住完整上下文 |
| **幻觉** | 检索到不相关的碎片化信息 |
| **平面检索** | 把文档切成碎片扔进大桶，像"大海捞针" |
| **Token浪费** | 读取大量无关片段 |

### 传统RAG工作流程

```
文档 → 切碎 → 向量库
               ↓
用户查询 → 相似度搜索 → 取出Top-K碎片 → 拼凑给LLM
               ↓
         ❌ 可能返回不相关信息
         ❌ 缺乏层次结构
         ❌ Token消耗大
```

---

## 💡 OpenViking的解决方案：文件系统范式

### 核心理念

**从"造书签"进化到"造图书馆索引"**

### 三层立体结构

```
┌─────────────────────────────────────────┐
│  L0 (摘要层) - 文件夹目录                 │
│  "先定领域，快速定位"                      │
│  Token消耗: 极少                          │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  L1 (概览层) - 文件大纲                   │
│  "确定相关后，读大纲"                      │
│  Token消耗: 少                            │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  L2 (细节层) - 具体内容                   │
│  "最后才看逻辑行"                         │
│  Token消耗: 完整                          │
└─────────────────────────────────────────┘
           ↓
    ┌──────────────────┐
    │  向量库(Milvus/   │
    │  Chroma)底层存储  │
    └──────────────────┘
```

### 工作流程对比

| 传统RAG | 文件系统范式 |
|---------|-------------|
| 搜"代码" → 100条碎片 | 1. 定项目目录 |
| ❌ 不相关 | 2. 定具体文件 |
| ❌ Token浪费 | 3. 看逻辑行 |
| | ✅ 精准定位 |

---

## 🏗️ 实现架构

### 1. L0: 摘要层 (Abstract)

**功能**: 领域定位
**内容**: 
- 文件夹名称
- 领域分类
- 摘要说明

**示例**:
```
memory/
├── 📁 agent-skills/     # Agent技能相关
├── 📁 user-context/     # 用户上下文
├── 📁 project-memory/   # 项目记忆
├── 📁 daily-logs/       # 每日日志
└── 📁 long-term/        # 长期记忆
```

### 2. L1: 概览层 (Overview)

**功能**: 文件级定位
**内容**:
- 文件大纲
- 关键节点
- 摘要信息

**示例**:
```
agent-skills/
├── SKILL.md          # 技能定义
├── 技能列表.md       # 技能索引
├── 📄 skill-001.md   # 技能详情 (大纲)
└── 📄 skill-002.md   # 技能详情 (大纲)
```

### 3. L2: 细节层 (Detail)

**功能**: 精准内容
**内容**:
- 具体行/块
- 完整上下文
- 逻辑关系

---

## 🔧 技术实现要点

### 1. 向量库分层

```python
# 传统方式
all_chunks = ["chunk1", "chunk2", ...]  # 扁平化
results = vector_store.search("query", top_k=10)

# 文件系统范式
layer0_indexes = {
    "agent-skills": vector_index_0,
    "user-context": vector_index_1,
    "project-memory": vector_index_2
}

layer1_indexes = {
    "agent-skills/SKILL.md": vector_index_0_0,
    "agent-skills/技能列表.md": vector_index_0_1
}

# 检索流程
def retrieve(query):
    # Step 1: L0检索 - 找到相关领域
    domain = layer0_search(query)  # 返回: "agent-skills"
    
    # Step 2: L1检索 - 找到相关文件
    file = layer1_search(query, domain)  # 返回: "agent-skills/SKILL.md"
    
    # Step 3: L2检索 - 获取具体内容
    content = layer2_search(query, file)  # 返回: 精准片段
    
    return content
```

### 2. 索引维护

```python
class FileSystemMemory:
    def __init__(self):
        self.layers = {
            'L0': {},  # 领域索引
            'L1': {},  # 文件索引
            'L2': {}   # 块索引
        }
    
    def add_document(self, path, content):
        # L0: 生成摘要索引
        abstract = self.generate_abstract(content)
        self.layers['L0'][path] = vectorize(abstract)
        
        # L1: 生成大纲索引
        outline = self.generate_outline(content)
        self.layers['L1'][path] = vectorize(outline)
        
        # L2: 切块索引
        chunks = self.chunk_content(content)
        self.layers['L2'][path] = [vectorize(c) for c in chunks]
    
    def retrieve(self, query):
        # Step 1: L0检索
        domain = self.search_layer('L0', query)
        
        # Step 2: L1检索
        file = self.search_layer('L1', query, domain=domain)
        
        # Step 3: L2检索
        content = self.search_layer('L2', query, file=file)
        
        return content
```

### 3. Token优化

| 层级 | 检索内容 | Token消耗 |
|------|----------|----------|
| L0 | 领域摘要 | ~100 tokens |
| L1 | 文件大纲 | ~500 tokens |
| L2 | 具体内容 | ~2000 tokens |
| **总计** | | **~2600 tokens** |
| vs 传统RAG | | **~5000+ tokens** |

**节省Token**: ~50%

---

## 📊 效果对比

| 指标 | 传统RAG | 文件系统范式 |
|------|---------|-------------|
| 检索精度 | 60-70% | 90%+ |
| Token消耗 | 高 | 低50% |
| 记忆深度 | 浅 | 深 |
| 幻觉率 | 高 | 低 |
| 定位速度 | 慢 | 快 |

---

## 🧠 对我的启发

### 当前OpenClaw的记忆系统

```
MEMORY.md          ← 扁平化
memory/*.md        ← 碎片化
```

### 可以改进的方向

#### 1. 引入层级结构

```
workspace/
├── 📁 MEMORY/              # L0: 领域层
│   ├── user_context.md     # 用户上下文
│   ├── project_memory.md   # 项目记忆
│   ├── skills_index.md     # 技能索引
│   └── long_term.md        # 长期记忆
│
├── 📁 skills/              # L1: 技能层
│   ├── skill-001.md
│   └── skill-002.md
│
└── 📁 projects/            # L2: 项目层
    ├── project-alpha.md
    └── project-beta.md
```

#### 2. 目录递归检索

```python
async def hierarchical_retrieve(query):
    # Step 1: 检索领域 (L0)
    domains = await search_domains(query)  # 返回: ["skills", "user_context"]
    
    # Step 2: 检索文件 (L1) 
    files = await search_files(query, domains)  # 返回: ["skills/coding"]
    
    # Step 3: 检索细节 (L2)
    content = await search_content(query, files)  # 返回: 精准片段
    
    return content
```

#### 3. 动态摘要

- 自动生成每个文件的摘要
- 定期更新层级索引
- 根据使用频率调整层级

---

## 🎯 实践计划

### 短期 (1周内)

- [ ] 重构MEMORY.md为目录结构
- [ ] 创建L0摘要层
- [ ] 实现层级检索脚本

### 中期 (1个月内)

- [ ] 完整实现文件系统范式
- [ ] 测试对比效果
- [ ] 优化Token消耗

### 长期 (3个月)

- [ ] 集成向量库
- [ ] 实现自动摘要生成
- [ ] 建立完整记忆系统

---

## 🔗 参考资源

- OpenViking GitHub: https://github.com/voloclete/OpenViking/
- Milvus向量库: https://milvus.io/
- Chroma向量库: https://www.trychroma.com/

---

## 💡 金句

> "这套'文件系统范式'，才是Agent真正拥有大脑的样子。"

> "从'造书签'进化到'造图书馆索引'"

---

*学习笔记 v1.0 | 2026-02-19*
*来源: OpenViking GitHub项目*
*主题: Agent记忆系统重构*