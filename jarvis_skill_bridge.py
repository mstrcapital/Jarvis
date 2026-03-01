#!/usr/bin/env python3
"""
Jarvis Skill Bridge - 让子Agent调用主Agent技能
通过 sessions_send 调用此脚本

用法:
    python3 jarvis_skill_bridge.py list                           # 列出技能
    python3 jarvis_skill_bridge.py call <skill> [params]          # 调用技能
    python3 jarvis_skill_bridge.py help <skill>                   # 查看技能详情
"""

import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
SKILLS_DIR = f"{WORKSPACE}/skills"

# 可用技能映射
SKILL_MAP = {
    # 帮助
    "help": {"desc": "列出所有技能", "script": "internal"},
    "list": {"desc": "列出所有技能", "script": "internal"},
    
    # 分析类
    "analyze_market": {
        "desc": "Polymarket市场数据分析",
        "script": "agents/ken/market_scraper.py",
        "params": "无"
    },
    "global_macro": {
        "desc": "全球宏观经济报告",
        "script": "agents/cio/report.py", 
        "params": "无"
    },
    "stock_analysis": {
        "desc": "股票分析 (daily_stock_analysis)",
        "script": "daily_stock_analysis/main.py",
        "params": "stock_code"
    },
    "cio_report": {
        "desc": "CIO投资报告",
        "script": "agents/cio/report.py",
        "params": "无"
    },
    
    # 搜索类
    "search": {
        "desc": "网络搜索 (Tavily)",
        "script": "skills/tavily-search",
        "params": "query"
    },
    "knowledge": {
        "desc": "知识库搜索",
        "script": "skills/knowledge-base",
        "params": "query"
    },
    
    # 记忆类
    "memory": {
        "desc": "记忆操作 (读取/写入)",
        "script": "skills/jarvis-memory-architecture",
        "params": "action, key, value"
    },
    "longterm_memory": {
        "desc": "长期记忆管理",
        "script": "skills/elite-longterm-memory",
        "params": "action"
    },
    
    # 技能类
    "self_evolve": {
        "desc": "自我进化",
        "script": "skills/self-evolve",
        "params": "无"
    },
    "agent_builder": {
        "desc": "Agent构建器",
        "script": "skills/agent-builder",
        "params": "agent_name, role"
    },
    "weather": {
        "desc": "天气查询",
        "script": "skills/weather",
        "params": "location"
    },
    
    # 实用工具
    "send_telegram": {
        "desc": "发送Telegram消息",
        "script": "internal",
        "params": "message, chat_id"
    },
    "web_fetch": {
        "desc": "获取网页内容",
        "script": "internal",
        "params": "url"
    },
    
    # Polymarket 相关
    "pm_update": {
        "desc": "更新Polymarket数据",
        "script": "polymarket_monitor/update_v1_2.py",
        "params": "无"
    },
    "pm_dashboard": {
        "desc": "Polymarket仪表板",
        "script": "polymarket_monitor/ascii_dashboard.py",
        "params": "无"
    },
    "pm_visualization": {
        "desc": "Polymarket可视化",
        "script": "polymarket_monitor/visualization.py",
        "params": "无"
    },
    
    # COO 功能
    "team_status": {
        "desc": "团队状态报告",
        "script": "internal",
        "params": "无"
    },
    "weekly_report": {
        "desc": "COO周报",
        "script": "jarvis_memory/weekly_report_telegram.py",
        "params": "无"
    },
    
    # 来自 OpenBrowserClaw 的集成
    "update_memory": {
        "desc": "直接更新记忆 (OpenBrowserClaw风格)",
        "script": "openbrowserclaw/tools.py",
        "params": "content, agent"
    },
    "execute_js": {
        "desc": "执行JavaScript代码",
        "script": "openbrowserclaw/tools.py",
        "params": "code"
    },
    "create_task": {
        "desc": "创建定时任务",
        "script": "openbrowserclaw/tools.py",
        "params": "schedule, prompt, name"
    },
}

