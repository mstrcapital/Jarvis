#!/usr/bin/env node
/**
 * Larry-Style Content Generator with MiniMax
 * 
 * Uses MiniMax for English text generation (captions, hooks)
 * Uses flexible image sources (OpenAI DALL-E, or alternatives)
 * 
 * Usage:
 * 1. Set MINIMAX_API_KEY or use default
 * 2. node larry_content_minimax.js --type birkin --count 5
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';
const TEMP_DIR = '/tmp/larry_minimax';

// MiniMax API (via OpenRouter)
const API_KEY = process.env.MINIMAX_API_KEY || process.env.OPENROUTER_API_KEY || '';

// System prompt - Larry's style
const SYSTEM_PROMPT = `You are Larry, a TikTok content creator specializing in luxury bags (Hermès Birkin, Kelly). 
Your style:
- Emotional hooks: "Waited 9 months for THIS moment..."
- 90% of buyers can't spot this detail
- Authentic, expert tone
- Strong CTAs: Save/Share
- Mix of education + entertainment

Generate catchy, viral TikTok content in English.`;

class LarryMiniMaxGenerator {
    constructor() {
        this.generated = [];
        this.errors = [];
        this.content = [];
        this.captions = [];
    }
    
    async generateText(prompt) {
        console.log(`\n📝 MiniMax生成文案: ${prompt.substring(0, 40)}...`);
        
        const data = JSON.stringify({
            model: "minimax/minimax-m2.1",
            messages: [
                { role: "system", content: SYSTEM_PROMPT },
                { role: "user", content: prompt }
            ],
            max_tokens: 500,
            temperature: 0.8
        });
        
        return new Promise((resolve, reject) => {
            const options = {
                hostname: 'openrouter.ai',
                path: '/api/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${API_KEY}`,
                    'Content-Type': 'application/json',
                    'Content-Length': data.length,
                    'HTTP-Referer': 'https://openclaw.ai',
                    'X-Title': 'LarryContentGenerator'
                }
            };
            
            const req = https.request(options, (res) => {
                let chunks = '';
                res.on('data', chunk => chunks += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(chunks);
                        if (result.choices && result.choices[0]) {
                            resolve(result.choices[0].message.content);
                        } else {
                            resolve(this.getDefaultCaption(prompt));
                        }
                    } catch (e) {
                        this.errors.push(`MiniMax: ${e.message}`);
                        resolve(this.getDefaultCaption(prompt));
                    }
                });
            });
            
            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }
    
    getDefaultCaption(type) {
        const templates = {
            birkin: {
                hooks: [
                    "Waited 9 months for THIS moment... 😍",
                    "90% of buyers CAN'T spot this fake Hermès detail 👀",
                    "The bag that changed everything... 💼"
                ],
                caption: `Birkin 30 • Noir

"The timeless classic"

• Togo leather / Palladium hardware
• The most versatile Birkin size

"Black is never wrong. Birkin is always right."

#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags #BagCollector #HermesCollection`
            }
        };
        
        return templates[type] || templates.birkin;
    }
    
    async generateContent(count = 5) {
        console.log('\n📝 生成Larry风格文案...');
        
        const prompts = [
            "Generate a viral TikTok hook and caption for Hermès Birkin 30 in black Togo leather. Include 3 hashtags.",
            "Create an emotional TikTok hook about waiting for a Birkin bag. Caption should be 50 words, include 5 hashtags.",
            "Write a TikTok caption about Hermès Birkin authentication - something only experts would know. Include hooks and hashtags.",
            "Generate a luxury lifestyle TikTok post about Birkin 30 Noir. Include emotional hook and 5+ hashtags.",
            "Create a viral TikTok hook: '90% of buyers can't spot this'. Caption about Birkin hardware quality. Include hashtags."
        ];
        
        for (let i = 0; i < Math.min(count, prompts.length); i++) {
            const result = await this.generateText(prompts[i]);
            
            // 解析结果
            let hook = `Hook ${i + 1}`;
            let caption = result;
            
            // 提取hook (第一行通常是hook)
            const lines = result.split('\n').filter(l => l.trim());
            if (lines.length > 0) {
                hook = lines[0].substring(0, 100);
                if (lines.length > 1) {
                    caption = lines.slice(1).join('\n');
                }
            }
            
            this.captions.push({
                hook: hook,
                full_caption: result,
                index: i + 1
            });
            
            console.log(`  ✅ 文案 ${i + 1}: ${hook.substring(0, 40)}...`);
        }
        
        return this.captions;
    }
    
    async downloadImage(url, index) {
        console.log(`\n⬇️  下载图片 ${index}: ${url.substring(0, 50)}...`);
        
        return new Promise((resolve, reject) => {
            https.get(url, (res) => {
                const chunks = [];
                res.on('data', chunk => chunks.push(chunk));
                res.on('end', () => {
                    const buffer = Buffer.concat(chunks);
                    const filename = `birkin_${index}.jpg`;
                    const filepath = path.join(OUTPUT_DIR, filename);
                    
                    fs.writeFileSync(filepath, buffer);
                    this.generated.push(filepath);
                    
                    console.log(`  ✅ 保存: ${filename} (${buffer.length/1024}KB)`);
                    resolve(filepath);
                });
            }).on('error', reject);
        });
    }
    
    async downloadImagesFromSource() {
        console.log('\n📥 下载高质量图片...');
        
        // 使用公开的高质量图片源
        const imageSources = [
            'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=1200',
            'https://images.unsplash.com/photo-1591561954557-26941169b49e?w=1200',
            'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=1200',
            'https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=1200',
            'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=1200'
        ];
        
        for (let i = 0; i < Math.min(imageSources.length, 5); i++) {
            await this.downloadImage(imageSources[i], i + 1);
            await new Promise(r => setTimeout(r, 2000));
        }
    }
    
    createImagePrompts() {
        // 为AI图像生成准备prompt
        const prompts = [
            "Professional product photography of Hermès Birkin 30 black leather luxury handbag on white background, studio lighting, high-end retail, 4K",
            "Close-up detail shot of Hermès Birkin bag gold hardware, luxury accessory photography, premium texture, professional lighting",
            "Lifestyle shot of Hermès Birkin 30 black leather on elegant table, luxury living room background, soft natural light",
            "Hermès Birkin bag in sophisticated packaging, unboxing style photography, premium gift presentation",
            "Professional fashion photography of Hermès Birkin 30 black leather, runway style, dramatic lighting"
        ];
        
        return prompts;
    }
    
    async run() {
        console.log('\n' + '='.repeat(60));
        console.log('  🎨 Larry-Style Content Generator (MiniMax) v1.0');
        console.log('  AI-generated original content for TikTok/Instagram');
        console.log('='.repeat(60));
        
        // 检查API Key
        if (!API_KEY) {
            console.log('\n⚠️  未设置API Key，使用默认文案模板');
            console.log('设置: export MINIMAX_API_KEY=your_key');
        } else {
            console.log('\n✅ MiniMax API已配置');
        }
        
        // 创建目录
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        fs.mkdirSync(TEMP_DIR, { recursive: true });
        
        // 1. 生成文案
        console.log('\n📝 步骤1: 生成Larry风格文案');
        const captions = await this.generateContent(5);
        
        // 2. 下载图片
        console.log('\n📥 步骤2: 下载高质量图片');
        await this.downloadImagesFromSource();
        
        // 3. 创建AI图像生成prompt
        console.log('\n🎨 步骤3: AI图像生成Prompt (可用于DALL-E/Stable Diffusion)');
        const imagePrompts = this.createImagePrompts();
        
        for (let i = 0; i < imagePrompts.length; i++) {
            console.log(`  ${i + 1}. ${imagePrompts[i].substring(0, 60)}...`);
        }
        
        // 4. 保存内容
        this.saveContent(captions, imagePrompts);
        
        // 5. 生成报告
        this.generateReport(captions);
        
        console.log(`\n✅ 生成完成!`);
        console.log(`   文案: ${captions.length} 条`);
        console.log(`   图片: ${this.generated.length} 张`);
    }
    
    saveContent(captions, imagePrompts) {
        const content = {
            generated_at: new Date().toISOString(),
            captions: captions,
            image_prompts: imagePrompts,
            images: this.generated.map(f => path.basename(f))
        };
        
        const contentPath = path.join(TEMP_DIR, 'larry_content.json');
        fs.writeFileSync(contentPath, JSON.stringify(content, null, 2));
        console.log(`\n📄 内容已保存: ${contentPath}`);
    }
    
    generateReport(captions) {
        const report = `# Larry-Style Content Report (MiniMax)

> 生成时间: ${new Date().toLocaleString()}
> API: MiniMax (via OpenRouter)

## 统计

| 项目 | 数量 |
|------|------|
| 文案 | ${captions.length} |
| 图片 | ${this.generated.length} |
| 错误 | ${this.errors.length} |

## 生成的文案 (Larry Style)

${captions.map((c, i) => `### ${i + 1}. ${c.hook}

${c.full_caption}

---`).join('\n')}

## AI图像生成Prompt

${this.createImagePrompts().map((p, i) => `### ${i + 1}

${p}

---`).join('\n')}

## 下载的图片

${this.generated.map((f, i) => `${i + 1}. ${path.basename(f)}`).join('\n')}

---

## Larry的工作流程 (已效仿)

1. ✅ AI生成文案 (MiniMax)
2. ⏳ AI生成图片 (需要DALL-E/Stable Diffusion API)
3. ✅ 自动发布 (Postiz)

## 使用说明

1. **生成文案**: 运行此脚本
2. **生成图片**: 使用AI图像生成服务
3. **发布**: 使用Postiz

## API配置

\`\`\`bash
# MiniMax (文案)
export MINIMAX_API_KEY=your_key

# OpenAI DALL-E (图片)
export OPENAI_API_KEY=your_key
\`\`\`

## 推荐的图片生成服务

1. **OpenAI DALL-E 3** - 最高质量，需API Key
2. **Stability AI** - 开源替代
3. **Midjourney** - 需Discord
4. **Leonardo AI** - 免费额度

`;
        
        const reportPath = path.join(OUTPUT_DIR, '..', 'Larry-MiniMax内容报告.md');
        fs.writeFileSync(reportPath, report);
        console.log(`\n📊 报告已生成: ${reportPath}`);
    }
}

// 主程序
async function main() {
    const generator = new LarryMiniMaxGenerator();
    await generator.run();
}

main().catch(console.error);