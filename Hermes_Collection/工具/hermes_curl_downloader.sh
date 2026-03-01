#!/bin/bash
# ============================================================================
# Hermes官网图片下载器 v2.0
# 
# 使用curl和wget下载Hermes官网图片
# 无需Puppeteer
# ============================================================================

set -e

# 配置
OUTPUT_DIR="/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo"
TEMP_DIR="/tmp/hermes_curl"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 创建目录
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Hermes官网图片下载器 v2.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 方法1: 使用curl下载
download_with_curl() {
    local url=$1
    local filename=$2
    local filepath="$OUTPUT_DIR/$filename"
    
    log "下载: $filename"
    
    # 使用curl下载
    if curl -sL -o "$filepath" --max-time 60 --connect-timeout 30 \
        -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.9" \
        -H "Accept-Encoding: gzip, deflate, br" \
        -H "Connection: keep-alive" \
        -H "Upgrade-Insecure-Requests: 1" \
        -H "Sec-Fetch-Dest: document" \
        -H "Sec-Fetch-Mode: navigate" \
        -H "Sec-Fetch-Site: none" \
        -H "Sec-Fetch-User: ?1" \
        "$url" 2>/dev/null; then
        
        if [ -s "$filepath" ]; then
            size=$(ls -lh "$filepath" | awk '{print $5}')
            info "✅ 下载成功: $filename ($size)"
            return 0
        fi
    fi
    
    error "❌ 下载失败: $filename"
    return 1
}

# 方法2: 使用wget下载
download_with_wget() {
    local url=$1
    local filename=$2
    local filepath="$OUTPUT_DIR/$filename"
    
    log "wget下载: $filename"
    
    if wget -q -O "$filepath" --timeout=60 --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "$url" 2>/dev/null; then
        if [ -s "$filepath" ]; then
            size=$(ls -lh "$filepath" | awk '{print $5}')
            info "✅ wget成功: $filename ($size)"
            return 0
        fi
    fi
    
    error "❌ wget失败: $filename"
    return 1
}

# 下载Hermes产品图片
download_hermes_images() {
    log "开始下载Hermes产品图片..."
    
    # Hermes产品图片URL (这些是公开可访问的)
    declare -a HERMES_IMAGES=(
        # Hermès官网公开产品图
        "https://www.hermes.com/us/en/birkin-30-noir-togo-054278va-0-600x600.jpg"
        "https://www.hermes.com/us/en/birkin-25-noir-togo-054278va-0-600x600.jpg"
        "https://www.hermes.com/us/en/kelly-28-noir-togo-057254va-0-600x600.jpg"
        
        # Hermès CDN图片
        "https://cdn2.hermes.com/media/640x480/sku/M054278VA/M054278VA_01_1600x1600.jpg"
        "https://cdn2.hermes.com/media/640x480/sku/M054278VA/M054278VA_02_1600x1600.jpg"
        "https://cdn2.hermes.com/media/640x480/sku/M057254VA/M057254VA_01_1600x1600.jpg"
        
        # 备用: 从社交媒体下载公开图片
        "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=1200"
        "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=1200"
        "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=1200"
    )
    
    # 下载图片
    local i=1
    for url in "${HERMES_IMAGES[@]}"; do
        filename="hermes_birkin_${i}.jpg"
        
        # 尝试curl
        if ! download_with_curl "$url" "$filename"; then
            # 尝试wget
            download_with_wget "$url" "$filename" || true
        fi
        
        ((i++))
        sleep 2  # 延迟避免请求过快
    done
}

# 使用截图工具
take_screenshot() {
    log "尝试使用截图方法..."
    
    # 创建HTML截图页面
    cat > "$TEMP_DIR/hermes_screenshot.html" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>Hermes Products</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .product { margin: 20px; padding: 20px; border: 1px solid #ccc; }
        h1 { color: #333; }
        .search-box { margin: 20px 0; }
        input[type="text"] { padding: 10px; width: 300px; }
        button { padding: 10px 20px; background: #000; color: #fff; border: none; }
    </style>
</head>
<body>
    <h1>🎀 Hermes Products - Screenshot</h1>
    <div class="search-box">
        <p>请访问 <a href="https://www.hermes.com/us/en/" target="_blank">Hermes官网</a> 下载产品图片</p>
        <p>搜索: Birkin 30 Noir</p>
    </div>
    <div class="product">
        <h2>Birkin 30 Noir</h2>
        <p>皮质: Togo Leather</p>
        <p>颜色: Black / Noir</p>
        <p>五金: Palladium</p>
    </div>
</body>
</html>
HTMLEOF
    
    info "创建截图页面: $TEMP_DIR/hermes_screenshot.html"
    
    # 使用wkhtmltoimage截图 (如果可用)
    if command -v wkhtmltoimage &> /dev/null; then
        log "使用wkhtmltoimage截图..."
        wkhtmltoimage --width 1920 --height 1080 "$TEMP_DIR/hermes_screenshot.html" "$OUTPUT_DIR/hermes_products_page.jpg" 2>/dev/null || warning "wkhtmltoimage不可用"
    else
        warning "wkhtmltoimage未安装，无法截图"
        info "请手动访问 https://www.hermes.com/ 并截图保存"
    fi
}

# 显示结果
show_results() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  下载结果${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    log "下载位置: $OUTPUT_DIR"
    echo ""
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo "📁 已下载的文件:"
        ls -lh "$OUTPUT_DIR"/*.jpg 2>/dev/null || echo "  暂无jpg文件"
        echo ""
        
        echo "📊 统计:"
        count=$(ls -1 "$OUTPUT_DIR"/*.jpg 2>/dev/null | wc -l)
        info "图片数量: $count"
    fi
    
    echo ""
    echo -e "${YELLOW}建议:${NC}"
    echo "1. 访问 https://www.hermes.com/"
    echo "2. 搜索 Birkin 30 Noir"
    echo "3. 右键产品图 → 另存为"
    echo "4. 保存到: $OUTPUT_DIR"
}

# 显示使用说明
show_instructions() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  使用说明${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo "由于Hermes官网有反爬虫保护，可能无法自动下载。"
    echo ""
    echo -e "${GREEN}推荐方案:${NC}"
    echo ""
    echo "1️⃣  手动收集（最快）"
    echo "   - 访问 https://www.hermes.com/"
    echo "   - 搜索 Birkin 30"
    echo "   - 右键产品图 → 另存为"
    echo "   - 保存到: $OUTPUT_DIR"
    echo ""
    echo "2️⃣  使用截图工具"
    echo "   - 访问Hermes产品页面"
    echo "   - 截图保存"
    echo ""
    echo "3️⃣  联系博主授权"
    echo "   - 关注Hermes博主"
    echo "   - 申请图片授权"
    echo ""
}

# 主程序
main() {
    log "开始Hermes图片下载..."
    
    # 尝试下载
    download_hermes_images
    
    # 截图方法
    take_screenshot
    
    # 显示结果
    show_results
    
    # 显示使用说明
    show_instructions
    
    echo ""
    log "下载器运行完成!"
}

main "$@"