def call_skill(skill_name: str, params: dict) -> str:
    """调用指定技能"""
    
    # 帮助/列表
    if skill_name in ["help", "list"]:
        return list_skills()
    
    if skill_name not in SKILL_MAP:
        return f"❌ 未知技能: {skill_name}\n可用: {', '.join(SKILL_MAP.keys())}\n\n输入 'list' 查看所有技能"
    
    skill_info = SKILL_MAP[skill_name]
    script_path = skill_info["script"]
    
    # 内部技能 (直接执行)
    if script_path == "internal":
        return call_internal_skill(skill_name, params)
    
    full_path = f"{WORKSPACE}/{script_path}"
    
    # 检查脚本是否存在
    if not Path(full_path).exists():
        return f"❌ 脚本不存在: {full_path}"
    
    try:
        # 根据技能执行
        if skill_name == "analyze_market":
            result = subprocess.run(
                ["python3", full_path],
                capture_output=True, text=True, timeout=60,
                cwd=WORKSPACE
            )
            output = result.stdout if result.stdout else result.stderr
            return f"📊 市场分析:\n{output[:800]}"
        
        elif skill_name == "global_macro" or skill_name == "cio_report":
            result = subprocess.run(
                ["python3", full_path],
                capture_output=True, text=True, timeout=60,
                cwd=f"{WORKSPACE}/agents/cio"
            )
            output = result.stdout if result.stdout else result.stderr
            return f"🌍 宏观报告:\n{output[:800]}"
        
        elif skill_name == "stock_analysis":
            stock = params.get("stock_code", "AAPL")
            result = subprocess.run(
                ["python3", full_path, "--stocks", stock, "--dry-run"],
                capture_output=True, text=True, timeout=60,
                cwd=WORKSPACE
            )
            return f"📈 股票分析 {stock}:\n{result.stdout[:500]}" if result.stdout else result.stderr[:300]
        
        elif skill_name == "weather":
            location = params.get("location", "Beijing")
            result = subprocess.run(
                ["curl", f"wttr.in/{location}?format=j1"],
                capture_output=True, text=True, timeout=10
            )
            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    current = data.get("current_condition", [{}])[0]
                    return f"🌤️ {location}:\n温度: {current.get('temp_C', 'N/A')}°C\n天气: {current.get('weatherDesc', 'N/A')}"
                except:
                    return f"🌤️ {location}: {result.stdout[:200]}"
            return f"❌ 无法获取天气"
        
        elif skill_name == "search":
            query = params.get("query", "")
            if not query:
                return "❌ 需要 query 参数"
            return f"🔍 搜索: {query}\n(需要 Tavily API key)"
        
        # Polymarket
        elif skill_name == "pm_update":
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/polymarket_monitor/update_v1_2.py"],
                capture_output=True, text=True, timeout=60, cwd=WORKSPACE
            )
            return f"📊 Polymarket更新:\n{result.stdout[:500]}" if result.stdout else result.stderr[:300]
        
        elif skill_name == "pm_dashboard":
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/polymarket_monitor/ascii_dashboard.py"],
                capture_output=True, text=True, timeout=30, cwd=WORKSPACE
            )
            return f"📊 Polymarket仪表板:\n{result.stdout[:800]}" if result.stdout else result.stderr[:300]
        
        # COO
        elif skill_name == "team_status":
            agents = ["alex", "karl", "ken", "gerri", "frank", "tan", "mustafa", "xiaomei", "pepe"]
            status = []
            for a in agents:
                path = f"{WORKSPACE}/agents/{a}"
                if Path(path).exists():
                    status.append(f"✅ {a}")
                else:
                    status.append(f"❌ {a}")
            return "👥 团队状态:\n" + "\n".join(status)
        
        elif skill_name == "weekly_report":
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/jarvis_memory/weekly_report_telegram.py"],
                capture_output=True, text=True, timeout=60, cwd=WORKSPACE
            )
            return f"📅 周报:\n{result.stdout[:300]}" if result.stdout else result.stderr[:300]
        
        # OpenBrowserClaw 集成
        elif skill_name == "update_memory":
            content = params.get("content", "")
            agent = params.get("agent")
            if not content:
                return "❌ 需要 content 参数"
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/openbrowserclaw/tools.py", "memory", content, agent or ""],
                capture_output=True, text=True, timeout=10, cwd=WORKSPACE
            )
            return result.stdout or result.stderr
        
        elif skill_name == "execute_js":
            code = params.get("code", "")
            if not code:
                return "❌ 需要 code 参数"
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/openbrowserclaw/tools.py", "js", code],
                capture_output=True, text=True, timeout=10, cwd=WORKSPACE
            )
            return result.stdout or result.stderr
        
        elif skill_name == "create_task":
            schedule = params.get("schedule", "")
            prompt = params.get("prompt", "")
            name = params.get("name")
            if not schedule or not prompt:
                return "❌ 需要 schedule 和 prompt 参数"
            result = subprocess.run(
                ["python3", f"{WORKSPACE}/openbrowserclaw/tools.py", "task", schedule, prompt, name or ""],
                capture_output=True, text=True, timeout=10, cwd=WORKSPACE
            )
            return result.stdout or result.stderr
        
        else:
            return f"⚠️ 技能 {skill_name} 实现中...\n{skill_info['desc']}"
            
    except subprocess.TimeoutExpired:
        return f"❌ 执行超时"
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def call_internal_skill(skill_name: str, params: dict) -> str:
    """内部技能直接执行"""
    import requests
    
    if skill_name == "send_telegram":
        message = params.get("message", "")
        chat_id = params.get("chat_id", "8591571345")
        token = params.get("token", "8382988751:AAG-Xlis9OoqqC93M1xCufl2FEa6kh7JlbI")
        
        if not message:
            return "❌ 需要 message 参数"
        
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": message},
                timeout=10
            )
            return "✅ 消息已发送" if resp.status_code == 200 else f"❌ 发送失败: {resp.status_code}"
        except Exception as e:
            return f"❌ 错误: {e}"
    
    elif skill_name == "web_fetch":
        url = params.get("url", "")
        if not url:
            return "❌ 需要 url 参数"
        
        try:
            resp = requests.get(url, timeout=15)
            return f"🌐 {url}\n状态: {resp.status_code}\n内容: {resp.text[:500]}"
        except Exception as e:
            return f"❌ 错误: {e}"
    
    elif skill_name == "pm_update":
        result = subprocess.run(
            ["python3", f"{WORKSPACE}/polymarket_monitor/update_v1_2.py"],
            capture_output=True, text=True, timeout=60, cwd=WORKSPACE
        )
        return f"📊 Polymarket更新:\n{result.stdout[:500]}" if result.stdout else result.stderr[:300]
    
    elif skill_name == "pm_dashboard":
        result = subprocess.run(
            ["python3", f"{WORKSPACE}/polymarket_monitor/ascii_dashboard.py"],
            capture_output=True, text=True, timeout=30, cwd=WORKSPACE
        )
        return f"📊 Polymarket仪表板:\n{result.stdout[:800]}" if result.stdout else result.stderr[:300]
    
    elif skill_name == "team_status":
        agents = ["alex", "karl", "ken", "gerri", "frank", "tan", "mustafa", "xiaomei", "pepe"]
        status = []
        for a in agents:
            path = f"{WORKSPACE}/agents/{a}"
            if Path(path).exists():
                status.append(f"✅ {a}")
            else:
                status.append(f"❌ {a}")
        return "👥 团队状态:\n" + "\n".join(status)
    
    elif skill_name == "weekly_report":
        result = subprocess.run(
            ["python3", f"{WORKSPACE}/jarvis_memory/weekly_report_telegram.py"],
            capture_output=True, text=True, timeout=60, cwd=WORKSPACE
        )
        return f"📅 周报:\n{result.stdout[:300]}" if result.stdout else result.stderr[:300]
    
    return "❌ 未知内部技能"

def list_skills():
    """列出所有可用技能"""
    return "📦 可用技能:\n" + "\n".join(f"- {k}" for k in SKILL_MAP.keys())

def main():
    # 解析参数
    if len(sys.argv) < 2:
        print(list_skills())
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list":
        print(list_skills())
    
    elif command == "call":
        skill_name = sys.argv[2] if len(sys.argv) > 2 else ""
        params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        print(call_skill(skill_name, params))
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()