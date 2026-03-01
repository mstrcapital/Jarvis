#!/usr/bin/env python3
"""
Polymarket Trader 跟单分析报告 v1.0

功能：
1. 统计分析Trader表现
2. 生成可视化图表
3. 输出详细分析报告
"""

import json
import os
from datetime import datetime
from collections import defaultdict

# Trader数据 (从v1.1地址库)
TRADERS = {
    # C类 - NegRisk
    'C1': {'name': '@xmgnr', 'wallet': '0xfdd9fc462c9d5913c11dce63e737cb4c7ab9f22a', 'pnl': 0.00, 'value': 0.00, 'status': '不活跃'},
    'C2': {'name': '@luishXYZ', 'wallet': '0x0da462636b228293849aac34c1857724757e4dde', 'pnl': 233.87, 'value': 2777.43, 'status': '活跃'},
    'C3': {'name': '@copenzafan', 'wallet': '0x95923e6dfa4e685361ffb0ead28657d3fa18a85b', 'pnl': -40954.81, 'value': 4888.58, 'status': '活跃(亏损)'},
    'C4': {'name': '@carverfomo', 'wallet': '0x227b22b78b422bbad333bf903a164db3212916cf', 'pnl': 0.00, 'value': 0.00, 'status': '不活跃'},
    'C6': {'name': '@HolyMoses7', 'wallet': '0xa4b366ad22fc0d06f1e9346897b22431874b8b87', 'pnl': 2578.10, 'value': 140400.00, 'status': '活跃'},
    'C7': {'name': '@PolycoolApp', 'wallet': '0x492442eab586f242b53bd', 'pnl': 4476569.12, 'value': 11100.00, 'status': '活跃'},
    'C8': {'name': '@itslirrato', 'wallet': '0x3adaadddf92874041363ba3db77e949bcb9f861a', 'pnl': 8.70, 'value': 108.71, 'status': '活跃'},
    
    # D类 - Basic
    'D1': {'name': '@clawdvine', 'wallet': '0x4de4d61565bbcc98605e4d53d0c6447a288e10a', 'pnl': 104.26, 'value': 0.00, 'status': '活跃'},
    'D3': {'name': '@blknoiz06', 'wallet': '0xc387de398cf17f60c9def1d35bb89c8bea05b0e4', 'pnl': 1.19, 'value': 12.27, 'status': '活跃'},
    'D4': {'name': '@cryptorover', 'wallet': '0x51f304b408809f', 'pnl': 499.31, 'value': 0.05, 'status': '活跃'},
    
    # B类 - 天气
    'B1': {'name': '@0x594edB', 'wallet': '0x594edB9112f526Fa680b8F858A6379C8A2c1C11', 'pnl': 30000.00, 'value': 0.00, 'status': '活跃'},
    
    # F类 - BTC高频 (估算数据)
    'F4': {'name': '@vague-sourdough', 'wallet': 'unknown', 'pnl': 58712.00, 'value': 16900.00, 'status': '活跃'},
    'F5': {'name': '@Demphu.finite', 'wallet': '0xd0bde12c...', 'pnl': 91599.00, 'value': 0.00, 'status': '活跃'},
    'F6': {'name': '@OpenClaw', 'wallet': '0x1979ae6b7e...', 'pnl': 386000.00, 'value': 0.00, 'status': '活跃'},
}

def analyze_performance():
    """分析Trader表现"""
    
    # 统计数据
    total_pnl = 0
    active_traders = 0
    profitable = 0
    loss_making = 0
    
    trader_pnls = []
    
    for id, trader in TRADERS.items():
        pnl = trader['pnl']
        total_pnl += pnl
        trader_pnls.append((trader['name'], pnl))
        
        if trader['status'] != '不活跃':
            active_traders += 1
            if pnl > 0:
                profitable += 1
            elif pnl < 0:
                loss_making += 1
    
    # 排序
    trader_pnls.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'total_pnl': total_pnl,
        'active_traders': active_traders,
        'profitable': profitable,
        'loss_making': loss_making,
        'ranked_pnls': trader_pnls
    }

