#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频号素材收集工具 - Python版
Video Materials Collection Tool - Python Version

功能:
1. 下载Instagram、TikTok、YouTube、Twitter素材
2. 批量重命名
3. 版权检查
4. 生成报告

依赖:
- yt-dlp (YouTube下载): pip install yt-dlp
- requests (HTTP请求): pip install requests
- tqdm (进度条): pip install tqdm

作者: Jarvis
创建日期: 2026-02-15
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import subprocess

# 尝试导入可选依赖
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class Colors:
    """终端颜色"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def log_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")


def log_success(msg):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")


def log_warning(msg):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")


def log_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")


class VideoCollector:
    """视频素材收集器"""
    
    def __init__(self, base_dir: str = "/root/.openclaw/workspace/video-materials"):
        self.base_dir = Path(base_dir)
        self.materials_dir = self.base_dir / "素材"
        self.log_dir = self.base_dir / "日志"
        
        # 创建目录
        self._setup_directories()
        
        # 配置日志
        self._setup_logging()
    
    def _setup_directories(self):
        """创建目录结构"""
        categories = [
            "迪拜-阿布扎比",
            "土豪日常",
            "华人群体",
            "生活定居",
            "高清街拍",
            "已发布"
        ]
        
        for cat in categories:
            (self.materials_dir / cat).mkdir(parents=True, exist_ok=True)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        log_success("目录结构创建完成")
    
    def _setup_logging(self):
        """配置日志"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"collect_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def download_instagram(self, url: str, category: str = "迪拜-阿布扎比"):
        """Instagram下载指引"""
        log_info(f"Instagram下载指引: {url}")
        log_info(f"分类: {category}")
        print("\n请使用以下工具:")
        print("1. 4K Stogram: https://www.4kdownload.com/products/product-stogram")
        print("2. Instagram Downloader Chrome扩展")
        print("3. 命令行: instaloader https://instagram.com/p/... (需安装instaloader)")
        return True
    
    def download_tiktok(self, url: str, category: str = "迪拜-阿布扎比"):
        """TikTok下载"""
        log_info(f"TikTok下载指引: {url}")
        log_info(f"分类: {category}")
        print("\n请使用以下工具:")
        print("1. SSSTik: https://ssstik.io")
        print("2. TikMate: https://www.tikmate.io")
        print("3. 命令行: yt-dlp \"{url}\" -o \"output.mp4\"")
        return True
    
    def download_youtube(self, url: str, category: str = "迪拜-阿布扎比"):
        """YouTube下载"""
        log_info(f"YouTube下载: {url}")
        log_info(f"分类: {category}")
        
        output_dir = self.materials_dir / category
        
        try:
            cmd = [
                "yt-dlp",
                "-o", f"{output_dir}/%(title)s.%(ext)s",
                "--format", "best",
                "--no-check-certificate",
                url
            ]
            
            log_info(f"执行命令: {' '.join(cmd[:3])}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success("下载完成")
                return True
            else:
                log_warning("yt-dlp未安装或下载失败，将使用指引模式")
                print("\n请使用以下工具:")
                print("1. 4K Video Downloader: https://www.4kdownload.com/products/video-downloader")
                return False
                
        except FileNotFoundError:
            log_warning("yt-dlp未安装，请先安装: pip install yt-dlp")
            print("\n请使用以下工具:")
            print("1. 4K Video Downloader: https://www.4kdownload.com/products/video-downloader")
            return False
    
    def download_twitter(self, url: str, category: str = "迪拜-阿布扎比"):
        """Twitter/X下载"""
        log_info(f"Twitter下载指引: {url}")
        log_info(f"分类: {category}")
        print("\n请使用以下工具:")
        print("1. Twitter Video Downloader: https://twdownloader.com/")
        print("2. SSSTwitter: https://ssstwitter.com/")
        print("3. 命令行: yt-dlp \"{url}\"")
        return True
    
    def rename_files(self, category: str):
        """批量重命名文件"""
        category_dir = self.materials_dir / category
        
        if not category_dir.exists():
            log_error(f"分类目录不存在: {category_dir}")
            return False
        
        log_info(f"重命名文件: {category}")
        
        extensions = ['.mp4', '.jpg', '.jpeg', '.png', '.mov', '.avi']
        renamed_count = 0
        
        for ext in extensions:
            for file_path in category_dir.rglob(f"*{ext}"):
                if file_path.is_file():
                    # 创建新文件名
                    timestamp = datetime.now().strftime("%Y%m%d")
                    new_name = f"{category}_{timestamp}_{file_path.stem[:30]}{ext}"
                    new_path = file_path.parent / new_name
                    
                    if file_path != new_path:
                        file_path.rename(new_path)
                        log_success(f"重命名: {file_path.name} -> {new_name}")
                        renamed_count += 1
        
        log_success(f"共重命名 {renamed_count} 个文件")
        return True
    
    def copyright_check(self, file_path: str):
        """版权检查"""
        print("\n" + "="*50)
        print(f"版权检查: {file_path}")
        print("="*50)
        
        questions = [
            ("素材有水印?", "has_watermark"),
            ("有明确的版权声明?", "has_copyright"),
            ("可用于商业用途?", "can_commercial"),
            ("已获得作者授权?", "has_permission")
        ]
        
        answers = {}
        for question, key in questions:
            response = input(f"{question} (y/n): ").strip().lower()
            answers[key] = response == 'y'
        
        # 判断版权状态
        if not answers['has_watermark'] and answers['has_permission']:
            status = "可用"
        elif answers['can_commercial']:
            status = "需标注来源"
        else:
            status = "待确认"
        
        print(f"\n版权状态: {status}")
        
        # 记录到日志
        log_entry = {
            "time": datetime.now().isoformat(),
            "file": file_path,
            "status": status,
            "answers": answers
        }
        
        log_file = self.log_dir / "copyright_check.json"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        return status
    
    def generate_report(self) -> Dict:
        """生成素材报告"""
        log_info("生成素材报告...")
        
        report = {
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "分类统计": {},
            "总计": {
                "视频数": 0,
                "图片数": 0,
                "总文件数": 0
            }
        }
        
        categories = [
            "迪拜-阿布扎比",
            "土豪日常",
            "华人群体",
            "生活定居",
            "高清街拍",
            "已发布"
        ]
        
        for cat in categories:
            cat_dir = self.materials_dir / cat
            if cat_dir.exists():
                videos = list(cat_dir.rglob("*.mp4"))
                images = list(cat_dir.rglob("*.jpg")) + list(cat_dir.rglob("*.png"))
                
                report["分类统计"][cat] = {
                    "视频数": len(videos),
                    "图片数": len(images)
                }
                
                report["总计"]["视频数"] += len(videos)
                report["总计"]["图片数"] += len(images)
        
        report["总计"]["总文件数"] = report["总计"]["视频数"] + report["总计"]["图片数"]
        
        # 保存报告
        report_file = self.log_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        log_success(f"报告已保存: {report_file}")
        
        return report
    
    def quick_download_all(self):
        """快速下载所有平台指引"""
        print("\n" + "="*60)
        print("  视频号素材收集 - 快速下载指引")
        print("="*60)
        print("\n【Instagram】")
        print("  工具: 4K Stogram")
        print("  地址: https://www.4kdownload.com/products/product-stogram")
        print("  用法: 粘贴账号或标签，自动下载")
        
        print("\n【TikTok】")
        print("  工具: SSSTik.io")
        print("  地址: https://ssstik.io")
        print("  用法: 粘贴视频链接，下载无水印版本")
        
        print("\n【YouTube Shorts】")
        print("  工具: 4K Video Downloader")
        print("  地址: https://www.4kdownload.com/products/video-downloader")
        print("  用法: 复制链接，一键下载")
        
        print("\n【Twitter/X】")
        print("  工具: Twitter Video Downloader")
        print("  地址: https://twdownloader.com")
        print("  用法: 粘贴推文链接，下载视频")
        
        print("\n" + "="*60)
        
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="视频号素材收集工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python collect.py setup                    # 创建目录
  python collect.py instagram <url>         # Instagram指引
  python collect.py tiktok <url>           # TikTok指引
  python collect.py youtube <url>           # YouTube下载
  python collect.py rename <分类名>          # 重命名文件
  python collect.py check <文件路径>         # 版权检查
  python collect.py report                  # 生成报告
  python collect.py quick                  # 快速下载指引
        """
    )
    
    parser.add_argument("command", choices=[
        "setup", "instagram", "tiktok", "youtube", "twitter",
        "rename", "check", "report", "quick", "all"
    ], help="命令")
    
    parser.add_argument("target", nargs="?", help="目标URL或分类名")
    parser.add_argument("--dir", "-d", default="/root/.openclaw/workspace/video-materials",
                        help="素材库根目录")
    
    args = parser.parse_args()
    
    # 创建收集器
    collector = VideoCollector(args.dir)
    
    # 执行命令
    if args.command == "setup":
        collector._setup_directories()
    
    elif args.command == "instagram":
        collector.download_instagram(args.target or "")
    
    elif args.command == "tiktok":
        collector.download_tiktok(args.target or "")
    
    elif args.command == "youtube":
        collector.download_youtube(args.target or "")
    
    elif args.command == "twitter":
        collector.download_twitter(args.target or "")
    
    elif args.command == "rename":
        collector.rename_files(args.target or "迪拜-阿布扎比")
    
    elif args.command == "check":
        collector.copyright_check(args.target or "")
    
    elif args.command == "report":
        report = collector.generate_report()
        print("\n" + "="*50)
        print("素材统计报告")
        print("="*50)
        for cat, stats in report["分类统计"].items():
            print(f"{cat}: 视频{stats['视频数']}个, 图片{stats['图片数']}张")
        print(f"\n总计: 视频{report['总计']['视频数']}个, 图片{report['总计']['图片数']}张")
    
    elif args.command == "quick":
        collector.quick_download_all()
    
    elif args.command == "all":
        collector._setup_directories()
        collector.quick_download_all()


if __name__ == "__main__":
    main()
