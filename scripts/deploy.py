#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI教程博客自动生成并部署脚本 + 飞书通知
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# 飞书用户ID
FEISHU_USER_ID = "ou_cbeea7989e1b69e855fb519e31a57f34"

# 配置
BLOG_DIR = "/home/jacory/clawd/projects/tech-blog"

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
    print("正在生成今日教程文章...")
    success, stdout, stderr = run_command(
        f"python3 scripts/generate_ai_tutorial.py",
        cwd=BLOG_DIR
    )
    if success:
        # 解析输出获取信息
        title = ""
        next_title = ""
        for line in stdout.split("\n"):
            if "标题:" in line:
                title = line.split(": ")[1].strip()
            if "明天预告:" in line:
                next_title = line.split(": ")[1].strip()
        return {"title": title, "next_title": next_title}
    else:
        print(f"文章生成失败: {stderr}")
        return None

def build_and_deploy():
    """构建并部署"""
    print("正在构建网站...")
    
    # 构建
    success, stdout, stderr = run_command("npm run build:github", cwd=BLOG_DIR)
    if not success:
        print(f"构建失败: {stderr}")
        return False
    
    print("构建成功，正在推送到GitHub...")
    
    # 配置git
    run_command('git config user.email "bot@clawd.ai"', cwd=BLOG_DIR)
    run_command('git config user.name "Clawd Bot"', cwd=BLOG_DIR)
    
    # 提交并推送
    run_command("git add -A", cwd=BLOG_DIR)
    
    today = datetime.now().strftime("%Y-%m-%d")
    success, stdout, stderr = run_command(
        f'git commit -m "[Auto] Daily AI tutorial - {today}"',
        cwd=BLOG_DIR
    )
    
    success, stdout, stderr = run_command("git push origin HEAD", cwd=BLOG_DIR)
    if not success:
        print(f"推送失败: {stderr}")
        return False
    
    print("推送成功，GitHub Actions将自动部署")
    return True

def send_feishu_notification(post_info):
    """发送飞书通知"""
    if not post_info:
        return
    
    title = post_info.get("title", "AI教程文章")
    next_title = post_info.get("next_title", "敬请期待")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建通知消息
    message = f"""🎉 今日AI教程博客已发布

📄 文章标题：{title}
⏱️ 阅读时间：约20分钟
📅 发布日期：{today}

🔗 在线阅读：
   • Netlify：https://serene-mochi-6ec644.netlify.app/posts.html
   • GitHub Pages：https://jacoryou.github.io/tech-blog/posts.html

📝 后台管理：https://serene-mochi-6ec644.netlify.app/admin/

📚 明天预告：{next_title}

---
每天08:00自动更新，欢迎阅读学习！"""

    # 创建通知文件（供飞书工具读取）
    notification_file = "/tmp/feishu_notification.txt"
    with open(notification_file, "w", encoding="utf-8") as f:
        f.write(message)
    
    print(f"飞书通知已准备: {notification_file}")
    print(f"通知内容:\n{message}")
    
    return message

def main():
    """主函数"""
    print("=" * 50)
    print("开始执行 AI教程博客自动发布")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 生成文章
    post_info = generate_post()
    if not post_info:
        print("文章生成失败")
        return False
    
    print(f"文章生成成功: {post_info['title']}")
    
    # 2. 构建并部署
    if not build_and_deploy():
        print("部署失败")
        return False
    
    # 3. 发送飞书通知
    notification = send_feishu_notification(post_info)
    
    print("=" * 50)
    print("全部完成！")
    print(f"文章: {post_info['title']}")
    print(f"明天: {post_info['next_title']}")
    print("=" * 50)
    
    # 输出通知内容供外部使用
    if notification:
        print(f"\nFEISHU_NOTIFICATION_START\n{notification}\nFEISHU_NOTIFICATION_END")
    
    return True, post_info

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
