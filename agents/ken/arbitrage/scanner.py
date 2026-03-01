#!/usr/bin/env python3
"""
Ken 套利扫描器
监控 Polymarket, Kalshi 价格差异
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, List

class ArbitrageScanner:
    """套利机会扫描器"""
    
    def __init__(self):
        self.results = []
        
    async def fetch_polymarket(self) -> List[Dict]:
        """获取 Polymarket 市场数据"""
        markets = []
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://gamma-api.polymarket.com/markets"
                params = {"closed": "false", "limit": "100"}
                async with session.get(url, params=params) as resp:
                    data = await resp.json()
                    for m in data:
                        if m.get('volume24hr', 0) > 50000:  # 高流动性
                            markets.append({
                                'platform': 'Polymarket',
                                'question': m.get('question', ''),
                                'yes_price': float(m.get('yesPrice', 0.5)),
                                'no_price': float(m.get('noPrice', 0.5)),
                                'volume': m.get('volume24hr', 0)
                            })
        except Exception as e:
            print(f"Polymarket error: {e}")
        return markets
    
    async def fetch_kalshi(self) -> List[Dict]:
        """获取 Kalshi 市场数据"""
        markets = []
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.kalshi.com/trade-api/v2/markets"
                headers = {"Accept": "application/json"}
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for m in data.get('markets', []):
                            if m.get('volume24h', 0) > 50000:
                                yes_ask = float(m.get('yes_ask', 0.5) or 0.5)
                                no_ask = float(m.get('no_ask', 0.5) or 0.5)
                                markets.append({
                                    'platform': 'Kalshi',
                                    'question': m.get('title', ''),
                                    'yes_price': 1 - no_ask if yes_ask > 0 else 0.5,
                                    'no_price': 1 - yes_ask if no_ask > 0 else 0.5,
                                    'volume': m.get('volume24h', 0)
                                })
        except Exception as e:
            print(f"Kalshi error: {e}")
        return markets
    
    def find_arbitrage(self, polymarket: List[Dict], kalshi: List[Dict]) -> List[Dict]:
        """寻找套利机会"""
        opportunities = []
        
        for pm in polymarket:
            pm_q = pm['question'].lower()
            for kl in kalshi:
                kl_q = kl['question'].lower()
                
                # 简单匹配
                common = set(pm_q.split()) & set(kl_q.split())
                if len(common) >= 2:
                    yes_diff = abs(pm['yes_price'] - kl['yes_price'])
                    no_diff = abs(pm['no_price'] - kl['no_price'])
                    
                    if yes_diff > 0.03 or no_diff > 0.03:
                        opportunities.append({
                            'timestamp': datetime.now().isoformat(),
                            'event': pm['question'][:80],
                            'platforms': ['Polymarket', 'Kalshi'],
                            'polymarket_yes': pm['yes_price'],
                            'kalshi_yes': kl['yes_price'],
                            'profit_pct': max(yes_diff, no_diff) * 100
                        })
        
        return sorted(opportunities, key=lambda x: x['profit_pct'], reverse=True)[:5]
    
    async def scan(self) -> Dict:
        """执行扫描"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 套利扫描中...")
        
        polymarket, kalshi = await asyncio.gather(
            self.fetch_polymarket(),
            self.fetch_kalshi()
        )
        
        opportunities = self.find_arbitrage(polymarket, kalshi)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'markets_scanned': len(polymarket) + len(kalshi),
            'opportunities': opportunities
        }

async def main():
    scanner = ArbitrageScanner()
    result = await scanner.scan()
    
    print("\n" + "="*50)
    print(f"📊 套利扫描 - {result['timestamp']}")
    print("="*50)
    print(f"扫描市场: {result['markets_scanned']}")
    print(f"发现机会: {len(result['opportunities'])}")
    
    if result['opportunities']:
        print("\n🔥 Top 机会:")
        for i, o in enumerate(result['opportunities'][:3], 1):
            print(f"\n{i}. {o['event']}")
            print(f"   Polymarket YES: {o['polymarket_yes']:.1%}")
            print(f"   Kalshi YES: {o['kalshi_yes']:.1%}")
            print(f"   利润空间: {o['profit_pct']:.1f}%")
    
    # 保存结果
    with open('/root/.openclaw/workspace/agents/ken/arbitrage/latest.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    return result

if __name__ == "__main__":
    asyncio.run(main())