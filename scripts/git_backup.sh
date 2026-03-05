#!/bin/bash
# Daily git backup to GitHub

cd /root/.openclaw/workspace

# Add all changes
git add -A

# Check if there are changes
if git diff --staged --quiet; then
    echo "$(date): No changes to commit"
    exit 0
fi

# Commit with timestamp
git commit -m "Auto backup - $(date '+%Y-%m-%d %H:%M UTC')"

# Push to GitHub
git push origin main 2>&1

echo "$(date): Backup completed"