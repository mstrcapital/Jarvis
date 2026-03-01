#!/bin/bash

# =====================================================
# 视频号素材收集工具包 - Video Materials Collection Kit
# =====================================================
# 支持平台: Instagram, TikTok, YouTube, Twitter/X
# 系统: Linux/macOS/Windows (WSL)
# =====================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 输出函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =====================================================
# 配置区域 - 修改这里的路径
# =====================================================

# 主素材目录
MATERIALS_DIR="/root/.openclaw/workspace/video-materials/素材"

# 视频保存目录
VIDEO_DIR="$MATERIALS_DIR/视频"

# 图片保存目录
IMAGE_DIR="$MATERIALS_DIR/图片"

# 日志目录
LOG_DIR="$MATERIALS_DIR/日志"

# 下载时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# =====================================================
# 工具函数
# =====================================================

# 创建目录结构
setup_directories() {
    log_info "创建目录结构..."
    mkdir -p "$VIDEO_DIR"
    mkdir -p "$IMAGE_DIR"
    mkdir -p "$LOG_DIR"
    mkdir -p "$MATERIALS_DIR/迪拜-阿布扎比"
    mkdir -p "$MATERIALS_DIR/土豪日常"
    mkdir -p "$MATERIALS_DIR/华人群体"
    mkdir -p "$MATERIALS_DIR/生活定居"
    mkdir -p "$MATERIALS_DIR/高清街拍"
    mkdir -p "$MATERIALS_DIR/已发布"
    log_success "目录创建完成"
}

# 下载Instagram帖子（需配合4K Stogram）
download_instagram() {
    local url=$1
    local category=$2
    
    log_info "下载Instagram: $url"
    log_info "分类: $category"
    
    # 这里需要手动使用4K Stogram或其他工具
    # 推荐命令（在4K Stogram中）：
    # 1. 打开4K Stogram
    # 2. 粘贴URL
    # 3. 选择保存目录: $MATERIALS_DIR/$category/
    
    echo "请手动使用以下工具:"
    echo "1. 4K Stogram: https://www.4kdownload.com/products/product-stogram"
    echo "2. Instagram Downloader Chrome扩展"
}

# 下载TikTok视频（使用ssstik.io）
download_tiktok() {
    local url=$1
    local category=$2
    
    log_info "下载TikTok: $url"
    log_info "分类: $category"
    
    echo "请使用以下工具之一:"
    echo "1. SSSTik: https://ssstik.io"
    echo "2. TikMate: https://www.tikmate.io"
    echo "3. 浏览器扩展: TikTok Video Downloader"
}

# 下载YouTube视频
download_youtube() {
    local url=$1
    local category=$2
    
    log_info "下载YouTube: $url"
    log_info "分类: $category"
    
    echo "请使用以下工具:"
    echo "1. 4K Video Downloader: https://www.4kdownload.com/products/video-downloader"
    echo "2. yt-dlp (命令行): pip install yt-dlp"
    echo "   使用命令: yt-dlp -o '$MATERIALS_DIR/$category/%(title)s.%(ext)s' $url"
}

# 下载Twitter/X视频
download_twitter() {
    local url=$1
    local category=$2
    
    log_info "下载Twitter: $url"
    log_info "分类: $category"
    
    echo "请使用以下工具:"
    echo "1. Twitter Video Downloader: https://twdownloader.com/"
    echo "2. SSSTwitter: https://ssstwitter.com/"
    echo "3. 4K Video Downloader也支持Twitter"
}

# 批量下载YouTube Shorts
batch_download_shorts() {
    local playlist_url=$1
    local category=$2
    
    log_info "批量下载YouTube Shorts: $playlist_url"
    
    if command -v yt-dlp &> /dev/null; then
        yt-dlp --cookies-from-browser chrome \
            -o "$MATERIALS_DIR/$category/%(title)s.%(ext)s" \
            --format best \
            "$playlist_url"
        log_success "下载完成"
    else
        log_warning "未安装yt-dlp，请先安装: pip install yt-dlp"
    fi
}

# 重命名文件（统一格式）
rename_files() {
    local category=$1
    log_info "重命名文件: $category"
    
    # 查找并重命名
    find "$MATERIALS_DIR/$category" -type f \( -name "*.mp4" -o -name "*.jpg" -o -name "*.png" \) | while read file; do
        # 获取文件扩展名
        ext="${file##*.}"
        
        # 创建新文件名
        new_name="${category}_$(date +%Y%m%d)_$(basename "$file" | head -c 30 | tr ' ' '_').$ext"
        new_path="$(dirname "$file")/$new_name"
        
        if [ "$file" != "$new_path" ]; then
            mv "$file" "$new_path"
            log_success "重命名: $(basename $file) -> $new_name"
        fi
    done
}

