#!/usr/bin/env python3
"""
Hermes图片爬虫 v1.0
从合法网站爬取Hermes相关图片

使用说明:
1. 安装依赖: pip3 install requests beautifulsoup4
2. 运行脚本: python3 hermes_crawler.py
"""

import os
import sys
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from datetime import datetime
import re

# 配置
OUTPUT_DIR = Path("/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo")
TEMP_DIR = Path("/tmp/hermes_crawler")

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

class HermesCrawler:
    """Hermes图片爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.downloaded = []
        self.errors = []
        
    def crawl_pexels(self, query="luxury handbag black", pages=3):
        """从Pexels爬取免费图片"""
        print(f"\n🔍 从Pexels爬取: {query}")
        
        results = []
        
        for page in range(1, pages + 1):
            try:
                url = f"https://www.pexels.com/search/{query.replace(' ', '%20')}/?page={page}"
                print(f"  📄 爬取页面 {page}...")
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找图片
                    images = soup.find_all('img', src=re.compile(r'images\.pexels\.com'))
                    
                    for img in images[:10]:  # 每页最多10张
                        src = img.get('src', '')
                        if src:
                            results.append(src)
                            print(f"    ✅ 找到图片: {src[:50]}...")
                
                time.sleep(2)  # 避免请求过快
                
            except Exception as e:
                self.errors.append(f"Pexels page {page}: {str(e)}")
                print(f"    ❌ 错误: {e}")
        
        return results
    
    def crawl_unsplash(self, query="luxury bag", pages=2):
        """从Unsplash爬取免费图片"""
        print(f"\n🔍 从Unsplash爬取: {query}")
        
        results = []
        
        for page in range(1, pages + 1):
            try:
                url = f"https://unsplash.com/s/photos/{query.replace(' ', '-')}?page={page}"
                print(f"  📄 爬取页面 {page}...")
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找图片
                    images = soup.find_all('img', src=re.compile(r'images\.unsplash\.com'))
                    
                    for img in images[:10]:
                        src = img.get('src', '')
                        if src:
                            results.append(src)
                            print(f"    ✅ 找到图片: {src[:50]}...")
                
                time.sleep(2)
                
            except Exception as e:
                self.errors.append(f"Unsplash page {page}: {str(e)}")
                print(f"    ❌ 错误: {e}")
        
        return results
    
    def crawl_pinterest(self, query="hermes birkin black", pages=2):
        """从Pinterest爬取图片"""
        print(f"\n🔍 从Pinterest爬取: {query}")
        
        results = []
        
        try:
            url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
            print(f"  📄 爬取Pinterest...")
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找图片
                images = soup.find_all('img', src=re.compile(r'i\.pinimg\.com'))
                
                for img in images[:20]:
                    src = img.get('src', '')
                    if src and '236x' in src:  # 选择合适尺寸
                        results.append(src)
                        print(f"    ✅ 找到图片: {src[:50]}...")
            
            time.sleep(2)
            
        except Exception as e:
            self.errors.append(f"Pinterest: {str(e)}")
            print(f"    ❌ 错误: {e}")
        
        return results
    
    def download_images(self, urls, category="hermes"):
        """下载图片"""
        print(f"\n📥 开始下载 {len(urls)} 张图片...")
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        for i, url in enumerate(urls[:20], 1):  # 最多下载20张
            try:
                # 获取图片
                response = self.session.get(url, timeout=30, allow_redirects=True)
                
                if response.status_code == 200:
                    # 生成文件名
                    ext = '.jpg'
                    if '.png' in url:
                        ext = '.png'
                    
                    filename = f"{category}_{i:03d}{ext}"
                    filepath = OUTPUT_DIR / filename
                    
                    # 保存图片
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    self.downloaded.append(str(filepath))
                    print(f"  ✅ 下载成功: {filename} ({len(response.content)/1024:.1f}KB)")
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                self.errors.append(f"Download {i}: {str(e)}")
                print(f"  ❌ 下载失败: {e}")
        
        return self.downloaded
    
    def generate_report(self):
        """生成报告"""
        report = f"""# Hermes图片爬虫报告

> 爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 输出目录: {OUTPUT_DIR}

## 下载统计

| 项目 | 数量 |
|------|------|
| 成功下载 | {len(self.downloaded)} |
| 错误数 | {len(self.errors)} |

## 下载的文件

"""
        
        for i, filepath in enumerate(self.downloaded, 1):
            report += f"{i}. {os.path.basename(filepath)}\n"
        
        report += "\n## 错误记录\n\n"
        
        if self.errors:
            for error in self.errors:
                report += f"- {error}\n"
        else:
            report += "无错误记录\n"
        
        report += f"""
---

## 使用说明

1. 下载的图片保存在: `{OUTPUT_DIR}`
2. 图片可直接用于TikTok/Instagram发布
3. 建议手动筛选高质量图片

## 下一步

1. 筛选高质量图片 (2000px+)
2. 验证是正品Hermes
3. 创建内容并发布
"""
        
        report_path = OUTPUT_DIR.parent / "爬虫报告.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📊 报告已生成: {report_path}")
        return report_path


def main():
    """主程序"""
    print("\n" + "=" * 50)
    print("  🎀 Hermes图片爬虫 v1.0")
    print("=" * 50)
    
    crawler = HermesCrawler()
    
    # 爬取图片
    all_urls = []
    
    # Pexels
    urls = crawler.crawl_pexels("luxury handbag black", pages=2)
    all_urls.extend(urls)
    
    # Unsplash
    urls = crawler.crawl_unsplash("luxury bag black", pages=2)
    all_urls.extend(urls)
    
    # Pinterest
    urls = crawler.crawl_pinterest("hermes birkin black", pages=1)
    all_urls.extend(urls)
    
    # 去重
    all_urls = list(set(all_urls))
    print(f"\n📦 总共找到 {len(all_urls)} 张图片")
    
    # 下载
    if all_urls:
        downloaded = crawler.download_images(all_urls, "hermes")
        
        # 生成报告
        crawler.generate_report()
        
        print(f"\n✅ 爬取完成!")
        print(f"   下载: {len(downloaded)} 张")
        print(f"   错误: {len(crawler.errors)} 个")
        print(f"   位置: {OUTPUT_DIR}")
    else:
        print("\n⚠️  未找到图片，请尝试手动收集")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())