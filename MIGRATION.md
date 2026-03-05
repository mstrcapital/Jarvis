# AWS → Aliyun 迁移 Checklist

## 当前状态
- GitHub 仓库: https://github.com/mstrcapital/Jarvis (private)
- 代码已全部备份 ✅

---

## 在 Aliyun 上执行

### 1. 安装环境
```bash
# 安装 Node.js 18+ (如果还没)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 OpenClaw
npm install -g openclaw

# 安装 Python 依赖 (如果 agents 需要)
sudo apt-get install -y python3 python3-pip git
```

### 2. 克隆代码
```bash
git clone https://github.com/mstrcapital/Jarvis.git /root/.openclaw/workspace
```

### 3. 恢复配置
```bash
# 从 AWS 复制敏感配置
# 方式 A: 手动复制
scp ubuntu@<AWS-IP>:/root/.openclaw/openclaw.json /root/.openclaw/

# 方式 B: 如果用同一套配置，直接用仓库里的
cp /root/.openclaw/workspace/config/openclaw.json /root/.openclaw/openclaw.json
```

### 4. 安装 skills 依赖
```bash
cd /root/.openclaw/workspace
npm install
```

### 5. 启动
```bash
sudo openclaw gateway start
sudo openclaw gateway status
```

### 6. 配置 Cron
```bash
# 复制 crontab
crontab -l  # 查看当前 crontab
# 在新机器上重新添加 cron jobs
```

---

## 验证清单
- [ ] OpenClaw 启动成功
- [ ] Telegram 连接正常
- [ ] 所有 sub-agents 可用
- [ ] Cron jobs 运行正常
- [ ] 每日备份自动运行

---

## 注意事项
1. **Telegram Webhook** - 如果 IP 变了，需要更新 bot webhook
2. **API Keys** - 确认各 API 服务的 IP 白名单
3. **域名** - 如果有自定义域名，更新 DNS
4. **安全组** - 确认 Aliyun 安全组开放必要端口