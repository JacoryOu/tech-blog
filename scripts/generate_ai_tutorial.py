#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客文章自动生成器
每天生成一篇AI智能体/RAG/n8n工作流教程
"""

import os
import json
from datetime import datetime

# 教程主题库 - 简化版
TUTORIAL_TOPICS = [
    {
        "title": "AI智能体入门：从概念到实践",
        "category": "AI",
        "tags": ["AI Agents", "OpenClaw", "入门"],
        "excerpt": "深入理解AI智能体的核心概念，学习如何使用OpenClaw框架构建你的第一个智能助手。",
        "content": """## 什么是AI智能体

AI智能体（AI Agent）是一种能够自主感知环境、做出决策并执行行动的AI系统。与传统的单次问答模型不同，智能体可以：

- **持续运行**：7×24小时不间断工作
- **自主决策**：根据环境变化调整策略
- **工具调用**：使用外部API和工具完成任务
- **记忆管理**：保存和检索历史信息

## 核心架构

```
感知层 → 思考层 → 行动层 → 记忆层
  ↓        ↓        ↓        ↓
输入处理  推理决策  工具执行  知识存储
```

## 实操案例：天气查询助手

```python
import requests

class WeatherAgent:
    def __init__(self):
        self.memory = {}
    
    def perceive(self, user_input):
        # 提取城市名称
        if "天气" in user_input:
            city = user_input.replace("天气", "").replace("怎么样", "").strip()
            return {"intent": "weather", "city": city}
        return {"intent": "unknown"}
    
    def think(self, perception):
        if perception["intent"] == "weather":
            return {"action": "fetch_weather", "params": perception["city"]}
        return {"action": "ask_clarification"}
    
    def act(self, decision):
        if decision["action"] == "fetch_weather":
            return self.get_weather(decision["params"])
        return "请告诉我你想查询哪个城市的天气？"
    
    def get_weather(self, city):
        # 模拟天气API调用
        return f"{city}今天晴朗，温度25°C，适合出行！"

# 使用示例
agent = WeatherAgent()
result = agent.act(agent.think(agent.perceive("北京天气怎么样？")))
print(result)
```

## 进阶：添加记忆功能

```python
def remember(self, key, value):
    self.memory[key] = {
        "value": value,
        "timestamp": datetime.now()
    }

def recall(self, key):
    return self.memory.get(key, {}).get("value")
```

## 常见问题

**Q: 智能体和传统程序有什么区别？**
A: 智能体具备自主性和适应性，能处理不确定性；传统程序是确定性的指令序列。

**Q: 如何评估智能体性能？**
A: 主要指标包括任务完成率、响应时间、错误恢复能力、用户满意度。

## 总结

AI智能体代表了AI应用的新范式。通过合理设计感知-思考-行动-记忆架构，你可以构建出真正有用的智能助手。"""
    },
    {
        "title": "RAG入门：让AI拥有外部知识",
        "category": "AI",
        "tags": ["RAG", "LLM", "向量数据库"],
        "excerpt": "详解检索增强生成（RAG）技术，学习如何让大语言模型访问外部知识库。",
        "content": """## 什么是RAG

RAG（Retrieval-Augmented Generation，检索增强生成）是一种将外部知识检索与语言模型生成能力结合的技术。

### 为什么需要RAG

- **知识时效性**：模型训练数据有截止日期
- **领域专业性**：通用模型缺乏垂直领域知识
- **数据隐私**：企业私有数据不能上传到云端
- **成本控制**：避免频繁微调大模型

## RAG工作原理

```
用户提问 → 向量化 → 检索相关文档 → 拼接上下文 → LLM生成答案
```

## 实操案例：企业知识库问答系统

### 步骤1：准备文档

```python
documents = [
    {
        "id": "doc_1",
        "content": "公司年假政策：入职满1年享受5天年假，满3年享受10天",
        "metadata": {"category": "HR"}
    },
    {
        "id": "doc_2", 
        "content": "报销流程：填写报销单→部门经理审批→财务部审核→打款",
        "metadata": {"category": "财务"}
    }
]
```

### 步骤2：文档切分与向量化

```python
from sentence_transformers import SentenceTransformer
import chromadb

class SimpleRAG:
    def __init__(self):
        self.embedder = SentenceTransformer('BAAI/bge-large-zh-v1.5')
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("docs")
    
    def add_documents(self, docs):
        embeddings = self.embedder.encode([d["content"] for d in docs])
        self.collection.add(
            ids=[d["id"] for d in docs],
            embeddings=embeddings.tolist(),
            documents=[d["content"] for d in docs]
        )
    
    def query(self, question, top_k=2):
        q_embedding = self.embedder.encode([question])
        results = self.collection.query(
            query_embeddings=q_embedding.tolist(),
            n_results=top_k
        )
        return results["documents"][0]

# 使用
rag = SimpleRAG()
rag.add_documents(documents)
context = rag.query("年假有多少天？")
print(context)
```

### 步骤3：生成答案

```python
def answer_question(question, context):
    prompt = f"基于以下文档回答问题：\\n\\n{context}\\n\\n问题：{question}"
    # 调用LLM生成答案
    return llm.generate(prompt)
```

## 优化技巧

1. **混合检索**：语义检索 + 关键词检索
2. **重排序**：使用CrossEncoder对结果重新排序
3. **提示工程**：优化Prompt模板，指导模型如何引用文档

## 常见问题

**Q: RAG和微调哪个更好？**
A: 看场景。RAG适合知识频繁更新的场景，微调适合需要改变模型行为的场景。

**Q: 向量数据库怎么选？**
A: 小项目用Chroma，企业级用Milvus/Pinecone，需要事务用pgvector。"""
    },
    {
        "title": "n8n入门：零代码构建AI自动化工作流",
        "category": "工具",
        "tags": ["n8n", "自动化", "工作流"],
        "excerpt": "学习使用n8n可视化工作流工具，无需编程即可连接AI API和各类服务。",
        "content": """## 什么是n8n

n8n是一个开源的、可视化的工作流自动化工具，类似于Zapier或Make，但可以自托管。

### 核心优势

- **可视化编辑**：拖拽式界面，无需编程
- **400+集成**：支持主流API和服务
- **自托管**：数据完全掌控
- **免费开源**：社区版功能完整

## 安装部署

### Docker快速部署

```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - ~/.n8n:/home/node/.n8n
```

```bash
docker-compose up -d
```

访问 http://localhost:5678 进入n8n界面

## 实操案例：RSS+AI摘要自动化

### 场景
每天自动抓取AI新闻RSS，用GPT生成摘要，发送到飞书。

### 工作流步骤

#### 1. 触发器：定时任务
- 节点：Schedule Trigger
- 配置：每天上午9点执行

#### 2. 获取RSS内容
- 节点：RSS Feed Read
- URL: `https://www.jiqizhixin.com/rss`

#### 3. AI生成摘要
- 节点：OpenAI Chat Model
- System Prompt: "用3句话总结新闻要点"

#### 4. 发送到飞书
- 节点：HTTP Request
- Method: POST
- URL: 飞书Webhook地址

### 完整工作流配置

```json
{
  "name": "RSS AI摘要推送",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "cron": "0 9 * * *"
      }
    },
    {
      "type": "n8n-nodes-base.rssFeedRead", 
      "parameters": {
        "url": "https://www.jiqizhixin.com/rss"
      }
    },
    {
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "model": "gpt-4o-mini",
        "prompt": "总结新闻"
      }
    }
  ]
}
```

## 进阶技巧

### 数据转换
使用Function节点编写JavaScript：
```javascript
// 数据清洗
const items = $input.all();
const cleaned = items.map(item => ({
  title: item.json.title?.trim(),
  url: item.json.link
}));
return cleaned;
```

### 条件分支
使用IF节点根据条件分流：
- 条件：文章标题包含"AI"
- True：生成详细摘要
- False：简单记录

## 实际应用场景

| 场景 | 核心节点 |
|------|---------|
| 客服自动回复 | Webhook + OpenAI |
| 数据同步 | MySQL → PostgreSQL |
| 社交媒体 | RSS + Twitter |
| 监控告警 | HTTP监控 + 飞书 |

## 最佳实践

1. **命名规范**：给每个节点起有意义的名称
2. **错误处理**：关键流程配置错误处理
3. **版本管理**：定期导出工作流JSON备份
4. **测试先行**：生产环境前充分测试

## 总结

n8n让自动化变得简单直观。从简单的定时任务到复杂的多系统协调，都可以用可视化方式实现。"""
    },
    {
        "title": "智能体记忆管理：从短期到长期",
        "category": "AI",
        "tags": ["AI Agents", "Memory", "架构"],
        "excerpt": "探索AI智能体的记忆机制，学习如何实现短期上下文记忆和长期知识存储。",
        "content": """## 智能体为什么需要记忆

- **上下文连续性**：跨会话保持对话连贯
- **个性化服务**：记住用户偏好和历史
- **知识积累**：从交互中学习和成长
- **错误避免**：记住失败经历，避免重复

## 记忆类型

### 1. 短期记忆（工作记忆）
```python
class ShortTermMemory:
    def __init__(self, max_turns=10):
        self.history = []
        self.max_turns = max_turns
    
    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]
    
    def get_context(self):
        return self.history
```

### 2. 长期记忆（知识库）
```python
import sqlite3

class LongTermMemory:
    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def store(self, key, value):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO memories VALUES (?, ?, datetime('now'))",
            (key, value)
        )
        conn.commit()
        conn.close()
    
    def retrieve(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT value FROM memories WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
```

## 实操案例：个人助理记忆系统

```python
class PersonalAssistant:
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
    
    def chat(self, user_input):
        # 获取长期记忆
        user_name = self.long_term.retrieve("user_name")
        
        # 构建上下文
        context = f"用户名称：{user_name}\\n"
        context += f"近期对话：{self.short_term.get_context()}"
        
        # 生成回复
        response = f"你好{user_name}！{user_input}"
        
        # 更新记忆
        self.short_term.add("user", user_input)
        self.short_term.add("assistant", response)
        
        # 提取新记忆
        if "我叫" in user_input:
            name = user_input.replace("我叫", "").strip()
            self.long_term.store("user_name", name)
        
        return response
```

## 记忆压缩策略

当上下文过长时，需要智能压缩：

```python
def compress_memory(self, memories, max_tokens=2000):
    # 按重要性排序
    sorted_memories = sorted(memories, key=lambda x: x.get("importance", 0), reverse=True)
    
    # 保留高优先级记忆
    compressed = []
    total = 0
    
    for mem in sorted_memories:
        length = len(mem["content"])
        if total + length <= max_tokens:
            compressed.append(mem)
            total += length
    
    return compressed
```

## 最佳实践

1. **分层存储**：短期记忆在内存，长期记忆在数据库
2. **重要性评分**：给记忆设置权重
3. **定期清理**：删除过期或低价值记忆
4. **隐私保护**：敏感信息加密存储

## 总结

合理的记忆管理是智能体的核心能力之一。通过分层存储和智能压缩，可以在有限的上下文中最大化利用历史信息。"""
    },
    {
        "title": "向量数据库选型指南：Pinecone vs Milvus vs Chroma",
        "category": "AI",
        "tags": ["RAG", "向量数据库", "选型"],
        "excerpt": "对比主流向量数据库的特点、性能和适用场景，帮助你选择最适合的向量存储方案。",
        "content": """## 什么是向量数据库

向量数据库专门用于存储和检索高维向量数据，是RAG系统的核心组件。

## 主流向量数据库对比

| 特性 | Chroma | Pinecone | Milvus |
|------|--------|----------|--------|
| 部署方式 | 本地/云 | 纯云服务 | 本地/云 |
| 开源 | ✅ | ❌ | ✅ |
| 扩展性 | 中等 | 高 | 很高 |
| 学习曲线 | 低 | 低 | 中等 |
| 适用规模 | 小到中型 | 中大型 | 大型 |

## Chroma：快速入门首选

### 特点
- 纯Python实现，安装简单
- 无需额外依赖
- 适合原型开发和小型项目

### 代码示例
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_docs")

