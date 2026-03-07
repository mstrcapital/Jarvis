#!/usr/bin/env python3
"""
Alex (CTO) - 每日系统健康检查 + Telegram告警
每天自动运行，检查系统稳定性和安全性
"""

import os
import subprocess
import json
import requests
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"

# Telegram 配置
TELEGRAM_TOKEN = "8382988751:AAG-Xlis9OoqqC93M1xCufl2FEa6kh7JlbI"
TELEGRAM_CHAT_ID = "8591571345"

def send_alert(message):
    """发送Telegram告警"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🔴 *Alex 系统告警*\n\n{message}",
            "parse_mode": "Markdown"
        }, timeout=10)
        print("✅ 告警已发送")
    except Exception as e:
        print(f"❌ 告警发送失败: {e}")

def check_resources():
    """检查系统资源"""
    issues = []
    
    # 内存
    mem = subprocess.run(["free", "-m"], capture_output=True, text=True)
    lines = mem.stdout.strip().split("\n")
    if len(lines) >= 2:
        parts = lines[1].split()
        total = int(parts[1])
        used = int(parts[2])
        free = int(parts[3])
        if free < 500:
            issues.append(f"⚠️ 内存不足: {free}MB 空闲")
    
    # 磁盘
    disk = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    parts = disk.stdout.strip().split("\n")[1].split()
    usage = int(parts[4].replace("%", ""))
    if usage > 85:
        issues.append(f"⚠️ 磁盘空间: {usage}% 已使用")
    
    return issues

def check_processes():
    """检查关键进程"""
    issues = []
    
    # 检查必需的进程
    required = ["telegram_bot", "openclaw", "cron"]
    running = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    
    for proc in required:
        if proc.lower() not in running.stdout.lower():
            issues.append(f"❌ 进程缺失: {proc}")
    
    # 检查失败的进程
    failed = subprocess.run(["systemctl", "--failed"], capture_output=True, text=True)
    if "failed" in failed.stdout.lower():
        issues.append(f"⚠️ 有失败的systemd服务")
    
    return issues

def check_security():
    """检查安全"""
    issues = []
    
    # SSH 失败登录
    ssh = subprocess.run(["grep", "Invalid user", "/var/log/auth.log"], 
                         capture_output=True, text=True, timeout=5)
    if ssh.returncode == 0:
        count = len(ssh.stdout.strip().split("\n"))
        if count > 10:
            issues.append(f"⚠️ SSH暴力破解尝试: {count}次")
    
    # 检查开放端口
    ports = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
    dangerous = ["23", "21", "23", "139", "445"]
    for port in dangerous:
        if f":{port}" in ports.stdout:
            issues.append(f"⚠️ 危险端口开放: {port}")
    
    return issues

def check_crons():
    """检查定时任务"""
    issues = []
    
    # 检查cron是否运行
    cron = subprocess.run(["systemctl", "is-active", "cron"], capture_output=True, text=True)
    if "inactive" in cron.stdout:
        issues.append(f"❌ Cron未运行")
    
    return issues

def check_workspace():
    """检查workspace错误"""
    issues = []
    
    # 检查最近修改的文件是否有错误
    log_files = [
        "agents/ken/cron.log",
        "agents/cio/cron.log",
        "jarvis_memory/reports/cron.log"
    ]
    
    for log in log_files:
        path = f"{WORKSPACE}/{log}"
        if Path(path).exists():
            with open(path) as f:
                content = f.read()
                if "Error" in content or "error" in content:
                    issues.append(f"⚠️ 日志错误: {log}")
    
    return issues

def check_apis():
    """检查API连通性"""
    issues = []
    import yfinance as yf
    import ccxt
    
    # Stock API (yfinance)
    try:
        spy = yf.download('SPY', period='1d', progress=False, timeout=10)
        if spy.empty:
            issues.append("❌ yfinance股票API: 无数据")
        else:
            print("  ✅ yfinance股票API: SPY $" + str(spy['Close'].iloc[-1].values[0])[:6])
    except Exception as e:
        issues.append(f"❌ yfinance股票API: {str(e)[:30]}")
    
    # Crypto APIs
    crypto_exchanges = [
        ("kraken", "BTC/USDT"),
        ("coinbase", "BTC/USDT"),
    ]
    for ex, pair in crypto_exchanges:
        try:
            exchange = getattr(ccxt, ex)()
            ticker = exchange.fetch_ticker(pair)
            price = ticker.get('last', 0)
            if price > 0:
                print(f"  ✅ {ex}: BTC ${price}")
            else:
                issues.append(f"❌ {ex}: 无价格数据")
        except Exception as e:
            issues.append(f"❌ {ex}: {str(e)[:25]}")
    
    # Polymarket
    try:
        r = requests.get('https://gamma-api.polymarket.com/markets', timeout=10)
        if r.status_code == 200:
            print("  ✅ Polymarket Gamma API")
        else:
            issues.append(f"❌ Polymarket: {r.status_code}")
    except Exception as e:
        issues.append(f"❌ Polymarket: {str(e)[:25]}")
    
    # Deribit Options (volatility proxy)
    try:
        r = requests.get('https://www.deribit.com/api/v2/public/get_book_summary_by_currency',
                        params={'currency': 'BTC', 'kind': 'option', 'count': 5}, timeout=10)
        if r.status_code == 200:
            print("  ✅ Deribit Options API")
        else:
            issues.append(f"❌ Deribit: {r.status_code}")
    except Exception as e:
        issues.append(f"❌ Deribit: {str(e)[:25]}")
    
    return issues

def main():
    print(f"🔍 Alex System Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    all_issues = []
    
    print("\n📊 资源检查...")
    issues = check_resources()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n🔄 进程检查...")
    issues = check_processes()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n🔒 安全检查...")
    issues = check_security()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n⏰ Cron检查...")
    issues = check_crons()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n📁 工作区检查...")
    issues = check_workspace()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n🌐 API检查...")
    issues = check_apis()
    all_issues.extend(issues)
    for i in issues:
        print(f"  {i}")
    
    print("\n" + "=" * 50)
    if all_issues:
        print(f"❌ 发现 {len(all_issues)} 个问题:")
        for i in all_issues:
            print(f"  - {i}")
        
        # 发送 Telegram 告警
        alert_msg = "\n".join([f"- {i}" for i in all_issues])
        send_alert(alert_msg)
    else:
        print("✅ 系统运行正常")
    
    return all_issues

if __name__ == "__main__":
    main()