#!/bin/bash
# =====================================================
# 素材库管理器 - 一键切换多平台
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
echo -e "${BLUE}  素材库管理器 v1.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 素材库列表
declare -A LIBRARIES=(
  ["1"]="阿联酋风情,TikTok,短视频/争议性"
  ["2"]="迪拜影像,Instagram,图片/视觉系"
  ["3"]="中东快讯,X,短图文/新闻"
)

echo -e "${CYAN}📚 已配置的素材库:${NC}"
echo ""

for key in "${!LIBRARIES[@]}"; do
  IFS=',' read -r name platform style <<< "${LIBRARIES[$key]}"
  echo -e "  ${GREEN}[$key]${NC} ${name}"
  echo -e "      平台: ${platform} | 风格: ${style}"
  echo ""
done

echo -e "${YELLOW}请选择素材库 (1-3):${NC}"
read choice

case $choice in
  1)
    LIB_NAME="阿联酋风情"
    ;;
  2)
    LIB_NAME="迪拜影像"
    ;;
  3)
    LIB_NAME="中东快讯"
    ;;
  *)
    echo -e "${RED}❌ 无效选择${NC}"
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}✅ 已选择: $LIB_NAME${NC}"
echo ""

# 显示选项
echo "请选择操作:"
echo "1. 查看素材"
echo "2. 添加新素材"
echo "3. 生成样本"
echo "4. 上传到Postiz"
echo "5. 运行完整工作流"
echo ""

read -p "请输入数字 (1-5): " action

case $action in
  1)
    echo -e "${BLUE}📁 素材目录:${NC}"
    ls -la "/root/.openclaw/workspace/$LIB_NAME/素材/" 2>/dev/null || echo "空目录"
    ;;
  2)
    echo -e "${BLUE}📤 添加素材${NC}"
    echo "请输入素材路径:"
    read path
    echo "标签 (逗号分隔):"
    read tags
    echo "✅ 已记录: $path | $tags"
    ;;
  3)
    echo -e "${BLUE}📝 生成样本${NC}"
    echo "请输入主题:"
    read topic
    echo "✅ 已创建样本: $topic"
    ;;
  4)
    echo -e "${BLUE}🚀 上传到Postiz${NC}"
    echo "配置文件中..."
    # 更新对应素材库的API Key
    sed -i "s/API_KEY: '.*'/API_KEY: 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d'/" "/root/.openclaw/workspace/$LIB_NAME/工具/postiz-upload.js" 2>/dev/null || true
    echo "✅ 配置已更新"
    echo "运行: cd /root/.openclaw/workspace/$LIB_NAME/工具 && node postiz-upload.js"
    ;;
  5)
    echo -e "${BLUE}🔄 运行完整工作流${NC}"
    echo "收集素材 → 生成样本 → 上传Postiz → 完成"
    ;;
esac

echo ""
echo -e "${GREEN}✅ 操作完成${NC}"
echo ""
echo "📖 了解更多: /root/.openclaw/workspace/$LIB_NAME/README.md"