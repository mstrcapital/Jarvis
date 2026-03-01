#!/usr/bin/env python3
"""
集成自 OpenBrowserClaw 的工具
- update_memory: 直接更新记忆
- execute_js: JavaScript 执行
- create_task: 创建定时任务
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"

def update_memory(content: str, agent: str = None) -> str:
    """
    更新记忆 - 类似 OpenBrowserClaw 的 update_memory
    用法: python3 tools.py update_memory "内容" [agent]
    """
    if agent:
        # 更新指定 agent 的记忆
        mem_file = f"{WORKSPACE}/agents/{agent}/memory/CLAUDE.md"
    else:
        # 更新主记忆
        mem_file = f"{WORKSPACE}/MEMORY.md"
    
    try:
        with open(mem_file, 'a') as f:
            f.write(f"\n\n---\n# {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{content}\n")
        return f"✅ 记忆已更新: {mem_file}"
    except Exception as e:
        return f"❌ 错误: {e}"

def execute_js(code: str) -> str:
    """
    执行 JavaScript 代码
    用法: python3 tools.py js "console.log('hello')"
    """
    try:
        result = subprocess.run(
            ["node", "-e", code],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return f"✅ 结果:\n{result.stdout}"
        else:
            return f"❌ 错误:\n{result.stderr}"
    except FileNotFoundError:
        return "❌ Node.js 未安装"
    except Exception as e:
        return f"❌ 错误: {e}"

def create_task(schedule: str, prompt: str, name: str = None) -> str:
    """
    创建定时任务 - 类似 OpenBrowserClaw 的 create_task
    用法: python3 tools.py task "0 9 * * 1-5" "运行分析"
    """
    if not name:
        name = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    task_file = f"{WORKSPACE}/jarvis_memory/tasks/{name}.sh"
    os.makedirs(f"{WORKSPACE}/jarvis_memory/tasks", exist_ok=True)
    
    # 创建任务脚本
    with open(task_file, 'w') as f:
        f.write(f"""#!/bin/bash
# 任务: {name}
# 计划: {schedule}
# 创建时间: {datetime.now()}
# 执行内容: {prompt}

echo "执行任务: {name}"
echo "{prompt}"
# 在这里添加实际的执行命令
""")
    
    # 添加到 crontab
    cron_cmd = f"0 13 * * 1-5 cd {WORKSPACE} && bash {task_file} >> {WORKSPACE}/jarvis_memory/tasks/{name}.log 2>&1"
    
    # 读取现有 crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current = result.stdout if result.returncode == 0 else ""
    
    # 添加新任务
    new_cron = f"{current}\n# {name}\n{cron_cmd}"
    subprocess.run(["crontab", "-"], input=new_cron, text=True)
    
    return f"✅ 任务已创建: {name}\n计划: {schedule}\n脚本: {task_file}"

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
🔧 Jarvis 工具集 (来自 OpenBrowserClaw)

用法:
    python3 tools.py memory "内容" [agent]
    python3 tools.py js "JavaScript代码"
    python3 tools.py task "cron表达式" "任务描述" [任务名]

示例:
    python3 tools.py memory "今天学会了新技能" ken
    python3 tools.py js "console.log(1+1)"
    python3 tools.py task "0 9 * * 1-5" "运行每日报告" daily_report
        """)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "memory":
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        agent = sys.argv[3] if len(sys.argv) > 3 else None
        print(update_memory(content, agent))
    
    elif cmd == "js":
        code = sys.argv[2] if len(sys.argv) > 2 else ""
        print(execute_js(code))
    
    elif cmd == "task":
        schedule = sys.argv[2] if len(sys.argv) > 2 else ""
        prompt = sys.argv[3] if len(sys.argv) > 3 else ""
        name = sys.argv[4] if len(sys.argv) > 4 else None
        print(create_task(schedule, prompt, name))
    
    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == "__main__":
    main()