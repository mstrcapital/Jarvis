#!/usr/bin/env python3
"""
Polymarket Order Book Monitor
=============================
Tan (Chief Quant) - 实时订单簿监控工具

功能:
- 实时订单簿数据
- VPIN 毒性检测
- Spread 异常告警
- 流动性分析
"""

import asyncio
import json
import time
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess

# 配置
POLYMARKET_API = "https://clob.polymarket.com"
TELEGRAM_BOT_TOKEN = "8269082567:AAFS7XtOg5qyh3Svdk5c0CF8KkbNW8muY-4"
REPORT_CHAT_ID = "8591571345"

class OrderBook:
    """订单簿数据"""
    def __init__(self):
        self.bids = []  # [(price, size), ...]
        self.asks = []  # [(price, size), ...]
        self.last_update = time.time()
    
    @property
    def mid_price(self) -> float:
        if self.bids and self.asks:
            return (self.bids[0][0] + self.asks[0][0]) / 2
        return 0
    
    @property
    def spread(self) -> float:
        if self.bids and self.asks:
            return self.asks[0][0] - self.bids[0][0]
        return 0
    
    @property
    def spread_pct(self) -> float:
        if self.mid_price > 0:
            return (self.spread / self.mid_price) * 100
        return 0
    
    def best_bid(self) -> float:
        return self.bids[0][0] if self.bids else 0
    
    def best_ask(self) -> float:
        return self.asks[0][0] if self.asks else 0
    
    def total_bid_size(self) -> float:
        return sum(size for _, size in self.bids[:5])
    
    def total_ask_size(self) -> float:
        return sum(size for _, size in self.asks[:5])
    
    def imbalance(self) -> float:
        """订单簿不平衡度"""
        total = self.total_bid_size() + self.total_ask_size()
        if total > 0:
            return (self.total_bid_size() - self.total_ask_size()) / total
        return 0


class VPINCalculator:
    """VPIN (Volume-weighted Order Imbalance) 计算器"""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.buy_volumes = deque(maxlen=window_size)
        self.sell_volumes = deque(maxlen=window_size)
    
    def update(self, order_book: OrderBook, traded_buy: float, traded_sell: float):
        """更新 VPIN"""
        self.buy_volumes.append(traded_buy)
        self.sell_volumes.append(traded_sell)
    
    def calculate(self) -> float:
        """计算 VPIN"""
        total = sum(self.buy_volumes) + sum(self.sell_volumes)
        if total > 0:
            vpin = abs(sum(self.buy_volumes) - sum(self.sell_volumes)) / total
            return vpin
        return 0


