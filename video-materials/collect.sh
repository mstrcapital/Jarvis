#!/bin/bash
# 素材收集一键脚本
# Created: 2026-02-19

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║       📦 素材收集系统                                         ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

# 配置
WORKSPACE="/root/.openclaw/workspace/video-materials"
LINKS_FILE="${WORKSPACE}/links/links_pool.txt"
DOWNLOAD_DIR="${WORKSPACE}/raw"
DB_FILE="${WORKSPACE}/database/download_status.json"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 检查目录
check_dirs() {
    log_info "检查目录结构..."
    mkdir -p "${DOWNLOAD_DIR}"
    mkdir -p "${WORKSPACE}/links"
    mkdir -p "${WORKSPACE}/database"
    log_success "目录检查完成"
}

# 导入链接池
import_links() {
    log_info "从链接池导入..."
    python3 "${WORKSPACE}/batch_downloader.py" import
}

# 开始下载
start_download() {
    log_info "开始批量下载..."
    python3 "${WORKSPACE}/batch_downloader.py" run
}

# 查看状态
show_status() {
    log_info "查看下载状态..."
    python3 "${WORKSPACE}/batch_downloader.py" status
}

# 添加链接
add_link() {
    if [ -z "$1" ]; then
        echo "用法: $0 add <url> [标签] [优先级]"
        echo "示例: $0 add \"https://youtu.be/xxx\" luxury high"
        return
    fi
    
    local url="$1"
    local tags="${2:-general}"
    local priority="${3:-medium}"
    
    log_info "添加链接: $url"
    python3 "${WORKSPACE}/batch_downloader.py" add "$url" "$tags" "$priority"
}

# 查看链接池
show_links() {
    log_info "链接池内容:"
    echo ""
    if [ -f "$LINKS_FILE" ]; then
        cat "$LINKS_FILE"
    else
        log_warn "链接池文件不存在"
    fi
}

# 编辑链接池
edit_links() {
    log_info "编辑链接池: $LINKS_FILE"
    nano "$LINKS_FILE" 2>/dev/null || vi "$LINKS_FILE" 2>/dev/null || echo "请手动编辑: $LINKS_FILE"
}

# 清理下载完成的文件
clean_downloaded() {
    log_info "清理已完成的下载..."
    # 可以添加清理逻辑
    log_success "清理完成"
}

# 重试失败
retry_failed() {
    log_info "重试失败任务..."
    python3 "${WORKSPACE}/batch_downloader.py" retry
}

# 显示帮助
show_help() {
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  import        从链接池导入所有链接"
    echo "  download      开始批量下载"
    echo "  status        查看下载状态"
    echo "  add <url>     添加单个链接"
    echo "  links         查看链接池"
    echo "  edit          编辑链接池"
    echo "  retry         重试失败任务"
    echo "  clean         清理下载"
    echo "  help          显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 import"
    echo "  $0 download"
    echo "  $0 add \"https://youtu.be/xxx\" luxury high"
    echo "  $0 status"
    echo ""
}

# 主程序
case "$1" in
    import)
        check_dirs
        import_links
        ;;
    download)
        check_dirs
        start_download
        ;;
    status)
        show_status
        ;;
    add)
        shift
        add_link "$@"
        ;;
    links)
        show_links
        ;;
    edit)
        edit_links
        ;;
    retry)
        retry_failed
        ;;
    clean)
        clean_downloaded
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        ;;
esac

echo ""
