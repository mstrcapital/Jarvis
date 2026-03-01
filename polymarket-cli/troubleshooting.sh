#!/bin/bash
# Polymarket 交易问题诊断脚本

echo "========================================"
echo "🔍 Polymarket 交易诊断"
echo "========================================"

echo -e "\n📋 1. 钱包状态"
polymarket wallet address

echo -e "\n📋 2. 合约批准状态"
polymarket approve check

echo -e "\n📋 3. CLOB API 状态"
polymarket clob ok

echo -e "\n📋 4. 测试订单簿访问"
polymarket clob price --token-id 0x1234567890abcdef1234567890abcdef12345678 2>&1 || echo "需要有效的 token ID"

echo -e "\n========================================"
echo "💡 如果 Neg Risk 显示 ✗，运行:"
echo "   polymarket approve set"
echo "   (需要支付 gas fee)"
echo "========================================"
