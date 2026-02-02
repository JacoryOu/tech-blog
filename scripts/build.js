/**
 * TechBlog 构建脚本
 * 将 Markdown 文章转换为静态 HTML
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');

// 配置
const CONFIG = {
  postsDir: path.join(__dirname, '../content/posts'),
  pagesDir: path.join(__dirname, '../content/pages'),
  outputDir: path.join(__dirname, '..'),
  postsPerPage: 6
};

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 读取所有文章
function loadPosts() {
  ensureDir(CONFIG.postsDir);
  
  const files = fs.readdirSync(CONFIG.postsDir).filter(f => f.endsWith('.md'));
  
  const posts = files.map(file => {
    const content = fs.readFileSync(path.join(CONFIG.postsDir, file), 'utf8');
    const parsed = matter(content);
    const slug = file.replace('.md', '');
    
    return {
      slug,
      ...parsed.data,
      content: parsed.content,
      html: marked(parsed.content),
      dateObj: new Date(parsed.data.date)
    };
  });
  
  // 按日期倒序排列
  return posts.sort((a, b) => b.dateObj - a.dateObj);
}

// 生成文章 HTML 页面
function generatePostPage(post) {
  const coverHtml = post.cover 
    ? `\n            \u003cdiv class="article-cover"\u003e\n                \u003cimg src="${post.cover}" alt="${post.title}"\u003e\n            \u003c/div\u003e`
    : '';
    
  const tagsHtml = post.tags && post.tags.length 
    ? post.tags.map(tag => `\u003cspan class="tag"\u003e${tag}\u003c/span\u003e`).join('')
    : `\u003cspan class="tag tag-${post.category?.toLowerCase()}"\u003e${post.category}\u003c/span\u003e`;

  return `\u003c!DOCTYPE html\u003e
\u003chtml lang="zh-CN"\u003e
\u003chead\u003e
    \u003cmeta charset="UTF-8"\u003e
    \u003cmeta name="viewport" content="width=device-width, initial-scale=1.0"\u003e
    \u003ctitle\u003e${post.title} - TechBlog\u003c/title\u003e
    \u003cmeta name="description" content="${post.excerpt}"\u003e
    \u003clink rel="stylesheet" href="/css/style.css"\u003e
    \u003clink href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700\u0026family=JetBrains+Mono:wght@400;500\u0026display=swap" rel="stylesheet"\u003e
    \u003clink rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"\u003e
\u003c/head\u003e
\u003cbody\u003e
    \u003c!-- 导航栏 --\u003e
    \u003cnav class="navbar"\u003e
        \u003cdiv class="nav-container"\u003e
            \u003ca href="/index.html" class="nav-logo"\u003e
                \u003cspan class="logo-icon"\u003e\u0026lt;/\u0026gt;\u003c/span\u003e
                \u003cspan class="logo-text"\u003eTechBlog\u003c/span\u003e
            \u003c/a\u003e
            \u003cul class="nav-menu"\u003e
                \u003cli\u003e\u003ca href="/index.html" class="nav-link"\u003e首页\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/posts.html" class="nav-link"\u003e文章\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/about.html" class="nav-link"\u003e关于\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/contact.html" class="nav-link"\u003e联系\u003c/a\u003e\u003c/li\u003e
            \u003c/ul\u003e
            \u003cdiv class="nav-actions"\u003e
                \u003cbutton class="theme-toggle" id="themeToggle"\u003e\u003ci class="fas fa-moon"\u003e\u003c/i\u003e\u003c/button\u003e
                \u003cbutton class="mobile-menu-toggle" id="mobileMenuToggle"\u003e\u003ci class="fas fa-bars"\u003e\u003c/i\u003e\u003c/button\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/nav\u003e

    \u003carticle\u003e
        \u003cheader class="article-header"\u003e
            \u003cdiv class="container"\u003e
                \u003cdiv class="article-meta"\u003e
                    \u003cdiv class="post-tags"\u003e${tagsHtml}\u003c/div\u003e
                    \u003cspan class="read-time"\u003e\u003ci class="far fa-clock"\u003e\u003c/i\u003e ${post.readTime || 5} 分钟阅读\u003c/span\u003e
                \u003c/div\u003e
                \u003ch1 class="article-title"\u003e${post.title}\u003c/h1\u003e
                \u003cdiv class="post-meta" style="justify-content: flex-start; gap: 2rem;"\u003e
                    \u003cdiv class="author"\u003e
                        \u003cimg src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100\u0026h=100\u0026fit=crop" alt="作者" class="author-avatar"\u003e
                        \u003cdiv\u003e
                            \u003cspan class="author-name"\u003e${post.author}\u003c/span\u003e\u003cbr\u003e
                            \u003cspan style="font-size: 0.875rem; color: var(--text-muted);"\u003e前端开发工程师\u003c/span\u003e
                        \u003c/div\u003e
                    \u003c/div\u003e
                    \u003cspan class="post-date"\u003e${post.dateObj.toLocaleDateString('zh-CN')} · 阅读量 ${Math.floor(Math.random() * 2000) + 500}\u003c/span\u003e
                \u003c/div\u003e
            \u003c/div\u003e
        \u003c/header\u003e

        \u003cdiv class="container"\u003e${coverHtml}
        \u003c/div\u003e

        \u003cdiv class="article-content"\u003e
            ${post.html}
        \u003c/div\u003e
    \u003c/article\u003e

    \u003c!-- 分享区域 --\u003e
    \u003csection style="background: var(--bg-secondary); padding: 3rem 0;"\u003e
        \u003cdiv class="container"\u003e
            \u003cdiv style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;"\u003e
                \u003cdiv\u003e
                    \u003ch3\u003e喜欢这篇文章？\u003c/h3\u003e
                    \u003cp style="color: var(--text-secondary);"\u003e分享给更多开发者\u003c/p\u003e
                \u003c/div\u003e
                \u003cdiv style="display: flex; gap: 1rem;"\u003e
                    \u003cbutton class="btn btn-secondary"\u003e\u003ci class="fab fa-twitter"\u003e\u003c/i\u003e\u003cspan\u003eTwitter\u003c/span\u003e\u003c/button\u003e
                    \u003cbutton class="btn btn-secondary"\u003e\u003ci class="fab fa-weixin"\u003e\u003c/i\u003e\u003cspan\u003e微信\u003c/span\u003e\u003c/button\u003e
                \u003c/div\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/section\u003e

    \u003c!-- 相关文章占位 --\u003e
    \u003csection class="featured-section"\u003e
        \u003cdiv class="container"\u003e
            \u003cdiv class="section-header"\u003e
                \u003ch2 class="section-title"\u003e更多文章\u003c/h2\u003e
            \u003c/div\u003e
            \u003cdiv class="section-footer"\u003e
                \u003ca href="/posts.html" class="btn btn-outline"\u003e\u003cspan\u003e查看全部文章\u003c/span\u003e\u003ci class="fas fa-arrow-right"\u003e\u003c/i\u003e\u003c/a\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/section\u003e

    \u003cfooter class="footer"\u003e
        \u003cdiv class="container"\u003e
            \u003cdiv class="footer-bottom"\u003e
                \u003cp\u003e\u0026copy; ${new Date().getFullYear()} TechBlog. All rights reserved.\u003c/p\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/footer\u003e

    \u003cscript src="/js/main.js"\u003e\u003c/script\u003e
\u003c/body\u003e
\u003c/html\u003e`;
}

// 生成文章卡片 HTML
function generatePostCard(post) {
  const cover = post.cover || 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800\u0026h=400\u0026fit=crop';
  const tagsHtml = post.tags && post.tags.length 
    ? post.tags.slice(0, 2).map(tag => `\u003cspan class="tag"\u003e${tag}\u003c/span\u003e`).join('')
    : `\u003cspan class="tag tag-${post.category?.toLowerCase()}"\u003e${post.category}\u003c/span\u003e`;

  return `\u003carticle class="post-card"\u003e
                    \u003cdiv class="post-image"\u003e
                        \u003cimg src="${cover}" alt="${post.title}"\u003e
                        \u003cdiv class="post-overlay"\u003e
                            \u003cspan class="read-time"\u003e\u003ci class="far fa-clock"\u003e\u003c/i\u003e ${post.readTime || 5} 分钟\u003c/span\u003e
                        \u003c/div\u003e
                    \u003c/div\u003e
                    \u003cdiv class="post-content"\u003e
                        \u003cdiv class="post-tags"\u003e${tagsHtml}\u003c/div\u003e
                        \u003ch3 class="post-title"\u003e\u003ca href="/posts/${post.slug}.html"\u003e${post.title}\u003c/a\u003e\u003c/h3\u003e
                        \u003cp class="post-excerpt"\u003e${post.excerpt}\u003c/p\u003e
                        \u003cdiv class="post-meta"\u003e
                            \u003cdiv class="author"\u003e
                                \u003cimg src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100\u0026h=100\u0026fit=crop" alt="作者" class="author-avatar"\u003e
                                \u003cspan class="author-name"\u003e${post.author}\u003c/span\u003e
                            \u003c/div\u003e
                            \u003cspan class="post-date"\u003e${post.dateObj.toLocaleDateString('zh-CN')}\u003c/span\u003e
                        \u003c/div\u003e
                    \u003c/div\u003e
                \u003c/article\u003e`;
}

// 生成首页
function generateIndexPage(posts) {
  const featuredPost = posts.find(p => p.featured) || posts[0];
  const recentPosts = posts.slice(0, 4).filter(p => p !== featuredPost);
  
  const cardsHtml = recentPosts.map(generatePostCard).join('\n\n                ');
  
  // 读取现有 index.html 模板
  const templatePath = path.join(__dirname, '../index.html');
  let template = fs.readFileSync(templatePath, 'utf8');
  
  // 这里简化处理，实际应该使用模板引擎
  // 目前保持静态页面，手动更新文章列表
  console.log('首页文章列表已生成');
  return template;
}

// 生成文章列表页
function generatePostsPage(posts) {
  const postsHtml = posts.map(generatePostCard).join('\n\n                ');
  
  return `\u003c!DOCTYPE html\u003e
\u003chtml lang="zh-CN"\u003e
\u003chead\u003e
    \u003cmeta charset="UTF-8"\u003e
    \u003cmeta name="viewport" content="width=device-width, initial-scale=1.0"\u003e
    \u003ctitle\u003e文章列表 - TechBlog\u003c/title\u003e
    \u003clink rel="stylesheet" href="/css/style.css"\u003e
    \u003clink href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700\u0026family=JetBrains+Mono:wght@400;500\u0026display=swap" rel="stylesheet"\u003e
    \u003clink rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"\u003e
\u003c/head\u003e
\u003cbody\u003e
    \u003cnav class="navbar"\u003e
        \u003cdiv class="nav-container"\u003e
            \u003ca href="/index.html" class="nav-logo"\u003e\u003cspan class="logo-icon"\u003e\u0026lt;/\u0026gt;\u003c/span\u003e\u003cspan class="logo-text"\u003eTechBlog\u003c/span\u003e\u003c/a\u003e
            \u003cul class="nav-menu"\u003e
                \u003cli\u003e\u003ca href="/index.html" class="nav-link"\u003e首页\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/posts.html" class="nav-link active"\u003e文章\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/about.html" class="nav-link"\u003e关于\u003c/a\u003e\u003c/li\u003e
                \u003cli\u003e\u003ca href="/contact.html" class="nav-link"\u003e联系\u003c/a\u003e\u003c/li\u003e
            \u003c/ul\u003e
            \u003cdiv class="nav-actions"\u003e
                \u003cbutton class="theme-toggle" id="themeToggle"\u003e\u003ci class="fas fa-moon"\u003e\u003c/i\u003e\u003c/button\u003e
                \u003cbutton class="mobile-menu-toggle" id="mobileMenuToggle"\u003e\u003ci class="fas fa-bars"\u003e\u003c/i\u003e\u003c/button\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/nav\u003e

    \u003cheader class="page-header"\u003e
        \u003cdiv class="container"\u003e
            \u003ch1 class="page-title"\u003e所有文章\u003c/h1\u003e
            \u003cp class="page-description"\u003e共 ${posts.length} 篇技术文章\u003c/p\u003e
        \u003c/div\u003e
    \u003c/header\u003e

    \u003csection class="featured-section"\u003e
        \u003cdiv class="container"\u003e
            \u003cdiv class="featured-grid"\u003e
                ${postsHtml}
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/section\u003e

    \u003cfooter class="footer"\u003e
        \u003cdiv class="container"\u003e
            \u003cdiv class="footer-bottom"\u003e
                \u003cp\u003e\u0026copy; ${new Date().getFullYear()} TechBlog. All rights reserved.\u003c/p\u003e
            \u003c/div\u003e
        \u003c/div\u003e
    \u003c/footer\u003e

    \u003cscript src="/js/main.js"\u003e\u003c/script\u003e
\u003c/body\u003e
\u003c/html\u003e`;
}

// 主构建函数
function build() {
  console.log('🚀 开始构建...\n');
  
  // 加载文章
  const posts = loadPosts();
  console.log(`📄 找到 ${posts.length} 篇文章`);
  
  if (posts.length === 0) {
    console.log('⚠️ 没有找到文章，创建示例文章...');
    createSamplePost();
    return build();
  }
  
  // 创建输出目录
  ensureDir(path.join(CONFIG.outputDir, 'posts'));
  
  // 生成每篇文章的页面
  posts.forEach(post => {
    const html = generatePostPage(post);
    const outputPath = path.join(CONFIG.outputDir, 'posts', `${post.slug}.html`);
    fs.writeFileSync(outputPath, html);
    console.log(`✅ 生成: posts/${post.slug}.html`);
  });
  
  // 生成文章列表页
  const postsPageHtml = generatePostsPage(posts);
  fs.writeFileSync(path.join(CONFIG.outputDir, 'posts.html'), postsPageHtml);
  console.log('✅ 生成: posts.html');
  
  // 生成首页
  // 这里我们保持原有首页，但可以考虑自动生成
  console.log('✅ 首页保持原样\n');
  
  console.log('🎉 构建完成！');
  console.log(`\n📁 输出目录: ${CONFIG.outputDir}`);
  console.log('\n💡 提示:');
  console.log('   运行 npm run serve 启动本地服务器');
  console.log('   访问 http://localhost:8080 查看网站');
  console.log('   访问 http://localhost:8080/admin 进入管理后台');
}

// 创建示例文章
function createSamplePost() {
  const samplePost = `---
title: "欢迎使用 TechBlog"
date: ${new Date().toISOString()}
author: "张工程师"
category: "前端"
tags: ["博客", "教程"]
readTime: 3
cover: ""
excerpt: "这是一篇示例文章，展示了 TechBlog 的所有功能特性。"
featured: true
---

# 欢迎来到 TechBlog

这是一个基于 **Decap CMS** + **Markdown** 的技术博客系统。

## 特性

- 📝 使用 Markdown 编写文章
- 🎨 精美的响应式设计
- 🌓 支持暗黑/亮色模式
- 🔍 代码高亮显示
- 📱 完美适配移动端

## 开始使用

1. 访问 "/admin" 进入管理后台
2. 点击 "New Post" 创建新文章
3. 填写文章信息并保存
4. 运行 \\\`npm run build\\\` 生成静态页面

## 代码示例

\`\`\`javascript
function hello() {
  console.log('Hello, TechBlog!');
}
\`\`\`

祝你写作愉快！
`;
  
  const slug = `${new Date().toISOString().split('T')[0]}-welcome`;
  fs.writeFileSync(path.join(CONFIG.postsDir, `${slug}.md`), samplePost);
  console.log('✅ 已创建示例文章');
}

// 执行构建
build();
