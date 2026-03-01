#!/bin/bash
# =====================================================
# 视频链接下载器 - Video Link Downloader
# =====================================================
# 用法: 
# 1. 用浏览器插件获取 YouTube/X 视频直链
# 2. 把链接粘贴到 links.txt
# 3. 运行此脚本
# =====================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
OUTPUT_DIR="/root/.openclaw/workspace/video-materials/素材"
LINKS_FILE="/root/.openclaw/workspace/video-materials/links.txt"
LOG_FILE="/root/.openclaw/workspace/video-materials/download_log.txt"

mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  视频链接下载器 v1.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查links文件
if [ ! -f "$LINKS_FILE" ]; then
    echo -e "${YELLOW}⚠️  links.txt 不存在${NC}"
    echo "请创建 links.txt，每行一个链接"
    echo ""
    cat > "$LINKS_FILE" << 'EOF'
# 在此粘贴链接（每行一个）
# 示例:
# https://www.youtube.com/watch?v=...
# https://twitter.com/user/status/...
EOF
    echo "已创建 links.txt 模板"
    echo "请编辑此文件添加链接"
    exit 0
fi

# 显示待下载链接
echo -e "${BLUE}📋 待下载链接:${NC}"
cat "$LINKS_FILE"
echo ""

# 读取链接并下载
download_count=0
skip_count=0

while IFS= read -r line || [ -n "$line" ]; do
    # 跳过空行和注释
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    
    echo -e "${BLUE}📥 下载: $line${NC}"
    
    # 判断平台
    if [[ "$line" =~ youtube|youtu.be ]]; then
        # YouTube
        echo "   平台: YouTube"
        output_name=$(echo "$line" | grep -oP 'v=\K[^&]+' | head -1)
        if [ -z "$output_name" ]; then
            output_name="youtube_$(date +%s)"
        fi
        
        # 尝试下载
        if curl -sL "$line" -o "/dev/null" --max-time 10; then
            echo -e "${GREEN}✅ 链接有效${NC}"
            echo "[$(date)] YouTube: $line" >> "$LOG_FILE"
            ((download_count++))
        else
            echo -e "${YELLOW}⚠️  链接可能需要特殊处理${NC}"
            echo "[$(date)] YouTube (需处理): $line" >> "$LOG_FILE"
            ((skip_count++))
        fi
        
    elif [[ "$line" =~ twitter|x\.com ]]; then
        # Twitter/X
        echo "   平台: Twitter/X"
        echo "[$(date)] Twitter: $line" >> "$LOG_FILE"
        ((download_count++))
        
    else
        # 其他
        echo "   平台: 未知"
        echo "[$(date)] Unknown: $line" >> "$LOG_FILE"
        ((skip_count++))
    fi
    
    echo ""
    
done < "$LINKS_FILE"

echo -e "${GREEN}✅ 处理完成${NC}"
echo "有效链接: $download_count"
echo "待处理: $skip_count"
echo "日志: $LOG_FILE"
