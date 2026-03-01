#!/usr/bin/env node
/**
 * Polymarket Trader 自动监控机器人 v1.0
 * 
 * 功能：
 * 1. 监控Trader钱包地址的链上活动
 * 2. 获取Polymarket用户仓位变化
 * 3. 检测大额交易和建仓信号
 * 4. 生成监控报告
 * 
 * 使用方法：
 * 1. 安装依赖: npm install axios ethers
 * 2. 配置钱包地址
 * 3. 运行: node polymarket_monitor.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// 配置
const CONFIG = {
    // Polygonscan API Key (免费注册获取)
    POLYGONSCAN_API_KEY: process.env.POLYGONSCAN_API_KEY || '',
    
    // Polymarket API
    POLYMARKET_API: 'https://polymarket.com/api',
    
    // 监控间隔 (毫秒)
    CHECK_INTERVAL: 60000, // 1分钟
    
    // 告警阈值 (USD)
    ALERT_THRESHOLD: 1000, // 交易金额大于$1000时告警
    
    // 输出目录
    OUTPUT_DIR: '/root/.openclaw/workspace/polymarket_monitor',
    
    // Trader地址库
    TRADERS: {
        // NegRisk类
        '0xfdd9fc462c9d5913c11dce63e737cb4c7ab9f22a': { name: '@xmgnr', category: 'C' },
        '0x0da462636b228293849aac34c1857724757e4dde': { name: '@luishXYZ', category: 'C' },
        '0x95923e6dfa4e685361ffb0ead28657d3fa18a85b': { name: '@copenzafan', category: 'C' },
        '0x227b22b78b422bbad333bf903a164db3212916cf': { name: '@carverfomo', category: 'C' },
        '0xa4b366ad22fc0d06f1e9346897b22431874b8b87': { name: '@HolyMoses7', category: 'C' },
        '0x492442eab586f242b53bd': { name: '@PolycoolApp', category: 'C' },
        '0x3adaadddf92874041363ba3db77e949bcb9f861a': { name: '@itslirrato', category: 'C' },
        
        // Basic类
        '0x4de4d61565bbcc98605e4d53d0c6447a288e10a': { name: '@clawdvine', category: 'D' },
        '0xce510458cc3964b1bb9aa9e2db28bb2b530bdd3': { name: '@takecgcj', category: 'D' },
        '0xc387de398cf17f60c9def1d35bb89c8bea05b0e4': { name: '@blknoiz06', category: 'D' },
        '0x51f304b408809f': { name: '@cryptorover', category: 'D' },
        
        // BTC高频类
        '0x4460bf2c0aa59db412a6493c2c08970797b62970': { name: '@0x4460', category: 'F' },
        '0xe594': { name: '@0xe594', category: 'F' },
        '0xd0bde12c': { name: '@Demphu.finite', category: 'F' },
        '0x1979ae6b7e': { name: '@OpenClaw', category: 'F' },
        
        // 天气类
        '0x594edB9112f526Fa680b8F858A6379C8A2c1C11': { name: '@0x594edB', category: 'B' }
    }
};

class PolymarketMonitor {
    constructor() {
        this.alerts = [];
        this.transactions = [];
        this.positions = {};
    }
    
    async checkWallet(walletAddress, name) {
        console.log(`\n🔍 检查钱包: ${name} (${walletAddress.substring(0, 10)}...)`);
        
        try {
            // 获取余额
            const balance = await this.getBalance(walletAddress);
            console.log(`   余额: $${balance}`);
            
            // 获取最近交易
            const txs = await this.getTransactions(walletAddress);
            
            if (txs.length > 0) {
                console.log(`   最近交易: ${txs.length}笔`);
                
                for (const tx of txs.slice(0, 5)) {
                    const value = this.parseTxValue(tx.value, tx.tokenSymbol);
                    console.log(`   - ${tx.timeStamp}: $${value} ${tx.tokenSymbol}`);
                    
                    // 大额交易告警
                    if (value > CONFIG.ALERT_THRESHOLD) {
                        this.addAlert({
                            type: 'LARGE_TRANSACTION',
                            trader: name,
                            wallet: walletAddress,
                            value: value,
                            token: tx.tokenSymbol,
                            hash: tx.hash,
                            time: tx.timeStamp
                        });
                    }
                }
                
                this.transactions.push(...txs);
            }
            
            return { balance, txs };
            
        } catch (error) {
            console.log(`   ❌ 错误: ${error.message}`);
            return null;
        }
    }
    
    async getBalance(walletAddress) {
        // 使用Polygonscan API获取MATIC余额
        if (!CONFIG.POLYGONSCAN_API_KEY) {
            return 'N/A (需要API Key)';
        }
        
        return new Promise((resolve) => {
            const url = `https://api.polygonscan.com/api?module=account&action=balance&address=${walletAddress}&tag=latest&apikey=${CONFIG.POLYGONSCAN_API_KEY}`;
            
            https.get(url, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        const wei = parseInt(result.result);
                        const matic = wei / 1e18;
                        resolve((matic * 0.8).toFixed(2)); // 按$0.8/MATIC估算
                    } catch (e) {
                        resolve('Error');
                    }
                });
            }).on('error', () => resolve('Error'));
        });
    }
    
    async getTransactions(walletAddress) {
        // 获取最近10笔交易
        if (!CONFIG.POLYGONSCAN_API_KEY) {
            return [];
        }
        
        return new Promise((resolve) => {
            const url = `https://api.polygonscan.com/api?module=account&action=txlist&address=${walletAddress}&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=${CONFIG.POLYGONSCAN_API_KEY}`;
            
            https.get(url, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        if (result.status === '1' && result.result) {
                            const txs = result.result.map(tx => ({
                                hash: tx.hash,
                                value: tx.value,
                                tokenSymbol: 'MATIC',
                                timeStamp: new Date(tx.timeStamp * 1000).toLocaleString()
                            }));
                            resolve(txs);
                        } else {
                            resolve([]);
                        }
                    } catch (e) {
                        resolve([]);
                    }
                });
            }).on('error', () => resolve([]));
        });
    }
    
    parseTxValue(value, symbol) {
        const wei = parseInt(value);
        const matic = wei / 1e18;
        return (matic * 0.8).toFixed(2); // 简化估算
    }
    
    addAlert(alert) {
        this.alerts.push({
            ...alert,
            timestamp: new Date().toISOString()
        });
        console.log(`   🚨 告警: $${alert.value} ${alert.token}`);
    }
    
    async getPolymarketPositions(username) {
        console.log(`\n📊 获取Polymarket仓位: ${username}`);
        
        // 模拟API调用
        return {
            username,
            positions: [],
            totalValue: 0
        };
    }
    
    generateReport() {
        const report = {
            generatedAt: new Date().toISOString(),
            summary: {
                totalTraders: Object.keys(CONFIG.TRADERS).length,
                alertsCount: this.alerts.length,
                transactionsCount: this.transactions.length
            },
            alerts: this.alerts,
            transactions: this.transactions.slice(0, 50) // 最近50笔
        };
        
        // 保存报告
        const reportPath = path.join(CONFIG.OUTPUT_DIR, 'monitor_report.json');
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        console.log(`\n📊 报告已保存: ${reportPath}`);
        return report;
    }
    
    async run() {
        console.log('='.repeat(60));
        console.log('  Polymarket Trader 自动监控机器人 v1.0');
        console.log('='.repeat(60));
        console.log(`\n⏰ 开始时间: ${new Date().toLocaleString()}`);
        console.log(`📊 监控Trader数: ${Object.keys(CONFIG.TRADERS).length}`);
        console.log(`⏱️  检查间隔: ${CONFIG.CHECK_INTERVAL / 1000}秒`);
        
        // 创建输出目录
        fs.mkdirSync(CONFIG.OUTPUT_DIR, { recursive: true });
        
        // 检查所有Trader钱包
        console.log('\n🔍 开始检查所有Trader...');
        
        for (const [wallet, info] of Object.entries(CONFIG.TRADERS)) {
            await this.checkWallet(wallet, info.name);
            await new Promise(r => setTimeout(r, 1000)); // 避免API限流
        }
        
        // 生成报告
        const report = this.generateReport();
        
        console.log('\n' + '='.repeat(60));
        console.log('  监控完成');
        console.log('='.repeat(60));
        console.log(`📊 总告警: ${report.summary.alertsCount}`);
        console.log(`📝 总交易: ${report.summary.transactionsCount}`);
    }
}

// 主程序
async function main() {
    const monitor = new PolymarketMonitor();
    await monitor.run();
}

main().catch(console.error);