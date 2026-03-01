#!/usr/bin/env python3
"""
Polymarket Trader 分析报告 v1.2
包含新增的2个Trader (@mikocrypto11, @xpredicter)
"""

import json
from datetime import datetime
from collections import defaultdict

# 完整Trader数据 v1.2
TRADERS = {
    # NegRisk类 (C)
    '@PolycoolApp': {'pnl': 4476569.12, 'value': 11100.00, 'category': 'NegRisk', 'status': '活跃'},
    '@HolyMoses7': {'pnl': 2578.10, 'value': 140400.00, 'category': 'NegRisk', 'status': '活跃'},
    '@copenzafan': {'pnl': -40954.81, 'value': 4888.58, 'category': 'NegRisk', 'status': '亏损'},
    '@luishXYZ': {'pnl': 233.87, 'value': 2777.43, 'category': 'NegRisk', 'status': '活跃'},
    '@clawdvine': {'pnl': 104.26, 'value': 0.00, 'category': 'Basic', 'status': '活跃'},
    '@cryptorover': {'pnl': 499.31, 'value': 0.05, 'category': 'Basic', 'status': '活跃'},
    '@itslirrato': {'pnl': 8.70, 'value': 108.71, 'category': 'NegRisk', 'status': '活跃'},
    '@blknoiz06': {'pnl': 1.19, 'value': 12.27, 'category': 'Basic', 'status': '活跃'},
    
    # BTC高频类 (F)
    '@OpenClaw': {'pnl': 386000.00, 'value': 0.00, 'category': 'BTC高频', 'status': '活跃'},
    '@Demphu.finite': {'pnl': 91599.00, 'value': 0.00, 'category': 'BTC高频', 'status': '活跃'},
    '@vague-sourdough': {'pnl': 58712.00, 'value': 16900.00, 'category': 'BTC高频', 'status': '活跃'},
    '@0x594edB': {'pnl': 30000.00, 'value': 0.00, 'category': 'Weather', 'status': '活跃'},
    
    # 新增 - 待验证 (G) - v1.2
    '@mikocrypto11': {'pnl': 0.00, 'value': 0.00, 'category': '待验证', 'status': '待验证'},
    '@xpredicter': {'pnl': 0.00, 'value': 0.00, 'category': '待验证', 'status': '待验证'},
}

def generate_dashboard_v1_2():
    """生成v1.2仪表板"""
    
    total_pnl = sum([t['pnl'] for t in TRADERS.values()])
    active = sum([1 for t in TRADERS.values() if t['status'] == '活跃'])
    profitable = sum([1 for t in TRADERS.values() if t['pnl'] > 0])
    loss_making = sum([1 for t in TRADERS.values() if t['pnl'] < 0])
    
    dashboard = []
    dashboard.append('='*70)
    dashboard.append('  📊 Polymarket Trader 数据仪表板 v1.2')
    dashboard.append('='*70)
    dashboard.append(f'  更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    dashboard.append(f'  数据来源: v1.2增量更新 (新增2个Trader)')
    dashboard.append('')
    
    # 关键指标
    dashboard.append('┌─────────────────────────────────────────┐')
    dashboard.append('│           📈 关键指标 (v1.2)              │')
    dashboard.append('├─────────────────────────────────────────┤')
    dashboard.append(f'│  总Trader数     │ {len(TRADERS):>10}                │')
    dashboard.append(f'│  活跃Trader     │ {active:>10}                │')
    dashboard.append(f'│  盈利Trader     │ {profitable:>10}                │')
    dashboard.append(f'│  亏损Trader     │ {loss_making:>10}                │')
    dashboard.append(f'│  待验证         │ {2:>10}                │')
    dashboard.append(f'│  ─────────────────────────────────────── │')
    dashboard.append(f'│  💰 总盈亏       │ ${total_pnl:>12,.2f}         │')
    dashboard.append('└─────────────────────────────────────────┘')
    dashboard.append('')
    
    # Top 10
    sorted_traders = sorted(TRADERS.items(), key=lambda x: x[1]['pnl'], reverse=True)[:10]
    
    dashboard.append('='*70)
    dashboard.append('  🏆 Top 10 Trader P&L')
    dashboard.append('='*70 + '\n')
    
    max_val = sorted_traders[0][1]['pnl'] if sorted_traders else 1
    scale = 40 / max_val
    
    for name, data in sorted_traders:
        bar_len = int(data['pnl'] * scale)
        bar = '█' * bar_len if data['pnl'] > 0 else '░'
        dashboard.append(f"{name:20} │ ${data['pnl']:>12,.2f} │ {bar}")
    
    # 新增Trader
    dashboard.append('')
    dashboard.append('='*70)
    dashboard.append('  🆕 v1.2 新增Trader')
    dashboard.append('='*70 + '\n')
    dashboard.append('G1 @mikocrypto11 │ Polymarket trader, 预测市场分析 │ 待验证')
    dashboard.append('G2 @xpredicter │ X上活跃的预测市场Trader │ 待验证')
    dashboard.append('')
    
    # 分类统计
    category_pnl = defaultdict(float)
    for trader, data in TRADERS.items():
        category_pnl[data['category']] += data['pnl']
    
    dashboard.append('='*70)
    dashboard.append('  📊 分类统计')
    dashboard.append('='*70 + '\n')
    
    for cat, pnl in sorted(category_pnl.items(), key=lambda x: x[1], reverse=True):
        bar = '█' * int(abs(pnl) / 100000) if pnl > 0 else '░'
        dashboard.append(f"{cat:15} │ ${pnl:>12,.2f} │ {bar}")
    
    return '\n'.join(dashboard)

def save_v1_2():
    """保存v1.2更新"""
    
    dashboard = generate_dashboard_v1_2()
    
    output_dir = '/root/.openclaw/workspace/polymarket_monitor'
    
    # 保存仪表板
    with open(f'{output_dir}/dashboard_v1.2.txt', 'w', encoding='utf-8') as f:
        f.write(dashboard)
    
    # 保存JSON
    with open(f'{output_dir}/traders_v1.2.json', 'w', encoding='utf-8') as f:
        json.dump({
            'version': 'v1.2',
            'updatedAt': datetime.now().isoformat(),
            'newTraders': ['@mikocrypto11', '@xpredicter'],
            'totalTraders': len(TRADERS),
            'traders': TRADERS
        }, f, indent=2, ensure_ascii=False)
    
    print(f'✅ v1.2已保存:')
    print(f'   📄 dashboard_v1.2.txt')
    print(f'   📊 traders_v1.2.json')

def main():
    print('='*70)
    print('  Polymarket Trader v1.2 增量更新')
    print('='*70)
    print()
    
    dashboard = generate_dashboard_v1_2()
    print(dashboard)
    
    save_v1_2()
    
    print()
    print('='*70)
    print('  ✅ v1.2 更新完成!')
    print('='*70)

if __name__ == '__main__':
    main()