#!/bin/bash
# GitClaw Backup Setup - 自动备份 OpenClaw workspace 到私有 GitHub 仓库
# 用法: ./gitclaw-setup.sh <github-repo-url> <pat-token>

set -e

REPO_URL="$1"
PAT="$2"
WORKSPACE="/root/.openclaw/workspace"
GITIGNORE_FILE="$WORKSPACE/.gitignore"

if [ -z "$REPO_URL" ] || [ -z "$PAT" ]; then
    echo "用法: $0 <github-repo-url> <pat-token>"
    echo "示例: $0 https://github.com/yourusername/backup-repo ghp_xxxxxxxxxxxx"
    exit 1
fi

echo "=== GitClaw 备份设置 ==="

cd "$WORKSPACE"

# 1. 初始化 Git (如果还没有)
if [ ! -d ".git" ]; then
    echo "[1/5] 初始化 Git 仓库..."
    git init
    git config user.email "jarvis@openclaw.local"
    git config user.name "Jarvis Backup"
else
    echo "[1/5] Git 已初始化"
fi

# 2. 创建 .gitignore 排除敏感文件
echo "[2/5] 创建 .gitignore..."
cat > "$GITIGNORE_FILE" << 'EOF'
# 敏感文件
.env
.env.*
*.pem
*.key
tokens/
credentials/
*.log

# 临时文件
tmp/
temp/
.cache/
node_modules/ (可选)

# 系统文件
.DS_Store
Thumbs.db
*.swp
*~

# OpenClaw 特定
agents/*/memory/
agents/*/session/
*.session
cron.log
EOF

# 3. 添加 remote
echo "[3/5] 配置远程仓库..."
# 移除旧的 remote (如果有)
git remote remove origin 2>/dev/null || true

# 使用 PAT 认证
# 将 https://github.com/user/repo 转换为 https://oauth2:PAT@github.com/user/repo
REMOTE_URL="${REPO_URL/https:\/\/github.com\//https://oauth2:${PAT}@github.com/}"
git remote add origin "$REMOTE_URL"

# 4. 首次提交
echo "[4/5] 创建初始提交..."
git add .
git commit -m "Initial backup - $(date '+%Y-%m-%d %H:%M')"

# 5. 推送到远程
echo "[5/5] 推送到远程仓库..."
git branch -M main
git push -u origin main --force

echo ""
echo "✅ GitClaw 备份设置完成!"
echo "📁 仓库: $REPO_URL"
echo ""
echo "后续备份命令:"
echo "  git add ."
echo "  git commit -m 'Update: $(date)'"
echo "  git push"