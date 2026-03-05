#!/usr/bin/env python3
"""
Polymarket Finance Market Monitor - Liquidity & VPIN
=====================================================
Tan (Chief Quant) - 监控 Finance 市场的流动性和毒性

监控:
- 流动性枯竭 (spread 异常大)
- VPIN 毒性 (买卖单不平衡)
- 价格剧烈波动
"""

import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque
import math

# 配置
TELEGRAM_BOT_TOKEN = "8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4"
REPORT_CHAT_ID = "8591571345"

@dataclass
class Market:
    """市场数据"""
    id: str
    question: str
    price: float
    spread: float
    spread_pct: float
    volume: float
    volume_24h: float
    best_bid: float
    best_ask: float
    liquidity: float
    active: bool
    
    @property
    def is_low_liquidity(self) -> bool:
        """流动性低 (spread > 5% 或 交易量低)"""
        return self.spread_pct > 5 or self.volume < 10000
    
    @property
    def liquidity_score(self) -> float:
        """流动性评分 (0-100)"""
        # 基于 spread 和 volume 的综合评分
        spread_score = max(0, 100 - self.spread_pct * 10)  # spread 越低越好
        volume_score = min(100, self.volume / 1000)  # volume 越高越好
        return (spread_score * 0.7 + volume_score * 0.3)


