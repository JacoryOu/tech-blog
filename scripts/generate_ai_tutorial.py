#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客文章自动生成器 - 详细版
每天生成一篇详细的AI教程文章
"""

import os
import json
from datetime import datetime, timedelta

# 详细教程主题库
TUTORIAL_TOPICS = [
    {
        "title": "AI智能体入门：从概念到实践",
        "category": "AI",
        "tags": ["AI Agents", "OpenClaw", "入门", "教程"],
        "excerpt": "深入理解AI智能体的核心概念、工作原理和架构设计，通过完整的天气查询助手案例，学习如何使用Python构建你的第一个AI智能体。",
        "sections": [
            "什么是AI智能体",
            "为什么需要AI智能体", 
            "AI智能体的核心架构",
            "环境准备",
            "实操案例：天气查询助手",
            "进阶功能：记忆系统",
            "总结与展望"
        ]
    },
    {
        "title": "RAG入门：让大模型拥有外部知识",
        "category": "AI",
        "tags": ["RAG", "LLM", "向量数据库", "LangChain"],
        "excerpt": "详解检索增强生成(RAG)技术原理、系统架构和完整实现，通过企业知识库问答案例，学习如何让大语言模型访问和利用外部知识。",
        "sections": [
            "什么是RAG",
            "为什么需要RAG",
            "RAG工作原理",
            "系统架构设计",
            "环境准备",
            "实操案例：企业知识库问答",
            "优化技巧",
            "总结"
        ]
    },
    {
        "title": "n8n入门：零代码构建AI自动化工作流",
        "category": "工具",
        "tags": ["n8n", "自动化", "工作流", "NoCode"],
        "excerpt": "学习使用n8n可视化工作流工具，无需编程即可连接AI API和各类服务，通过RSS+AI摘要自动化案例掌握n8n核心用法。",
        "sections": [
            "什么是n8n",
            "n8n的核心优势",
            "安装部署",
            "基础概念：节点与工作流",
            "实操案例：RSS+AI摘要自动化",
            "进阶技巧：条件分支与错误处理",
            "最佳实践",
            "总结"
        ]
    },
    {
        "title": "智能体记忆管理：从短期到长期",
        "category": "AI",
        "tags": ["AI Agents", "Memory", "架构设计"],
        "excerpt": "探索AI智能体的记忆机制，学习如何实现短期上下文记忆和长期知识存储，构建具备持续学习能力的智能体。",
        "sections": [
            "为什么需要记忆",
            "记忆类型：短期vs长期",
            "短期记忆实现",
            "长期记忆：数据库存储",
            "记忆压缩策略",
            "实操案例：个人助理记忆系统",
            "隐私保护",
            "总结"
        ]
    },
    {
        "title": "向量数据库选型与实战",
        "category": "AI",
        "tags": ["RAG", "向量数据库", "选型指南"],
        "excerpt": "对比Chroma、Pinecone、Milvus等主流向量数据库，通过实际案例学习如何选择和优化向量存储方案。",
        "sections": [
            "什么是向量数据库",
            "主流方案对比",
            "Chroma快速入门",
            "Pinecone云服务",
            "Milvus企业级部署",
            "选型建议",
            "性能优化",
            "总结"
        ]
    },
    {
        "title": "n8n进阶：复杂工作流设计",
        "category": "工具",
        "tags": ["n8n", "工作流", "进阶"],
        "excerpt": "掌握n8n高级功能，学习条件分支设计、错误处理、数据转换和监控告警，构建生产级自动化工作流。",
        "sections": [
            "条件分支设计",
            "错误处理机制",
            "数据转换技巧",
            "循环与批处理",
            "工作流监控",
            "实操案例：内容审核系统",
            "性能优化",
            "总结"
        ]
    }
]

def get_tutorial_for_date(date=None):
    """根据日期获取当天的教程主题"""
    if date is None:
        date = datetime.now()
    
    start_date = datetime(2026, 2, 5)
    day_number = (date - start_date).days
    index = day_number % len(TUTORIAL_TOPICS)
    return TUTORIAL_TOPICS[index]

def get_next_tutorial(date=None):
    """获取明天的教程主题（用于预告）"""
    if date is None:
        date = datetime.now()
    next_date = date + timedelta(days=1)
    return get_tutorial_for_date(next_date)

def generate_detailed_content(topic):
    """生成详细的教程内容"""
    sections_text = []
    
    for i, section in enumerate(topic["sections"], 1):
        sections_text.append(f"### {i}. {section}")
        sections_text.append("")
        sections_text.append(f"【{section}的详细内容将在发布时生成】")
        sections_text.append("")
    
    return "\n".join(sections_text)

def generate_blog_post(date=None):
    """生成博客文章"""
    if date is None:
        date = datetime.now()
    
    tutorial = get_tutorial_for_date(date)
    next_tutorial = get_next_tutorial(date)
    
    date_str = date.strftime("%Y-%m-%d")
    time_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成详细内容
    detailed_content = generate_detailed_content(tutorial)
    
    lines = [
        "---",
        f'title: "{tutorial["title"]}"',
        f"date: {time_str}",
        'author: "小欧Jacory"',
        f'category: "{tutorial["category"]}"',
        f'tags: {json.dumps(tutorial["tags"], ensure_ascii=False)}',
        "readTime: 20",
        'cover: ""',
        f'excerpt: "{tutorial["excerpt"]}"',
        "featured: false",
        "---",
        "",
        "## 目录",
        ""
    ]
    
    # 添加目录链接
    for section in tutorial["sections"]:
        anchor = section.lower().replace(" ", "-").replace("：", "").replace("|", "")
        lines.append(f"- [{section}](#{anchor})")
    
    lines.extend([
        "",
        "## 正文",
        "",
        detailed_content,
        "",
        "## 总结",
        "",
        f"本篇文章详细介绍了**{tutorial['title']}**的核心概念和实践方法。",
        "",
        "### 重点回顾",
        ""
    ])
    
    # 添加要点回顾
    for section in tutorial["sections"][:4]:
        lines.append(f"- {section}")
    
    lines.extend([
        "",
        "---",
        "",
        "*本文由AI自动生成，每日更新AI技术教程。如有疑问欢迎留言交流！*"
    ])
    
    content = "\n".join(lines)
    
    # 生成文件名
    title_slug = tutorial["title"].lower().replace(" ", "-").replace(":", "-").replace("|", "-")[:50]
    filename = f"{date_str}-{title_slug}.md"
    
    return {
        "filename": filename,
        "content": content,
        "title": tutorial["title"],
        "excerpt": tutorial["excerpt"],
        "sections": tutorial["sections"],
        "next_title": next_tutorial["title"]
    }

def save_post(post, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """保存文章到文件"""
    filepath = os.path.join(output_dir, post["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post["content"])
    return filepath

if __name__ == "__main__":
    post = generate_blog_post()
    filepath = save_post(post)
    print(f"文章已生成: {filepath}")
    print(f"标题: {post['title']}")
    print(f"明天预告: {post['next_title']}")
