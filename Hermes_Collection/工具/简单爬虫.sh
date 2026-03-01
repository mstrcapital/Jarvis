#!/bin/bash
# Hermes图片简单下载器
# 从公开链接下载免费图片

OUTPUT_DIR="/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo"
TEMP_DIR="/tmp/hermes_downloads"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo "🎀 Hermes图片下载器"
echo "===================="
echo ""

# 使用curl从公开API下载图片
# Unsplash Source (已关闭，改用其他源)
# Pexels需要API Key

# 方法1: 使用Lorem Picsum (高质量占位图)
echo "📥 从Lorem Picsum下载高质量测试图..."
curl -L -o "$TEMP_DIR/sample_1.jpg" "https://picsum.photos/2000/2000" 2>/dev/null

# 方法2: 使用其他公开图源
echo "📥 从公开图源下载..."

# 下载一些示例图
DOWNLOAD_URLS=(
    "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=2000"
    "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=2000"
    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=2000"
)

for i in "${!DOWNLOAD_URLS[@]}"; do
    idx=$((i+1))
    url="${DOWNLOAD_URLS[$i]}"
    echo "下载 $idx: ${url:0:50}..."
    curl -sL -o "$TEMP_DIR/luxury_$idx.jpg" "$url" 2>/dev/null || echo "  ❌ 下载失败"
done

echo ""
echo "✅ 下载完成!"
echo ""
echo "📁 下载位置: $TEMP_DIR"
ls -lh "$TEMP_DIR/"

echo ""
echo "📋 下一步:"
echo "1. 手动从Hermes官网下载高清产品图"
echo "2. 保存到: $OUTPUT_DIR/"
echo "3. 发布时使用高质量图片"
