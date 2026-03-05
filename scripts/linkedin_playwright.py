#!/usr/bin/env python3
"""
LinkedIn Automation with Playwright
支持: 登录、发帖子、获取cookies
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# 配置
COOKIES_FILE = "/root/.openclaw/workspace/.linkedin_cookies.json"
SCREENSHOTS_DIR = "/root/.openclaw/workspace/screenshots"

class LinkedInBot:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
    async def init(self):
        """初始化浏览器"""
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US'
        )
        self.page = await self.context.new_page()
        
        # 注入脚本绕过检测
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
    async def save_cookies(self):
        """保存 cookies"""
        cookies = await self.context.cookies()
        os.makedirs(os.path.dirname(COOKIES_FILE), exist_ok=True)
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Cookies saved")
        
    async def load_cookies(self):
        """加载 cookies"""
        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
            await self.context.add_cookies(cookies)
            return True
        return False
        
    async def login(self, email: str, password: str, save_session: bool = True):
        """登录 LinkedIn"""
        print("🔐 登录 LinkedIn...")
        
        await self.page.goto("https://www.linkedin.com/login")
        await self.page.fill('#username', email)
        await self.page.fill('#password', password)
        await self.page.click('button[type="submit"]')
        
        # 等待登录完成
        try:
            await self.page.wait_for_url("**/feed/**", timeout=30000)
            print("✅ 登录成功!")
            
            if save_session:
                await self.save_cookies()
            return True
            
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            # 可能需要验证码
            await self.screenshot("login_error")
            return False
    
    async def is_logged_in(self) -> bool:
        """检查是否已登录"""
        await self.page.goto("https://www.linkedin.com/feed", timeout=10000)
        return "login" not in self.page.url.lower()
    
    async def post(self, content: str, media_urls: list = None) -> bool:
        """发布帖子"""
        print(f"📝 发布帖子...")
        
        # 点击创建帖子按钮
        try:
            # 尝试多种选择器
            selectors = [
                'button[aria-label="Start a post"]',
                'button[aria-label="创建帖子"]',
                'button:has-text("Start a post")',
                'div[aria-label="Create a post"]'
            ]
            
            for sel in selectors:
                try:
                    await self.page.click(sel, timeout=3000)
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 找不到发布按钮: {e}")
        
        # 等待编辑器出现
        await asyncio.sleep(2)
        
        # 输入内容
        try:
            # 尝试点击编辑器并输入
            await self.page.click('div[role="textbox"]', timeout=5000)
            await self.page.keyboard.type(content, delay=50)
        except:
            print("❌ 无法输入内容")
            return False
            
        # 点击发布
        await asyncio.sleep(1)
        
        try:
            publish_selectors = [
                'button:has-text("Post")',
                'button:has-text("发布")',
                'button[aria-label="Post"]'
            ]
            
            for sel in publish_selectors:
                try:
                    await self.page.click(sel, timeout=3000)
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 找不到发布按钮: {e}")
            
        await asyncio.sleep(3)
        print("✅ 帖子已发布!")
        await self.screenshot("posted")
        return True
    
    async def get_profile(self, handle: str) -> dict:
        """获取用户资料"""
        await self.page.goto(f"https://www.linkedin.com/in/{handle}/")
        await asyncio.sleep(2)
        
        # 提取信息
        name = await self.page.text_content('h1', timeout=5000).catch(lambda: "N/A")
        title = await self.page.text_content('.text-body-medium', timeout=5000).catch(lambda: "N/A")
        
        return {"name": name, "title": title}
    
    async def screenshot(self, name: str):
        """截图"""
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        await self.page.screenshot(path=f"{SCREENSHOTS_DIR}/linkedin_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()

async def main():
    if len(sys.argv) < 2:
        print("""
LinkedIn Automation Bot

用法:
    python3 linkedin_playwright.py login <email> <password>
    python3 linkedin_playwright.py post "内容"
    python3 linkedin_playwright.py profile <handle>
    python3 linkedin_playwright.py test
        """)
        return
        
    command = sys.argv[1]
    bot = LinkedInBot(headless=False)
    await bot.init()
    
    try:
        if command == "login":
            email = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("LINKEDIN_EMAIL", "")
            password = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("LINKEDIN_PASSWORD", "")
            await bot.login(email, password)
            
        elif command == "post":
            content = sys.argv[2] if len(sys.argv) > 2 else "测试帖子 🤖"
            await bot.load_cookies()
            if not await bot.is_logged_in():
                print("❌ 未登录,请先运行 login 命令")
                return
            await bot.post(content)
            
        elif command == "profile":
            handle = sys.argv[2] if len(sys.argv) > 2 else ""
            await bot.load_cookies()
            profile = await bot.get_profile(handle)
            print(profile)
            
        elif command == "test":
            # 测试登录状态
            await bot.load_cookies()
            if await bot.is_logged_in():
                print("✅ 已登录")
            else:
                print("❌ 未登录")
                
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
