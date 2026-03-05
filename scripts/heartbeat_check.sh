#!/bin/bash
# Daily heartbeat check - runs OpenClaw with heartbeat prompt
# Logs to memory/daily/YYYY-MM-DD.md

DATE=$(date +%Y-%m-%d)
LOG_DIR="/root/.openclaw/workspace/memory/daily"
LOG_FILE="$LOG_DIR/${DATE}.md"

mkdir -p "$LOG_DIR"

echo "## Heartbeat Check - $(date '+%Y-%m-%d %H:%M UTC')" >> "$LOG_FILE"
echo "Gateway status check..." >> "$LOG_FILE"

/usr/bin/openclaw gateway status 2>&1 | head -20 >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "✅ Heartbeat logged at $(date)"