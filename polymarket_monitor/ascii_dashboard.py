#!/usr/bin/env python3
"""
Polymarket Trader 数据可视化 (ASCII版本)
无需额外依赖
"""

import json
from collections import defaultdict

TRADERS = {
    '@PolycoolApp': {'pnl': 4476569.12, 'value': 11100.00, 'category': 'NegRisk'},
    '@OpenClaw': {'pnl': 386000.00, 'value': 0.00, 'category': 'BTC高频'},
    '@Demphu.finite': {'pnl': 91599.00, 'value': 0.00, 'category': 'BTC高频'},
    '@vague-sourdough': {'pnl': 58712.00, 'value': 16900.00, 'category': 'BTC高频'},
    '@0x594edB': {'pnl': 30000.00, 'value': 0.00, 'category': 'Weather'},
    '@HolyMoses7': {'pnl': 2578.10, 'value': 140400.00, 'category': 'NegRisk'},
    '@copenzafan': {'pnl': -40954.81, 'value': 4888.58, 'category': 'NegRisk'},
    '@cryptorover': {'pnl': 499.31, 'value': 0.05, 'category': 'Basic'},
    '@luishXYZ': {'pnl': 233.87, 'value': 2777.43, 'category': 'NegRisk'},
    '@clawdvine': {'pnl': 104.26, 'value': 0.00, 'category': 'Basic'},
    '@itslirrato': {'pnl': 8.70, 'value': 108.71, 'category': 'NegRisk'},
    '@blknoiz06': {'pnl': 1.19, 'value': 12.27, 'category': 'Basic'},
}

def ascii_bar_chart(data, title, max_width=50):
    """生成ASCII条形图"""
    
    lines = []
    lines.append('\n' + '='*70)
    lines.append(f'  {title}')
    lines.append('='*70 + '\n')
    
    max_val = max([v for v in data.values()]) if data else 1
    scale = max_width / max_val
    
    for name, value in data.items():
        bar_len = int(abs(value) * scale)
        if value >= 0:
            bar = '█' * bar_len
            lines.append(f"{name:20} │ ${value:>12,.2f} │ {bar}")
        else:
            bar = '█' * bar_len
            lines.append(f"{name:20} │ ${value:>12,.2f} │ {bar} (亏损)")
    
    return '\n'.join(lines)

def ascii_pie_chart(data, title):
    """生成ASCII饼图"""
    
    total = sum(data.values())
    if total == 0:
        return ''
    
    lines = []
    lines.append('\n' + '='*70)
    lines.append(f'  {title}')
    lines.append('='*70 + '\n')
    
    for name, value in data.items():
        pct = (value / total) * 100
        bar = '▓' * int(pct / 2)
        lines.append(f"{name:15} │ {pct:5.1f}% │ {bar}")
    
    lines.append(f"\n总计: ${total:,.2f}")
    return '\n'.join(lines)

def generate_all_charts():
    """生成所有图表"""
    
    all_charts = []
    
    # 1. Top 10 Trader盈亏
    sorted_traders = sorted(TRADERS.items(), key=lambda x: x[1]['pnl'], reverse=True)[:10]
    top10 = {t[0]: t[1]['pnl'] for t in sorted_traders}
    all_charts.append(ascii_bar_chart(top10, '🏆 Top 10 Trader P&L'))
    
    # 2. 分类汇总
    category_pnl = defaultdict(float)
    for trader, data in TRADERS.items():
        category_pnl[data['category']] += data['pnl']
    all_charts.append(ascii_pie_chart(dict(category_pnl), '📊 P&L by Category'))
    
    # 3. 分类柱状图
    all_charts.append(ascii_bar_chart(dict(category_pnl), '📈 P&L by Category (Bar)'))
    
    return '\n'.join(all_charts)