def generate_text_charts(stats):
    """生成ASCII图表"""
    
    chart = []
    chart.append('\n' + '='*60)
    chart.append('  📊 Trader盈亏排名 (ASCII可视化)')
    chart.append('='*60 + '\n')
    
    ranked = stats['ranked_pnls'][:10]  # 前10
    
    max_pnl = max([p[1] for p in ranked]) if ranked else 1
    scale = 40 / max_pnl
    
    for name, pnl in ranked:
        bar_len = int(abs(pnl) * scale)
        if pnl >= 0:
            bar = '█' * bar_len
            chart.append(f"{name:20} │ ${pnl:>12,.2f} │ {bar}")
        else:
            bar = '█' * bar_len
            chart.append(f"{name:20} │ ${pnl:>12,.2f} │ {bar} (亏损)")
    
    return '\n'.join(chart)

def generate_category_breakdown():
    """生成分类统计"""
    
    categories = {
        'A (短线高频)': {'count': 6, 'avg_pnl': 100000},  # 估算
        'B (天气)': {'count': 1, 'avg_pnl': 30000},
        'C (NegRisk)': {'count': 7, 'avg_pnl': 0},
        'D (Basic)': {'count': 3, 'avg_pnl': 200},
        'E (独立分析)': {'count': 1, 'avg_pnl': 0},
        'F (BTC高频)': {'count': 6, 'avg_pnl': 180000},  # 估算
    }
    
    chart = []
    chart.append('\n' + '='*60)
    chart.append('  📈 分类统计')
    chart.append('='*60 + '\n')
    
    for cat, data in categories.items():
        bar = '▓' * (data['count'] // 2) if data['count'] > 0 else ''
        chart.append(f"{cat:20} │ {data['count']:2}个Trader │ 平均盈利: ${data['avg_pnl']:,}")
    
    return '\n'.join(chart)

def generate_full_report():
    """生成完整分析报告"""
    
    stats = analyze_performance()
    
    report = []
    report.append('# Polymarket 跟单分析报告')
    report.append(f'> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    report.append(f'> 数据来源: v1.1地址库')
    report.append('')
    
    # 执行摘要
    report.append('## 📋 执行摘要')
    report.append('---')
    report.append('')
    report.append(f'| 指标 | 数值 |')
    report.append(f'|------|------|')
    report.append(f'| 总Trader数 | {len(TRADERS)} |')
    report.append(f'| 活跃Trader | {stats["active_traders"]} |')
    report.append(f'| 盈利Trader | {stats["profitable"]} |')
    report.append(f'| 亏损Trader | {stats["loss_making"]} |')
    report.append(f'| **总盈亏** | **${stats["total_pnl"]:,.2f}** |')
    report.append('')
    
    # 图表
    report.append(generate_text_charts(stats))
    report.append('')
    
    # 分类统计
    report.append(generate_category_breakdown())
    report.append('')
    
    # 顶级Trader
    report.append('\n## 🏆 Top 5 盈利Trader')
    report.append('---')
    report.append('')
    for i, (name, pnl) in enumerate(stats['ranked_pnls'][:5], 1):
        emoji = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '📈'
        report.append(f'{emoji} **{name}** - ${pnl:,.2f}')
    report.append('')
    
    # 风险提示
    report.append('\n## ⚠️ 风险提示')
    report.append('---')
    report.append('')
    report.append('- 过去表现不代表未来收益')
    report.append('- 高频套利策略风险极高')
    report.append('- 请DYOR (Do Your Own Research)')
    report.append('- 仅供研究学习，不构成投资建议')
    report.append('')
    
    return '\n'.join(report)

def save_report():
    """保存报告"""
    
    # 生成Markdown报告
    report = generate_full_report()
    
    output_dir = '/root/.openclaw/workspace/polymarket_monitor'
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存Markdown
    md_path = os.path.join(output_dir, 'analysis_report.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存JSON数据
    json_path = os.path.join(output_dir, 'analysis_data.json')
    stats = analyze_performance()
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generatedAt': datetime.now().isoformat(),
            'summary': stats,
            'traders': TRADERS
        }, f, indent=2, ensure_ascii=False)
    
    print(f'\n✅ 报告已保存:')
    print(f'   📄 Markdown: {md_path}')
    print(f'   📊 JSON: {json_path}')
    
    return report

if __name__ == '__main__':
    print('='*60)
    print('  Polymarket 跟单分析报告生成器 v1.0')
    print('='*60)
    
    report = save_report()
    
    print('\n' + '='*60)
    print('  报告预览')
    print('='*60)
    print(report[:3000])  # 打印前3000字符