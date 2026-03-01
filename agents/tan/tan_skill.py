#!/usr/bin/env python3
"""
Tan Skill Wrapper - 量化策略专用技能调用
"""

import sys
import subprocess
import json

WORKSPACE = "/root/.openclaw/workspace"
BRIDGE = f"{WORKSPACE}/jarvis_skill_bridge.py"

SKILLS = {
    "help": "list",
    "analyze": "analyze_market",
    "stock": "stock_analysis",
    "macro": "global_macro",
    "search": "search",
    "telegram": "send_telegram",
}

def main():
    if len(sys.argv) < 2:
        print("🧮 Tan Skill Wrapper")
        print("用法: tan <skill> [params]")
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
    
    cmd = ["python3", BRIDGE, "call", actual]
    if params:
        cmd.append(json.dumps(params))
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    print(result.stdout or result.stderr)

if __name__ == "__main__":
    main()