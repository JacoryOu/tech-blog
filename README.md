# TechBlog - 技术博客系统

基于 **Decap CMS** + **Markdown** + **Node.js 构建** 的现代化静态博客系统。

## ✨ 特性

| 功能 | 描述 |
|------|------|
| 📝 Markdown 写作 | 使用 Markdown 格式编写文章，支持 YAML Frontmatter |
| 🎨 精美界面 | 现代化响应式设计，支持暗黑/亮色模式 |
| 🔧 后台管理 | 通过 Decap CMS 管理文章，所见即所得 |
| ⚡ 快速构建 | Node.js 脚本自动将 Markdown 转换为静态 HTML |
| 📱 移动优先 | 完美适配手机、平板、桌面设备 |
| 🔍 SEO 友好 | 自动生成元标签、友好的 URL 结构 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd tech-blog
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

这将启动：
- 🌐 网站服务器: http://localhost:8080
- 📝 管理后台: http://localhost:8080/admin
- 👀 文件监视: 自动检测文章变化并重建

### 3. 访问管理后台

1. 打开 http://localhost:8080/admin
2. 使用本地模式（无需登录）
3. 点击 "New Post" 创建新文章
4. 填写文章信息并保存

### 4. 构建网站

```bash
npm run build
```

构建完成后，所有静态文件都在项目根目录，可直接部署。

---

## 📁 项目结构

```
tech-blog/
├── admin/                  # Decap CMS 管理后台
│   ├── config.yml         # CMS 配置
│   └── index.html         # 管理界面入口
├── content/               # 内容目录
│   ├── posts/            # Markdown 文章
│   └── images/           # 文章图片
├── scripts/               # 构建脚本
│   ├── build.js          # 主构建脚本
│   └── dev.js            # 开发服务器
├── css/                   # 样式文件
│   └── style.css
├── js/                    # JavaScript
│   └── main.js
├── posts/                 # 生成的文章页面
├── index.html            # 首页
├── posts.html            # 文章列表页
├── about.html            # 关于页面
├── contact.html          # 联系页面
└── package.json
```

---

## 📝 写作指南

### 文章格式

文章使用 Markdown + YAML Frontmatter：

```markdown
---
title: "文章标题"
date: 2024-01-15 10:00:00
author: "作者名"
category: "前端"
tags: ["React", "教程"]
readTime: 8
cover: "/content/images/cover.jpg"
excerpt: "文章摘要，显示在列表页"
featured: true
---

# 正文标题

正文内容支持 **Markdown** 语法。

## 代码块

```javascript
console.log('Hello World');
```

## 列表

- 项目1
- 项目2
- 项目3
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 文章标题 |
| `date` | ✅ | 发布日期 |
| `author` | ✅ | 作者名称 |
| `category` | ✅ | 分类（React/TypeScript/Node.js/AI/架构/前端/后端/云原生/工具） |
| `tags` | ❌ | 标签数组 |
| `readTime` | ❌ | 预计阅读时间（分钟） |
| `cover` | ❌ | 封面图片路径 |
| `excerpt` | ✅ | 文章摘要 |
| `featured` | ❌ | 是否首页精选 |

---

## 🛠️ 自定义配置

### 修改网站信息

编辑 `admin/config.yml`：

```yaml
site_url: https://your-domain.com
display_url: https://your-domain.com
```

### 修改主题色

编辑 `css/style.css` 中的 CSS 变量：

```css
:root {
  --primary: #6366f1;      /* 主色 */
  --secondary: #06b6d4;    /* 次色 */
  --accent: #f472b6;       /* 强调色 */
}
```

### 添加新页面

1. 在 `content/pages/` 创建 Markdown 文件
2. 运行 `npm run build`

---

## 📦 部署

### 方案 1：静态托管（推荐）

构建完成后，将以下文件上传到任意静态托管：
- Vercel
- Netlify
- GitHub Pages
- Cloudflare Pages
- 阿里云 OSS / 腾讯云 COS

```bash
npm run build
# 上传所有文件到服务器
```

### 方案 2：Node.js 服务器

```bash
npm install
npm run build
npm start
```

### 方案 3：Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 8080
CMD ["npm", "start"]
```

---

## 🔐 生产环境配置

当前使用的是 **本地模式**（`local_backend: true`），适合本地开发。

### 启用 Git 同步（生产环境）

1. 将代码推送到 GitHub
2. 注册 [Netlify Identity](https://docs.netlify.com/visitor-access/identity/)
3. 修改 `admin/config.yml`：

```yaml
backend:
  name: git-gateway
  repo: yourusername/tech-blog
  branch: main

# 删除或注释掉 local_backend
# local_backend: true
```

4. 部署到 Netlify 并启用 Identity 服务

---

## 🐛 常见问题

### 1. 管理后台无法访问

确保通过 HTTP 服务器访问，而不是直接打开文件：
```bash
npm run serve
```

### 2. 文章不显示

检查文章文件格式：
- 必须是 `.md` 扩展名
- 必须包含 YAML Frontmatter（`---` 包裹的头部信息）
- `title` 和 `date` 字段必填

### 3. 图片无法显示

- 图片上传到 `content/images/`
- 在文章中引用：`/content/images/your-image.jpg`

### 4. 构建失败

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📄 许可证

MIT License

---

## 💡 技术支持

遇到问题？检查以下资源：
- [Decap CMS 文档](https://decapcms.org/docs/)
- [Markdown 语法指南](https://www.markdownguide.org/)
- [Marked.js 文档](https://marked.js.org/)

Happy Blogging! 🎉
