#!/usr/bin/env python3
"""
Ken Skill Wrapper - 让Ken快速调用Jarvis的技能
"""

import sys
import subprocess
import json
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
BRIDGE = f"{WORKSPACE}/jarvis_skill_bridge.py"

# Ken常用的技能
KEN_SKILLS = {
    "market": "analyze_market",
    "polymarket": "analyze_market", 
    "bitcoin": "analyze_market",
    "macro": "global_macro",
    "search": "search",
    "weather": "weather",
    "help": "help",
}

def main():
    if len(sys.argv) < 2:
        print("🧑‍💼 Ken Skill Wrapper")
        print("用法: ken <skill> [params]")
        print(f"可用技能: {', '.join(KEN_SKILLS.keys())}")
        return
    
    skill = sys.argv[1].lower()
    
    if skill not in KEN_SKILLS:
        print(f"❌ 未知技能: {skill}")
        print(f"可用: {', '.join(KEN_SKILLS.keys())}")
        return
    
    # 获取实际skill名称
    actual_skill = KEN_SKILLS[skill]
    
    # 构建参数
    params = {}
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[2])
    
    # 调用bridge
    cmd = ["python3", BRIDGE, "call", actual_skill]
    if params:
        cmd.append(json.dumps(params))
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    print(result.stdout or result.stderr)

if __name__ == "__main__":
    main()