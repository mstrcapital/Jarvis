#!/bin/bash
# ============================================================================
# Hermes图片自动下载器 v2.0
# 
# 功能: 从免费图库下载Hermes相关图片
# 特点: 无需API Key，使用公共链接
# ============================================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
OUTPUT_DIR="/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo"
TEMP_DIR="/tmp/hermes_images"

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# 创建目录
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Hermes图片自动下载器 v2.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 方法1: 尝试下载Wikimedia Commons的版权图片
download_wikimedia() {
    log "尝试从Wikimedia Commons下载..."
    
    # Hermès相关的公共领域图片
    WIKIMEDIA_URLS=(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Hermes_logo.svg/1200px-Hermes_logo.svg.png"
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Paris_Hermes_store.jpg/1280px-Paris_Hermes_store.jpg"
    )
    
    for url in "${WIKIMEDIA_URLS[@]}"; do
        filename=$(basename "$url" | cut -d'?' -f1)
        filepath="$TEMP_DIR/$filename"
        
        log "下载: $filename"
        if curl -sL -o "$filepath" --max-time 30 "$url" 2>/dev/null; then
            if [ -s "$filepath" ]; then
                info "✅ 下载成功: $filename"
                ls -lh "$filepath"
            fi
        else
            error "❌ 下载失败: $filename"
        fi
    done
}

# 方法2: 创建占位图
create_placeholder() {
    log "创建占位图..."
    
    # 创建高质量占位图（棕色皮质感）
    cat > "$TEMP_DIR/create_placeholder.py" << 'PYEOF'
import math
from PIL import Image, ImageDraw, ImageFont

def create_birkin_placeholder():
    # 创建3000x3000的高清图
    width, height = 3000, 3000
    img = Image.new('RGB', (width, height), color='#F5F5F5')
    draw = ImageDraw.Draw(img)
    
    # 绘制Birkin包轮廓（简化版）
    # 包身
    draw.rectangle([800, 600, 2200, 2400], fill='#2C2C2C', outline='#1a1a1a', width=20)
    
    # 包盖
    draw.rectangle([800, 600, 2200, 1200], fill='#3C3C3C', outline='#1a1a1a', width=20)
    
    # 手柄
    draw.rectangle([1100, 300, 1900, 600], fill='#4C4C4C', outline='#1a1a1a', width=15)
    
    # 锁扣（金色）
    draw.rectangle([1350, 1200, 1650, 1500], fill='#FFD700', outline='#DAA520', width=10)
    
    # 刻印文字区域
    draw.rectangle([1000, 2200, 2000, 2350], fill='#1a1a1a', width=5)
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    draw.text((1500, 1250), "HERMÈS", fill='#FFD700', anchor='mm', font=font)
    draw.text((1500, 2275), "PARIS", fill='#FFFFFF', anchor='mm', font=font)
    
    # 保存
    filepath = "/tmp/hermes_images/birkin_30_black_placeholder.jpg"
    img.save(filepath, quality=95, optimize=True)
    print(f"占位图已创建: {filepath}")
    return filepath

if __name__ == "__main__":
    create_birkin_placeholder()
PYEOF

    python3 "$TEMP_DIR/create_placeholder.py" 2>/dev/null || echo "Python PIL未安装，使用备用方案"
}

# 方法3: 下载示例图
download_sample_images() {
    log "尝试下载示例图片..."
    
    # 使用公共可用的高质量图片链接
    SAMPLE_URLS=(
        # Pexels免费图片（需要手动下载）
        "https://images.pexels.com/photos/954254/pexels-photo-954254.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        "https://images.pexels.com/photos/299252/pexels-photo-299252.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    )
    
    info "示例图片需要手动下载："
    echo ""
    echo "请访问以下链接，右键图片 → 另存为："
    echo ""
    echo "Pexels (免费高清图库):"
    echo "  1. 打开 https://www.pexels.com/"
    echo "  2. 搜索 'luxury handbag black'"
    echo "  3. 下载高清图片"
    echo ""
    echo "Unsplash (免费高清图库):"
    echo "  1. 打开 https://unsplash.com/"
    echo "  2. 搜索 'luxury bag'"
    echo "  3. 下载高清图片"
    echo ""
}

# 显示使用说明
show_instructions() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  Hermes图片收集使用说明${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo "由于版权原因，无法自动下载Hermes官方图片。"
    echo ""
    echo -e "${YELLOW}推荐方案：${NC}"
    echo ""
    echo "1️⃣  手动收集（推荐）"
    echo "    - 访问 https://www.hermes.com/"
    echo "    - 搜索 Birkin 30"
    echo "    - 右键产品图 → 另存为"
    echo "    - 保存到: $OUTPUT_DIR/"
    echo ""
    
    echo "2️⃣  使用免费图库"
    echo "    - Pexels.com (搜索 luxury handbag)"
    echo "    - Unsplash.com (搜索 luxury bag)"
    echo "    - 下载免费高清图片"
    echo ""
    
    echo "3️⃣  联系博主授权"
    echo "    - 关注Hermes博主"
    echo "    - 申请图片授权"
    echo "    - 获得使用许可"
    echo ""
    
    echo -e "${GREEN}收集完成后，图片会自动用于内容创作！${NC}"
    echo ""
}

# 主程序
main() {
    log "开始Hermes图片收集..."
    
    # 创建占位图
    create_placeholder
    
    # 尝试下载Wikimedia图片
    download_wikimedia
    
    # 显示使用说明
    show_instructions
    
    # 显示收集的图片
    echo ""
    log "当前收集的图片："
    ls -lh "$TEMP_DIR/" 2>/dev/null || echo "暂无图片"
    
    echo ""
    log "输出目录: $OUTPUT_DIR"
    echo ""
    info "请手动收集Hermes图片后保存到上述目录"
}

main "$@"