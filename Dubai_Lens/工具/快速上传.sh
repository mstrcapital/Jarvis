#!/bin/bash
# =====================================================
# Postiz 快速上传 - 直接指定文件
# 用法: ./快速上传.sh <文件路径> <素材库编号>
# =====================================================

set -e

# 配置
API_KEY="c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d"
API_URL="https://api.postiz.com/public/v1"

# 素材库配置
declare -A CHANNELS=(
  ["1"]="cmlomzyp90166qf0y1qvcpzyh"  # TikTok
  ["2"]="cmlon7x9a016jqf0y440vzy3d"  # Instagram
  ["3"]="cmlomo6nn015kqf0y9re6jw09"  # X
)

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 显示帮助
if [ "$1" = "--help" ] || [ -z "$1" ]; then
    echo "Postiz 快速上传"
    echo ""
    echo "用法: $0 <文件路径> [素材库编号]"
    echo ""
    echo "素材库编号:"
    echo "  1 = TikTok (阿联酋风情)"
    echo "  2 = Instagram (迪拜影像)"
    echo "  3 = X (中东快讯)"
    echo ""
    echo "示例:"
    echo "  $0 ./video.mp4 1              # 上传视频到TikTok"
    echo "  $0 ./image.jpg 2              # 上传图片到Instagram"
    echo ""
    exit 0
fi

FILE="$1"
CHANNEL_NUM="${2:-1}"
CHANNEL="${CHANNELS[$CHANNEL_NUM]}"

# 验证文件
if [ ! -f "$FILE" ]; then
    echo -e "${RED}❌ 文件不存在: $FILE${NC}"
    exit 1
fi

# 验证渠道
if [ -z "$CHANNEL" ]; then
    echo -e "${RED}❌ 无效素材库编号: $CHANNEL_NUM${NC}"
    exit 1
fi

echo "📤 上传文件: $FILE"
echo "📡 目标渠道: $CHANNEL"
echo ""

# 上传文件
echo "🔄 上传中..."
UPLOAD_RESULT=$(postiz upload "$FILE" 2>&1)

if echo "$UPLOAD_RESULT" | grep -q "uploaded successfully"; then
    FILE_URL=$(echo "$UPLOAD_RESULT" | grep -o '"path":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ 文件上传成功！${NC}"
    echo "🔗 URL: $FILE_URL"
    echo ""
    
    # 默认文案
    CAPTION="分享一个精彩瞬间 #迪拜 #阿联酋"
    DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "📝 创建帖子..."
    echo "   文案: $CAPTION"
    echo "   时间: $DATE"
    
    # 创建帖子
    POST_RESULT=$(curl -s -X POST "$API_URL/posts" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"type\": \"now\",
        \"shortLink\": false,
        \"date\": \"$DATE\",
        \"tags\": [{\"value\": \"迪拜\", \"label\": \"迪拜\"}, {\"value\": \"阿联酋\", \"label\": \"阿联酋\"}],
        \"posts\": [{
          \"integration\": { \"id\": \"$CHANNEL\" },
          \"value\": [{
            \"content\": \"$CAPTION\",
            \"image\": [{ \"id\": \"new\", \"path\": \"$FILE_URL\" }]
          }]
        }]
      }" 2>&1)
    
    if echo "$POST_RESULT" | grep -q "id"; then
        echo -e "${GREEN}✅ 帖子创建成功！${NC}"
    else
        echo -e "${YELLOW}⚠️  文件已上传，但帖子创建失败${NC}"
        echo "错误: $POST_RESULT"
    fi
else
    echo -e "${RED}❌ 上传失败:${NC}"
    echo "$UPLOAD_RESULT"
fi

echo ""
echo "✅ 完成"