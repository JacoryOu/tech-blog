# 🚀 Netlify 部署指南

Netlify 是最适合 Decap CMS 的托管平台，提供原生 Git Gateway 支持。

---

## ✅ 部署前检查清单

- [ ] 代码已推送到 GitHub 仓库
- [ ] 仓库是公开的（免费版要求）
- [ ] `admin/config.yml` 已配置正确
- [ ] `netlify.toml` 已添加

---

## 📋 部署步骤

### 第一步：推送代码到 GitHub

```bash
cd /home/jacory/clawd/projects/tech-blog

# 确认文件已更新
git add .
git commit -m "Configure for Netlify deployment"
git push origin main
```

### 第二步：注册/登录 Netlify

1. 访问 https://app.netlify.com
2. 用 GitHub 账号登录（推荐）

### 第三步：导入项目

1. 点击 **"Add new site"** → **"Import an existing project"**
2. 选择 **GitHub**
3. 授权 Netlify 访问你的仓库
4. 选择 `your-blog-repo` 仓库

### 第四步：配置构建设置

| 设置项 | 值 |
|--------|-----|
| **Build command** | `npm run build:github` |
| **Publish directory** | `.` |
| **Node version** | `18` |

点击 **Deploy site**

### 第五步：启用 Identity（CMS 必需）

等待首次部署完成后：

1. 进入站点 → **Site settings** → **Identity**
2. 点击 **Enable Identity**
3. 在 **Registration** 中选择：
   - **Invite only**（推荐，安全）
   - 或 **Open**（任何人可注册）

4. 在 **External providers** 中启用 **GitHub**（可选，方便登录）

### 第六步：开启 Git Gateway

1. 进入 **Site settings** → **Identity** → **Services**
2. 点击 **Enable Git Gateway**
3. 选择 **GitHub** 作为提供商
4. 授权 Netlify 访问仓库

### 第七步：配置 CMS

1. 打开 `admin/config.yml`
2. 修改为你的信息：
   ```yaml
   backend:
     name: git-gateway
     repo: yourusername/your-blog-repo    # 你的仓库
     branch: main
   
   site_url: https://your-site-name.netlify.app  # 你的 Netlify 地址
   ```

3. 提交并推送：
   ```bash
   git add admin/config.yml
   git commit -m "Update CMS config for Netlify"
   git push
   ```

### 第八步：访问网站

- 🌐 **网站**：`https://your-site-name.netlify.app`
- 📝 **CMS 后台**：`https://your-site-name.netlify.app/admin`

---

## 👤 添加管理员用户

### 方式 1：邀请邮件

1. 进入 **Identity** → **Invite users**
2. 输入邮箱地址
3. 选择角色：
   - **Admin** - 可发布文章
   - **Editor** - 可编辑文章
   - **Visitor** - 只读
4. 点击 Send invite

### 方式 2：自己注册

如果设置为 Open registration：

1. 访问 `https://your-site.netlify.app/admin`
2. 点击 **Login with Netlify Identity**
3. 填写邮箱密码注册
4. 在 Netlify 后台批准该用户

---

## 🎨 自定义域名（可选）

1. 进入 **Domain settings** → **Domains**
2. 点击 **Add custom domain**
3. 输入你的域名（如 `blog.yourname.com`）
4. 按提示配置 DNS

免费 SSL 证书自动颁发 ✅

---

## 🔧 常见问题

### 1. CMS 登录失败

**检查：**
- Identity 是否已启用？
- Git Gateway 是否已启用？
- config.yml 中的 repo 是否正确？

### 2. 构建失败

查看构建日志：
```
Site → Deploys → 选择失败的部署 → Deploy log
```

常见错误：
- `npm not found` → 检查 Node version 设置
- `build command not found` → 确认 package.json 中有该脚本

### 3. 文章保存失败

- 检查用户是否有写入权限
- 确认 Git Gateway 连接正常
- 尝试重新授权 Git Gateway

---

## 🔄 工作流程

```
访问 /admin → 登录 → 写文章 → 点击 Publish
                                    ↓
                            自动提交到 GitHub
                                    ↓
                            触发 Netlify 构建
                                    ↓
                            网站自动更新 🎉
```

---

## 📞 需要帮助？

- [Netlify 文档](https://docs.netlify.com/)
- [Decap CMS 文档](https://decapcms.org/docs/)
- [Netlify Identity 文档](https://docs.netlify.com/visitor-access/identity/)

Happy Blogging! 🚀
