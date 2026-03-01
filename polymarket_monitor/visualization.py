#!/usr/bin/env python3
"""
Polymarket Trader 数据可视化 v1.0

生成图表：
1. 盈亏分布饼图
2. 分类盈亏柱状图
3. Top Trader排名图
4. 风险收益散点图
"""

import json
import matplotlib
matplotlib.use('Agg')  # 无GUI后端
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Trader数据
TRADERS = {
    # NegRisk类
    '@xmgnr': {'pnl': 0.00, 'value': 0.00, 'category': 'NegRisk'},
    '@luishXYZ': {'pnl': 233.87, 'value': 2777.43, 'category': 'NegRisk'},
    '@copenzafan': {'pnl': -40954.81, 'value': 4888.58, 'category': 'NegRisk'},
    '@carverfomo': {'pnl': 0.00, 'value': 0.00, 'category': 'NegRisk'},
    '@HolyMoses7': {'pnl': 2578.10, 'value': 140400.00, 'category': 'NegRisk'},
    '@PolycoolApp': {'pnl': 4476569.12, 'value': 11100.00, 'category': 'NegRisk'},
    '@itslirrato': {'pnl': 8.70, 'value': 108.71, 'category': 'NegRisk'},
    
    # Basic类
    '@clawdvine': {'pnl': 104.26, 'value': 0.00, 'category': 'Basic'},
    '@blknoiz06': {'pnl': 1.19, 'value': 12.27, 'category': 'Basic'},
    '@cryptorover': {'pnl': 499.31, 'value': 0.05, 'category': 'Basic'},
    
    # 天气类
    '@0x594edB': {'pnl': 30000.00, 'value': 0.00, 'category': 'Weather'},
    
    # BTC高频类
    '@vague-sourdough': {'pnl': 58712.00, 'value': 16900.00, 'category': 'BTC高频'},
    '@Demphu.finite': {'pnl': 91599.00, 'value': 0.00, 'category': 'BTC高频'},
    '@OpenClaw': {'pnl': 386000.00, 'value': 0.00, 'category': 'BTC高频'},
}

COLORS = {
    'NegRisk': '#FF6B6B',
    'Basic': '#4ECDC4',
    'Weather': '#45B7D1',
    'BTC高频': '#96CEB4',
    'profit': '#2ECC71',
    'loss': '#E74C3C'
}

