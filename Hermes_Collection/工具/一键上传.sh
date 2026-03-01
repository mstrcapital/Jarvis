#!/bin/bash
# =====================================================
# Postiz 一键上传脚本 - 支持多素材库
# =====================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Postiz 一键上传工具 v2.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查API Key
if [ -z "$POSTIZ_API_KEY" ]; then
    export POSTIZ_API_KEY="c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d"
fi

# 素材库配置
declare -A LIBRARIES=(
  ["1"]="阿联酋风情,TikTok,cmlomzyp90166qf0y1qvcpzyh,/root/.openclaw/workspace/阿联酋风情/素材"
  ["2"]="迪拜影像,Instagram,cmlon7x9a016jqf0y440vzy3d,/root/.openclaw/workspace/迪拜影像/素材"
  ["3"]="中东快讯,X,cmlomo6nn015kqf0y9re6jw09,/root/.openclaw/workspace/中东快讯/素材"
)

# 显示素材库
echo -e "${CYAN}📚 素材库列表:${NC}"
echo ""
for key in "${!LIBRARIES[@]}"; do
  IFS=',' read -r name platform channel path <<< "${LIBRARIES[$key]}"
  echo -e "  ${GREEN}[$key]${NC} $name → $platform"
done
echo ""

# 选择素材库
echo -e "${YELLOW}请选择素材库 (1-3):${NC}"
read choice

if [ -z "${LIBRARIES[$choice]}" ]; then
    echo -e "${RED}❌ 无效选择${NC}"
    exit 1
fi

IFS=',' read -r NAME PLATFORM CHANNEL PATH <<< "${LIBRARIES[$choice]}"
echo -e "${GREEN}✅ 已选择: $NAME → $PLATFORM${NC}"
echo ""

# 检查目录
if [ ! -d "$PATH" ]; then
    echo -e "${RED}❌ 目录不存在: $PATH${NC}"
    exit 1
fi

# 查找文件
echo -e "${BLUE}📁 查找素材文件...${NC}"
FILES=$(find "$PATH" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.mp4" -o -name "*.mov" \) 2>/dev/null | head -10)

if [ -z "$FILES" ]; then
    echo -e "${YELLOW}⚠️  未找到素材文件${NC}"
    echo "请先添加素材到: $PATH"
    exit 1
fi

echo ""
echo -e "${CYAN}可用文件:${NC}"
select FILE in $FILES "退出"; do
    if [ "$FILE" = "退出" ]; then
        echo "取消"
        exit 0
    fi
    
    if [ -n "$FILE" ]; then
        echo -e "\n${GREEN}已选择: $FILE${NC}"
        break
    fi
done

echo ""
echo -e "${BLUE}📤 上传文件中...${NC}"

# 上传文件
UPLOAD_RESULT=$(postiz upload "$FILE" 2>&1)

if echo "$UPLOAD_RESULT" | grep -q "uploaded successfully"; then
    echo -e "${GREEN}✅ 上传成功！${NC}"
    FILE_URL=$(echo "$UPLOAD_RESULT" | grep -o '"path":"[^"]*"' | cut -d'"' -f4)
    echo "文件URL: $FILE_URL"
    echo ""
    
    # 询问是否创建帖子
    echo -e "${YELLOW}是否创建帖子? (y/n)${NC}"
    read create_post
    
    if [ "$create_post" = "y" ] || [ "$create_post" = "Y" ]; then
        echo ""
        echo -e "${BLUE}📝 输入帖子信息:${NC}"
        
        echo "文案:"
        read caption
        
        echo "标签 (逗号分隔):"
        read tags
        
        echo "发布时间 (回车=立即发布, 格式=2026-02-16T09:00:00Z):"
        read scheduled_at
        
        if [ -z "$scheduled_at" ]; then
            scheduled_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        fi
        
        echo ""
        echo -e "${BLUE}🔄 创建帖子...${NC}"
        
        # 使用curl创建帖子
        curl -s -X POST "https://api.postiz.com/public/v1/posts" \
          -H "Authorization: Bearer $POSTIZ_API_KEY" \
          -H "Content-Type: application/json" \
          -d "{
            \"type\": \"now\",
            \"shortLink\": false,
            \"date\": \"$scheduled_at\",
            \"tags\": [$(echo "$tags" | tr ',' '\n' | xargs -I{} echo "\"$(echo {} | xargs)\"" | tr '\n' ',')],
            \"posts\": [{
              \"integration\": { \"id\": \"$CHANNEL\" },
              \"value\": [{
                \"content\": \"$caption\",
                \"image\": [{ \"id\": \"new\", \"path\": \"$FILE_URL\" }]
              }]
            }]
          }" 2>&1
        
        echo ""
        echo -e "${GREEN}✅ 帖子创建完成！${NC}"
    fi
else
    echo -e "${RED}❌ 上传失败:${NC}"
    echo "$UPLOAD_RESULT"
fi

echo ""
echo -e "${GREEN}✅ 操作完成！${NC}"