def generate_full_dashboard():
    """生成完整仪表板"""
    
    dashboard = []
    dashboard.append('='*70)
    dashboard.append('  📊 Polymarket Trader 数据仪表板 v1.0')
    dashboard.append('='*70)
    dashboard.append(f'  生成时间: 2026-02-17 21:25:00')
    dashboard.append('')
    
    # 统计
    total_pnl = sum([t['pnl'] for t in TRADERS.values()])
    profitable = sum([1 for t in TRADERS.values() if t['pnl'] > 0])
    loss_making = sum([1 for t in TRADERS.values() if t['pnl'] < 0])
    active = sum([1 for t in TRADERS.values() if t['value'] > 0 or t['pnl'] != 0])
    
    dashboard.append('┌─────────────────────────────────────────┐')
    dashboard.append('│           📈 关键指标                    │')
    dashboard.append('├─────────────────────────────────────────┤')
    dashboard.append(f'│  总Trader数     │ {len(TRADERS):>10}                │')
    dashboard.append(f'│  活跃Trader     │ {active:>10}                │')
    dashboard.append(f'│  盈利Trader     │ {profitable:>10}                │')
    dashboard.append(f'│  亏损Trader     │ {loss_making:>10}                │')
    dashboard.append(f'│  ─────────────────────────────────────── │')
    dashboard.append(f'│  💰 总盈亏       │ ${total_pnl:>12,.2f}         │')
    dashboard.append('└─────────────────────────────────────────┘')
    dashboard.append('')
    
    # 图表
    dashboard.append(generate_all_charts())
    
    # 风险分析
    dashboard.append('\n' + '='*70)
    dashboard.append('  ⚠️ 风险分析')
    dashboard.append('='*70 + '\n')
    
    high_risk = [(n, d) for n, d in TRADERS.items() if d['pnl'] < -10000]
    high_profit = [(n, d) for n, d in TRADERS.items() if d['pnl'] > 100000]
    
    if high_risk:
        dashboard.append('🚨 高风险Trader (亏损 >$10K):')
        for n, d in high_risk:
            dashboard.append(f'   - {n}: ${d["pnl"]:,.2f}')
        dashboard.append('')
    
    if high_profit:
        dashboard.append('💎 高收益Trader (盈利 >$100K):')
        for n, d in high_profit:
            dashboard.append(f'   - {n}: ${d["pnl"]:,.2f}')
        dashboard.append('')
    
    # 建议
    dashboard.append('📋 跟单建议:')
    dashboard.append('   1. @PolycoolApp 盈利最高，但需分析策略')
    dashboard.append('   2. @OpenClaw 月赚$386K，高频套利')
    dashboard.append('   3. @Demphu.finite 盈利率最高(65次预测)')
    dashboard.append('   4. 避免@copenzafan (亏损$40K)')
    dashboard.append('')
    
    return '\n'.join(dashboard)

def save_to_file():
    """保存到文件"""
    
    dashboard = generate_full_dashboard()
    
    output_dir = '/root/.openclaw/workspace/polymarket_monitor'
    
    # 保存ASCII仪表板
    with open(f'{output_dir}/dashboard.txt', 'w', encoding='utf-8') as f:
        f.write(dashboard)
    
    # 保存JSON数据
    json_path = f'{output_dir}/dashboard_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generatedAt': '2026-02-17T21:25:00Z',
            'summary': {
                'total_traders': len(TRADERS),
                'profitable': sum([1 for t in TRADERS.values() if t['pnl'] > 0]),
                'loss_making': sum([1 for t in TRADERS.values() if t['pnl'] < 0]),
                'total_pnl': sum([t['pnl'] for t in TRADERS.values()])
            },
            'traders': TRADERS
        }, f, indent=2, ensure_ascii=False)
    
    print(f'✅ 仪表板已保存: {output_dir}/dashboard.txt')
    print(f'✅ JSON数据已保存: {json_path}')

def main():
    print('='*70)
    print('  📊 Polymarket Trader 数据可视化 v1.0 (ASCII)')
    print('='*70)
    print()
    
    # 生成并显示仪表板
    dashboard = generate_full_dashboard()
    print(dashboard)
    
    # 保存
    save_to_file()
    
    print()
    print('='*70)
    print('  ✅ 完成!')
    print('='*70)

if __name__ == '__main__':
    main()