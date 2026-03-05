#!/usr/bin/env python3
"""
Polymarket NegRisk Arbitrage Monitor
=====================================
Tan (Chief Quant) - 监控 Finance 市场的 YES+NO < 1 套利机会

当 YES + NO 价格之和 < 1 时,买入 YES + NO,无论如何都盈利!
"""

import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# 配置
TELEGRAM_BOT_TOKEN = "8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4"
REPORT_CHAT_ID = "8591571345"

@dataclass
class Market:
    """市场数据"""
    id: str
    question: str
    yes_price: float
    no_price: float
    volume: float
    active: bool
    
    @property
    def total_price(self) -> float:
        return self.yes_price + self.no_price
    
    @property
    def arb_profit(self) -> float:
        """套利利润 (如果 YES+NO < 1)"""
        return 1 - self.total_price
    
    @property
    def arb_profit_pct(self) -> float:
        """套利利润百分比"""
        if self.total_price < 1:
            return self.arb_profit * 100
        return 0
    
    @property
    def is_arb_opportunity(self) -> bool:
        """是否是套利机会"""
        return self.total_price < 0.99  # 1% 缓冲


class ArbitrageMonitor:
    """套利机会监控器"""
    
    def __init__(self, min_volume: float = 10000, min_profit: float = 0.5):
        """
        min_volume: 最小交易量 ($)
        min_profit: 最小套利利润 (%)
        """
        self.min_volume = min_volume
        self.min_profit = min_profit
        self.opportunities: List[Market] = []
        self.history: List[Dict] = []
    
    def fetch_markets(self, category: str = "finance") -> List[Market]:
        """获取市场数据"""
        try:
            # 获取活跃市场
            result = subprocess.run(
                ["polymarket", "-o", "json", "markets", "list", 
                 "--active", "true", "--limit", "200"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return []
            
            markets_data = json.loads(result.stdout)
            markets = []
            
            for m in markets_data:
                question = m.get('question', '').lower()
                
                # 过滤 Finance 相关市场
                if category == "finance":
                    keywords = ['fed', 'rate', 'interest', 'inflation', 'gdp', 
                               'economy', 'economic', 'treasury', 'dollar', 'usd',
                               'stock', 'market', 'recession', 'unemployment',
                               'poll', 'election', 'president', 'congress',
                               'tariff', 'trade', 'china', 'eu', 'europe']
                    if not any(kw in question for kw in keywords):
                        continue
                
                # 解析价格
                outcome_prices = m.get('outcomePrices')
                if not outcome_prices:
                    continue
                
                try:
                    prices = json.loads(outcome_prices)
                    if len(prices) >= 2:
                        yes_price = float(prices[0])
                        no_price = float(prices[1])
                    else:
                        continue
                except:
                    continue
                
                volume = float(m.get('volumeNum', 0))
                
                # 过滤交易量
                if volume < self.min_volume:
                    continue
                
                market = Market(
                    id=m.get('id', ''),
                    question=m.get('question', '')[:60],
                    yes_price=yes_price,
                    no_price=no_price,
                    volume=volume,
                    active=m.get('active', True)
                )
                
                markets.append(market)
            
            return markets
            
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []
    
    def find_arbitrage(self, markets: List[Market]) -> List[Market]:
        """寻找套利机会"""
        opportunities = []
        
        for m in markets:
            # 检查 YES + NO < 1 (允许一点误差)
            if m.is_arb_opportunity and m.arb_profit_pct >= self.min_profit:
                opportunities.append(m)
        
        # 按利润排序
        opportunities.sort(key=lambda x: x.arb_profit_pct, reverse=True)
        
        return opportunities
    
    def analyze_market_pairs(self, markets: List[Market]) -> List[Dict]:
        """分析关联市场的套利机会"""
        # 寻找可能相关的市场对
        opportunities = []
        
        # 按关键字分组
        groups = {}
        for m in markets:
            # 提取关键词
            keywords = []
            q = m.question.lower()
            if 'fed' in q or 'rate' in q:
                keywords.append('fed')
            if 'election' in q or 'president' in q or 'trump' in q:
                keywords.append('election')
            if 'recession' in q or 'economy' in q:
                keywords.append('economy')
            if 'china' in q or 'tariff' in q:
                keywords.append('china')
            
            for kw in keywords:
                if kw not in groups:
                    groups[kw] = []
                groups[kw].append(m)
        
        # 检查组内是否有套利机会
        for kw, group_markets in groups.items():
            # 检查单个市场内部 YES+NO
            for m in group_markets:
                if m.arb_profit_pct >= self.min_profit:
                    opportunities.append({
                        'type': 'intra_market',
                        'market': m,
                        'profit': m.arb_profit_pct,
                        'keywords': kw
                    })
        
        return opportunities
    
    def format_report(self, opportunities: List[Market]) -> str:
        """生成报告"""
        if not opportunities:
            return "📊 Finance 市场套利监控\n\n⏰ {time}\n\n✅ 未发现套利机会 (YES+NO < 1)\n\n最小交易量: ${volume:,.0f}\n最小利润: {profit:.1f}%".format(
                time=datetime.now().strftime("%H:%M:%S UTC"),
                volume=self.min_volume,
                profit=self.min_profit
            )
        
        report = "📊 **Finance 市场套利机会!**\n"
        report += f"⏰ {datetime.now().strftime('%H:%M:%S UTC')}\n\n"
        
        for i, m in enumerate(opportunities[:10], 1):
            report += f"**{i}. {m.question}**\n"
            report += f"   💰 YES: ${m.yes_price:.4f} | NO: ${m.no_price:.4f}\n"
            report += f"   📈 合计: ${m.total_price:.4f} | 🎯 套利: **{m.arb_profit_pct:.2f}%**\n"
            report += f"   💵 交易量: ${m.volume:,.0f}\n\n"
        
        report += f"---\n"
        report += f"找到 {len(opportunities)} 个机会\n"
        report += f"最小交易量: ${self.min_volume:,.0f}\n"
        
        return report
    
    def run(self) -> str:
        """运行监控"""
        print(f"🔍 扫描 Finance 市场套利机会...")
        
        markets = self.fetch_markets("finance")
        print(f"   获取 {len(markets)} 个市场")
        
        opportunities = self.find_arbitrage(markets)
        print(f"   发现 {len(opportunities)} 个套利机会")
        
        self.opportunities = opportunities
        
        # 记录历史
        self.history.append({
            'time': datetime.now().isoformat(),
            'opportunities': len(opportunities),
            'top_opportunity': opportunities[0].arb_profit_pct if opportunities else 0
        })
        
        return self.format_report(opportunities)


def send_telegram(message: str):
    """发送到 Telegram"""
    try:
        import urllib.request
        import urllib.parse
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': REPORT_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def main():
    import sys
    
    # 设置
    min_volume = 10000  # 最小 $10K 交易量
    min_profit = 0.5    # 最小 0.5% 利润
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            # 测试模式
            min_volume = 1000
            min_profit = 0.1
    
    print("=" * 50)
    print("🎯 Polymarket Finance 套利监控")
    print("=" * 50)
    print(f"最小交易量: ${min_volume:,}")
    print(f"最小利润: {min_profit}%")
    print()
    
    monitor = ArbitrageMonitor(min_volume=min_volume, min_profit=min_profit)
    report = monitor.run()
    
    print("\n" + report)
    
    # 如果有套利机会,发送到 Telegram
    if monitor.opportunities:
        send_telegram(report)


if __name__ == "__main__":
    main()