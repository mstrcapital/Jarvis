#!/usr/bin/env node
/**
 * Larry Content Generator - OpenRouter Version
 */

const https = require('https');
const fs = require('fs');

const API_KEY = process.env.OPENROUTER_API_KEY || process.env.MINIMAX_API_KEY;
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';

async function generate(prompt) {
    return new Promise((resolve) => {
        const data = JSON.stringify({
            model: "minimax/minimax-m2.1",
            messages: [
                { role: "system", content: "You are Larry, TikTok creator for Hermès luxury bags. Write viral English hooks and captions." },
                { role: "user", content: prompt }
            ],
            max_tokens: 400,
            temperature: 0.9
        });

        const req = https.request({
            hostname: 'openrouter.ai',
            path: '/api/v1/chat/completions',
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://openclaw.ai',
                'X-Title': 'LarryGenerator'
            }
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(body);
                    const text = json?.choices?.[0]?.message?.content || '';
                    resolve(text);
                } catch (e) {
                    resolve('ERROR');
                }
            });
        });

        req.on('error', () => resolve('ERROR'));
        req.write(data);
        req.end();
    });
}

async function main() {
    console.log('\n' + '='.repeat(60));
    console.log('  🚀 Larry Content Generator - OpenRouter');
    console.log('='.repeat(60));

    if (!API_KEY) {
        console.log('\n❌ 请设置: export OPENROUTER_API_KEY=sk-or-v1-xxx');
        return;
    }

    console.log('\n✅ API已配置');
    console.log('Key: ' + API_KEY.substring(0, 15) + '...\n');

    const prompts = [
        "Write a viral TikTok hook (1 line) and caption (2-3 lines) for Hermès Birkin 30 black leather. Include hashtags #HermesBirkin #Birkin30",
        "Create emotional hook: '90% of buyers can't spot this fake detail'. Caption about Hermès hardware quality. Include 3-5 hashtags.",
        "Write a luxury unboxing TikTok post about Birkin 30 Noir. Emotional hook + caption. Include hashtags."
    ];

    const results = [];
    for (let i = 0; i < prompts.length; i++) {
        process.stdout.write(`📝 生成文案 ${i+1}/3... `);
        const text = await generate(prompts[i]);
        results.push({ index: i+1, prompt: prompts[i], text });
        console.log('✅\n');
        console.log(text);
        console.log('');
    }

    // 保存
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(`${OUTPUT_DIR}/larry_content.json`, JSON.stringify(results, null, 2));
    
    console.log('='.repeat(60));
    console.log(`✅ 已保存到 ${OUTPUT_DIR}/larry_content.json`);
    console.log('='.repeat(60));
}

main().catch(console.error);