# 添加文档
collection.add(
    ids=["doc1", "doc2"],
    embeddings=[[0.1, 0.2], [0.3, 0.4]],
    documents=["文本1", "文本2"]
)

# 查询
results = collection.query(
    query_embeddings=[[0.1, 0.2]],
    n_results=2
)
```

## Pinecone：企业级云服务

### 特点
- 全托管，无需运维
- 自动扩展
- 高可用性保证

### 代码示例
```python
import pinecone

pinecone.init(api_key="your-key", environment="us-west1-gcp")
index = pinecone.Index("my-index")

# 添加向量
index.upsert([
    ("id1", [0.1, 0.2], {"category": "tech"}),
    ("id2", [0.3, 0.4], {"category": "biz"})
])

# 查询
results = index.query(
    vector=[0.1, 0.2],
    top_k=2,
    filter={"category": "tech"}
)
```

## Milvus：高性能开源方案

### 特点
- 支持十亿级向量
- 多种索引类型
- 分布式架构

### 代码示例
```python
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

connections.connect("default", host="localhost", port="19530")

# 创建集合
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128)
]
schema = CollectionSchema(fields, "my_collection")
collection = Collection("my_collection", schema)

# 插入数据
collection.insert([[1, 2], [[0.1]*128, [0.2]*128]])

# 创建索引
index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
collection.create_index("embedding", index_params)
```

## 选型建议

| 场景 | 推荐方案 |
|------|---------|
| 个人项目/原型 | Chroma |
| 快速上线，无运维团队 | Pinecone |
| 大规模企业应用 | Milvus |
| 已有PostgreSQL | pgvector |

## 性能优化技巧

1. **选择合适的索引**：HNSW适合高召回，IVF适合高吞吐
2. **维度降维**：使用PCA将高维向量降至合理范围
3. **批量操作**：减少API调用次数
4. **预过滤**：先过滤再向量检索

## 总结

没有最好的向量数据库，只有最适合的。根据团队规模、技术栈和性能需求做选择。"""
    },
    {
        "title": "n8n进阶：复杂条件分支与错误处理",
        "category": "工具",
        "tags": ["n8n", "工作流", "最佳实践"],
        "excerpt": "学习n8n的高级功能，掌握条件分支设计、错误处理和监控告警。",
        "content": """## n8n进阶功能概览

- 条件分支（IF/Switch节点）
- 错误处理和重试
- 数据转换和映射
- 工作流监控

## 条件分支设计

### IF节点基础用法
```
IF 条件判断
├── True分支：条件满足时执行
└── False分支：条件不满足时执行
```

### 实际案例：内容审核工作流

```
Webhook接收内容
    ↓
AI内容审核（OpenAI）
    ↓
IF 审核结果
├── 通过 → 发布到网站
├── 可疑 → 人工审核队列  
└── 拒绝 → 发送拒绝通知
```

### 多条件判断（Switch节点）

```
Switch 根据类型路由
├── 新闻 → RSS处理流程
├── 图片 → 图像识别流程
├── 视频 → 转码处理流程
└── 默认 → 通用处理流程
```

## 错误处理机制

### 基础错误捕获

在每个关键节点后添加Error Trigger：

```
主要节点
    ↓
Error Trigger（捕获错误）
    ↓
发送告警通知
```

### 重试策略

```
API调用节点
├── 成功 → 继续流程
└── 失败 → 等待30秒 → 重试（最多3次）
            ↓
        仍失败 → 记录日志 → 人工介入
```

### 错误处理配置示例

```json
{
  "nodes": [
    {
      "name": "API调用",
      "type": "n8n-nodes-base.httpRequest",
      "retryOnFail": true,
      "maxTries": 3,
      "waitBetweenTries": 30000
    },
    {
      "name": "错误处理",
      "type": "n8n-nodes-base.errorTrigger",
      "webhook": "https://lark.com/notify"
    }
  ]
}
```

## 数据转换技巧

### Function节点高级用法

```javascript
// 数据清洗和转换
const items = $input.all();