def create_profit_distribution():
    """盈亏分布饼图"""
    
    # 计算盈利/亏损比例
    total_profit = sum([t['pnl'] for t in TRADERS.values() if t['pnl'] > 0])
    total_loss = abs(sum([t['pnl'] for t in TRADERS.values() if t['pnl'] < 0]))
    
    labels = ['Profit', 'Loss']
    sizes = [total_profit, total_loss]
    colors = [COLORS['profit'], COLORS['loss']]
    explode = (0.05, 0)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        explode=explode,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f'${pct/100*(total_profit+total_loss):,.0f}',
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    ax.set_title('Polymarket Trader P&L Distribution\n总盈亏: ${:,.2f}'.format(total_profit - total_loss), 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/polymarket_monitor/chart_profit_distribution.png', dpi=150)
    plt.close()
    
    print('✅ 盈亏分布图已保存')

def create_category_bar():
    """分类盈亏柱状图"""
    
    # 按类别汇总
    category_pnl = defaultdict(float)
    for trader, data in TRADERS.items():
        category_pnl[data['category']] += data['pnl']
    
    categories = list(category_pnl.keys())
    values = [category_pnl[c] for c in categories]
    
    # 颜色
    colors = [COLORS.get(c, '#95A5A6') for c in categories]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.annotate(f'${value:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('P&L ($)', fontsize=12)
    ax.set_title('Polymarket Trader P&L by Category', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linewidth=0.5)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/polymarket_monitor/chart_category.png', dpi=150)
    plt.close()
    
    print('✅ 分类盈亏图已保存')

def create_top_traders():
    """Top Trader排名图"""
    
    # 排序
    sorted_traders = sorted(TRADERS.items(), key=lambda x: x[1]['pnl'], reverse=True)[:10]
    
    names = [t[0] for t in sorted_traders]
    values = [t[1]['pnl'] for t in sorted_traders]
    
    # 颜色
    colors = [COLORS['profit'] if v > 0 else COLORS['loss'] for v in values]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1], edgecolor='white', linewidth=1)
    
    # 添加数值标签
    for bar, value in zip(bars, values[::-1]):
        width = bar.get_width()
        ax.annotate(f'${value:,.0f}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=10, fontweight='bold')
    
    ax.set_xlabel('P&L ($)', fontsize=12)
    ax.set_title('Top 10 Polymarket Traders by P&L', fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/polymarket_monitor/chart_top_traders.png', dpi=150)
    plt.close()
    
    print('✅ Top Trader图已保存')

def create_risk_return():
    """风险收益散点图"""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for trader, data in TRADERS.items():
        category = data['category']
        color = COLORS.get(category, '#95A5A6')
        
        # 盈亏为收益，持仓为风险指标
        ax.scatter(data['value'], data['pnl'], 
                   c=color, s=100, alpha=0.7,
                   edgecolors='white', linewidth=2)
        
        # 添加标签
        if data['pnl'] > 10000 or data['value'] > 10000:
            ax.annotate(trader, 
                       (data['value'], data['pnl']),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.8)
    
    # 图例
    patches = [mpatches.Patch(color=v, label=k) for k, v in COLORS.items() if k != 'profit' and k != 'loss']
    ax.legend(handles=patches, loc='upper left')
    
    ax.set_xlabel('Position Value ($)', fontsize=12)
    ax.set_ylabel('P&L ($)', fontsize=12)
    ax.set_title('Risk-Return Analysis\n(Position Value vs P&L)', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('/root/.openclaw/workspace/polymarket_monitor/chart_risk_return.png', dpi=150)
    plt.close()
    
    print('✅ 风险收益图已保存')

def generate_summary_stats():
    """生成汇总统计"""
    
    total_pnl = sum([t['pnl'] for t in TRADERS.values()])
    active = sum([1 for t in TRADERS.values() if t['value'] > 0 or t['pnl'] != 0])
    profitable = sum([1 for t in TRADERS.values() if t['pnl'] > 0])
    
    stats = {
        'total_traders': len(TRADERS),
        'active_traders': active,
        'profitable_traders': profitable,
        'total_pnl': total_pnl,
        'avg_pnl': total_pnl / len(TRADERS),
        'best_trader': max(TRADERS.items(), key=lambda x: x[1]['pnl']),
        'worst_trader': min(TRADERS.items(), key=lambda x: x[1]['pnl'])
    }
    
    return stats

def main():
    print('='*60)
    print('  Polymarket Trader 数据可视化 v1.0')
    print('='*60)
    print()
    
    # 生成所有图表
    print('📊 生成可视化图表...')
    create_profit_distribution()
    create_category_bar()
    create_top_traders()
    create_risk_return()
    
    # 统计
    print()
    stats = generate_summary_stats()
    
    print()
    print('='*60)
    print('  📈 统计摘要')
    print('='*60)
    print(f'  总Trader数: {stats["total_traders"]}')
    print(f'  活跃Trader: {stats["active_traders"]}')
    print(f'  盈利Trader: {stats["profitable_traders"]}')
    print(f'  总盈亏: ${stats["total_pnl"]:,.2f}')
    print(f'  平均盈亏: ${stats["avg_pnl"]:,.2f}')
    print()
    print(f'  🏆 最佳: {stats["best_trader"][0]} (${stats["best_trader"][1]["pnl"]:,.2f})')
    print(f'  ⚠️  最差: {stats["worst_trader"][0]} (${stats["worst_trader"][1]["pnl"]:,.2f})')
    
    print()
    print('='*60)
    print('  ✅ 图表已保存到 /root/.openclaw/workspace/polymarket_monitor/')
    print('='*60)
    
    print()
    print('生成的文件:')
    print('  📊 chart_profit_distribution.png (盈亏分布)')
    print('  📈 chart_category.png (分类盈亏)')
    print('  🏆 chart_top_traders.png (Top Trader)')
    print('  📉 chart_risk_return.png (风险收益)')

if __name__ == '__main__':
    main()