class OrderBookMonitor:
    """订单簿监控器"""
    
    def __init__(self, token_id: str, name: str = ""):
        self.token_id = token_id
        self.name = name
        self.order_book = OrderBook()
        self.vpin_calc = VPINCalculator(window_size=10)
        self.last_trade_buy = 0
        self.last_trade_sell = 0
        self.spread_history = deque(maxlen=20)
        self.price_history = deque(maxlen=50)
        
        # 告警阈值
        self.spread_wide_threshold = 0.05  # 5% spread
        self.vpin_high_threshold = 0.6     # 60% imbalance
        self.price_change_threshold = 0.03 # 3% 价格变化
        
        self.alerts = []
    
    def fetch_order_book(self) -> bool:
        """获取订单簿数据 - 使用市场列表 API"""
        try:
            # 使用 polymarket CLI 获取市场数据
            result = subprocess.run(
                ["polymarket", "-o", "json", "markets", "get", self.token_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                # 尝试用 list
                result = subprocess.run(
                    ["polymarket", "-o", "json", "markets", "list", "--active", "true", "--limit", "50"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    return False
                
                # 找到对应的市场
                import json
                markets = json.loads(result.stdout)
                market = None
                for m in markets:
                    if m.get('id') == self.token_id or m.get('question', '').lower().find(self.name.lower()) >= 0:
                        market = m
                        break
                
                if not market:
                    return False
                
                self._parse_market_data(market)
                return True
            
            # 解析单个市场
            import json
            market = json.loads(result.stdout)
            self._parse_market_data(market)
            return True
            
        except Exception as e:
            print(f"Error fetching order book: {e}")
            return False
    
    def _parse_market_data(self, market: dict):
        """解析市场数据"""
        # 从市场数据中获取订单簿信息
        best_bid = market.get('bestBid', 0)
        best_ask = market.get('bestAsk', 0)
        spread = market.get('spread', 0)
        
        # 如果没有直接的数据,尝试从价格推断
        outcome_prices = market.get('outcomePrices')
        if outcome_prices and not best_bid:
            try:
                import json
                prices = json.loads(outcome_prices)
                if len(prices) >= 2:
                    best_bid = float(prices[0])
                    best_ask = float(prices[1])
            except:
                pass
        
        # 更新订单簿 (确保是 float)
        try:
            best_bid = float(best_bid) if best_bid else 0
            best_ask = float(best_ask) if best_ask else 0
        except (ValueError, TypeError):
            best_bid = 0
            best_ask = 0
        
        if best_bid > 0:
            self.order_book.bids = [(best_bid, 100)]  # 模拟数据
        if best_ask > 0:
            self.order_book.asks = [(best_ask, 100)]
        
        self.order_book.last_update = time.time()
    
    def parse_cli_output(self, output: str):
        """解析 CLI 输出"""
        # 这是一个简化版本 - 需要根据实际 CLI 输出格式调整
        lines = output.strip().split('\n')
        
        bids = []
        asks = []
        
        in_bids = False
        in_asks = False
        
        for line in lines:
            if 'Bids' in line or 'Buy' in line:
                in_bids = True
                in_asks = False
            elif 'Asks' in line or 'Sell' in line:
                in_bids = False
                in_asks = True
            elif line.strip() and not line.startswith('-'):
                try:
                    parts = line.split()
                    if len(parts) >= 2:
                        price = float(parts[0])
                        size = float(parts[1])
                        if in_bids:
                            bids.append((price, size))
                        elif in_asks:
                            asks.append((price, size))
                except:
                    continue
        
        self.order_book.bids = sorted(bids, reverse=True)
        self.order_book.asks = sorted(asks)
        self.order_book.last_update = time.time()
    
    def check_alerts(self) -> List[str]:
        """检查是否触发告警"""
        alerts = []
        ob = self.order_book
        
        # Spread 告警
        if ob.spread_pct > self.spread_wide_threshold * 100:
            alerts.append(f"⚠️ Spread 异常: {ob.spread_pct:.2f}% (阈值: {self.spread_wide_threshold*100}%)")
        
        # VPIN 告警
        vpin = self.vpin_calc.calculate()
        if vpin > self.vpin_high_threshold:
            alerts.append(f"🔴 VPIN 过高: {vpin:.2%} (有毒交易风险!)")
        
        # 价格剧烈变化
        if len(self.price_history) > 1:
            price_change = abs(ob.mid_price - self.price_history[-2]) / self.price_history[-2]
            if price_change > self.price_change_threshold:
                alerts.append(f"📊 价格剧烈变化: {price_change:.2%}")
        
        # 流动性枯竭
        if ob.total_bid_size() < 10 or ob.total_ask_size() < 10:
            alerts.append(f"💧 流动性低: Bid=${ob.total_bid_size():.2f} Ask=${ob.total_ask_size():.2f}")
        
        return alerts
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        ob = self.order_book
        vpin = self.vpin_calc.calculate()
        
        return {
            "token": self.token_id,
            "name": self.name,
            "mid_price": ob.mid_price,
            "spread": ob.spread,
            "spread_pct": ob.spread_pct,
            "best_bid": ob.best_bid(),
            "best_ask": ob.best_ask(),
            "bid_size_5": ob.total_bid_size(),
            "ask_size_5": ob.total_ask_size(),
            "imbalance": ob.imbalance(),
            "vpin": vpin,
            "last_update": datetime.fromtimestamp(ob.last_update).strftime("%H:%M:%S")
        }
    
    def format_status(self) -> str:
        """格式化状态输出"""
        stats = self.get_stats()
        
        return f"""
📊 {stats['name']} ({stats['token']})
─────────────────────────
💰 价格: ${stats['mid_price']:.4f}
📐 Spread: {stats['spread']:.4f} ({stats['spread_pct']:.2f}%)
🟢 Best Bid: ${stats['best_bid']:.4f} (${stats['bid_size_5']:.2f})
🔴 Best Ask: ${stats['best_ask']:.4f} (${stats['ask_size_5']:.2f})
⚖️ 不平衡: {stats['imbalance']:+.2%}
🧪 VPIN: {stats['vpin']:.2%}
⏰ 更新: {stats['last_update']}
"""


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
    except Exception as e:
        print(f"Telegram error: {e}")


async def monitor_continuous(token_id: str, name: str, interval: int = 5):
    """持续监控"""
    monitor = OrderBookMonitor(token_id, name)
    
    print(f"开始监控: {name} ({token_id})")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            # 获取订单簿
            if monitor.fetch_order_book():
                # 解析数据 (需要根据实际 CLI 输出调整)
                # monitor.parse_cli_output(...)
                
                # 更新 VPIN
                monitor.vpin_calc.update(
                    monitor.order_book,
                    monitor.last_trade_buy,
                    monitor.last_trade_sell
                )
                
                # 记录历史
                if monitor.order_book.mid_price > 0:
                    monitor.price_history.append(monitor.order_book.mid_price)
                
                # 检查告警
                alerts = monitor.check_alerts()
                
                # 打印状态
                print(monitor.format_status())
                
                if alerts:
                    print("🚨 告警:")
                    for alert in alerts:
                        print(f"  {alert}")
                
                # 如果有严重告警,发送到 Telegram
                vpin = monitor.vpin_calc.calculate()
                if vpin > 0.6:
                    send_telegram(f"🔴 VPIN 告警!\n{monitor.format_status()}")
            
            await asyncio.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n停止监控")


def quick_check(token_id: str, name: str = ""):
    """快速检查订单簿"""
    monitor = OrderBookMonitor(token_id, name)
    
    print(f"=== 订单簿快速检查: {name} ({token_id}) ===\n")
    
    # 获取数据
    if monitor.fetch_order_book():
        print("📡 数据获取成功")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S UTC')}\n")
        print(monitor.format_status())
        
        alerts = monitor.check_alerts()
        if alerts:
            print("\n🚨 告警:")
            for alert in alerts:
                print(f"  {alert}")
    else:
        print("❌ 数据获取失败")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════╗
║     Polymarket Order Book Monitor                     ║
║     Tan (Chief Quant) - 实时订单簿监控                 ║
╠══════════════════════════════════════════════════════╣
║                                                       ║
║  用法:                                                ║
║    python3 orderbook_monitor.py <token_id> [name]   ║
║    python3 orderbook_monitor.py continuous <token_id> <name>  ║
║    python3 orderbook_monitor.py quick <token_id> <name>      ║
║                                                       ║
║  示例:                                                ║
║    python3 orderbook_monitor.py 1414949 "BTC>$68K"   ║
║    python3 orderbook_monitor.py continuous 1414949   ║
║                                                       ║
╚══════════════════════════════════════════════════════╝
        """)
    else:
        command = sys.argv[1]
        
        if command == "continuous" and len(sys.argv) >= 4:
            token_id = sys.argv[2]
            name = sys.argv[3]
            asyncio.run(monitor_continuous(token_id, name))
            
        elif command == "quick" and len(sys.argv) >= 4:
            token_id = sys.argv[2]
            name = sys.argv[3]
            quick_check(token_id, name)
            
        elif len(sys.argv) >= 3:
            token_id = sys.argv[1]
            name = sys.argv[2]
            asyncio.run(monitor_continuous(token_id, name, interval=10))
        else:
            print("参数不足")