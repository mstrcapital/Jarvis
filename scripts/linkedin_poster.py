#!/usr/bin/env python3
"""
LinkedIn Automation Script
使用 Playwright 自动登录 LinkedIn 并发布内容
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright

# 配置
LINKEDIN_EMAIL = os.environ.get("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD", "")
COOKIES_FILE = "/root/.openclaw/workspace/.linkedin_cookies.json"

async def save_cookies(context, cookies_file):
    """保存 cookies"""
    cookies = await context.cookies()
    with open(cookies_file, 'w') as f:
        json.dump(cookies, f)
    print(f"✅ Cookies saved to {cookies_file}")

async def load_cookies(context, cookies_file):
    """加载 cookies"""
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
        print(f"✅ Cookies loaded from {cookies_file}")
        return True
    return False

async def login_linkedin(page, email, password):
    """手动登录 LinkedIn (用于首次登录或 cookies 过期时)"""
    print("📝 需要手动登录...")
    print("请在打开的浏览器中完成登录...")
    
    # 等待用户手动登录
    await page.wait_for_url("**/feed/**", timeout=120000)
    print("✅ 登录成功!")

async def post_linkedin(page, content: str):
    """发布 LinkedIn 帖子"""
    print(f"📝 准备发布内容: {content[:50]}...")
    
    # 点击"开始帖子"按钮
    try:
        # 尝试点击 "开始帖子" 按钮
        await page.click('button[aria-label="开始帖子"]', timeout=5000)
    except:
        try:
            # 备选方案: 点击 "Post" 按钮
            await page.click('button[aria-label="Post"]', timeout=5000)
        except:
            print("⚠️ 找不到发布按钮,尝试直接导航到发布页面")
            await page.goto("https://www.linkedin.com/feed/")
            await asyncio.sleep(2)
    
    # 等待编辑器加载
    await page.wait_for_selector('div[role="textbox"]', timeout=10000)
    
    # 输入内容
    await page.fill('div[role="textbox"]', content)
    
    # 点击发布按钮
    await page.click('button:has-text("发布")', timeout=10000)
    
    print("✅ 帖子已发布!")
    return True

async def main(action="post", content="", cookies_only=False):
    """主函数"""
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # 尝试加载 cookies
        has_cookies = await load_cookies(context, COOKIES_FILE)
        
        # 访问 LinkedIn
        await page.goto("https://www.linkedin.com")
        
        # 检查是否已登录
        if "login" in page.url.lower() or not has_cookies:
            # 需要登录
            if LINKEDIN_EMAIL and LINKEDIN_PASSWORD:
                # 自动登录
                print("🔐 尝试自动登录...")
                await page.fill('#username', LINKEDIN_EMAIL)
                await page.fill('#password', LINKEDIN_PASSWORD)
                await page.click('button[type="submit"]')
                await page.wait_for_url("**/feed/**", timeout=30000)
                await save_cookies(context, COOKIES_FILE)
            else:
                # 需要手动登录
                await login_linkedin(page, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
                await save_cookies(context, COOKIES_FILE)
        
        if cookies_only:
            print("✅ Cookies 已保存")
            await browser.close()
            return
        
        if action == "post" and content:
            await post_linkedin(page, content)
        
        # 保持浏览器打开一会儿
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    import sys
    
    action = sys.argv[1] if len(sys.argv) > 1 else "post"
    content = sys.argv[2] if len(sys.argv) > 2 else "测试帖子来自 Jarvis AI Agent 🤖"
    
    if action == "login":
        asyncio.run(main(cookies_only=True))
    else:
        asyncio.run(main(action=action, content=content))
