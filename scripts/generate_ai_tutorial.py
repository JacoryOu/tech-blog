#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客文章自动生成器 - 系列化版本
按学习路径组织，避免重复，循序渐进
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

# 学习路径设计 - 90个主题，支撑3个月日更
# 每个系列内部从入门→进阶→实战→专家
# 主题用完后可基于已有内容生成进阶变体
LEARNING_PATH = [
    # ==================== 第1系列：AI智能体基础（12篇） ====================
    {
        "title": "AI智能体入门：从概念到第一个智能体",
        "category": "AI智能体",
        "tags": ["AI Agents", "入门", "教程"],
        "excerpt": "深入理解AI智能体的核心概念、工作原理和架构设计，通过完整的天气查询助手案例，学习如何构建你的第一个AI智能体。",
        "series": "AI智能体系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "智能体工具链设计：让AI拥有超能力",
        "category": "AI智能体",
        "tags": ["AI Agents", "Tools", "Function Calling"],
        "excerpt": "学习如何为AI智能体设计工具接口，让AI能够调用搜索引擎、数据库、API等外部服务，大幅扩展能力边界。",
        "series": "AI智能体系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "智能体记忆系统：短期记忆与长期知识",
        "category": "AI智能体",
        "tags": ["AI Agents", "Memory", "架构设计"],
        "excerpt": "探索AI智能体的记忆机制，实现短期上下文记忆和长期知识存储，构建具备持续学习能力的智能体。",
        "series": "AI智能体系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "多智能体协作系统设计与实现",
        "category": "AI智能体",
        "tags": ["AI Agents", "Multi-Agent", "协作"],
        "excerpt": "学习如何设计多个AI智能体协作的复杂系统，实现任务分解、角色分工和结果整合。",
        "series": "AI智能体系列",
        "series_order": 4,
        "level": "实战"
    },
    {
        "title": "智能体规划与推理：ReAct与CoT技术",
        "category": "AI智能体",
        "tags": ["AI Agents", "ReAct", "Chain-of-Thought"],
        "excerpt": "深入理解AI智能体的推理机制，学习ReAct、Chain-of-Thought等规划技术，让AI能够进行复杂任务分解和多步推理。",
        "series": "AI智能体系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "智能体安全与对齐：防止AI失控",
        "category": "AI智能体",
        "tags": ["AI Agents", "Safety", "Alignment"],
        "excerpt": "探讨AI智能体的安全问题，学习如何设计安全边界、防止提示注入、确保AI行为符合人类价值观。",
        "series": "AI智能体系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "AutoGPT与自主智能体：从概念到陷阱",
        "category": "AI智能体",
        "tags": ["AI Agents", "AutoGPT", "自主智能体"],
        "excerpt": "分析AutoGPT等自主智能体的技术原理、实际能力和当前局限，了解何时应该使用、何时应该避免。",
        "series": "AI智能体系列",
        "series_order": 7,
        "level": "实战"
    },
    {
        "title": "智能体评估与测试：如何衡量AI表现",
        "category": "AI智能体",
        "tags": ["AI Agents", "Evaluation", "Testing"],
        "excerpt": "学习如何系统性地评估AI智能体的性能，设计测试用例、建立评估指标、进行A/B对比实验。",
        "series": "AI智能体系列",
        "series_order": 8,
        "level": "进阶"
    },
    {
        "title": "构建个人AI助手：从0到1完整项目",
        "category": "AI智能体",
        "tags": ["AI Agents", "项目实战", "个人助手"],
        "excerpt": "完整项目实战：构建一个具备记忆、工具调用、任务规划能力的个人AI助手，包含代码实现和部署指南。",
        "series": "AI智能体系列",
        "series_order": 9,
        "level": "实战"
    },
    {
        "title": "智能体与人类的协作模式",
        "category": "AI智能体",
        "tags": ["AI Agents", "Human-AI", "协作"],
        "excerpt": "探讨AI智能体与人类的最佳协作方式，包括人机回环、监督机制、权限设计等实践方案。",
        "series": "AI智能体系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "智能体在客服场景的深度应用",
        "category": "AI智能体",
        "tags": ["AI Agents", "客服", "行业应用"],
        "excerpt": "深入分析AI智能体在客服领域的应用，包括意图识别、多轮对话、情绪处理、工单流转等完整方案。",
        "series": "AI智能体系列",
        "series_order": 11,
        "level": "实战"
    },
    {
        "title": "智能体架构设计模式总结",
        "category": "AI智能体",
        "tags": ["AI Agents", "架构", "设计模式"],
        "excerpt": "总结智能体系统的常见架构模式，包括分层架构、事件驱动、微服务化等，提供选型指南。",
        "series": "AI智能体系列",
        "series_order": 12,
        "level": "专家"
    },

    # ==================== 第2系列：RAG与知识增强（12篇） ====================
    {
        "title": "RAG技术详解：让大模型拥有外部知识",
        "category": "RAG",
        "tags": ["RAG", "LLM", "知识增强"],
        "excerpt": "详解检索增强生成(RAG)技术原理、系统架构和完整实现，让大语言模型能够访问和利用外部知识库。",
        "series": "RAG系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "文档处理与文本分块策略",
        "category": "RAG",
        "tags": ["RAG", "文本处理", "分块策略"],
        "excerpt": "学习如何处理PDF、Word、网页等多种文档格式，掌握递归分割、语义分块等文本分块技术。",
        "series": "RAG系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "向量数据库选型与性能优化",
        "category": "RAG",
        "tags": ["RAG", "向量数据库", "性能优化"],
        "excerpt": "对比Chroma、Pinecone、Milvus等主流向量数据库，学习如何选择和优化向量存储方案。",
        "series": "RAG系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "企业级RAG系统实战：从零搭建知识库问答",
        "category": "RAG",
        "tags": ["RAG", "企业应用", "实战"],
        "excerpt": "完整实战案例：为企业搭建基于RAG的内部知识库问答系统，包含权限管理、多租户和审计日志。",
        "series": "RAG系列",
        "series_order": 4,
        "level": "实战"
    },
    {
        "title": "RAG检索优化：混合搜索与重排序",
        "category": "RAG",
        "tags": ["RAG", "检索优化", "重排序"],
        "excerpt": "深入RAG检索环节，学习混合搜索（关键词+向量）、重排序模型、查询扩展等优化技术。",
        "series": "RAG系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "RAG中的幻觉问题与解决方案",
        "category": "RAG",
        "tags": ["RAG", "幻觉", "解决方案"],
        "excerpt": "分析RAG系统中产生幻觉的原因，学习引用溯源、置信度评估、多模型验证等解决方案。",
        "series": "RAG系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "GraphRAG：基于知识图谱的增强检索",
        "category": "RAG",
        "tags": ["RAG", "GraphRAG", "知识图谱"],
        "excerpt": "学习GraphRAG技术，将知识图谱与向量检索结合，实现更精准的多跳推理和关系查询。",
        "series": "RAG系列",
        "series_order": 7,
        "level": "实战"
    },
    {
        "title": "多模态RAG：处理图片、音频、视频",
        "category": "RAG",
        "tags": ["RAG", "多模态", "CLIP"],
        "excerpt": "扩展RAG到多模态场景，学习如何处理和检索图片、音频、视频等非文本内容。",
        "series": "RAG系列",
        "series_order": 8,
        "level": "进阶"
    },
    {
        "title": "RAG系统评估与指标设计",
        "category": "RAG",
        "tags": ["RAG", "评估", "指标"],
        "excerpt": "建立RAG系统的评估体系，包括召回率、精确率、回答相关性等关键指标的定义和测量。",
        "series": "RAG系列",
        "series_order": 9,
        "level": "进阶"
    },
    {
        "title": "RAG与Fine-tuning的选择与结合",
        "category": "RAG",
        "tags": ["RAG", "Fine-tuning", "模型优化"],
        "excerpt": "对比RAG和模型微调的优缺点，学习如何根据场景选择方案，以及两者的结合策略。",
        "series": "RAG系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "RAG在垂直领域的应用：法律、医疗、金融",
        "category": "RAG",
        "tags": ["RAG", "垂直应用", "行业解决方案"],
        "excerpt": "分析RAG在法律、医疗、金融等垂直领域的特殊要求和最佳实践，包括领域知识整合和合规性。",
        "series": "RAG系列",
        "series_order": 11,
        "level": "实战"
    },
    {
        "title": "高级RAG架构：Agentic RAG与Self-RAG",
        "category": "RAG",
        "tags": ["RAG", "Agentic RAG", "Self-RAG"],
        "excerpt": "探索下一代RAG架构，学习Agentic RAG的主动检索和Self-RAG的自我反思机制。",
        "series": "RAG系列",
        "series_order": 12,
        "level": "专家"
    },

    # ==================== 第3系列：自动化与工具链（12篇） ====================
    {
        "title": "n8n入门：零代码构建自动化工作流",
        "category": "自动化",
        "tags": ["n8n", "自动化", "NoCode"],
        "excerpt": "学习使用n8n可视化工作流工具，无需编程即可连接AI API和各类服务，实现RSS+AI摘要等自动化场景。",
        "series": "自动化工具系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "n8n进阶：条件分支与错误处理",
        "category": "自动化",
        "tags": ["n8n", "工作流", "进阶"],
        "excerpt": "掌握n8n高级功能，学习条件分支设计、错误处理、数据转换和监控告警，构建生产级自动化工作流。",
        "series": "自动化工具系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "AI工作流编排：从n8n到LangChain",
        "category": "自动化",
        "tags": ["n8n", "LangChain", "工作流"],
        "excerpt": "对比n8n和LangChain两种工作流方案，学习如何根据场景选择合适的技术栈。",
        "series": "自动化工具系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "自动化内容生产系统实战",
        "category": "自动化",
        "tags": ["自动化", "内容生产", "实战"],
        "excerpt": "完整案例：搭建自动化的内容生产流水线，从选题、写作、配图到发布的一站式解决方案。",
        "series": "自动化工具系列",
        "series_order": 4,
        "level": "实战"
    },
    {
        "title": "Zapier与Make平台深度对比",
        "category": "自动化",
        "tags": ["Zapier", "Make", "自动化平台"],
        "excerpt": "全面对比Zapier、Make等主流自动化平台的功能、定价和适用场景，帮助你做出正确选择。",
        "series": "自动化工具系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "GitHub Actions工作流自动化",
        "category": "自动化",
        "tags": ["GitHub Actions", "CI/CD", "DevOps"],
        "excerpt": "学习使用GitHub Actions实现代码自动化，包括持续集成、自动部署、定时任务等场景。",
        "series": "自动化工具系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "浏览器自动化：Puppeteer与Playwright",
        "category": "自动化",
        "tags": ["自动化", "Puppeteer", "Playwright"],
        "excerpt": "掌握浏览器自动化技术，学习如何使用Puppeteer和Playwright进行网页抓取、测试和自动化操作。",
        "series": "自动化工具系列",
        "series_order": 7,
        "level": "实战"
    },
    {
        "title": "API编排与集成最佳实践",
        "category": "自动化",
        "tags": ["API", "集成", "编排"],
        "excerpt": "学习如何高效集成多个API服务，处理认证、限流、错误重试等常见问题，构建稳定的API工作流。",
        "series": "自动化工具系列",
        "series_order": 8,
        "level": "进阶"
    },
    {
        "title": "数据同步与ETL流程自动化",
        "category": "自动化",
        "tags": ["ETL", "数据同步", "数据处理"],
        "excerpt": "构建自动化的数据同步和ETL流程，学习数据清洗、转换、加载的最佳实践和工具选择。",
        "series": "自动化工具系列",
        "series_order": 9,
        "level": "实战"
    },
    {
        "title": "消息队列与异步任务处理",
        "category": "自动化",
        "tags": ["消息队列", "异步任务", "Redis"],
        "excerpt": "学习使用消息队列（Redis/RabbitMQ）处理异步任务，构建高可靠的自动化系统。",
        "series": "自动化工具系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "自动化测试与监控告警",
        "category": "自动化",
        "tags": ["自动化测试", "监控", "告警"],
        "excerpt": "为自动化工作流添加测试和监控，学习如何检测故障、发送告警、确保系统稳定运行。",
        "series": "自动化工具系列",
        "series_order": 11,
        "level": "实战"
    },
    {
        "title": "构建个人自动化中台",
        "category": "自动化",
        "tags": ["自动化", "个人中台", "效率工具"],
        "excerpt": "整合各种自动化工具，构建个人专属的自动化中台，实现信息、任务、内容的统一管理。",
        "series": "自动化工具系列",
        "series_order": 12,
        "level": "实战"
    },

    # ==================== 第4系列：生产部署与运维（12篇） ====================
    {
        "title": "AI应用容器化部署：Docker与K8s入门",
        "category": "部署",
        "tags": ["Docker", "Kubernetes", "部署"],
        "excerpt": "学习如何将AI应用容器化部署，掌握Docker基础、镜像构建和K8s集群管理。",
        "series": "生产部署系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "大模型API性能优化与成本控制",
        "category": "部署",
        "tags": ["LLM", "性能优化", "成本控制"],
        "excerpt": "学习大模型API的调用优化技巧，包括缓存策略、批处理、模型降级等成本优化方案。",
        "series": "生产部署系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "AI应用监控与可观测性",
        "category": "部署",
        "tags": ["监控", "可观测性", "生产环境"],
        "excerpt": "搭建AI应用的监控体系，学习如何追踪调用链、监控成本和异常告警。",
        "series": "生产部署系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "从0到1：AI产品上线完整指南",
        "category": "部署",
        "tags": ["产品上线", "全栈开发", "实战"],
        "excerpt": "综合实战：从需求分析、架构设计、开发测试到上线运维的完整AI产品开发指南。",
        "series": "生产部署系列",
        "series_order": 4,
        "level": "实战"
    },
    {
        "title": "Serverless部署：Cloudflare Workers与Vercel",
        "category": "部署",
        "tags": ["Serverless", "Cloudflare", "Vercel"],
        "excerpt": "学习使用Serverless平台部署AI应用，享受自动扩缩容、按需付费的便利。",
        "series": "生产部署系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "AI模型私有化部署指南",
        "category": "部署",
        "tags": ["私有化", "本地部署", "模型推理"],
        "excerpt": "学习如何在本地或私有云部署开源大模型，包括硬件选型、模型量化和推理优化。",
        "series": "生产部署系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "负载均衡与高可用架构设计",
        "category": "部署",
        "tags": ["负载均衡", "高可用", "架构设计"],
        "excerpt": "设计高可用的AI服务架构，学习负载均衡、故障转移、限流降级等技术。",
        "series": "生产部署系列",
        "series_order": 7,
        "level": "进阶"
    },
    {
        "title": "CI/CD流水线设计与实践",
        "category": "部署",
        "tags": ["CI/CD", "DevOps", "自动化部署"],
        "excerpt": "构建完整的CI/CD流水线，实现代码提交到生产部署的全自动化。",
        "series": "生产部署系列",
        "series_order": 8,
        "level": "实战"
    },
    {
        "title": "数据库选型与AI应用存储方案",
        "category": "部署",
        "tags": ["数据库", "存储", "方案选型"],
        "excerpt": "对比关系型、文档型、图数据库，为AI应用选择合适的存储方案。",
        "series": "生产部署系列",
        "series_order": 9,
        "level": "进阶"
    },
    {
        "title": "安全防护：AI应用的常见攻击与防御",
        "category": "部署",
        "tags": ["安全", "防御", "攻击防护"],
        "excerpt": "了解AI应用面临的提示注入、数据投毒等攻击手段，学习相应的防御策略。",
        "series": "生产部署系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "日志管理与故障排查",
        "category": "部署",
        "tags": ["日志", "故障排查", "运维"],
        "excerpt": "建立完善的日志管理体系，学习如何快速定位和解决生产环境问题。",
        "series": "生产部署系列",
        "series_order": 11,
        "level": "实战"
    },
    {
        "title": "AI产品规模化部署架构",
        "category": "部署",
        "tags": ["规模化", "架构", "高性能"],
        "excerpt": "设计支撑百万用户的AI产品架构，包括微服务拆分、数据分片、全球部署等。",
        "series": "生产部署系列",
        "series_order": 12,
        "level": "专家"
    },

    # ==================== 第5系列：提示工程与LLM基础（12篇） ====================
    {
        "title": "提示工程入门：写好Prompt的基本原则",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "提示工程", "入门"],
        "excerpt": "学习提示工程的基础知识，掌握清晰、具体、结构化的Prompt编写原则，让AI输出更符合预期。",
        "series": "提示工程系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "Few-shot与Zero-shot提示技巧",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "Few-shot", "Zero-shot"],
        "excerpt": "深入理解Few-shot和Zero-shot学习，学习如何通过示例引导AI完成新任务。",
        "series": "提示工程系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "Chain-of-Thought：让AI一步步思考",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "CoT", "思维链"],
        "excerpt": "学习Chain-of-Thought提示技术，让AI展示推理过程，提升复杂任务的解决能力。",
        "series": "提示工程系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "结构化输出：JSON、XML与Schema约束",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "结构化输出", "JSON"],
        "excerpt": "学习如何让AI生成结构化的输出，使用JSON Schema约束输出格式，便于程序处理。",
        "series": "提示工程系列",
        "series_order": 4,
        "level": "进阶"
    },
    {
        "title": "提示模板与变量管理",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "模板", "变量"],
        "excerpt": "构建可复用的提示模板系统，学习变量替换、条件渲染和模板管理最佳实践。",
        "series": "提示工程系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "角色扮演与系统提示设计",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "角色扮演", "系统提示"],
        "excerpt": "学习如何设计系统提示和角色定义，让AI以特定身份和风格进行回应。",
        "series": "提示工程系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "提示优化与迭代策略",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "优化", "迭代"],
        "excerpt": "建立提示优化流程，学习A/B测试、版本管理和持续改进的方法论。",
        "series": "提示工程系列",
        "series_order": 7,
        "level": "进阶"
    },
    {
        "title": "多语言提示与跨文化适配",
        "category": "提示工程",
        "tags": ["Prompt Engineering", "多语言", "跨文化"],
        "excerpt": "处理多语言场景的提示设计，学习跨文化适配和语言特性处理技巧。",
        "series": "提示工程系列",
        "series_order": 8,
        "level": "进阶"
    },
    {
        "title": "LLM选型：GPT、Claude、Gemini对比",
        "category": "LLM基础",
        "tags": ["LLM", "选型", "对比"],
        "excerpt": "全面比较主流大语言模型的能力、价格和适用场景，提供选型决策框架。",
        "series": "LLM基础系列",
        "series_order": 9,
        "level": "入门"
    },
    {
        "title": "模型微调基础：从预训练到SFT",
        "category": "LLM基础",
        "tags": ["LLM", "微调", "Fine-tuning"],
        "excerpt": "了解大模型微调的基本概念，学习数据准备、训练流程和效果评估。",
        "series": "LLM基础系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "大模型量化与推理加速",
        "category": "LLM基础",
        "tags": ["LLM", "量化", "推理优化"],
        "excerpt": "学习大模型量化技术（INT8/INT4），降低显存占用并提升推理速度。",
        "series": "LLM基础系列",
        "series_order": 11,
        "level": "进阶"
    },
    {
        "title": "开源大模型生态：Llama、Qwen、ChatGLM",
        "category": "LLM基础",
        "tags": ["LLM", "开源模型", "生态"],
        "excerpt": "深入了解开源大模型生态，对比Llama、Qwen、ChatGLM等主流模型的特点和应用。",
        "series": "LLM基础系列",
        "series_order": 12,
        "level": "进阶"
    },

    # ==================== 第6系列：AI应用与行业实践（12篇） ====================
    {
        "title": "AI写作助手：从选题到成稿",
        "category": "AI应用",
        "tags": ["AI写作", "内容创作", "应用"],
        "excerpt": "构建完整的AI写作工作流，学习选题分析、大纲生成、内容撰写和润色优化的全流程。",
        "series": "AI应用系列",
        "series_order": 1,
        "level": "实战"
    },
    {
        "title": "AI辅助编程：Copilot与Codeium深度使用",
        "category": "AI应用",
        "tags": ["AI编程", "Copilot", "开发工具"],
        "excerpt": "深度使用AI编程助手，学习提示技巧、代码审查、测试生成等高级功能。",
        "series": "AI应用系列",
        "series_order": 2,
        "level": "实战"
    },
    {
        "title": "AI数据分析：从Excel到智能洞察",
        "category": "AI应用",
        "tags": ["AI数据分析", "Excel", "洞察"],
        "excerpt": "使用AI进行数据分析，学习自然语言查询、自动可视化、异常检测等技巧。",
        "series": "AI应用系列",
        "series_order": 3,
        "level": "实战"
    },
    {
        "title": "AI图像生成：Midjourney与Stable Diffusion",
        "category": "AI应用",
        "tags": ["AI图像", "Midjourney", "Stable Diffusion"],
        "excerpt": "掌握AI图像生成技术，学习提示词工程、参数调优和风格控制。",
        "series": "AI应用系列",
        "series_order": 4,
        "level": "实战"
    },
    {
        "title": "AI视频创作：Runway与Pika实战",
        "category": "AI应用",
        "tags": ["AI视频", "Runway", "Pika"],
        "excerpt": "探索AI视频生成和编辑工具，学习文生视频、图生视频和视频风格迁移。",
        "series": "AI应用系列",
        "series_order": 5,
        "level": "实战"
    },
    {
        "title": "AI音频处理：语音合成与克隆",
        "category": "AI应用",
        "tags": ["AI音频", "语音合成", "声音克隆"],
        "excerpt": "学习AI语音合成技术，掌握文本转语音、声音克隆和音频编辑工具。",
        "series": "AI应用系列",
        "series_order": 6,
        "level": "实战"
    },
    {
        "title": "AI在电商领域的应用",
        "category": "行业应用",
        "tags": ["AI电商", "应用案例", "行业"],
        "excerpt": "分析AI在电商场景的应用，包括智能客服、商品推荐、内容生成等实践案例。",
        "series": "行业应用系列",
        "series_order": 7,
        "level": "实战"
    },
    {
        "title": "AI在教育领域的创新应用",
        "category": "行业应用",
        "tags": ["AI教育", "个性化学习", "行业"],
        "excerpt": "探索AI在教育领域的应用，包括个性化学习、智能辅导、自动批改等场景。",
        "series": "行业应用系列",
        "series_order": 8,
        "level": "实战"
    },
    {
        "title": "AI医疗：辅助诊断与健康管理",
        "category": "行业应用",
        "tags": ["AI医疗", "辅助诊断", "行业"],
        "excerpt": "了解AI在医疗健康领域的应用，包括影像分析、病历处理和健康管理。",
        "series": "行业应用系列",
        "series_order": 9,
        "level": "实战"
    },
    {
        "title": "AI金融：风控与投资分析",
        "category": "行业应用",
        "tags": ["AI金融", "风控", "投资分析"],
        "excerpt": "学习AI在金融领域的应用，包括风险评估、智能投顾和市场分析。",
        "series": "行业应用系列",
        "series_order": 10,
        "level": "实战"
    },
    {
        "title": "AI法律：合同审查与案例分析",
        "category": "行业应用",
        "tags": ["AI法律", "合同审查", "行业"],
        "excerpt": "探索AI在法律领域的应用，包括合同审查、案例检索和文书生成。",
        "series": "行业应用系列",
        "series_order": 11,
        "level": "实战"
    },
    {
        "title": "AI产品设计：从需求到原型",
        "category": "AI应用",
        "tags": ["AI产品", "设计", "原型"],
        "excerpt": "学习如何将AI能力融入产品设计，从需求分析到原型验证的完整流程。",
        "series": "AI应用系列",
        "series_order": 12,
        "level": "实战"
    },

    # ==================== 第7系列：前沿技术与趋势（12篇） ====================
    {
        "title": "多模态AI：GPT-4V与视觉理解",
        "category": "前沿技术",
        "tags": ["多模态", "视觉AI", "GPT-4V"],
        "excerpt": "学习多模态AI技术，掌握图像理解、视觉问答和跨模态内容生成。",
        "series": "前沿技术系列",
        "series_order": 1,
        "level": "进阶"
    },
    {
        "title": "AI智能体协议：MCP与A2A",
        "category": "前沿技术",
        "tags": ["MCP", "A2A", "协议"],
        "excerpt": "深入了解MCP和A2A等AI智能体协议，学习标准化智能体交互的技术细节。",
        "series": "前沿技术系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "推理模型：o1与DeepSeek R1技术解析",
        "category": "前沿技术",
        "tags": ["推理模型", "o1", "DeepSeek"],
        "excerpt": "解析推理增强型大模型的技术原理，了解链式思考、自我验证等机制。",
        "series": "前沿技术系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "AI芯片与推理加速：GPU、TPU、NPU",
        "category": "前沿技术",
        "tags": ["AI芯片", "推理加速", "硬件"],
        "excerpt": "了解AI芯片的演进，学习GPU、TPU、NPU等不同硬件的特性和选型。",
        "series": "前沿技术系列",
        "series_order": 4,
        "level": "进阶"
    },
    {
        "title": "联邦学习与隐私计算",
        "category": "前沿技术",
        "tags": ["联邦学习", "隐私计算", "分布式"],
        "excerpt": "学习联邦学习和隐私计算技术，在保护数据隐私的前提下进行AI模型训练。",
        "series": "前沿技术系列",
        "series_order": 5,
        "level": "专家"
    },
    {
        "title": "神经符号AI：结合深度学习与知识推理",
        "category": "前沿技术",
        "tags": ["神经符号", "知识推理", "混合AI"],
        "excerpt": "探索神经符号AI，学习如何将深度学习的感知能力与符号推理结合。",
        "series": "前沿技术系列",
        "series_order": 6,
        "level": "专家"
    },
    {
        "title": "世界模型：AI理解物理世界",
        "category": "前沿技术",
        "tags": ["世界模型", "物理AI", "预测"],
        "excerpt": "了解世界模型技术，学习如何让AI建立对物理世界的理解和预测能力。",
        "series": "前沿技术系列",
        "series_order": 7,
        "level": "专家"
    },
    {
        "title": "AI安全：对齐、越狱与防御",
        "category": "前沿技术",
        "tags": ["AI安全", "对齐", "越狱防御"],
        "excerpt": "深入AI安全领域，学习模型对齐、越狱攻击手段和防御策略。",
        "series": "前沿技术系列",
        "series_order": 8,
        "level": "专家"
    },
    {
        "title": "具身智能：机器人与AI的结合",
        "category": "前沿技术",
        "tags": ["具身智能", "机器人", "物理AI"],
        "excerpt": "探索具身智能前沿，了解AI如何与机器人结合，实现物理世界交互。",
        "series": "前沿技术系列",
        "series_order": 9,
        "level": "专家"
    },
    {
        "title": "AI研究前沿：2025年最值得关注的方向",
        "category": "前沿技术",
        "tags": ["AI研究", "趋势", "2025"],
        "excerpt": "盘点2025年AI领域最值得关注的研究方向和技术趋势，把握未来机遇。",
        "series": "前沿技术系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "AI与量子计算：下一个计算范式",
        "category": "前沿技术",
        "tags": ["量子计算", "AI", "未来技术"],
        "excerpt": "了解量子计算与AI的结合，探索量子机器学习的前沿进展。",
        "series": "前沿技术系列",
        "series_order": 11,
        "level": "专家"
    },
    {
        "title": "AGI展望：通往通用人工智能的道路",
        "category": "前沿技术",
        "tags": ["AGI", "通用人工智能", "未来"],
        "excerpt": "探讨AGI的发展路径、技术挑战和社会影响，思考人工智能的未来。",
        "series": "前沿技术系列",
        "series_order": 12,
        "level": "专家"
    },

    # ==================== 第8系列：AI开发框架与工具（12篇） ====================
    {
        "title": "LangChain入门：构建LLM应用的第一选择",
        "category": "开发框架",
        "tags": ["LangChain", "LLM应用", "框架"],
        "excerpt": "学习LangChain框架的基础用法，掌握链式调用、提示模板和工具集成。",
        "series": "开发框架系列",
        "series_order": 1,
        "level": "入门"
    },
    {
        "title": "LangGraph：构建复杂智能体工作流",
        "category": "开发框架",
        "tags": ["LangGraph", "工作流", "智能体"],
        "excerpt": "使用LangGraph构建复杂的多智能体工作流，学习状态管理和图结构编排。",
        "series": "开发框架系列",
        "series_order": 2,
        "level": "进阶"
    },
    {
        "title": "LlamaIndex：数据驱动的LLM应用",
        "category": "开发框架",
        "tags": ["LlamaIndex", "RAG", "数据集成"],
        "excerpt": "学习LlamaIndex框架，轻松将私有数据接入大模型，构建数据驱动的AI应用。",
        "series": "开发框架系列",
        "series_order": 3,
        "level": "进阶"
    },
    {
        "title": "Haystack：企业级NLP框架",
        "category": "开发框架",
        "tags": ["Haystack", "NLP", "企业级"],
        "excerpt": "了解Haystack企业级NLP框架，学习问答系统、文档检索等生产级应用开发。",
        "series": "开发框架系列",
        "series_order": 4,
        "level": "进阶"
    },
    {
        "title": "AutoGen：微软的多智能体框架",
        "category": "开发框架",
        "tags": ["AutoGen", "多智能体", "微软"],
        "excerpt": "学习微软AutoGen框架，快速构建多智能体对话系统和复杂工作流。",
        "series": "开发框架系列",
        "series_order": 5,
        "level": "进阶"
    },
    {
        "title": "CrewAI：协作式AI智能体",
        "category": "开发框架",
        "tags": ["CrewAI", "协作", "智能体"],
        "excerpt": "使用CrewAI构建角色扮演式的多智能体团队，实现协作任务处理。",
        "series": "开发框架系列",
        "series_order": 6,
        "level": "进阶"
    },
    {
        "title": "Semantic Kernel：微软的AI开发SDK",
        "category": "开发框架",
        "tags": ["Semantic Kernel", "微软", "SDK"],
        "excerpt": "了解微软Semantic Kernel，学习如何使用C#或Python构建企业级AI应用。",
        "series": "开发框架系列",
        "series_order": 7,
        "level": "进阶"
    },
    {
        "title": "OpenAI API深度使用指南",
        "category": "开发框架",
        "tags": ["OpenAI", "API", "开发指南"],
        "excerpt": "深度使用OpenAI API，学习Chat Completions、Embeddings、Fine-tuning等功能。",
        "series": "开发框架系列",
        "series_order": 8,
        "level": "进阶"
    },
    {
        "title": "Hugging Face生态：模型与数据集",
        "category": "开发框架",
        "tags": ["Hugging Face", "Transformers", "开源"],
        "excerpt": "探索Hugging Face生态系统，学习使用Transformers库和分享模型、数据集。",
        "series": "开发框架系列",
        "series_order": 9,
        "level": "进阶"
    },
    {
        "title": "vLLM：高性能大模型推理引擎",
        "category": "开发框架",
        "tags": ["vLLM", "推理优化", "性能"],
        "excerpt": "学习vLLM推理引擎，实现高吞吐量、低延迟的大模型服务部署。",
        "series": "开发框架系列",
        "series_order": 10,
        "level": "进阶"
    },
    {
        "title": "Ollama：本地大模型管理工具",
        "category": "开发框架",
        "tags": ["Ollama", "本地部署", "模型管理"],
        "excerpt": "使用Ollama轻松在本地运行和管理开源大模型，无需复杂配置。",
        "series": "开发框架系列",
        "series_order": 11,
        "level": "入门"
    },
    {
        "title": "AI开发框架选型指南",
        "category": "开发框架",
        "tags": ["框架选型", "对比", "指南"],
        "excerpt": "全面对比主流AI开发框架，根据项目需求选择最合适的技术栈。",
        "series": "开发框架系列",
        "series_order": 12,
        "level": "进阶"
    }
]

