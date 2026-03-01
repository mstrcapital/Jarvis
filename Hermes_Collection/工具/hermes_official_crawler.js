#!/usr/bin/env node
/**
 * Hermes官网图片爬虫 v2.0
 * 
 * 专门用于下载Hermes官网产品图片
 * 使用Puppeteer绕过反爬虫保护
 * 
 * 使用方法:
 * 1. npm install puppeteer
 * 2. node hermes_official_crawler.js
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const https = require('https');

// 配置
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';
const TEMP_DIR = '/tmp/hermes_official';

class HermesOfficialCrawler {
    constructor() {
        this.browser = null;
        this.downloaded = [];
        this.errors = [];
    }
    
    async init() {
        console.log('\n🔧 初始化Hermes官网爬虫...');
        
        // 创建目录
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        fs.mkdirSync(TEMP_DIR, { recursive: true });
        
        // 启动浏览器
        try {
            this.browser = await puppeteer.launch({
                headless: 'new',
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--window-size=1920,1080',
                    '--start-maximized'
                ]
            });
            
            // 设置User-Agent
            const page = await this.browser.newPage();
            await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
            await page.setExtraHTTPHeaders({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            });
            
            console.log('✅ 浏览器启动成功');
            
        } catch (e) {
            console.log('⚠️ 浏览器启动失败:', e.message);
            throw e;
        }
    }
    
    async crawlHermesProducts() {
        console.log('\n🔍 开始爬取Hermes官网...');
        
        const products = [
            {
                name: 'Birkin 30 Noir',
                url: 'https://www.hermes.com/us/en/birkin-30-noir-togo-p054278VA 00.html'
            },
            {
                name: 'Birkin 25 Noir', 
                url: 'https://www.hermes.com/us/en/birkin-25-noir-togo-p054278VA 00.html'
            },
            {
                name: 'Birkin 30 Gold',
                url: 'https://www.hermes.com/us/en/birkin-30-ete-gm-togo-p054278VA 00.html'
            },
            {
                name: 'Kelly 28 Noir',
                url: 'https://www.hermes.com/us/en/kelly-28-noir-togo-p057254VA 00.html'
            }
        ];
        
        for (const product of products) {
            console.log(`\n📦 爬取: ${product.name}`);
            await this.crawlProductPage(product);
            await new Promise(r => setTimeout(r, 3000)); // 延迟
        }
    }
    
    async crawlProductPage(product) {
        const page = await this.browser.newPage();
        
        try {
            // 访问产品页面
            console.log(`  🌐 访问: ${product.url}`);
            
            await page.goto(product.url, {
                waitUntil: 'networkidle2',
                timeout: 60000
            });
            
            // 等待页面加载
            await page.waitForTimeout(3000);
            
            // 查找产品图片
            const images = await page.$$eval('img', imgs => 
                imgs.map(img => ({
                    src: img.src,
                    alt: img.alt,
                    className: img.className
                })).filter(img => 
                    img.src && (
                        img.src.includes('hermes.com') ||
                        img.src.includes('cdn.shopify.com') ||
                        img.src.includes('medias') ||
                        img.src.includes('product')
                    )
                )
            );
            
            console.log(`  📸 找到 ${images.length} 张图片`);
            
            // 下载高质量图片
            for (let i = 0; i < Math.min(images.length, 5); i++) {
                const img = images[i];
                if (img.src) {
                    await this.downloadImage(img.src, product.name, i + 1);
                    await new Promise(r => setTimeout(r, 2000));
                }
            }
            
        } catch (e) {
            this.errors.push(`${product.name}: ${e.message}`);
            console.log(`  ❌ 错误: ${e.message}`);
        }
        
        await page.close();
    }
    
    async downloadImage(url, productName, index) {
        try {
            // 处理URL
            let downloadUrl = url;
            
            // 尝试获取高清版本
            if (url.includes('?')) {
                downloadUrl = url.split('?')[0];
            }
            
            // 如果是相对URL，添加域名
            if (!downloadUrl.startsWith('http')) {
                downloadUrl = 'https://www.hermes.com' + downloadUrl;
            }
            
            console.log(`  ⬇️  下载图片 ${index}...`);
            
            // 下载图片
            const response = await this.browser.newPage();
            await response.goto(downloadUrl, { waitUntil: 'networkidle2', timeout: 30000 });
            
            const buffer = await response.screenshot({ fullPage: false });
            await response.close();
            
            // 生成文件名
            const filename = `${productName.replace(/\s+/g, '_')}_${index}.jpg`;
            const filepath = path.join(OUTPUT_DIR, filename);
            
            // 保存文件
            fs.writeFileSync(filepath, buffer);
            this.downloaded.push(filepath);
            
            console.log(`  ✅ 保存: ${filename} (${buffer.length/1024}KB)`);
            
        } catch (e) {
            this.errors.push(`Download ${productName} ${index}: ${e.message}`);
            console.log(`  ❌ 下载失败: ${e.message}`);
        }
    }
    
    async crawlUsingViewport() {
        console.log('\n🎯 使用全页面截图方法...');
        
        const page = await this.browser.newPage();
        
        // 设置视口
        await page.setViewport({ width: 1920, height: 3000 });
        
        try {
            // 访问Hermes主页
            console.log('  🌐 访问Hermes官网...');
            await page.goto('https://www.hermes.com/us/en/', {
                waitUntil: 'networkidle2',
                timeout: 60000
            });
            
            // 搜索Birkin
            console.log('  🔍 搜索Birkin...');
            const searchInput = await page.$('input[type="search"], input[name="search"], input[placeholder*="Search"]');
            
            if (searchInput) {
                await searchInput.type('Birkin 30 Noir', { delay: 100 });
                await searchInput.press('Enter');
                await page.waitForTimeout(5000);
                
                // 截图页面
                const screenshotPath = path.join(TEMP_DIR, 'hermes_search_results.jpg');
                await page.screenshot({ 
                    path: screenshotPath, 
                    fullPage: false,
                    clip: { x: 0, y: 0, width: 1920, height: 1080 }
                });
                
                console.log(`  📸 截图已保存: ${screenshotPath}`);
                
                // 复制到素材库
                fs.copyFileSync(screenshotPath, path.join(OUTPUT_DIR, 'hermes_search_results.jpg'));
                this.downloaded.push(path.join(OUTPUT_DIR, 'hermes_search_results.jpg'));
                console.log(`  ✅ 已复制到素材库`);
            }
            
        } catch (e) {
            this.errors.push(`Viewport method: ${e.message}`);
            console.log(`  ❌ 错误: ${e.message}`);
        }
        
        await page.close();
    }
    
    async generateReport() {
        const report = `# Hermes官网图片爬虫报告

> 爬取时间: ${new Date().toLocaleString()}
> 输出目录: ${OUTPUT_DIR}

## 下载统计

| 项目 | 数量 |
|------|------|
| 成功下载 | ${this.downloaded.length} |
| 错误数 | ${this.errors.length} |

## 下载的文件

${this.downloaded.map((f, i) => `${i + 1}. ${path.basename(f)}`).join('\n') || '无'}

## 错误记录

${this.errors.length > 0 ? this.errors.map(e => `- ${e}`).join('\n') : '无错误'}

---

## 使用说明

1. 下载的图片保存在: \`${OUTPUT_DIR}\`
2. 建议手动访问Hermes官网下载高清产品图
3. 版权原因，自动下载可能受限

## 下一步

1. 手动从 https://www.hermes.com/ 下载
2. 保存到素材库对应目录
3. 创建内容并发布

`;
        
        const reportPath = path.join(OUTPUT_DIR, '..', '爬虫报告.md');
        fs.writeFileSync(reportPath, report);
        console.log(`\n📊 报告已生成: ${reportPath}`);
    }
    
    async run() {
        console.log('\n' + '='.repeat(60));
        console.log('  🎀 Hermes官网图片爬虫 v2.0');
        console.log('='.repeat(60));
        
        await this.init();
        
        // 方法1: 爬取产品页面
        await this.crawlHermesProducts();
        
        // 方法2: 全页面截图
        await this.crawlUsingViewport();
        
        // 关闭浏览器
        if (this.browser) {
            await this.browser.close();
        }
        
        // 生成报告
        this.generateReport();
        
        console.log(`\n✅ 爬取完成!`);
        console.log(`   下载: ${this.downloaded.length} 张`);
        console.log(`   错误: ${this.errors.length} 个`);
        console.log(`   位置: ${OUTPUT_DIR}`);
    }
}

// 检查依赖
async function checkDependencies() {
    console.log('\n🔍 检查依赖...');
    
    try {
        require.resolve('puppeteer');
        console.log('✅ Puppeteer已安装');
        return true;
    } catch (e) {
        console.log('⚠️  Puppeteer未安装');
        console.log('\n📋 安装方法:');
        console.log('1. npm install puppeteer');
        console.log('2. node hermes_official_crawler.js');
        return false;
    }
}

// 主程序
async function main() {
    const hasPuppeteer = await checkDependencies();
    
    if (hasPuppeteer) {
        const crawler = new HermesOfficialCrawler();
        await crawler.run();
    } else {
        console.log('\n📋 替代方案:');
        console.log('');
        console.log('1️⃣  手动访问Hermes官网');
        console.log('   访问: https://www.hermes.com/');
        console.log('   搜索: Birkin 30 Noir');
        console.log('   右键图片 → 另存为');
        console.log('');
        console.log('2️⃣  使用截图工具');
        console.log('   打开Hermes产品页面');
        console.log('   截图保存');
        console.log('');
        console.log('3️⃣  联系Hermes公关获取官方素材');
    }
}

main().catch(console.error);