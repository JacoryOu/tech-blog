/**
 * TechBlog 构建脚本 - GitHub Pages 版本
 * 使用相对路径，支持项目站点部署
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');

// 配置
const CONFIG = {
  postsDir: path.join(__dirname, '../content/posts'),
  outputDir: path.join(__dirname, '..'),
  postsPerPage: 6,
  // 相对路径模式
  useRelativePaths: true
};

// 路径助手
function getBasePath(depth) {
  if (!CONFIG.useRelativePaths) return '';
  return depth === 0 ? './' : '../'.repeat(depth);
}

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
  
  return posts.sort((a, b) => b.dateObj - a.dateObj);
}

// 生成导航栏
function generateNav(depth) {
  const base = getBasePath(depth);
  return `    <nav class="navbar">
        <div class="nav-container">
            <a href="${base}index.html" class="nav-logo">
                <span class="logo-icon">&lt;/&gt;</span>
                <span class="logo-text">TechBlog</span>
            </a>
            <ul class="nav-menu">
                <li><a href="${base}index.html" class="nav-link">首页</a></li>
                <li><a href="${base}posts.html" class="nav-link">文章</a></li>
                <li><a href="${base}about.html" class="nav-link">关于</a></li>
                <li><a href="${base}contact.html" class="nav-link">联系</a></li>
            </ul>
            <div class="nav-actions">
                <button class="theme-toggle" id="themeToggle"><i class="fas fa-moon"></i></button>
                <button class="mobile-menu-toggle" id="mobileMenuToggle"><i class="fas fa-bars"></i></button>
            </div>
        </div>
    </nav>`;
}

// 生成页脚
function generateFooter(depth) {
  const base = getBasePath(depth);
  const year = new Date().getFullYear();
  return `    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="${base}index.html" class="footer-logo">
                        <span class="logo-icon">&lt;/&gt;</span>
                        <span class="logo-text">TechBlog</span>
                    </a>
                    <p class="footer-description">记录技术成长的每一步，分享编程的乐趣与思考。</p>
                    <div class="social-links">
                        <a href="#" class="social-link"><i class="fab fa-github"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-linkedin"></i></a>
                        <a href="#" class="social-link"><i class="fas fa-rss"></i></a>
                    </div>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="${base}index.html">首页</a></li>
                        <li><a href="${base}posts.html">文章</a></li>
                        <li><a href="${base}about.html">关于</a></li>
                        <li><a href="${base}contact.html">联系</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>技术标签</h4>
                    <ul>
                        <li><a href="#">React</a></li>
                        <li><a href="#">TypeScript</a></li>
                        <li><a href="#">Node.js</a></li>
                        <li><a href="#">云原生</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; ${year} TechBlog. All rights reserved.</p>
                <p>Made with <i class="fas fa-heart"></i> and lots of <i class="fas fa-coffee"></i></p>
            </div>
        </div>
    </footer>`;
}

// 默认头像（优先使用本地头像，如果没有则使用网络图片）
const LOCAL_AVATAR = './images/avatar.png';
const FALLBACK_AVATAR = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop';

// 检查本地头像是否存在
function getDefaultAvatar(depth) {
  const basePath = getBasePath(depth);
  const localPath = basePath + 'images/avatar.png';
  // 检查文件是否存在（构建时检查根目录）
  const absolutePath = path.join(CONFIG.outputDir, 'images', 'avatar.png');
  if (fs.existsSync(absolutePath)) {
    return localPath;
  }
  return FALLBACK_AVATAR;
}

// 生成文章 HTML 页面
function generatePostPage(post, allPosts) {
  const coverHtml = post.cover 
    ? `\n        <div class="container">\n            <div class="article-cover">\n                <img src="${post.cover}" alt="${post.title}">\n            </div>\n        </div>`
    : '';
    
  const defaultAvatar = getDefaultAvatar(1);
  const avatarUrl = post.authorAvatar || defaultAvatar;
  
  const tagsHtml = post.tags && post.tags.length 
    ? post.tags.map(tag => `<span class="tag">${tag}</span>`).join('')
    : `<span class="tag tag-${post.category?.toLowerCase()}">${post.category}</span>`;

  // 找相关文章
  const relatedPosts = allPosts
    .filter(p => p.slug !== post.slug && p.category === post.category)
    .slice(0, 2);

  const relatedHtml = relatedPosts.length > 0 
    ? relatedPosts.map(p => `
                <article class="post-card">
                    <div class="post-content">
                        <div class="post-tags">
                            <span class="tag tag-${p.category?.toLowerCase()}">${p.category}</span>
                        </div>
                        <h3 class="post-title">
                            <a href="./${p.slug}.html">${p.title}</a>
                        </h3>
                        <p class="post-excerpt">${p.excerpt}</p>
                    </div>
                </article>`).join('')
    : `
                <div style="text-align: center; padding: 2rem;">
                    <p style="color: var(--text-secondary);">暂无相关文章</p>
                </div>`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${post.title} - TechBlog</title>
    <meta name="description" content="${post.excerpt}">
    <link rel="stylesheet" href="../css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
${generateNav(1)}

    <article>
        <header class="article-header">
            <div class="container">
                <div class="article-meta">
                    <div class="post-tags">${tagsHtml}</div>
                    <span class="read-time"><i class="far fa-clock"></i> ${post.readTime || 5} 分钟阅读</span>
                </div>
                <h1 class="article-title">${post.title}</h1>
                <div class="post-meta" style="justify-content: flex-start; gap: 2rem;">
                    <div class="author">
                        <img src="${avatarUrl}" alt="${post.author}" class="author-avatar">
                        <div>
                            <span class="author-name">${post.author}</span><br>
                            <span style="font-size: 0.875rem; color: var(--text-muted);">前端开发工程师</span>
                        </div>
                    </div>
                    <span class="post-date">${post.dateObj.toLocaleDateString('zh-CN')}</span>
                </div>
            </div>
        </header>

${coverHtml}

        <div class="article-content">
            ${post.html}
        </div>
    </article>

    <section style="background: var(--bg-secondary); padding: 3rem 0;">
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h3>喜欢这篇文章？</h3>
                    <p style="color: var(--text-secondary);">分享给更多开发者</p>
                </div>
                <div style="display: flex; gap: 1rem;">
                    <button class="btn btn-secondary"><i class="fab fa-twitter"></i><span>Twitter</span></button>
                    <button class="btn btn-secondary"><i class="fab fa-weixin"></i><span>微信</span></button>
                </div>
            </div>
        </div>
    </section>

    <section class="featured-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">相关文章</h2>
            </div>
            <div class="featured-grid" style="grid-template-columns: repeat(2, 1fr);">
${relatedHtml}
            </div>
        </div>
    </section>

${generateFooter(1)}

    <script src="../js/main.js"></script>
</body>
</html>`;
}

// 生成文章卡片
function generatePostCard(post, basePath) {
  const cover = post.cover || 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=400&fit=crop';
  const defaultAvatar = getDefaultAvatar(0);
  const avatarUrl = post.authorAvatar || defaultAvatar;
  const tagsHtml = post.tags && post.tags.length 
    ? post.tags.slice(0, 2).map(tag => `<span class="tag">${tag}</span>`).join('')
    : `<span class="tag tag-${post.category?.toLowerCase()}">${post.category}</span>`;

  return `<article class="post-card">
                    <div class="post-image">
                        <img src="${cover}" alt="${post.title}">
                        <div class="post-overlay">
                            <span class="read-time"><i class="far fa-clock"></i> ${post.readTime || 5} 分钟</span>
                        </div>
                    </div>
                    <div class="post-content">
                        <div class="post-tags">${tagsHtml}</div>
                        <h3 class="post-title"><a href="${basePath}posts/${post.slug}.html">${post.title}</a></h3>
                        <p class="post-excerpt">${post.excerpt}</p>
                        <div class="post-meta">
                            <div class="author">
                                <img src="${avatarUrl}" alt="${post.author}" class="author-avatar">
                                <span class="author-name">${post.author}</span>
                            </div>
                            <span class="post-date">${post.dateObj.toLocaleDateString('zh-CN')}</span>
                        </div>
                    </div>
                </article>`;
}

// 生成文章列表页
function generatePostsPage(posts) {
  const postsHtml = posts.map(p => generatePostCard(p, './')).join('\n\n                ');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章列表 - TechBlog</title>
    <link rel="stylesheet" href="./css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
${generateNav(0)}

    <header class="page-header">
        <div class="container">
            <h1 class="page-title">所有文章</h1>
            <p class="page-description">共 ${posts.length} 篇技术文章</p>
        </div>
    </header>

    <section class="featured-section">
        <div class="container">
            <div class="featured-grid">
                ${postsHtml}
            </div>
        </div>
    </section>

${generateFooter(0)}

    <script src="./js/main.js"></script>
</body>
</html>`;
}

// 更新首页文章列表
function updateIndexPage(posts) {
  const indexPath = path.join(CONFIG.outputDir, 'index.html');
  if (!fs.existsSync(indexPath)) {
    console.log('⚠️ index.html 不存在，跳过更新');
    return;
  }

  // 获取精选文章
  const featuredPost = posts.find(p => p.featured) || posts[0];
  const recentPosts = posts.filter(p => p !== featuredPost).slice(0, 3);

  // 读取现有首页
  let html = fs.readFileSync(indexPath, 'utf8');
  
  // 这里简化处理：只输出提示
  console.log(`📝 首页精选文章: ${featuredPost?.title || '无'}`);
  console.log(`📝 最近文章: ${recentPosts.map(p => p.title).join(', ')}`);
  console.log('💡 提示: 首页使用静态模板，如需自动更新请使用模板引擎');
}

// 主构建函数
function build() {
  console.log('🚀 开始构建 (GitHub Pages 版本)...\n');
  
  const posts = loadPosts();
  console.log(`📄 找到 ${posts.length} 篇文章`);
  
  if (posts.length === 0) {
    console.log('⚠️ 没有找到文章');
    return;
  }

  // 创建输出目录
  ensureDir(path.join(CONFIG.outputDir, 'posts'));

  // 生成每篇文章页面
  posts.forEach(post => {
    const html = generatePostPage(post, posts);
    const outputPath = path.join(CONFIG.outputDir, 'posts', `${post.slug}.html`);
    fs.writeFileSync(outputPath, html);
    console.log(`✅ 生成: posts/${post.slug}.html`);
  });

  // 生成文章列表页
  const postsPageHtml = generatePostsPage(posts);
  fs.writeFileSync(path.join(CONFIG.outputDir, 'posts.html'), postsPageHtml);
  console.log('✅ 生成: posts.html');

  // 更新首页
  updateIndexPage(posts);

  console.log('\n🎉 构建完成！');
  console.log('\n📁 输出目录结构:');
  console.log('   index.html          - 首页');
  console.log('   posts.html          - 文章列表');
  console.log('   posts/*.html        - 文章详情页');
  console.log('   css/style.css       - 样式文件');
  console.log('   js/main.js          - 脚本文件');
}

// 执行构建
build();
