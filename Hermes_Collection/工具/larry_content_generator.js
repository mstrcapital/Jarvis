#!/usr/bin/env node
/**
 * Larry-Style Content Generator
 * 
 * AI-generated original content for TikTok/Instagram
 * Uses OpenAI DALL-E for image generation
 * 
 * Usage:
 * 1. Set OPENAI_API_KEY
 * 2. node larry_content_generator.js --type birkin --count 5
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';
const TEMP_DIR = '/tmp/larry_content';

// OpenAI API配置
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';

// Larry's Content Templates
const CONTENT_TEMPLATES = {
    birkin: {
        hooks: [
            "Waited 9 months for THIS moment... 😍",
            "90% of buyers CAN'T spot this fake Hermès detail 👀",
            "The bag that changed everything... 💼",
            "Just received my dream bag! 😱",
            "POV: You finally got the call 📞"
        ],
        captions: [
            "Birkin 30 • Noir\n\n'The timeless classic'\n\n• Togo leather / Palladium hardware\n• The most versatile Birkin size\n\n'Black is never wrong. Birkin is always right.'",
            "Dream bag unlocked 🔓\n\nBirkin 30 in Black Togo\nThe bag that started it all\n\n#HermesBirkin #Birkin30 #LuxuryBags"
        ],
        hashtags: [
            '#HermesBirkin', '#Birkin30', '#BirkinNoir', '#LuxuryBags',
            '#BagCollector', '#HermesCollection', '#InvestmentBag',
            '#BirkinLove', '#HermesObsessed', '#LuxuryLife'
        ]
    },
    kelly: {
        hooks: [
            "Kelly 28 finally in my hands! 👜",
            "The elegant sister of Birkin 💎",
            "POV: Walking out with your Kelly 😎"
        ],
        captions: [
            "Kelly 28 • Noir\n\n'Elegance is the only beauty that never fades'\n\n• Epsom leather / Palladium hardware\n• Perfect for evening occasions\n\n#HermesKelly #Kelly28"
        ],
        hashtags: [
            '#HermesKelly', '#Kelly28', '#KellyNoir', '#LuxuryBags',
            '#BagCollector', '#HermesCollection'
        ]
    }
};

class LarryContentGenerator {
    constructor() {
        this.generated = [];
        this.errors = [];
        this.content = [];
    }
    
    async generateImage(prompt, index) {
        console.log(`\n🎨 生成图片 ${index}: ${prompt.substring(0, 50)}...`);
        
        if (!OPENAI_API_KEY) {
            console.log('⚠️  OpenAI API Key未设置，使用备用方案');
            return this.generatePlaceholderImage(prompt, index);
        }
        
        try {
            // 调用OpenAI DALL-E API
            const response = await this.callOpenAI(prompt);
            
            if (response && response.data) {
                // 下载图片
                const imageUrl = response.data[0].url;
                return await this.downloadImage(imageUrl, index);
            }
            
        } catch (e) {
            this.errors.push(`OpenAI API: ${e.message}`);
            console.log(`  ❌ API错误: ${e.message}`);
        }
        
        // 备用：生成占位图
        return this.generatePlaceholderImage(prompt, index);
    }
    
    async callOpenAI(prompt) {
        return new Promise((resolve, reject) => {
            const data = JSON.stringify({
                model: 'dall-e-3',
                prompt: prompt,
                n: 1,
                size: '1024x1024'
            });
            
            const options = {
                hostname: 'api.openai.com',
                path: '/v1/images/generations',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${OPENAI_API_KEY}`,
                    'Content-Type': 'application/json',
                    'Content-Length': data.length
                }
            };
            
            const req = https.request(options, (res) => {
                let chunks = '';
                res.on('data', chunk => chunks += chunk);
                res.on('end', () => {
                    try {
                        resolve(JSON.parse(chunks));
                    } catch (e) {
                        reject(e);
                    }
                });
            });
            
            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }
    
    async downloadImage(url, index) {
        return new Promise((resolve, reject) => {
            https.get(url, (res) => {
                const chunks = [];
                res.on('data', chunk => chunks.push(chunk));
                res.on('end', () => {
                    const buffer = Buffer.concat(chunks);
                    const filename = `larry_generated_${index}.png`;
                    const filepath = path.join(OUTPUT_DIR, filename);
                    
                    fs.writeFileSync(filepath, buffer);
                    this.generated.push(filepath);
                    
                    console.log(`  ✅ 保存: ${filename} (${buffer.length/1024}KB)`);
                    resolve(filepath);
                });
            }).on('error', reject);
        });
    }
    
    generatePlaceholderImage(prompt, index) {
        // 创建高质量占位图
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
            <rect width="1080" height="1080" fill="#1a1a1a"/>
            <text x="540" y="400" font-family="Arial" font-size="48" fill="#FFD700" text-anchor="middle">HERMÈS</text>
            <text x="540" y="500" font-family="Arial" font-size="32" fill="#ffffff" text-anchor="middle">${prompt.substring(0, 30)}</text>
            <text x="540" y="700" font-family="Arial" font-size="24" fill="#888888" text-anchor="middle">AI Generated Content</text>
            <text x="540" y="800" font-family="Arial" font-size="18" fill="#666666" text-anchor="middle">Larry Style Generator v1.0</text>
        </svg>`;
        
        const filename = `larry_generated_${index}.svg`;
        const filepath = path.join(OUTPUT_DIR, filename);
        
        fs.writeFileSync(filepath, svg);
        this.generated.push(filepath);
        
        console.log(`  ✅ 创建占位图: ${filename}`);
        return filepath;
    }
    
    generateCaption(type, hook) {
        const template = CONTENT_TEMPLATES[type];
        
        const caption = `${hook}\n\n${template.captions[0]}\n\n${template.hashtags.join(' ')}`;
        
        return caption;
    }
    
    async run() {
        console.log('\n' + '='.repeat(60));
        console.log('  🎨 Larry-Style Content Generator v1.0');
        console.log('  AI-generated original content for TikTok/Instagram');
        console.log('='.repeat(60));
        
        // 创建目录
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        fs.mkdirSync(TEMP_DIR, { recursive: true });
        
        console.log('\n📋 生成配置:');
        console.log(`   类型: birkin`);
        console.log(`   数量: 5`);
        console.log(`   输出: ${OUTPUT_DIR}`);
        
        // 生成图片
        const prompts = [
            'Hermes Birkin 30 black leather luxury bag on white background',
            'Hermes Birkin 30 noir Togo leather close-up detail',
            'Hermes Birkin bag in elegant lifestyle setting',
            'Hermes Birkin 30 with gold hardware close-up',
            'Hermes Birkin 30 black leather professional product photography'
        ];
        
        for (let i = 0; i < prompts.length; i++) {
            await this.generateImage(prompts[i], i + 1);
            await new Promise(r => setTimeout(r, 2000)); // 延迟
        }
        
        // 生成文案
        console.log('\n📝 生成文案...');
        const hooks = CONTENT_TEMPLATES.birkin.hooks;
        
        for (let i = 0; i < Math.min(hooks.length, this.generated.length); i++) {
            const caption = this.generateCaption('birkin', hooks[i]);
            
            this.content.push({
                image: this.generated[i],
                caption: caption,
                hook: hooks[i]
            });
            
            console.log(`  ✅ 文案 ${i + 1}: ${hooks[i].substring(0, 30)}...`);
        }
        
        // 保存内容到文件
        this.saveContent();
        
        // 生成报告
        this.generateReport();
        
        console.log(`\n✅ 生成完成!`);
        console.log(`   图片: ${this.generated.length} 张`);
        console.log(`   文案: ${this.content.length} 条`);
        console.log(`   错误: ${this.errors.length} 个`);
    }
    
    saveContent() {
        const contentPath = path.join(TEMP_DIR, 'content.json');
        
        fs.writeFileSync(contentPath, JSON.stringify(this.content, null, 2));
        console.log(`\n📄 内容已保存: ${contentPath}`);
    }
    
    generateReport() {
        const report = `# Larry-Style Content生成报告

> 生成时间: ${new Date().toLocaleString()}
> 输出目录: ${OUTPUT_DIR}

## 统计

| 项目 | 数量 |
|------|------|
| 生成图片 | ${this.generated.length} |
| 生成文案 | ${this.content.length} |
| 错误 | ${this.errors.length} |

## 生成的图片

${this.generated.map((f, i) => `${i + 1}. ${path.basename(f)}`).join('\n')}

## 生成的文案

${this.content.map((c, i) => `### ${i + 1}. ${c.hook}

${c.caption}

---`).join('\n')}

## 错误记录

${this.errors.length > 0 ? this.errors.map(e => `- ${e}`).join('\n') : '无'}

---

## 使用说明

1. 设置OpenAI API Key: \`export OPENAI_API_KEY=your_key\`
2. 运行: \`node larry_content_generator.js\`
3. 查看生成的内容
4. 使用Postiz发布

## Larry的工作流程

1. 研究TikTok趋势
2. AI生成图片 (DALL-E)
3. AI撰写文案 (Claude)
4. 自动发布 (Postiz)

## 与Larry的区别

| 项目 | Larry | 当前版本 |
|------|-------|----------|
| 图片生成 | OpenAI DALL-E 3 | 需API Key |
| 文案生成 | Claude | 模板 |
| 发布 | Postiz API | 需手动 |

`;
        
        const reportPath = path.join(OUTPUT_DIR, '..', 'Larry内容报告.md');
        fs.writeFileSync(reportPath, report);
        console.log(`\n📊 报告已生成: ${reportPath}`);
    }
}

// 主程序
async function main() {
    const generator = new LarryContentGenerator();
    await generator.run();
}

main().catch(console.error);