const processed = items.map(item => {
  const data = item.json;
  
  // 数据验证
  if (!data.email || !data.email.includes('@')) {
    return null; // 过滤无效数据
  }
  
  // 数据转换
  return {
    email: data.email.toLowerCase().trim(),
    name: data.name?.trim() || 'Unknown',
    created_at: new Date(data.timestamp).toISOString(),
    tags: data.tags?.split(',')?.map(t => t.trim()) || []
  };
}).filter(Boolean); // 移除null

return processed;
```

### 数据合并

```javascript
// 合并多个数据源
const users = $items('GetUsers').json;
const orders = $items('GetOrders').json;

const merged = users.map(user => ({
  ...user,
  orders: orders.filter(o => o.user_id === user.id)
}));

return merged;
```

## 监控和告警

### 工作流健康检查

```
定时触发（每5分钟）
    ↓
检查关键API状态
    ↓
IF 异常
└── 发送飞书告警
```

### 性能监控

使用Webhook节点将执行日志发送到监控系统：

```javascript
// 记录执行时间
const startTime = $run.startTime;
const endTime = new Date().toISOString();
const duration = new Date(endTime) - new Date(startTime);

return [{
  json: {
    workflow: $workflow.name,
    start_time: startTime,
    end_time: endTime,
    duration_ms: duration,
    status: 'success'
  }
}];
```

## 最佳实践总结

1. **模块化设计**：将复杂流程拆分为子工作流
2. **充分测试**：使用执行数据测试每个分支
3. **文档化**：给节点添加描述，记录业务逻辑
4. **版本控制**：导出JSON并提交到Git
5. **权限管理**：生产环境使用只读权限运行

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 工作流不触发 | 触发器配置错误 | 检查Cron表达式或Webhook |
| 数据传递失败 | 字段名不匹配 | 使用Debug节点查看数据结构 |
| API调用超时 | 网络或API问题 | 增加超时时间，添加重试 |
| 内存不足 | 处理大数据集 | 分批处理，使用Split节点 |

## 总结

掌握条件分支和错误处理，是构建生产级n8n工作流的关键。合理的设计可以让你的工作流更加健壮和可维护。"""
    }
]

def get_tutorial_for_date(date=None):
    """根据日期获取当天的教程主题"""
    if date is None:
        date = datetime.now()
    
    # 计算天数（从2026-02-05开始）
    start_date = datetime(2026, 2, 5)
    day_number = (date - start_date).days
    
    # 轮询主题
    index = day_number % len(TUTORIAL_TOPICS)
    return TUTORIAL_TOPICS[index]

def generate_blog_post(date=None):
    """生成博客文章"""
    if date is None:
        date = datetime.now()
    
    tutorial = get_tutorial_for_date(date)
    date_str = date.strftime("%Y-%m-%d")
    time_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成Markdown内容
    lines = []
    lines.append("---")
    lines.append(f'title: "{tutorial["title"]}"')
    lines.append(f"date: {time_str}")
    lines.append('author: "TechAI"')
    lines.append(f'category: "{tutorial["category"]}"')
    lines.append(f'tags: {json.dumps(tutorial["tags"], ensure_ascii=False)}')
    lines.append("readTime: 10")
    lines.append('cover: ""')
    lines.append(f'excerpt: "{tutorial["excerpt"]}"')
    lines.append("featured: false")
    lines.append("---")
    lines.append("")
    lines.append(tutorial["content"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*本文由AI自动生成，每日更新AI技术教程。如有疑问欢迎留言交流！*")
    
    content = "\n".join(lines)
    
    # 生成文件名
    title_slug = tutorial["title"].lower()
    for char in [" ", "：", "—", "/", "？", "vs", "."]:
        title_slug = title_slug.replace(char, "-")
    title_slug = title_slug.replace("--", "-").strip("-")[:50]
    
    filename = f"{date_str}-{title_slug}.md"
    
    return {
        "filename": filename,
        "content": content,
        "title": tutorial["title"]
    }

def save_post(post, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """保存文章到文件"""
    filepath = os.path.join(output_dir, post["filename"])
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post["content"])
    
    return filepath

if __name__ == "__main__":
    # 生成今天的文章
    post = generate_blog_post()
    filepath = save_post(post)
    print(f"✅ 文章已生成: {filepath}")
    print(f"📄 标题: {post['title']}")