# 版权检查清单
copyright_check() {
    local file=$1
    
    echo "=========================================="
    echo "版权检查: $(basename $file)"
    echo "=========================================="
    echo ""
    echo "请回答以下问题 (y/n):"
    
    read -p "1. 素材有水印? " has_watermark
    read -p "2. 有明确的版权声明? " has_copyright
    read -p "3. 可用于商业用途? " can_commercial
    read -p "4. 已获得作者授权? " has_permission
    
    if [ "$has_watermark" = "n" ] && [ "$has_permission" = "y" ]; then
        echo ""
        echo "✅ 版权状态: 可用"
        status="可用"
    elif [ "$can_commercial" = "y" ]; then
        echo ""
        echo "⚠️ 版权状态: 需标注来源"
        status="需标注"
    else
        echo ""
        echo "❌ 版权状态: 需确认/禁用"
        status="待确认"
    fi
    
    # 保存检查结果
    echo "$(date +%Y-%m-%d %H:%M:%S) | $file | $status" >> "$LOG_DIR/copyright_check.log"
}

# 生成素材报告
generate_report() {
    log_info "生成素材报告..."
    
    report_file="$LOG_DIR/素材报告_${TIMESTAMP}.md"
    
    cat > "$report_file" << EOF
# 素材收集报告

## 生成时间
$(date "+%Y-%m-%d %H:%M:%S")

## 收集统计

### 按分类统计

| 分类 | 视频数 | 图片数 | 总计 |
|------|--------|--------|------|
| 迪拜-阿布扎比 | $(find "$MATERIALS_DIR/迪拜-阿布扎比" -name "*.mp4" 2>/dev/null | wc -l) | $(find "$MATERIALS_DIR/迪拜-阿布扎比" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) | - |
| 土豪日常 | $(find "$MATERIALS_DIR/土豪日常" -name "*.mp4" 2>/dev/null | wc -l) | $(find "$MATERIALS_DIR/土豪日常" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) | - |
| 华人群体 | $(find "$MATERIALS_DIR/华人群体" -name "*.mp4" 2>/dev/null | wc -l) | $(find "$MATERIALS_DIR/华人群体" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) | - |
| 生活定居 | $(find "$MATERIALS_DIR/生活定居" -name "*.mp4" 2>/dev/null | wc -l) | $(find "$MATERIALS_DIR/生活定居" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) | - |
| 高清街拍 | $(find "$MATERIALS_DIR/高清街拍" -name "*.mp4" 2>/dev/null | wc -l) | $(find "$MATERIALS_DIR/高清街拍" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l) | - |

### 总计
- 视频总数: $(find "$MATERIALS_DIR" -name "*.mp4" 2>/dev/null | wc -l)
- 图片总数: $(find "$MATERIALS_DIR" -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l)
- 总文件数: $(find "$MATERIALS_DIR" -type f 2>/dev/null | wc -l)

## 版权状态
- 已检查: $(wc -l < "$LOG_DIR/copyright_check.log" 2>/dev/null || echo 0)
- 待检查: $(find "$MATERIALS_DIR" -type f ! -name ".*" 2>/dev/null | wc -l)

## 使用建议
1. 优先使用"可用"版权状态的素材
2. "需标注"素材请在发布时注明来源
3. "待确认"素材请勿使用，直至获得授权

---
报告生成完成
EOF

    log_success "报告已生成: $report_file"
    cat "$report_file"
}

# 帮助信息
show_help() {
    echo ""
    echo "=========================================="
    echo "  视频号素材收集工具包"
    echo "  Video Materials Collection Kit"
    echo "=========================================="
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "可用命令:"
    echo "  setup              - 创建目录结构"
    echo "  instagram <url>    - Instagram下载指引"
    echo "  tiktok <url>       - TikTok下载指引"
    echo "  youtube <url>      - YouTube下载指引"
    echo "  twitter <url>      - Twitter/X下载指引"
    echo "  shorts <url>       - 批量下载YouTube Shorts"
    echo "  rename <category>  - 重命名指定分类文件"
    echo "  check <file>       - 版权检查"
    echo "  report             - 生成素材报告"
    echo "  all                - 执行全部收集任务"
    echo "  help               - 显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 setup"
    echo "  $0 instagram https://www.instagram.com/p/abc123/"
    echo "  $0 tiktok https://www.tiktok.com/@user/video/123"
    echo "  $0 rename 迪拜-阿布扎比"
    echo "  $0 report"
    echo ""
}

# 主程序
case "$1" in
    setup)
        setup_directories
        ;;
    instagram)
        download_instagram "$2" "迪拜-阿布扎比"
        ;;
    tiktok)
        download_tiktok "$2" "迪拜-阿布扎比"
        ;;
    youtube)
        download_youtube "$2" "迪拜-阿布扎比"
        ;;
    twitter)
        download_twitter "$2" "迪拜-阿布扎比"
        ;;
    shorts)
        batch_download_shorts "$2" "迪拜-阿布扎比"
        ;;
    rename)
        rename_files "$2"
        ;;
    check)
        copyright_check "$2"
        ;;
    report)
        generate_report
        ;;
    all)
        setup_directories
        echo ""
        log_success "请手动执行以下下载任务:"
        echo ""
        echo "1. Instagram - 使用4K Stogram"
        echo "2. TikTok - 使用ssstik.io"
        echo "3. YouTube - 使用4K Video Downloader"
        echo "4. Twitter - 使用twdownloader.com"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac
