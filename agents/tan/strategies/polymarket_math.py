#!/usr/bin/env python3
"""
Polymarket 数学策略
基于 Avellaneda-Stoikov, Kelly Criterion, 概率校准
"""

import math
import json
from datetime import datetime
from typing import Dict, List, Optional

class PolymarketMathStrategy:
    """Polymarket 量化策略"""
    
    def __init__(self, capital: float = 10000):
        self.capital = capital
        self.risk_free_rate = 0.05  # 5% 无风险利率
        
    def avellaneda_stoikov_spread(self, volatility: float, time_horizon: float, 
                                   gamma: float = 0.5, kappa: float = 1.0) -> float:
        """
        Avellaneda-Stoikov 最优价差公式
        
        Args:
            volatility: 资产波动率 (0.01 = 1%)
            time_horizon: 时间范围 (秒)
            gamma: 风险厌恶系数
            kappa: 订单到达率
        
        Returns:
            最优价差
        """
        sigma = volatility
        T = time_horizon
        
        # 简化版公式
        spread = sigma * math.sqrt(2 * math.log(1/gamma) / T)
        return spread
    
    def kelly_criterion(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """
        Kelly Criterion 仓位计算
        
        Args:
            win_rate: 胜率 (0-1)
            avg_win: 平均盈利
            avg_loss: 平均亏损
        
        Returns:
            建议仓位比例 (0-1)
        """
        if avg_loss == 0:
            return 0
        
        b = avg_win / avg_loss  # 盈亏比
        p = win_rate
        
        # Kelly 公式: f* = (bp - q) / b
        q = 1 - p
        kelly = (b * p - q) / b
        
        # 半 Kelly 更安全
        return max(0, kelly * 0.5)
    
    def probability_calibration(self, predictions: List[Dict], actuals: List[bool]) -> Dict:
        """
        概率校准 - 验证预测准确性
        
        计算 Brier Score 和校准曲线
        """
        if not predictions:
            return {"brier_score": 1.0, "calibrated": False}
        
        brier_score = 0
        bins = {0.1: [], 0.2: [], 0.3: [], 0.4: [], 0.5: [], 
                0.6: [], 0.7: [], 0.8: [], 0.9: [], 1.0: []}
        
        for pred, actual in zip(predictions, actuals):
            prob = pred.get('probability', 0.5)
            brier_score += (prob - (1 if actual else 0)) ** 2
            
            # 分配到对应区间
            bin_key = round(prob * 10) / 10
            bins[bin_key].append(1 if actual else 0)
        
        brier_score /= len(predictions)
        
        # 计算校准率
        calibrations = []
        for prob, outcomes in bins.items():
            if outcomes:
                actual_prob = sum(outcomes) / len(outcomes)
                calibrations.append(abs(prob - actual_prob))
        
        avg_calibration_error = sum(calibrations) / len(calibrations) if calibrations else 1.0
        
        return {
            "brier_score": brier_score,
            "calibration_error": avg_calibration_error,
            "calibrated": avg_calibration_error < 0.1,
            "quality": "Good" if brier_score < 0.2 else "Needs Improvement"
        }
    
    def generate_signal(self, market_price: float, volatility: float, 
                       historical_predictions: List[Dict], actuals: List[bool]) -> Dict:
        """生成交易信号"""
        
        # 计算 Kelly 仓位
        win_rate = sum(actuals) / len(actuals) if actuals else 0.5
        kelly_size = self.kelly_criterion(win_rate, 1.5, 1.0)
        
        # 概率校准
        calibration = self.probability_calibration(historical_predictions, actuals)
        
        # Avellaneda-Stoikov 价差
        spread = self.avellaneda_stoikov_spread(volatility, 3600)  # 1小时
        
        return {
            "timestamp": datetime.now().isoformat(),
            "market_price": market_price,
            "kelly_position": kelly_size,
            "optimal_spread": spread,
            "calibration": calibration,
            "signal": "BUY" if kelly_size > 0.1 and calibration["calibrated"] else "HOLD",
            "confidence": min(kelly_size * 2, 1.0) * (1 if calibration["calibrated"] else 0.5)
        }

# 示例
if __name__ == "__main__":
    strategy = PolymarketMathStrategy(10000)
    
    # 模拟数据
    predictions = [
        {"probability": 0.7}, {"probability": 0.6}, {"probability": 0.8},
        {"probability": 0.5}, {"probability": 0.9}
    ]
    actuals = [True, True, True, False, True]
    
    signal = strategy.generate_signal(
        market_price=0.65,
        volatility=0.15,
        historical_predictions=predictions,
        actuals=actuals
    )
    
    print("📊 策略信号:")
    print(json.dumps(signal, indent=2))
