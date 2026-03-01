#!/bin/bash
# =====================================================
# Postiz 上传工具 - 一键运行脚本
# =====================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Postiz 自动上传工具 v1.0${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未找到Node.js${NC}"
    echo "请安装Node.js: https://nodejs.org"
    exit 1
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查依赖
echo -e "${BLUE}📦 检查依赖...${NC}"
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  未安装依赖，正在安装...${NC}"
    npm install
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
else
    echo -e "${GREEN}✅ 依赖已安装${NC}"
fi

# 检查配置文件
CONFIG_FILE="postiz-upload.js"
if ! grep -q "YOUR_POSTIZ_API_KEY" "$CONFIG_FILE"; then
    echo -e "${GREEN}✅ API Key已配置${NC}"
else
    echo -e "${YELLOW}⚠️  请先配置API Key${NC}"
    echo ""
    echo "步骤："
    echo "1. 登录 https://postiz.com"
    echo "2. 进入 Settings > API"
    echo "3. 复制API Key"
    echo "4. 修改 $CONFIG_FILE 中的 CONFIG.API_KEY"
    echo ""
    exit 1
fi

# 显示菜单
echo ""
echo "请选择操作:"
echo "1. 查看已连接频道"
echo "2. 上传单个视频"
echo "3. 批量上传"
echo "4. 查看帮助"
echo ""

read -p "请输入数字 (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}📋 获取频道列表...${NC}"
        node postiz-upload.js | grep -A 20 "已连接的频道"
        ;;
    2)
        read -p "视频路径: " videoPath
        read -p "文案: " caption
        read -p "标签 (逗号分隔): " tags
        tags_array=$(echo $tags | tr ',' ' ')
        node postiz-upload.js --video "$videoPath" --caption "$caption" --tags "$tags_array"
        ;;
    3)
        echo -e "${BLUE}🚀 批量上传模式${NC}"
        echo "请确保已在 postiz-upload.js 中配置好批量任务"
        echo ""
        read -p "确认执行批量上传? (y/n): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            node postiz-upload.js --batch
        fi
        ;;
    4)
        node postiz-upload.js --help
        ;;
    *)
        echo -e "${RED}❌ 无效选择${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ 操作完成${NC}"