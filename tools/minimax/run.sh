#!/bin/bash
# MiniMax Media Generator - Quick Start Script

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║           🎬 MiniMax Media Generator                           ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查环境变量
if [ -z "$MINIMAX_API_KEY" ]; then
    echo -e "${RED}❌ 请先设置环境变量:${NC}"
    echo ""
    echo "   export MINIMAX_API_KEY=\"sk-api-your-key\""
    echo "   export MINIMAX_API_HOST=\"https://api.minimaxi.com\""
    echo ""
    echo "   在 ~/.bashrc 或 ~/.zshrc 中添加以上内容"
    exit 1
fi

echo -e "${GREEN}✅ API Key已设置${NC}"
echo "   Host: ${MINIMAX_API_HOST:-https://api.minimaxi.com}"
echo ""

# 显示帮助
show_help() {
    echo -e "${YELLOW}使用方法:${NC}"
    echo ""
    echo "  生成视频:"
    echo "    ./run.sh video gold_necklace"
    echo "    ./run.sh video platinum_jewelry"
    echo "    ./run.sh video stacked_rings"
    echo "    ./run.sh video jewelry_box"
    echo ""
    echo "  生成图像:"
    echo "    ./run.sh image gold_necklace_product"
    echo "    ./run.sh image social_media_post"
    echo ""
    echo "  批量生成:"
    echo "    ./run.sh batch video gold_necklace lifestyle"
    echo "    ./run.sh batch image gold_necklace_product hero_banner"
    echo ""
    echo "  每日内容:"
    echo "    ./run.sh daily"
    echo ""
    echo "  查看状态:"
    echo "    ./run.sh query <task_id>"
    echo ""
    echo -e "${YELLOW}可用提示词:${NC}"
    echo ""
    echo "  视频: gold_necklace, platinum_jewelry, stacked_rings, jewelry_box,"
    echo "        abstract_background, lifestyle, luxury_store"
    echo ""
    echo "  图像: gold_necklace_product, jewelry_lifestyle, product_detail,"
    echo "        social_media_post, hero_banner, packaging"
}

# 运行命令
run_command() {
    cd "$(dirname "$0")"
    python3 minimax_tool.py "$@"
}

# 主逻辑
case "$1" in
    help|--help|-h)
        show_help
        ;;
    video|image|batch|daily|query)
        run_command "$@"
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac