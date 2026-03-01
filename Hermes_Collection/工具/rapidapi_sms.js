#!/usr/bin/env node
/**
 * RapidAPI UAE SMS Service Finder
 * 搜索并调用RapidAPI上的UAE接码服务
 */

const https = require('https');
const readline = require('readline');

// RapidAPI服务列表
const RAPIDAPI_SERVICES = [
    {
        name: 'SMSActivate',
        host: 'sms-activate.p.rapidapi.com',
        endpoint: '/stubs/handlerAPI',
        docs: 'https://rapidapi.com/sms-activate-sms-activate-sms-activate-vat-760252/api/sms-activate'
    },
    {
        name: 'Temp-Number',
        host: 'temp-number.p.rapidapi.com',
        endpoint: '/v1/phone-number',
        docs: 'https://rapidapi.com/alertfps/api/temp-number'
    },
    {
        name: 'Receive-SMS',
        host: 'receive-smss.p.rapidapi.com',
        endpoint: '/receive-smss',
        docs: 'https://rapidapi.com/kashipara/api/receive-smss'
    }
];

// API Key配置
const CONFIG = {
    RAPIDAPI_KEY: process.env.RAPIDAPI_KEY || '',
    // 如果没有，可以在这里填入你的RapidAPI Key
    // 从 https://rapidapi.com/ 注册获取
};

async function testSMSActivate() {
    console.log('\n📱 测试 SMSActivate...');
    console.log('文档: https://rapidapi.com/sms-activate-sms-activate-sms-activate-vat-760252/api/sms-activate');
    
    if (!CONFIG.RAPIDAPI_KEY) {
        console.log('❌ 需要RAPIDAPI_KEY');
        console.log('请设置: export RAPIDAPI_KEY=your_key');
        return;
    }
    
    // 获取号码
    const data = JSON.stringify({
        action: 'getNumber',
        service: 'any',
        country: 1, // 尝试不同国家代码
        forward: 0
    });
    
    const options = {
        hostname: 'sms-activate.p.rapidapi.com',
        path: '/stubs/handlerAPI',
        method: 'POST',
        headers: {
            'X-RapidAPI-Key': CONFIG.RAPIDAPI_KEY,
            'X-RapidAPI-Host': 'sms-activate.p.rapidapi.com',
            'Content-Type': 'application/json'
        }
    };
    
    return new Promise((resolve) => {
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                console.log('响应:', body);
                resolve(body);
            });
        });
        
        req.on('error', (e) => {
            console.log('错误:', e.message);
            resolve(null);
        });
        
        req.write(data);
        req.end();
    });
}

async function searchRapidAPI() {
    console.log('\n' + '='.repeat(60));
    console.log('  RapidAPI UAE SMS 服务搜索');
    console.log('='.repeat(60));
    
    console.log('\n📋 可用的RapidAPI接码服务:');
    
    console.log('\n1️⃣  SMSActivate');
    console.log('   Host: sms-activate.p.rapidapi.com');
    console.log('   需要Key: 是');
    console.log('   UAE支持: 可能');
    
    console.log('\n2️⃣  Temp-Number');
    console.log('   Host: temp-number.p.rapidapi.com');
    console.log('   需要Key: 是');
    console.log('   UAE支持: 可能');
    
    console.log('\n3️⃣  Receive-SMSs');
    console.log('   Host: receive-smss.p.rapidapi.com');
    console.log('   需要Key: 是');
    console.log('   UAE支持: 可能');
    
    console.log('\n' + '='.repeat(60));
    console.log('  使用步骤');
    console.log('='.repeat(60));
    
    console.log('\n1️⃣  访问 https://rapidapi.com/');
    console.log('2️⃣  注册账号 (免费)');
    console.log('3️⃣  搜索 "UAE SMS" 或 "SMS Activate"');
    console.log('4️⃣  订阅服务 (可能有免费额度)');
    console.log('5️⃣  获取API Key');
    console.log('6️⃣  设置环境变量: export RAPIDAPI_KEY=your_key');
    console.log('7️⃣  运行脚本获取号码');
    
    console.log('\n' + '='.repeat(60));
    console.log('  推荐服务');
    console.log('='.repeat(60));
    
    console.log('\n🔗 SMSActivate (推荐):');
    console.log('   https://rapidapi.com/sms-activate-sms-activate-sms-activate-vat-760252/api/sms-activate');
    console.log('   价格: 约$0.5-3/次');
    console.log('   支持: 多国号码');
    
    console.log('\n🔗 5Sim (备选):');
    console.log('   https://5sim.net/ (官网，API类似)');
    console.log('   价格: 约$0.5/次');
    
    console.log('\n🔗 SMSPool (备选):');
    console.log('   https://smspool.net/');
    console.log('   支持UAE，直接购买');
}

function generateSetupScript() {
    const script = `#!/bin/bash
# RapidAPI UAE SMS 设置脚本

echo "======================================"
echo "  RapidAPI UAE SMS 快速设置"
echo "======================================"

echo ""
echo "步骤1: 获取RapidAPI Key"
echo "  1. 访问 https://rapidapi.com/"
echo "  2. 注册免费账号"
echo "  3. 搜索 'SMS Activate'"
echo "  4. 点击 'Subscribe to Test' (免费额度)"
echo "  5. 复制你的API Key"

echo ""
echo "步骤2: 设置API Key"
echo "  export RAPIDAPI_KEY=你的Key"

echo ""
echo "步骤3: 运行脚本"
echo "  node rapidapi_sms.js"

echo ""
echo "======================================"
`;

    return script;
}

async function main() {
    console.log('\n' + '='.repeat(60));
    console.log('  🚀 RapidAPI UAE SMS 解决方案');
    console.log('='.repeat(60));
    
    // 显示设置指南
    searchRapidAPI();
    
    // 生成设置脚本
    const fs = require('fs');
    const script = generateSetupScript();
    fs.writeFileSync('/root/.openclaw/workspace/rapidapi_setup.sh', script);
    
    console.log('\n✅ 设置脚本已生成: rapidapi_setup.sh');
    
    // 检查是否有API Key
    if (!CONFIG.RAPIDAPI_KEY) {
        console.log('\n⚠️  未配置RAPIDAPI_KEY');
        console.log('请设置环境变量后重新运行');
    } else {
        await testSMSActivate();
    }
}

main().catch(console.error);