class FinanceMonitor:
    """Finance 市场监控器"""
    
    def __init__(self):
        self.markets: List[Market] = []
        self.price_history: Dict[str, deque] = {}  # 价格历史
        self.alerts: List[str] = []
        self.history: List[Dict] = []
        
        # 阈值
        self.spread_warning = 3      # 3% spread 警告
        self.spread_critical = 5     # 5% spread 危险
        self.volume_warning = 5000   # $5K 以下低量
        self.price_change_warning = 5   # 5% 价格变化警告
        
        # 历史记录
        self.max_history = 50
    
    def fetch_markets(self) -> List[Market]:
        """获取 Finance 市场数据"""
        try:
            result = subprocess.run(
                ["polymarket", "-o", "json", "markets", "list", 
                 "--active", "true", "--limit", "200"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                return []
            
            markets_data = json.loads(result.stdout)
            markets = []
            
            # Finance 关键词
            finance_keywords = ['fed', 'rate', 'interest', 'inflation', 'gdp', 
                               'economy', 'economic', 'treasury', 'dollar', 'usd',
                               'stock', 'market', 'recession', 'unemployment',
                               'poll', 'election', 'president', 'congress',
                               'tariff', 'trade', 'china', 'eu', 'europe',
                               'bitcoin', 'btc', 'ethereum', 'eth', 'crypto']
            
            for m in markets_data:
                question = m.get('question', '').lower()
                
                # 过滤 Finance/Crypto 相关
                if not any(kw in question for kw in finance_keywords):
                    continue
                
                # 解析价格
                outcome_prices = m.get('outcomePrices')
                if not outcome_prices:
                    continue
                
                try:
                    prices = json.loads(outcome_prices)
                    if len(prices) >= 2:
                        yes_price = float(prices[0])
                        price = yes_price
                    else:
                        continue
                except:
                    continue
                
                # Spread
                spread = m.get('spread', 0)
                try:
                    spread = float(spread) if spread else 0
                except:
                    spread = 0
                
                # Best bid/ask
                best_bid = m.get('bestBid', 0)
                best_ask = m.get('bestAsk', 0)
                try:
                    best_bid = float(best_bid) if best_bid else 0
                    best_ask = float(best_ask) if best_ask else 0
                except:
                    best_bid, best_ask = 0, 0
                
                # 计算 spread 百分比
                if best_bid > 0 and best_ask > 0:
                    spread_pct = ((best_ask - best_bid) / ((best_bid + best_ask) / 2)) * 100
                else:
                    spread_pct = spread * 100 if spread > 0 else 0
                
                # 交易量
                volume = float(m.get('volumeNum', 0))
                volume_24h = float(m.get('volume24hr', 0))
                
                # 流动性
                liquidity = float(m.get('liquidityNum', 0))
                
                market = Market(
                    id=m.get('id', ''),
                    question=m.get('question', '')[:60],
                    price=price,
                    spread=spread,
                    spread_pct=spread_pct,
                    volume=volume,
                    volume_24h=volume_24h,
                    best_bid=best_bid,
                    best_ask=best_ask,
                    liquidity=liquidity,
                    active=m.get('active', True)
                )
                
                markets.append(market)
                
                # 更新价格历史
                if market.id not in self.price_history:
                    self.price_history[market.id] = deque(maxlen=self.max_history)
                self.price_history[market.id].append({
                    'time': time.time(),
                    'price': price,
                    'spread': spread_pct
                })
            
            self.markets = markets
            return markets
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def check_liquidity_alerts(self) -> List[Dict]:
        """检查流动性告警"""
        alerts = []
        
        for m in self.markets:
            # Spread 告警
            if m.spread_pct > self.spread_critical:
                alerts.append({
                    'type': 'spread_critical',
                    'severity': '🔴',
                    'market': m,
                    'message': f"Spread 危险: {m.spread_pct:.1f}%"
                })
            elif m.spread_pct > self.spread_warning:
                alerts.append({
                    'type': 'spread_warning',
                    'severity': '🟡',
                    'market': m,
                    'message': f"Spread 警告: {m.spread_pct:.1f}%"
                })
            
            # 交易量告警
            if m.volume < self.volume_warning:
                alerts.append({
                    'type': 'volume_low',
                    'severity': '🟡',
                    'market': m,
                    'message': f"交易量低: ${m.volume:,.0f}"
                })
        
        return alerts
    
    def check_price_alerts(self) -> List[Dict]:
        """检查价格剧烈波动"""
        alerts = []
        
        for m in self.markets:
            history = self.price_history.get(m.id, [])
            if len(history) < 2:
                continue
            
            # 检查最近价格变化
            recent = list(history)[-5:]
            if len(recent) >= 2:
                price_change = abs(recent[-1]['price'] - recent[0]['price']) / recent[0]['price'] * 100
                
                if price_change > self.price_change_warning:
                    alerts.append({
                        'type': 'price_volatile',
                        'severity': '🟠',
                        'market': m,
                        'message': f"价格波动: {price_change:.1f}%"
                    })
        
        return alerts
    
    def simulate_vpin(self) -> List[Dict]:
        """
        模拟 VPIN (基于价格趋势)
        
        真正的 VPIN 需要真实的成交数据
        这里用价格动量作为代理指标
        """
        alerts = []
        
        for m in self.markets:
            history = list(self.price_history.get(m.id, []))
            if len(history) < 5:
                continue
            
            # 计算动量 (简化版 VPIN)
            recent_prices = [h['price'] for h in history[-5:]]
            
            # 如果价格持续上涨,可能是买盘压力
            # 如果价格持续下跌,可能是卖盘压力
            increases = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
            decreases = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
            
            total = increases + decreases
            if total > 0:
                imbalance = abs(increases - decreases) / total
                
                # 极端不平衡可能是毒性信号
                if imbalance > 0.7:  # 70% 一边倒
                    direction = "↑ 买盘" if increases > decreases else "↓ 卖盘"
                    alerts.append({
                        'type': 'vpin_simulated',
                        'severity': '🧪',
                        'market': m,
                        'imbalance': imbalance,
                        'direction': direction,
                        'message': f"毒性信号: {direction} ({imbalance:.0%} 一边倒)"
                    })
        
        return alerts
    
    def get_liquidity_report(self) -> str:
        """生成流动性报告"""
        if not self.markets:
            return "❌ 无法获取市场数据"
        
        # 按 spread 排序
        sorted_markets = sorted(self.markets, key=lambda x: x.spread_pct, reverse=True)
        
        # 分类
        critical = [m for m in sorted_markets if m.spread_pct > self.spread_critical]
        warning = [m for m in sorted_markets if self.spread_warning < m.spread_pct <= self.spread_critical]
        normal = [m for m in sorted_markets if m.spread_pct <= self.spread_warning]
        
        report = "📊 **Finance 市场流动性监控**\n"
        report += f"⏰ {datetime.now().strftime('%H:%M:%S UTC')}\n"
        report += f"📈 监控市场: {len(self.markets)}\n\n"
        
        # 概览
        report += "**概览**\n"
        report += f"🔴 高风险 (spread>5%): {len(critical)}\n"
        report += f"🟡 警告 (spread>3%): {len(warning)}\n"
        report += f"✅ 正常: {len(normal)}\n\n"
        
        # 高风险市场
        if critical:
            report += "**🔴 高风险市场**\n"
            for m in critical[:5]:
                report += f"• {m.question[:35]}...\n"
                report += f"  Spread: {m.spread_pct:.1f}% | Vol: ${m.volume:,.0f}\n"
            report += "\n"
        
        # 警告市场
        if warning:
            report += "**🟡 警告市场**\n"
            for m in warning[:5]:
                report += f"• {m.question[:35]}...\n"
                report += f"  Spread: {m.spread_pct:.1f}% | Vol: ${m.volume:,.0f}\n"
            report += "\n"
        
        # 最佳流动性
        if normal:
            report += "**✅ 最佳流动性**\n"
            best = sorted(normal, key=lambda x: x.volume, reverse=True)[:3]
            for m in best:
                report += f"• {m.question[:35]}...\n"
                report += f"  Spread: {m.spread_pct:.2f}% | Vol: ${m.volume:,.0f}\n"
        
        return report
    
    def get_vpin_report(self) -> str:
        """生成 VPIN 报告"""
        vpin_alerts = self.simulate_vpin()
        
        if not vpin_alerts:
            return "🧪 VPIN: 未检测到毒性信号"
        
        report = "🧪 **VPIN 毒性信号** (模拟)\n\n"
        
        for alert in vpin_alerts[:5]:
            m = alert['market']
            report += f"**{m.question[:40]}...**\n"
            report += f"   {alert['message']}\n"
            report += f"   价格: ${m.price:.4f} | 交易量: ${m.volume:,.0f}\n\n"
        
        return report
    
    def run(self) -> str:
        """运行监控"""
        print("🔍 扫描 Finance 市场...")
        
        markets = self.fetch_markets()
        print(f"   获取 {len(markets)} 个市场")
        
        # 检查告警
        liquidity_alerts = self.check_liquidity_alerts()
        price_alerts = self.check_price_alerts()
        vpin_alerts = self.simulate_vpin()
        
        all_alerts = liquidity_alerts + price_alerts + vpin_alerts
        print(f"   发现 {len(all_alerts)} 个告警")
        
        # 记录
        self.history.append({
            'time': datetime.now().isoformat(),
            'markets': len(markets),
            'alerts': len(all_alerts)
        })
        
        # 生成报告
        report = self.get_liquidity_report()
        report += "\n" + self.get_vpin_report()
        
        return report


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
    print("=" * 50)
    print("📊 Finance 市场流动性 & VPIN 监控")
    print("=" * 50)
    print()
    
    monitor = FinanceMonitor()
    report = monitor.run()
    
    print("\n" + report)


if __name__ == "__main__":
    main()