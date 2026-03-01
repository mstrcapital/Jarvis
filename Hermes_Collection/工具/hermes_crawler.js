#!/usr/bin/env node
/**
 * Hermes图片爬虫 v1.0
 * 
 * 从合法网站爬取Hermes相关免费图片
 * 
 * 使用方法:
 * 1. npm install puppeteer
 * 2. node hermes_crawler.js
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';
const TEMP_DIR = '/tmp/hermes_crawler';

class HermesCrawler {
    constructor() {
        this.downloaded = [];
        this.errors = [];
        this.browser = null;
    }
    
    async init() {
        console.log('\n🔧 初始化爬虫...');
        
        // 创建目录
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        fs.mkdirSync(TEMP_DIR, { recursive: true });
        
        // 尝试启动浏览器
        try {
            this.browser = await puppeteer.launch({
                headless: 'new',
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });
            console.log('✅ 浏览器启动成功');
        } catch (e) {
            console.log('⚠️  Puppeteer不可用，尝试其他方法');
        }
    }
    
    async crawlPexels(query) {
        console.log(`\n🔍 从Pexels爬取: ${query}`);
        
        if (!this.browser) {
            console.log('❌ 浏览器未启动，跳过Pexels');
            return [];
        }
        
        const page = await this.browser.newPage();
        const urls = [];
        
        try {
            await page.goto(`https://www.pexels.com/search/${query.replace(' ', '%20')}/`, {
                waitUntil: 'networkidle0',
                timeout: 30000
            });
            
            // 查找图片
            const images = await page.$$eval('img[src*="images.pexels.com"]', imgs => 
                imgs.map(img => img.src).slice(0, 10)
            );
            
            for (const src of images) {
                if (src && !urls.includes(src)) {
                    urls.push(src);
                    console.log(`  ✅ 找到图片: ${src.substring(0, 50)}...`);
                }
            }
            
        } catch (e) {
            this.errors.push(`Pexels: ${e.message}`);
            console.log(`  ❌ 错误: ${e.message}`);
        }
        
        await page.close();
        return urls;
    }
    
    async crawlUnsplash(query) {
        console.log(`\n🔍 从Unsplash爬取: ${query}`);
        
        if (!this.browser) {
            console.log('❌ 浏览器未启动，跳过Unsplash');
            return [];
        }
        
        const page = await this.browser.newPage();
        const urls = [];
        
        try {
            await page.goto(`https://unsplash.com/s/photos/${query.replace(' ', '-')}`, {
                waitUntil: 'networkidle0',
                timeout: 30000
            });
            
            // 查找图片
            const images = await page.$$eval('img[src*="images.unsplash.com"]', imgs =>
                imgs.map(img => img.src).slice(0, 10)
            );
            
            for (const src of images) {
                if (src && !urls.includes(src)) {
                    urls.push(src);
                    console.log(`  ✅ 找到图片: ${src.substring(0, 50)}...`);
                }
            }
            
        } catch (e) {
            this.errors.push(`Unsplash: ${e.message}`);
            console.log(`  ❌ 错误: ${e.message}`);
        }
        
        await page.close();
        return urls;
    }
    
    async crawlPinterest(query) {
        console.log(`\n🔍 从Pinterest爬取: ${query}`);
        
        if (!this.browser) {
            console.log('❌ 浏览器未启动，跳过Pinterest');
            return [];
        }
        
        const page = await this.browser.newPage();
        const urls = [];
        
        try {
            await page.goto(`https://www.pinterest.com/search/pins/?q=${query.replace(' ', '%20')}`, {
                waitUntil: 'networkidle0',
                timeout: 30000
            });
            
            // 查找图片
            const images = await page.$$eval('img[src*="i.pinimg.com"]', imgs =>
                imgs.map(img => img.src).filter(src => src.includes('236x')).slice(0, 20)
            );
            
            for (const src of images) {
                if (src && !urls.includes(src)) {
                    urls.push(src);
                    console.log(`  ✅ 找到图片: ${src.substring(0, 50)}...`);
                }
            }
            
        } catch (e) {
            this.errors.push(`Pinterest: ${e.message}`);
            console.log(`  ❌ 错误: ${e.message}`);
        }
        
        await page.close();
        return urls;
    }
    
    async downloadImage(url, index) {
        if (!this.browser) {
            console.log('❌ 浏览器未启动，无法下载');
            return null;
        }
        
        try {
            const page = await this.browser.newPage();
            
            // 转到图片URL
            await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
            
            // 获取页面HTML
            const html = await page.content();
            
            // 查找实际图片URL
            const match = html.match(/<img[^>]+src=["']([^"']+)["']/i);
            
            await page.close();
            
            if (match && match[1]) {
                const imgUrl = match[1];
                
                // 下载图片
                const response = await this.browser.newPage();
                await response.goto(imgUrl, { waitUntil: 'networkidle0', timeout: 30000 });
                
                const buffer = await response.screenshot();
                await response.close();
                
                // 保存文件
                const ext = imgUrl.includes('.png') ? '.png' : '.jpg';
                const filename = `hermes_${index}${ext}`;
                const filepath = path.join(OUTPUT_DIR, filename);
                
                fs.writeFileSync(filepath, buffer);
                this.downloaded.push(filepath);
                
                console.log(`  ✅ 下载成功: ${filename} (${buffer.length/1024}KB)`);
                
                return filepath;
            }
            
        } catch (e) {
            this.errors.push(`Download ${index}: ${e.message}`);
            console.log(`  ❌ 下载失败: ${e.message}`);
        }
        
        return null;
    }
    
    async run() {
        console.log('\n' + '='.repeat(50));
        console.log('  🎀 Hermes图片爬虫 v1.0');
        console.log('='.repeat(50));
        
        await this.init();
        
        const allUrls = [];
        
        // 爬取各网站
        allUrls.push(...await this.crawlPexels('luxury handbag black'));
        allUrls.push(...await this.crawlUnsplash('luxury bag black'));
        allUrls.push(...await this.crawlPinterest('hermes birkin black'));
        
        // 去重
        const uniqueUrls = [...new Set(allUrls)];
        console.log(`\n📦 总共找到 ${uniqueUrls.length} 张图片`);
        
        // 下载图片
        if (uniqueUrls.length > 0) {
            console.log(`\n📥 开始下载图片...`);
            
            for (let i = 0; i < Math.min(uniqueUrls.length, 20); i++) {
                await this.downloadImage(uniqueUrls[i], i + 1);
                await new Promise(r => setTimeout(r, 2000)); // 延迟避免请求过快
            }
        } else {
            console.log('\n⚠️  未找到图片');
        }
        
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
    
    generateReport() {
        const report = `# Hermes图片爬虫报告

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

${this.errors.length > 0 ? this.errors.map(e => `- ${e}`).join('\n') : '无错误记录'}

---

## 使用说明

1. 下载的图片保存在: \`${OUTPUT_DIR}\`
2. 图片可直接用于TikTok/Instagram发布
3. 建议手动筛选高质量图片

## 下一步

1. 筛选高质量图片 (2000px+)
2. 验证是正品Hermes
3. 创建内容并发布
`;
        
        const reportPath = path.join(OUTPUT_DIR, '..', '爬虫报告.md');
        fs.writeFileSync(reportPath, report);
        console.log(`\n📊 报告已生成: ${reportPath}`);
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
        console.log('请运行: npm install puppeteer');
        return false;
    }
}

// 主程序
async function main() {
    const hasPuppeteer = await checkDependencies();
    
    if (hasPuppeteer) {
        const crawler = new HermesCrawler();
        await crawler.run();
    } else {
        console.log('\n📋 替代方案:');
        console.log('1. 安装Puppeteer: npm install puppeteer');
        console.log('2. 然后运行: node hermes_crawler.js');
        console.log('');
        console.log('或手动收集:');
        console.log('1. 访问 https://www.pexels.com/');
        console.log('2. 搜索 "luxury handbag black"');
        console.log('3. 下载免费高清图片');
    }
}

main().catch(console.error);