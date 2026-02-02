# 🚀 GitHub Pages 部署指南

## 方案选择

### 方案 A：用户站点（推荐）
创建名为 `username.github.io` 的仓库，直接部署到根域名

**优点：**
- URL 简洁：`https://yourname.github.io`
- 绝对路径 `/` 直接可用

### 方案 B：项目站点
在任何仓库开启 GitHub Pages，部署到子路径

**URL 格式：** `https://yourname.github.io/repo-name`

---

## 📋 部署步骤

### 第一步：创建 GitHub 仓库

**对于方案 A（用户站点）：**
1. 在 GitHub 创建名为 `yourusername.github.io` 的仓库
   - 必须完全匹配你的用户名
   - 必须是公开仓库

**对于方案 B（项目站点）：**
1. 创建任意名称的仓库（如 `tech-blog`）

### 第二步：上传代码

```bash
cd /home/jacory/clawd/projects/tech-blog

# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/yourusername.github.io.git
# 或
git remote add origin https://github.com/yourusername/tech-blog.git

# 推送代码
git push -u origin main
```

### 第三步：启用 GitHub Pages

1. 打开仓库的 **Settings** → **Pages**
2. **Source** 选择 "GitHub Actions"
3. 等待 Action 自动运行

### 第四步：访问网站

- 用户站点：`https://yourusername.github.io`
- 项目站点：`https://yourusername.github.io/tech-blog`

---

## ⚙️ 针对项目站点的配置（方案 B）

如果你使用项目站点（子路径部署），需要修改配置文件：

### 1. 修改 admin/config.yml

```yaml
# 添加 base_url 配置
site_url: https://yourusername.github.io/tech-blog
display_url: https://yourusername.github.io/tech-blog

# 修改本地开发配置
local_backend:
  url: http://localhost:8080/api/v1
  allowed_hosts: ['localhost', '127.0.0.1', 'yourusername.github.io']
```

### 2. 修改构建脚本使用相对路径

编辑 `scripts/build.js`，将所有绝对路径改为相对路径：

```javascript
// 原代码
href="/css/style.css"
href="/index.html"
href="/posts.html"

// 修改为（文章页面）
href="../css/style.css"
href="../index.html"
href="../posts.html"

// 首页和列表页保持
href="./css/style.css"
href="./index.html"
```

我已经为你准备了 `scripts/build-github.js`，支持相对路径构建：

```bash
# 构建适合 GitHub Pages 的版本
npm run build:github
```

### 3. 修改 package.json

```bash
npm install
```

---

## 🔐 配置 Decap CMS（可选）

GitHub Pages 是纯静态托管，Decap CMS 需要 OAuth 认证。

### 方案 1：Netlify Identity（推荐，免费）

1. 在 [Netlify](https://netlify.com) 注册账号
2. 连接你的 GitHub 仓库
3. 启用 **Identity** 服务
4. 修改 `admin/config.yml`：

```yaml
backend:
  name: git-gateway
  repo: yourusername/yourusername.github.io
  branch: main
  
# 删除 local_backend 以启用在线模式
# local_backend:
```

### 方案 2：使用 Netlify 托管（更推荐）

Netlify 原生支持 Git 网关，与 Decap CMS 配合最好：

1. 将代码推送到 GitHub
2. 在 Netlify 导入仓库
3. 自动部署 + CMS 就绪

### 方案 3：纯本地写作模式

保持 `local_backend: true`，只在本地写作：

```bash
# 本地写作
npm run dev
# 访问 localhost:8080/admin 写文章

# 推送到 GitHub 自动部署
git add content/posts/
git commit -m "Add new post"
git push
```

---

## 🔄 自动部署流程

```
本地写作 ──▶ 推送代码 ──▶ GitHub Actions ──▶ 构建 ──▶ GitHub Pages
    │              │              │              │            │
    │              │              │              │            ▼
    │              │              │              │     🌐 网站更新
    │              │              │              ▼
    │              │              │     运行 npm run build
    │              │              ▼
    │              │     触发 .github/workflows/deploy.yml
    │              ▼
    │     git push origin main
    ▼
访问 localhost:8080/admin
```

---

## 🐛 常见问题

### 1. 页面样式不加载

**问题：** 路径错误导致 CSS 404

**解决：**
- 用户站点：检查是否为 `username.github.io` 格式
- 项目站点：使用 `npm run build:github` 生成相对路径版本

### 2. 文章页面 404

**问题：** 大小写敏感

**解决：** GitHub Pages 区分大小写，确保文件名全小写

### 3. CMS 无法登录

**问题：** GitHub Pages 不支持 OAuth 后端

**解决：**
- 使用 Netlify 托管
- 或保持本地模式（`local_backend: true`）

### 4. 构建失败

检查 GitHub Actions 日志：

```
仓库 → Actions → Deploy to GitHub Pages
```

常见错误：
- `package-lock.json` 缺失 → 运行 `npm install` 提交
- Node 版本问题 → 检查 `.github/workflows/deploy.yml` 中的版本

---

## 📱 推荐方案总结

| 需求 | 推荐方案 |
|------|----------|
| 完全免费 + 简单 | GitHub Pages + 本地写作 |
| CMS 后台管理 | Netlify（自带 Identity） |
| 自定义域名 | GitHub Pages 或 Netlify 都支持 |
| 国内访问速度 | 腾讯云 COS / 阿里云 OSS |

---

## 🎯 快速检查清单

部署前确认：

- [ ] 仓库名正确（用户站点必须匹配用户名）
- [ ] 仓库是公开的
- [ ] GitHub Actions 已启用
- [ ] `package-lock.json` 已提交
- [ ] 所有文件已推送到 main 分支

部署后检查：

- [ ] 首页能正常访问
- [ ] 文章列表页正常
- [ ] 样式加载正常
- [ ] 暗黑模式切换正常
- [ ] 移动端显示正常

---

有问题？查看：
- [GitHub Pages 文档](https://docs.github.com/pages)
- [Decap CMS 文档](https://decapcms.org/docs/)
- [GitHub Actions 文档](https://docs.github.com/actions)
