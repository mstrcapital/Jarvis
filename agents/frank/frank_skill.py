#!/usr/bin/env python3
"""
Frank Skill Wrapper - 法律顾问专用技能调用
"""

import sys
import subprocess
import json

WORKSPACE = "/root/.openclaw/workspace"
BRIDGE = f"{WORKSPACE}/jarvis_skill_bridge.py"

SKILLS = {
    "help": "list",
    "search": "search",
    "web": "web_fetch",
    "telegram": "send_telegram",
    "legal": "search",  # 法律搜索
}

def main():
    if len(sys.argv) < 2:
        print("⚖️ Frank Skill Wrapper")
        print("用法: frank <skill> [params]")
        print(f"可用: {', '.join(SKILLS.keys())}")
        return
    
    skill = sys.argv[1].lower()
    if skill not in SKILLS:
        print(f"❌ 未知: {skill}")
        return
    
    actual = SKILLS[skill]
    params = {}
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[2])
    
    # 特殊处理legal搜索
    if skill == "legal":
        params = {"query": params.get("query", "SEC regulation crypto")}
    
    cmd = ["python3", BRIDGE, "call", actual]
    if params:
        cmd.append(json.dumps(params))
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    print(result.stdout or result.stderr)

if __name__ == "__main__":
    main()