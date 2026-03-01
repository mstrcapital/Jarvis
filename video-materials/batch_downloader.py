#!/usr/bin/env python3
"""
批量下载管理器

功能:
1. 从链接池读取待下载列表
2. 批量下载视频
3. 自动分类存储
4. 记录下载状态

使用方式:
  python batch_downloader.py run          # 开始批量下载
  python batch_downloader.py status      # 查看状态
  python batch_downloader.py add <url>   # 添加链接
  python batch_downloader.py retry       # 重试失败任务
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============== 配置 ==============
LINKS_FILE = "/root/.openclaw/workspace/video-materials/links/links_pool.txt"
DOWNLOAD_DIR = "/root/.openclaw/workspace/video-materials/raw"
DATABASE_FILE = "/root/.openclaw/workspace/video-materials/database/download_status.json"
MAX_WORKERS = 3  # 并行下载数
RETRY_COUNT = 2  # 失败重试次数

# ============== 数据库 ==============
class DownloadDB:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.data = self.load()
    
    def load(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"tasks": {}, "stats": {"total": 0, "success": 0, "failed": 0}}
    
    def save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_task(self, url: str, platform: str, tags: str, priority: str):
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(url) % 10000}"
        
        self.data["tasks"][task_id] = {
            "id": task_id,
            "url": url,
            "platform": platform,
            "tags": tags.split(","),
            "priority": priority,
            "status": "pending",
            "retry_count": 0,
            "created_at": datetime.now().isoformat(),
            "downloaded_at": None,
            "file_path": None,
            "error": None
        }
        self.data["stats"]["total"] += 1
        self.save()
        return task_id
    
    def update_status(self, task_id: str, status: str, file_path: str = None, error: str = None):
        if task_id in self.data["tasks"]:
            self.data["tasks"][task_id]["status"] = status
            self.data["tasks"][task_id]["downloaded_at"] = datetime.now().isoformat()
            self.data["tasks"][task_id]["file_path"] = file_path
            self.data["tasks"][task_id]["error"] = error
            
            if status == "success":
                self.data["stats"]["success"] += 1
            elif status == "failed":
                self.data["stats"]["failed"] += 1
            
            self.save()
    
    def get_pending_tasks(self, priority_order: list = ["high", "medium", "low"]):
        pending = []
        for task_id, task in self.data["tasks"].items():
            if task["status"] == "pending":
                pending.append((task_id, task))
        
        # 按优先级排序
        pending.sort(key=lambda x: priority_order.index(x[1]["priority"]) if x[1]["priority"] in priority_order else 3)
        return pending
    
    def get_stats(self):
        return self.data["stats"]


# ============== 链接解析 ==============
def parse_links_file(filepath: str):
    """解析链接池文件"""
    links = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                links.append({
                    "platform": parts[0],
                    "url": parts[1],
                    "tags": parts[2],
                    "priority": parts[3],
                    "status": parts[4] if len(parts) > 4 else "pending",
                    "line": line_num
                })
    return links


def detect_platform(url: str) -> str:
    """检测URL平台"""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "bilibili.com" in url:
        return "bilibili"
    elif "instagram.com" in url:
        return "instagram"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "dailymotion.com" in url:
        return "dailymotion"
    elif "vimeo.com" in url:
        return "vimeo"
    else:
        return "other"


# ============== 下载函数 ==============
def download_single(task_id: str, url: str, platform: str, tags: list) -> dict:
    """下载单个视频"""
    print(f"\n📥 开始下载: {url}")
    
    # 根据平台选择下载参数
    if platform == "youtube":
        format_args = ["-f", "bestvideo[height<=1080]+bestaudio/best"]
    elif platform == "tiktok":
        format_args = ["-f", "best"]
    else:
        format_args = ["-f", "best"]
    
    # 构建输出路径
    output_name = f"{platform}_%(uploader)s_%(title)s_%(id)s.%(ext)s"
    output_path = os.path.join(DOWNLOAD_DIR, output_name)
    
    # 构建yt-dlp命令
    cmd = [
        "yt-dlp",
        *format_args,
        "-o", output_path,
        "--no-playlist",
        "--no-warnings",
        url
    ]
    
    try:
        # 执行下载
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )
        
        if result.returncode == 0:
            # 查找下载的文件
            downloaded_files = list(Path(DOWNLOAD_DIR).glob(f"*{url[-11:] if len(url) > 11 else url[-11:]}*"))
            if downloaded_files:
                file_path = str(downloaded_files[0])
                print(f"   ✅ 下载成功: {file_path}")
                return {"success": True, "file_path": file_path}
            else:
                print(f"   ⚠️  下载完成但未找到文件")
                return {"success": True, "file_path": None}
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            print(f"   ❌ 下载失败: {error_msg}")
            return {"success": False, "error": error_msg}
    
    except subprocess.TimeoutExpired:
        print(f"   ❌ 下载超时 (10分钟)")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"   ❌ 错误: {str(e)}")
        return {"success": False, "error": str(e)}


# ============== 主功能 ==============
def run_batch_download(max_workers: int = MAX_WORKERS):
    """运行批量下载"""
    print("\n" + "=" * 70)
    print("🚀 开始批量下载")
    print("=" * 70)
    
    db = DownloadDB()
    pending = db.get_pending_tasks()
    
    if not pending:
        print("\n✅ 没有待下载的任务")
        return
    
    print(f"\n📋 待下载任务: {len(pending)}个")
    
    # 并行下载
    completed = {"success": 0, "failed": 0}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        
        for task_id, task in pending:
            future = executor.submit(
                download_single,
                task_id,
                task["url"],
                task["platform"],
                task["tags"]
            )
            futures[future] = task_id
        
        for future in as_completed(futures):
            task_id = futures[future]
            result = future.result()
            
            if result["success"]:
                db.update_status(task_id, "success", result.get("file_path"))
                completed["success"] += 1
            else:
                task = db.data["tasks"][task_id]
                if task["retry_count"] < RETRY_COUNT:
                    task["retry_count"] += 1
                    print(f"   🔄 重试 ({task['retry_count']}/{RETRY_COUNT}): {task['url']}")
                    db.save()
                else:
                    db.update_status(task_id, "failed", error=result["error"])
                    completed["failed"] += 1
    
    print("\n" + "=" * 70)
    print("📊 下载完成")
    print(f"   ✅ 成功: {completed['success']}")
    print(f"   ❌ 失败: {completed['failed']}")
    print("=" * 70)


def import_from_links_pool():
    """从链接池导入"""
    print("\n📥 从链接池导入...")
    
    db = DownloadDB()
    links = parse_links_file(LINKS_FILE)
    
    imported = 0
    for link in links:
        # 检测平台
        platform = link["platform"] if link["platform"] != "auto" else detect_platform(link["url"])
        
        # 添加到数据库
        task_id = db.add_task(
            url=link["url"],
            platform=platform,
            tags=link["tags"],
            priority=link["priority"]
        )
        imported += 1
        print(f"   ✅ 添加: {link['url'][:50]}... [{platform}]")
    
    print(f"\n✅ 成功导入 {imported} 个任务")
    return imported


def show_status():
    """显示状态"""
    db = DownloadDB()
    stats = db.get_stats()
    
    print("\n" + "=" * 70)
    print("📊 下载状态")
    print("=" * 70)
    
    print(f"\n📈 统计:")
    print(f"   总任务: {stats['total']}")
    print(f"   ✅ 成功: {stats['success']}")
    print(f"   ❌ 失败: {stats['failed']}")
    print(f"   ⏳ 待处理: {stats['total'] - stats['success'] - stats['failed']}")
    
    # 按状态分组显示
    by_status = {"pending": [], "processing": [], "success": [], "failed": []}
    for task_id, task in db.data["tasks"].items():
        by_status[task["status"]].append(task)
    
    for status, tasks in by_status.items():
        if tasks:
            print(f"\n📁 {status.upper()} ({len(tasks)}个):")
            for task in tasks[:5]:  # 只显示前5个
                print(f"   - {task['url'][:60]}...")
            if len(tasks) > 5:
                print(f"   ... 还有 {len(tasks) - 5} 个")


def add_link(url: str, tags: str = "general", priority: str = "medium"):
    """添加单个链接"""
    db = DownloadDB()
    platform = detect_platform(url)
    
    task_id = db.add_task(url=url, platform=platform, tags=tags, priority=priority)
    print(f"\n✅ 添加成功: {url}")
    print(f"   平台: {platform}")
    print(f"   标签: {tags}")
    print(f"   优先级: {priority}")


def retry_failed():
    """重试失败任务"""
    db = DownloadDB()
    
    failed = [t for t in db.data["tasks"].values() if t["status"] == "failed"]
    
    if not failed:
        print("\n✅ 没有失败的任务")
        return
    
    print(f"\n🔄 重试 {len(failed)} 个失败任务...")
    
    for task in failed:
        task["status"] = "pending"
        task["retry_count"] = 0
        task["error"] = None
    
    db.save()
    print("✅ 已重置失败任务为待下载状态")


# ============== 主程序 ==============
def main():
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════════╗
║              批量下载管理器                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  使用方法:                                                    ║
║                                                              ║
║    python batch_downloader.py run          # 开始批量下载      ║
║    python batch_downloader.py import       # 从链接池导入      ║
║    python batch_downloader.py status       # 查看状态          ║
║    python batch_downloader.py add <url>    # 添加链接          ║
║    python batch_downloader.py retry       # 重试失败任务      ║
║    python batch_downloader.py clear       # 清空数据库        ║
║                                                              ║
║  示例:                                                        ║
║    python batch_downloader.py add "https://youtu.be/xxx"       ║
║    python batch_downloader.py add "https://youtu.be/xxx" luxury │║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "run":
        run_batch_download()
    
    elif command == "import":
        import_from_links_pool()
    
    elif command == "status":
        show_status()
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ 请提供URL")
            sys.exit(1)
        url = sys.argv[2]
        tags = sys.argv[3] if len(sys.argv) > 3 else "general"
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        add_link(url, tags, priority)
    
    elif command == "retry":
        retry_failed()
    
    elif command == "clear":
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)
            print("✅ 数据库已清空")
        else:
            print("✅ 数据库已经是空的")
    
    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
