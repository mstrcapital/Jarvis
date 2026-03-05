#!/usr/bin/env python3
"""
Kelly Criterion Calculator for Prediction Markets
==================================================
Tan (Chief Quant) - 量化策略工具

支持:
- 标准 Kelly
- Fractional Kelly
- Empirical Kelly (考虑不确定性)
- 多交易组合 Kelly
"""

import math
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
import random

@dataclass
class Trade:
    """单笔交易"""
    price: float          # 购买价格 (0-1)
    probability: float    # 你的胜率估计 (0-1)
    size: float           # 投注金额 ($)
    
@dataclass
class KellyResult:
    """Kelly 计算结果"""
    full_kelly: float          # 完整 Kelly (小数)
    fractional_kelly: float    # Fractional Kelly
    expected_value: float      # 期望值
    edge: float                # 边缘 (probability - price)
    payout_ratio: float        # 赔付率
    recommended_size: float    # 建议投注金额
    risk_notes: List[str]      # 风险提示

class KellyCalculator:
    """Kelly Criterion 计算器"""
    
    FRACTIONAL_FACTORS = {
        'full': 1.0,
        'half': 0.5,
        'quarter': 0.25,
        'tenth': 0.1,
        'twentieth': 0.05
    }
    
    def __init__(self, bankroll: float = 10000):
        self.bankroll = bankroll
    
    def calculate_payout_ratio(self, price: float) -> float:
        """计算赔付率"""
        if price <= 0 or price >= 1:
            return 0
        return (1 - price) / price
    
    def calculate_ev(self, price: float, probability: float) -> float:
        """计算期望值"""
        payout = self.calculate_payout_ratio(price)
        profit = payout * price  # 赢的情况
        loss = price             # 输的情况 (损失购买价格)
        
        ev = probability * profit - (1 - probability) * loss
        return ev
    
    def calculate_edge(self, price: float, probability: float) -> float:
        """计算边缘 (你的概率估计 - 市场概率)"""
        return probability - price
    
    def calculate_full_kelly(self, price: float, probability: float) -> float:
        """
        计算完整 Kelly
        
        f* = (p × b - q) / b
        其中 b = (1 - price) / price (赔付率)
        p = probability (胜率)
        q = 1 - p (败率)
        """
        if price <= 0 or price >= 1:
            return 0
        
        payout = self.calculate_payout_ratio(price)
        if payout <= 0:
            return 0
            
        p = probability
        q = 1 - p
        
        # Kelly 公式: f* = (p × b - q) / b
        kelly = (p * payout - q) / payout
        return max(0, kelly)  # 不允许负值
    
    def calculate_fractional_kelly(self, price: float, probability: float, 
                                   fraction: str = 'half') -> float:
        """计算 Fractional Kelly"""
        full = self.calculate_full_kelly(price, probability)
        factor = self.FRACTIONAL_FACTORS.get(fraction, 0.5)
        return full * factor
    
    def calculate_empirical_kelly(self, price: float, probability: float,
                                   uncertainty: float = 0.1,
                                   simulations: int = 10000) -> float:
        """
        Empirical Kelly with Monte Carlo
        
        考虑你的概率估计有不确定性
        uncertainty: 概率估计的标准差 (如 0.1 = 10%)
        """
        full_kelly = self.calculate_full_kelly(price, probability)
        
        # Monte Carlo 模拟
        edge_estimates = []
        for _ in range(simulations):
            # 从正态分布采样概率
            prob = random.gauss(probability, uncertainty)
            prob = max(0.01, min(0.99, prob))  # 限制在 1-99%
            
            sim_kelly = self.calculate_full_kelly(price, prob)
            edge_estimates.append(sim_kelly)
        
        # 使用 95th percentile (保守估计)
        p95 = sorted(edge_estimates)[int(simulations * 0.05)]  # 5th percentile for worst case
        
        # CV (coefficient of variation)
        mean_edge = sum(edge_estimates) / len(edge_estimates)
        if mean_edge > 0:
            cv = (max(edge_estimates) - min(edge_estimates)) / mean_edge
        else:
            cv = 1.0
        
        # Empirical Kelly = full_kelly × (1 - CV)
        empirical = full_kelly * max(0.1, 1 - cv)
        
        return max(0, empirical)
    
    def analyze_trade(self, price: float, probability: float,
                     fraction: str = 'half',
                     use_empirical: bool = False,
                     uncertainty: float = 0.1) -> KellyResult:
        """全面分析一笔交易"""
        
        # 计算各项指标
        ev = self.calculate_ev(price, probability)
        edge = self.calculate_edge(price, probability)
        payout = self.calculate_payout_ratio(price)
        
        if use_empirical:
            kelly = self.calculate_empirical_kelly(price, probability, uncertainty)
        else:
            kelly = self.calculate_full_kelly(price, probability)
        
        frac_kelly = kelly * self.FRACTIONAL_FACTORS.get(fraction, 0.5)
        recommended_size = frac_kelly * self.bankroll
        
        # 风险提示
        notes = []
        if edge < 0:
            notes.append("⚠️ 负边缘: 市场概率高于你的估计")
        if kelly > 0.25:
            notes.append("⚠️ 高 Kelly: 建议降低到 quarter 或 tenth")
        if probability < 0.1 or probability > 0.9:
            notes.append("⚠️ 极端概率: 流动性可能很差")
        if use_empirical:
            notes.append(f"📊 Empirical Kelly (不确定={uncertainty})")
        
        return KellyResult(
            full_kelly=kelly,
            fractional_kelly=frac_kelly,
            expected_value=ev,
            edge=edge,
            payout_ratio=payout,
            recommended_size=recommended_size,
            risk_notes=notes
        )
    
    def portfolio_kelly(self, trades: List[Dict]) -> float:
        """
        组合 Kelly - 多笔交易最优分配
        
        简化版: 假设不相关性,平均分配
        """
        kelly_fractions = []
        
        for trade in trades:
            k = self.calculate_full_kelly(trade['price'], trade['probability'])
            kelly_fractions.append(k)
        
        if not kelly_fractions:
            return 0
        
        # 组合 Kelly (简化版)
        # 实际需要协方差矩阵
        avg_kelly = sum(kelly_fractions) / len(kelly_fractions)
        
        return min(avg_kelly, 0.25)  # 限制最大


def demo():
    """演示"""
    print("=" * 60)
    print("🎰 Kelly Criterion Calculator - Demo")
    print("=" * 60)
    
    calc = KellyCalculator(bankroll=10000)
    
    # 示例交易
    test_cases = [
        {"name": "Fed 2次降息 2026", "price": 0.275, "probability": 0.35},
        {"name": "BTC >$68K Mar 1", "price": 0.12, "probability": 0.20},
        {"name": "Judy Shelton Fed Chair", "price": 0.0385, "probability": 0.08},
        {"name": "高概率交易", "price": 0.80, "probability": 0.85},
    ]
    
    for tc in test_cases:
        print(f"\n📌 {tc['name']}")
        print(f"   价格: ${tc['price']:.4f} | 估计概率: {tc['probability']:.1%}")
        
        result = calc.analyze_trade(tc['price'], tc['probability'], 'half')
        
        print(f"   ────────────────────────────────────────")
        print(f"   🎯 Full Kelly:     {result.full_kelly:.2%}")
        print(f"   📊 Half Kelly:     {result.fractional_kelly:.2%}")
        print(f"   💰 建议投注:       ${result.recommended_size:.2f}")
        print(f"   📈 期望值 (EV):    ${result.expected_value:.4f}")
        print(f"   edge:             {result.edge:.2%}")
        
        if result.risk_notes:
            for note in result.risk_notes:
                print(f"   {note}")
    
    print("\n" + "=" * 60)
    print("✅ 计算完成")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        try:
            price = float(sys.argv[1])
            probability = float(sys.argv[2])
            bankroll = float(sys.argv[3]) if len(sys.argv) > 3 else 10000
            fraction = sys.argv[4] if len(sys.argv) > 4 else 'half'
            
            calc = KellyCalculator(bankroll)
            result = calc.analyze_trade(price, probability, fraction)
            
            print(json.dumps({
                "full_kelly": f"{result.full_kelly:.4f}",
                "fractional_kelly": f"{result.fractional_kelly:.4f}",
                "expected_value": f"{result.expected_value:.4f}",
                "edge": f"{result.edge:.4f}",
                "recommended_size": f"{result.recommended_size:.2f}",
                "risk_notes": result.risk_notes
            }, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"错误: {e}")
            print("用法: python3 kelly_calculator.py <价格> <概率> [资金] [fraction]")
    else:
        demo()