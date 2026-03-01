#!/usr/bin/env python3
"""
Alex (CTO) - 网络爬取优化方案
针对 X (Twitter) 和通用网页爬取
"""

import subprocess
import json
import requests
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"

class WebCrawler:
    """多策略网页爬取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
    
    def fetch(self, url: str, strategy: str = "auto") -> str:
        """根据策略获取页面"""
        
        strategies = [
            self.fetch_via_curl_cffi,
            self.fetch_via_playwright,
            self.fetch_via_nitter,
            self.fetch_via_fxtwitter,
            self.fetch_via_jina,
        ]
        
        if strategy == "auto":
            # 尝试所有策略直到成功
            for s in strategies:
                try:
                    result = s(url)
                    if result and len(result) > 100:
                        return result
                except:
                    continue
            return "❌ 所有策略都失败"
        else:
            # 使用指定策略
            method = getattr(self, f"fetch_via_{strategy}", None)
            if method:
                return method(url)
            return f"❌ 未知策略: {strategy}"
    
    def fetch_via_curl_cffi(self, url: str) -> str:
        """使用 curl_cffi"""
        import curl_cffi
        r = curl_cffi.get(url, impersonate="chrome")
        return r.text if r.status_code == 200 else ""
    
    def fetch_via_playwright(self, url: str) -> str:
        """使用 Playwright (需要安装)"""
        # 需要先安装: pip install playwright && playwright install chromium
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, timeout=15000)
                content = page.content()
                browser.close()
                return content
        except:
            return ""
    
    def fetch_via_nitter(self, url: str) -> str:
        """通过 Nitter (Twitter 镜像) 获取"""
        # 提取 tweet ID
        if "twitter.com" in url or "x.com" in url:
            tweet_id = url.split("/")[-1]
            nitter_instances = [
                "nitter.net",
                "nitter.privacydev.net", 
                "nitter.poast.org"
            ]
            for instance in nitter_instances:
                try:
                    r = requests.get(f"https://{instance}/i/status/{tweet_id}", 
                                   timeout=10, headers=self.session.headers)
                    if r.status_code == 200:
                        return r.text
                except:
                    continue
        return ""
    
    def fetch_via_fxtwitter(self, url: str) -> str:
        """通过 fxtwitter/vxtwitter 获取嵌入"""
        if "twitter.com" in url or "x.com" in url:
            try:
                r = requests.get(f"https://fxtwitter.com/{url.split('com/')[-1]}", 
                               timeout=10, headers=self.session.headers)
                return r.text if r.status_code == 200 else ""
            except:
                pass
        return ""
    
    def fetch_via_jina(self, url: str) -> str:
        """通过 Jina AI Reader 获取"""
        try:
            r = requests.get(f"https://r.jina.ai/{url}", timeout=15)
            if r.status_code == 200:
                return r.text
        except:
            pass
        return ""

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
🕷️ Alex Web Crawler

用法:
    python3 crawler.py <URL> [strategy]

策略:
    auto        - 自动选择 (默认)
    curl_cffi   - 基础HTTP
    playwright  - 浏览器自动化
    nitter      - Twitter镜像
    fxtwitter   - Twitter嵌入
    jina        - Jina AI阅读器

示例:
    python3 crawler.py "https://x.com/user/status/123"
    python3 crawler.py "https://news.ycombinator.com" curl_cffi
        """)
        return
    
    url = sys.argv[1]
    strategy = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    print(f"🕷️ 爬取: {url}")
    print(f"📋 策略: {strategy}\n")
    
    crawler = WebCrawler()
    result = crawler.fetch(url, strategy)
    
    if result and len(result) > 100:
        print(f"✅ 成功! 获取 {len(result)} 字符")
        print("\n--- 预览 ---")
        print(result[:500])
    else:
        print("❌ 失败")

if __name__ == "__main__":
    main()