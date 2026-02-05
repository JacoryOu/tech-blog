#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客自动生成并部署脚本
1. 生成今天的教程文章
2. 构建网站
3. 推送到 GitHub（触发 GitHub Pages 或 Netlify 自动部署）
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# 配置
BLOG_DIR = "/home/jacory/clawd/projects/tech-blog"
POSTS_DIR = os.path.join(BLOG_DIR, "content/posts")
SCRIPT_DIR = os.path.join(BLOG_DIR, "scripts")

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or BLOG_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def generate_post():
    """生成今天的文章"""
    print("📝 正在生成今日教程文章...")
    success, stdout, stderr = run_command(
        f"python3 {SCRIPT_DIR}/generate_ai_tutorial.py",
        cwd=BLOG_DIR
    )
    if success:
        # 提取文件名和标题
        for line in stdout.split("\n"):
            if "文章已生成:" in line:
                filepath = line.split(": ")[1].strip()
                print(f"✅ 文章生成成功: {filepath}")
                return filepath
            if "标题:" in line:
                title = line.split(": ")[1].strip()
                print(f"📄 标题: {title}")
        return True
    else:
        print(f"❌ 文章生成失败: {stderr}")
        return None

def build_site():
    """构建网站"""
    print("🔨 正在构建网站...")
    success, stdout, stderr = run_command("npm run build", cwd=BLOG_DIR)
    if success:
        print("✅ 网站构建成功")
        return True
    else:
        print(f"❌ 构建失败: {stderr}")
        return False

def deploy_to_github():
    """推送到 GitHub"""
    print("🚀 正在推送到 GitHub...")
    
    # 配置 git（确保使用正确的身份）
    run_command('git config user.email "bot@clawd.ai"', cwd=BLOG_DIR)
    run_command('git config user.name "Clawd Bot"', cwd=BLOG_DIR)
    
    # 添加所有更改
    success, stdout, stderr = run_command("git add -A", cwd=BLOG_DIR)
    if not success:
        print(f"⚠️ git add 警告: {stderr}")
    
    # 检查是否有更改
    success, stdout, stderr = run_command("git status --porcelain", cwd=BLOG_DIR)
    if not stdout.strip():
        print("ℹ️ 没有新的更改需要提交")
        return True
    
    # 提交更改
    today = datetime.now().strftime("%Y-%m-%d")
    commit_msg = f"[Auto] Daily AI tutorial - {today}"
    success, stdout, stderr = run_command(
        f'git commit -m "{commit_msg}"',
        cwd=BLOG_DIR
    )
    if not success:
        print(f"❌ git commit 失败: {stderr}")
        return False
    
    # 推送到远程
    success, stdout, stderr = run_command("git push origin main", cwd=BLOG_DIR)
    if success:
        print("✅ 成功推送到 GitHub")
        print("🌐 GitHub Pages/Netlify 将自动部署更新")
        return True
    else:
        print(f"❌ git push 失败: {stderr}")
        return False

def get_today_post_title():
    """获取今天文章的标题"""
    today = datetime.now().strftime("%Y-%m-%d")
    posts_dir = os.path.join(BLOG_DIR, "content/posts")
    
    try:
        for filename in os.listdir(posts_dir):
            if filename.startswith(today) and filename.endswith(".md"):
                filepath = os.path.join(posts_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 提取标题
                    for line in content.split('\n'):
                        if line.startswith('title:'):
                            title = line.split(':', 1)[1].strip().strip('"').strip("'")
                            return title
        return "AI教程文章"
    except:
        return "AI教程文章"

def main():
    """主函数"""
    print("=" * 50)
    print("🤖 开始执行 AI教程博客自动发布")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 生成文章
    post_path = generate_post()
    if not post_path:
        print("❌ 文章生成失败，终止部署")
        return False
    
    # 2. 构建网站
    if not build_site():
        print("❌ 网站构建失败，终止部署")
        return False
    
    # 3. 推送到 GitHub
    if not deploy_to_github():
        print("❌ GitHub 推送失败")
        return False
    
    # 4. 获取文章标题
    title = get_today_post_title()
    
    print("=" * 50)
    print("🎉 全部完成！")
    print(f"📄 今日文章: {title}")
    print("🌐 网站将在几分钟后自动更新")
    print("=" * 50)
    
    return True, title

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