def get_existing_posts(output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """获取已存在的文章标题列表"""
    existing_titles = set()
    pattern = re.compile(r'title:\s*"([^"]+)"')
    
    posts_path = Path(output_dir)
    if not posts_path.exists():
        return existing_titles
    
    for md_file in posts_path.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                match = pattern.search(content)
                if match:
                    existing_titles.add(match.group(1))
        except:
            continue
    
    return existing_titles

def get_tutorial_for_date(date=None, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """
    根据日期获取当天的教程主题
    策略：
    1. 按学习路径顺序，跳过已存在的主题
    2. 当所有预定义主题用完时，生成进阶变体主题
    3. 支持无限扩展
    """
    if date is None:
        date = datetime.now()
    
    # 获取已存在的文章标题
    existing_titles = get_existing_posts(output_dir)
    
    # 统计每个系列已发布的数量
    series_count = {}
    for topic in LEARNING_PATH:
        if topic["title"] in existing_titles:
            series = topic.get("series", "默认系列")
            series_count[series] = series_count.get(series, 0) + 1
    
    # 找到第一个未发布的预定义主题
    for topic in LEARNING_PATH:
        if topic["title"] not in existing_titles:
            return topic
    
    # 预定义主题已用完，生成进阶变体
    print("预定义主题已用完，生成进阶变体主题...")
    return generate_advanced_variant(existing_titles, date, series_count)

def generate_advanced_variant(existing_titles, date, series_count):
    """
    当预定义主题用完时，生成进阶变体主题
    基于已有主题生成更深入的内容
    """
    # 找出发布最多的系列，在其基础上生成进阶内容
    if series_count:
        top_series = max(series_count.items(), key=lambda x: x[1])[0]
    else:
        top_series = "AI智能体系列"
    
    # 系列特定的进阶主题模板
    advanced_templates = {
        "AI智能体系列": [
            ("{series}第{order}期：高级{topic}实战案例", "专家", "深入分析{topic}在实际项目中的高级应用"),
            ("{series}第{order}期：{topic}性能优化与调优", "专家", "针对{topic}的性能瓶颈分析和优化方案"),
            ("{series}第{order}期：{topic}架构设计模式", "专家", "总结{topic}领域的架构设计最佳实践"),
        ],
        "RAG系列": [
            ("{series}第{order}期：高级RAG检索策略实战", "专家", "深入探讨RAG的高级检索和重排序技术"),
            ("{series}第{order}期：RAG系统性能调优指南", "专家", "针对大规模RAG系统的性能优化方案"),
            ("{series}第{order}期：RAG在{topic}的深度应用", "实战", "分析RAG在{topic}场景的实践"),
        ],
        "自动化工具系列": [
            ("{series}第{order}期：高级{topic}自动化方案", "专家", "设计复杂的{topic}自动化工作流"),
            ("{series}第{order}期：{topic}自动化最佳实践", "实战", "总结{topic}的自动化实战经验"),
        ],
        "生产部署系列": [
            ("{series}第{order}期：大规模{topic}部署方案", "专家", "设计支撑百万用户的{topic}架构"),
            ("{series}第{order}期：{topic}生产环境问题排查", "实战", "分享{topic}的真实故障案例"),
        ],
        "提示工程系列": [
            ("{series}第{order}期：高级{topic}提示技巧", "专家", "深入探讨{topic}的高级提示工程"),
            ("{series}第{order}期：{topic}提示优化实战", "实战", "通过案例优化{topic}的提示效果"),
        ],
        "LLM基础系列": [
            ("{series}第{order}期：{topic}深度解析", "专家", "深入分析{topic}的技术细节"),
            ("{series}第{order}期：{topic}实战优化", "实战", "针对{topic}的实战优化方案"),
        ],
        "AI应用系列": [
            ("{series}第{order}期：{topic}高级应用", "实战", "探索{topic}的高级应用场景"),
            ("{series}第{order}期：{topic}案例深度分析", "实战", "深度剖析{topic}的真实案例"),
        ],
        "行业应用系列": [
            ("{series}第{order}期：AI在{topic}的深度实践", "实战", "深入分析AI在{topic}行业的应用"),
            ("{series}第{order}期：{topic}行业AI解决方案", "实战", "针对{topic}行业的完整AI解决方案"),
        ],
        "前沿技术系列": [
            ("{series}第{order}期：{topic}最新进展", "专家", "追踪{topic}的最新研究进展"),
            ("{series}第{order}期：{topic}技术深度解析", "专家", "深入分析{topic}的技术原理"),
        ],
        "开发框架系列": [
            ("{series}第{order}期：{topic}高级特性", "进阶", "探索{topic}的高级功能和用法"),
            ("{series}第{order}期：{topic}源码解析", "专家", "深入分析{topic}的源码实现"),
        ]
    }
    
    # 获取模板
    templates = advanced_templates.get(top_series, advanced_templates["AI智能体系列"])
    
    # 根据日期选择模板
    day_index = date.day % len(templates)
    template = templates[day_index]
    
    # 从已有主题中提取关键词
    base_topics = ["智能体", "RAG", "自动化", "部署", "提示工程", "大模型", "AI应用", "行业解决方案"]
    topic_keyword = base_topics[date.day % len(base_topics)]
    
    # 生成变体序号
    variant_order = len(existing_titles) - len(LEARNING_PATH) + 1
    
    title = template[0].format(
        series=top_series.replace("系列", ""),
        order=len(existing_titles) + 1,
        topic=topic_keyword
    )
    
    # 确保标题不重复
    original_title = title
    counter = 1
    while title in existing_titles:
        title = f"{original_title}（{counter}）"
        counter += 1
    
    return {
        "title": title,
        "category": "AI进阶",
        "tags": ["AI", "进阶", "实战"],
        "excerpt": template[2].format(topic=topic_keyword),
        "series": f"{top_series}·进阶",
        "series_order": len(existing_titles) + 1,
        "level": template[1],
        "is_variant": True  # 标记为变体主题
    }

def get_next_tutorial(current_topic=None, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """获取明天的教程主题预告"""
    existing_titles = get_existing_posts(output_dir)
    
    # 找到当前主题之后的下一个未发布主题
    found_current = False
    for topic in LEARNING_PATH:
        if found_current and topic["title"] not in existing_titles:
            return topic
        if current_topic and topic["title"] == current_topic["title"]:
            found_current = True
    
    # 如果没找到，返回第一个未发布的
    for topic in LEARNING_PATH:
        if topic["title"] not in existing_titles:
            return topic
    
    return None

def generate_detailed_content(topic):
    """生成详细的教程内容 - 真实内容"""
    # 这里应该调用AI生成真实内容，暂时保留占位符但标记为待生成
    sections_text = []
    
    for i, section in enumerate(topic.get("sections", []), 1):
        sections_text.append(f"### {i}. {section}")
        sections_text.append("")
        sections_text.append(f"【{section}的详细内容将在发布时生成】")
        sections_text.append("")
    
    # 如果没有预设sections，根据主题生成
    if not topic.get("sections"):
        default_sections = [
            "核心概念介绍",
            "为什么需要这个技术",
            "工作原理详解",
            "环境准备与安装",
            "基础用法示例",
            "进阶技巧分享",
            "常见问题解答",
            "总结与下一步"
        ]
        for i, section in enumerate(default_sections, 1):
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
    
    # 如果所有主题都已发布且无法生成变体，返回None
    if tutorial is None:
        print("所有教程主题已发布完毕，今天不生成新文章")
        return None
    
    # 判断是预定义主题还是变体主题
    is_variant = tutorial.get("is_variant", False)
    
    if is_variant:
        # 变体主题直接返回，不包含next_title
        return generate_variant_post(tutorial, date)
    
    # 预定义主题的正常流程
    next_tutorial = get_next_tutorial(tutorial)
    
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
        f'series: "{tutorial.get("series", "")}"',
        f'seriesOrder: {tutorial.get("series_order", 0)}',
        f'level: "{tutorial.get("level", "入门")}"',
        "featured: false",
        "---",
        "",
        f"> 📚 **{tutorial.get('series', 'AI教程')}** · 第{tutorial.get('series_order', 1)}篇 · {tutorial.get('level', '入门')}级别",
        "",
        "## 目录",
        ""
    ]
    
    # 添加目录链接
    sections = tutorial.get("sections", [
        "核心概念介绍", "为什么需要这个技术", "工作原理详解", 
        "环境准备与安装", "基础用法示例", "进阶技巧分享", "总结与下一步"
    ])
    for section in sections:
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
    for section in sections[:4]:
        lines.append(f"- {section}")
    
    # 系列导航
    lines.extend([
        "",
        "### 系列导航",
        ""
    ])
    
    if tutorial.get("series_order", 1) > 1:
        lines.append(f"⬅️ 上一篇：同系列入门文章")
    lines.append(f"📖 当前：第{tutorial.get('series_order', 1)}篇")
    if next_tutorial:
        lines.append(f"➡️ 下一篇预告：{next_tutorial['title']}")
    else:
        lines.append("✅ 系列完结")
    
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
        "series": tutorial.get("series", ""),
        "series_order": tutorial.get("series_order", 1),
        "level": tutorial.get("level", "入门"),
        "next_title": next_tutorial["title"] if next_tutorial else "系列完结"
    }

def generate_variant_post(tutorial, date):
    """生成变体主题的文章"""
    date_str = date.strftime("%Y-%m-%d")
    time_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # 变体主题生成更详细的内容框架
    sections = [
        "背景与挑战",
        "核心问题分析", 
        "解决方案设计",
        "详细实现步骤",
        "性能优化技巧",
        "常见问题与解决",
        "最佳实践总结",
        "参考资料与延伸阅读"
    ]
    
    detailed_content = []
    for i, section in enumerate(sections, 1):
        detailed_content.append(f"### {i}. {section}")
        detailed_content.append("")
        detailed_content.append(f"【{section}的详细内容将在发布时生成】")
        detailed_content.append("")
    
    lines = [
        "---",
        f'title: "{tutorial["title"]}"',
        f"date: {time_str}",
        'author: "小欧Jacory"',
        f'category: "{tutorial["category"]}"',
        f'tags: {json.dumps(tutorial["tags"], ensure_ascii=False)}',
        "readTime: 25",
        'cover: ""',
        f'excerpt: "{tutorial["excerpt"]}"',
        f'series: "{tutorial.get("series", "")}"',
        f'seriesOrder: {tutorial.get("series_order", 0)}',
        f'level: "{tutorial.get("level", "入门")}"',
        "featured: false",
        "---",
        "",
        f"> 📚 **{tutorial.get('series', 'AI教程')}** · 进阶篇 · {tutorial.get('level', '进阶')}级别",
        "",
        "> 💡 本文是进阶变体内容，基于已有主题的深入探讨",
        "",
        "## 目录",
        ""
    ]
    
    for section in sections:
        anchor = section.lower().replace(" ", "-").replace("：", "").replace("|", "")
        lines.append(f"- [{section}](#{anchor})")
    
    lines.extend([
        "",
        "## 正文",
        "",
        "\n".join(detailed_content),
        "",
        "## 总结",
        "",
        f"本篇文章深入探讨了**{tutorial['title']}**的高级话题和实践方案。",
        "",
        "### 核心收获",
        ""
    ])
    
    for section in sections[:4]:
        lines.append(f"- {section}")
    
    lines.extend([
        "",
        "---",
        "",
        "*本文由AI自动生成，每日更新AI技术教程。如需深入探讨欢迎留言！*"
    ])
    
    content = "\n".join(lines)
    
    title_slug = tutorial["title"].lower().replace(" ", "-").replace(":", "-").replace("|", "-")[:40]
    filename = f"{date_str}-{title_slug}.md"
    
    return {
        "filename": filename,
        "content": content,
        "title": tutorial["title"],
        "excerpt": tutorial["excerpt"],
        "series": tutorial.get("series", ""),
        "series_order": tutorial.get("series_order", 1),
        "level": tutorial.get("level", "进阶"),
        "next_title": "持续更新中..."
    }

def save_post(post, output_dir="/home/jacory/clawd/projects/tech-blog/content/posts"):
    """保存文章到文件"""
    if post is None:
        return None
    
    filepath = os.path.join(output_dir, post["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(post["content"])
    return filepath

if __name__ == "__main__":
    post = generate_blog_post()
    if post:
        filepath = save_post(post)
        print(f"文章已生成: {filepath}")
        print(f"标题: {post['title']}")
        print(f"系列: {post['series']} · 第{post['series_order']}篇")
        print(f"级别: {post['level']}")
        print(f"明天预告: {post['next_title']}")
    else:
        print("今天不生成新文章（所有主题已发布）")
