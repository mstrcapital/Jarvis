#!/usr/bin/env node
/**
 * Larry-Style Content Generator with MiniMax v2.0
 * 
 * Fixed version - better error handling
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';
const TEMP_DIR = '/tmp/larry_minimax';

const API_KEY = process.env.MINIMAX_API_KEY || '';

class LarryMiniMaxGenerator {
    constructor() {
        this.generated = [];
        this.errors = [];
        this.captions = [];
    }
    
    async generateText(prompt) {
        console.log(`📝 生成: ${prompt.substring(0, 40)}...`);
        
        const data = JSON.stringify({
            model: "minimax/minimax-m2.1",
            messages: [
                { role: "system", content: "You are Larry, a TikTok creator for luxury bags. Write viral English hooks and captions." },
                { role: "user", content: prompt }
            ],
            max_tokens: 500
        });
        
        return new Promise((resolve) => {
            const options = {
                hostname: 'openrouter.ai',
                path: '/api/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${API_KEY}`,
                    'Content-Type': 'application/json'
                }
            };
            
            const req = https.request(options, (res) => {
                let chunks = '';
                res.on('data', chunk => chunks += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(chunks);
                        const text = result?.choices?.[0]?.message?.content || '';
                        resolve(text || generateFallback(prompt));
                    } catch (e) {
                        this.errors.push(e.message);
                        resolve(generateFallback(prompt));
                    }
                });
            });
            
            req.on('error', (e) => {
                this.errors.push(e.message);
                resolve(generateFallback(prompt));
            });
            
            req.write(data);
            req.end();
        });
    }
    
    async run() {
        console.log('\n' + '='.repeat(60));
        console.log('  🎨 Larry-Style Content Generator v2.0');
        console.log('='.repeat(60));
        
        if (!API_KEY) {
            console.log('\n⚠️  未配置API Key，使用默认模板');
        } else {
            console.log('\n✅ MiniMax已配置');
        }
        
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        fs.mkdirSync(TEMP_DIR, { recursive: true });
        
        // 生成5条Larry风格文案
        const prompts = [
            "Write a viral TikTok hook and caption for Hermès Birkin 30 black. Include 5 hashtags.",
            "Create emotional TikTok content about waiting 9 months for Birkin. Hook + caption.",
            "Write about Hermès hardware authentication - only experts know this detail. Hook + caption.",
            "Generate luxury lifestyle TikTok post about Birkin 30 Noir. Emotional hook + caption + hashtags.",
            "Create viral hook: '90% buyers can't spot this'. Caption about Birkin quality. Hashtags."
        ];
        
        for (let i = 0; i < prompts.length; i++) {
            const result = await this.generateText(prompts[i]);
            
            this.captions.push({
                hook: result.split('\n')[0] || `Hook ${i+1}`,
                full: result,
                index: i + 1
            });
            
            console.log(`  ✅ 文案 ${i+1}: ${this.captions[i].hook.substring(0, 40)}...`);
        }
        
        // 保存
        this.save();
        this.generateReport();
        
        console.log(`\n✅ 完成! 生成 ${this.captions.length} 条文案`);
    }
    
    save() {
        const contentPath = path.join(TEMP_DIR, 'captions.json');
        fs.writeFileSync(contentPath, JSON.stringify(this.captions, null, 2));
        console.log(`\n📄 文案已保存: ${contentPath}`);
    }
    
    generateReport() {
        const report = `# Larry-Style Content Report

> 生成时间: ${new Date().toLocaleString()}

## 生成的文案

${this.captions.map((c, i) => `### ${i+1}. ${c.hook}

${c.full}

---`).join('\n')}

## 发布到Postiz

\`\`\`bash
# 1. 上传图片
postiz upload [图片路径]

# 2. 发布文案
postiz posts:create -c "[文案]" -m [图片URL] -i [channel_id]
\`\`\`

`;
        
        const reportPath = path.join(OUTPUT_DIR, '..', 'Larry文案报告.md');
        fs.writeFileSync(reportPath, report);
        console.log(`📊 报告: ${reportPath}`);
    }
}

function generateFallback(prompt) {
    const fallbacks = {
        'birkin': `Waited 9 months for THIS moment... 😍

Birkin 30 • Noir

"The timeless classic"

• Togo leather / Palladium hardware
• The most versatile Birkin size

#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags`
    };
    
    if (prompt.includes('Birkin')) return fallbacks['birkin'];
    return `Viral TikTok content about luxury bags

#LuxuryBags #HermesBirkin`;
}

new LarryMiniMaxGenerator().run().catch(console.error);