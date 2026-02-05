#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客文章自动生成器 - 详细版
"""

import os
import json
from datetime import datetime

TUTORIAL_TOPICS = [
    {
        "title": "AI智能体入门：从概念到实践",
        "category": "AI",
        "tags": ["AI Agents", "OpenClaw", "入门", "教程"],
        "excerpt": "深入理解AI智能体的核心概念、工作原理和架构设计，通过完整的天气查询助手案例，学习如何使用Python构建你的第一个AI智能体。",
        "outline": [
            "什么是AI智能体",
            "核心架构设计", 
            "环境准备",
            "实操案例",
            "进阶功能",
            "部署运行"
        ]
    },
    {
        "title": "RAG入门：让大模型拥有外部知识",
        "category": "AI", 
        "tags": ["RAG", "LLM", "向量数据库", "LangChain"],
        "excerpt": "详解检索增强生成(RAG)技术原理、系统架构和完整实现，通过企业知识库问答案例，学习如何让大语言模型访问和利用外部知识。",
        "outline": [
            "什么是RAG",
            "为什么需要RAG",
            "RAG工作原理",
            "系统架构设计",
            "实操案例",
            "优化技巧"
        ]
    }
]

def get_tutorial_for_date(date=None):
    if date is None:
        date = datetime.now()
    start_date = datetime(2026, 2, 5)
    day_number = (date - start_date).days
    index = day_number % len(TUTORIAL_TOPICS)
    return TUTORIAL_TOPICS[index]

def generate_detailed_content(topic):
    # 这里会生成详细的内容
    return "详细教程内容"

def generate_blog_post(date=None):
    if date is None:
        date = datetime.now()
    tutorial = get_tutorial_for_date(date)
    date_str = date.strftime("%Y-%m-%d")
    time_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    content = generate_detailed_content(tutorial)
    
    lines = [
        "---",
        f'title: "{tutorial["title"]}"',
        f"date: {time_str}",
        'author: "小欧Jacory"',
        f'category: "{tutorial["category"]}"',
        f'tags: {json.dumps(tutorial["tags"], ensure_ascii=False)}',
        "readTime: 15",
        'cover: ""',
        f'excerpt: "{tutorial["excerpt"]}"',
        "featured: false",
        "---",
        "",
        f"## 本篇文章大纲",
        ""
    ]
    
    for item in tutorial["outline"]:
        lines.append(f"- {item}")
    
    lines.extend([
        "",
        "## 正文",
        "",
        "详细教程内容将在后续版本中添加...",
        "",
        "---",
        "",
        "*本文由AI自动生成，每日更新AI技术教程。*"
    ])
    
    full_content = "\n".join(lines)
    
    title_slug = tutorial["title"].lower().replace(" ", "-").replace(":", "-").replace("-", "-")[:50]
    filename = f"{date_str}-{title_slug}.md"
    
    return {
        "filename": filename,
        "content": full_content,
        "title": tutorial["title"]
    }

def save_post(post, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    filepath = os.path.join(output_dir, post["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post["content"])
    return filepath

if __name__ == "__main__":
    post = generate_blog_post()
    filepath = save_post(post)
    print(f"文章已生成: {filepath}")
    print(f"标题: {post['title']}")
