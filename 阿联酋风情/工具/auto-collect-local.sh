#!/bin/bash
# =====================================================
# 视频号素材自动收集器 - 本地版
# Video Materials Auto Collector - Local Version
# =====================================================
# 系统要求: macOS / Windows (WSL) / Linux
# 需安装: Homebrew (macOS) 或 Python 3
# =====================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  视频号素材自动收集器 v1.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 配置
OUTPUT_DIR="$HOME/Desktop/迪拜素材"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUTPUT_DIR/收集日志_$TIMESTAMP.txt"

mkdir -p "$OUTPUT_DIR/迪拜-阿布扎比"
mkdir -p "$OUTPUT_DIR/土豪日常"
mkdir -p "$OUTPUT_DIR/华人群体"
mkdir -p "$OUTPUT_DIR/生活定居"
mkdir -p "$OUTPUT_DIR/高清街拍"

echo "📁 素材保存目录: $OUTPUT_DIR"
echo "📝 日志文件: $LOG_FILE"
echo ""

# 检查工具
check_tool() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅${NC} $1 已安装"
        return 0
    else
        echo -e "${YELLOW}⚠️${NC} $1 未安装"
        return 1
    fi
}

echo "🔍 检查工具..."
echo ""
check_tool "yt-dlp" || echo "  安装命令: pip install yt-dlp"
echo ""

# 安装 yt-dlp
install_ytdlp() {
    echo -e "${BLUE}📦 安装 yt-dlp...${NC}"
    pip install yt-dlp
    echo -e "${GREEN}✅ yt-dlp 安装完成${NC}"
}

# 收集函数
collect_video() {
    local url=$1
    local category=$2
    local desc=$3
    
    echo -e "${BLUE}📥 下载: $desc${NC}"
    echo "   链接: $url"
    echo "   分类: $category"
    
    if command -v yt-dlp &> /dev/null; then
        yt-dlp -o "$OUTPUT_DIR/$category/%(title)s_$TIMESTAMP.%(ext)s" \
            --format best \
            --no-check-certificate \
            "$url" 2>&1 | grep -E "(\[download\]|ERROR)" || true
        
        echo -e "${GREEN}✅ 完成${NC}"
    else
        echo -e "${YELLOW}⚠️ yt-dlp 未安装，跳过下载${NC}"
    fi
    
    echo "" | tee -a "$LOG_FILE"
}

# 主收集任务
echo -e "${BLUE}🚀 开始收集素材...${NC}"
echo "" | tee -a "$LOG_FILE"
echo "⏰ 开始时间: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ============================================
# 任务1: 迪拜城市风光
# ============================================
echo -e "${YELLOW}📍 任务1: 迪拜城市风光${NC}" | tee -a "$LOG_FILE"

collect_video "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "迪拜-阿布扎比" "示例视频-替换为实际链接"

# ============================================
# 任务2: 奢华生活
# ============================================
echo -e "${YELLOW}💎 任务2: 奢华生活${NC}" | tee -a "$LOG_FILE"

collect_video "" "土豪日常" "超跑视频"

# ============================================
# 任务3: 华人内容
# ============================================
echo -e "${YELLOW}🇨🇳 任务3: 华人内容${NC}" | tee -a "$LOG_FILE"

collect_video "" "华人群体" "华人故事"

# ============================================
# 任务4: 生活攻略
# ============================================
echo -e "${YELLOW}📚 任务4: 生活攻略${NC}" | tee -a "$LOG_FILE"

collect_video "" "生活定居" "签证攻略"

# ============================================
# 任务5: 高清街拍
# ============================================
echo -e "${YELLOW}📸 任务5: 高清街拍${NC}" | tee -a "$LOG_FILE"

collect_video "" "高清街拍" "城市街拍"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  收集完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "⏰ 结束时间: $(date)" | tee -a "$LOG_FILE"
echo ""
echo -e "${YELLOW}📋 下一步操作:${NC}"
echo "1. 检查下载的文件"
echo "2. 确认版权状态"
echo "3. 整理后上传到素材库"
echo ""
