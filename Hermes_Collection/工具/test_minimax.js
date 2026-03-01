#!/usr/bin/env node
/**
 * Larry Content Generator - Direct API Test
 */

const https = require('https');

const API_KEY = process.env.MINIMAX_API_KEY;
const OUTPUT_DIR = '/root/.openclaw/workspace/Hermes_Collection/素材/Birkin/Birkin_30/Black_Togo';

async function generate(prompt) {
    return new Promise((resolve) => {
        const data = JSON.stringify({
            model: "minimax/minimax-m2.1",
            messages: [
                { role: "system", content: "You are Larry, TikTok creator for luxury Hermès bags. Write viral English hooks and captions." },
                { role: "user", content: prompt }
            ],
            max_tokens: 300
        });

        const req = https.request({
            hostname: 'openrouter.ai',
            path: '/api/v1/chat/completions',
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://openclaw.ai',
                'X-Title': 'LarryContent'
            }
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(body);
                    const text = json?.choices?.[0]?.message?.content || '';
                    resolve(text || 'ERROR');
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
    console.log('  🚀 Larry Content Generator - MiniMax API Test');
    console.log('='.repeat(60));

    if (!API_KEY) {
        console.log('\n❌ No API Key!');
        return;
    }

    console.log('\n✅ API Key configured');

    const prompts = [
        "Write a viral TikTok hook and caption for Hermès Birkin 30 black. Include 3 hashtags. Reply with ONLY the hook and caption.",
        "Create emotional TikTok hook: '90% of buyers can't spot this fake detail'. Caption about Hermès hardware quality. Include hashtags.",
        "Write a luxury unboxing TikTok post about Birkin 30 Noir. Emotional hook + caption + 5 hashtags."
    ];

    const results = [];
    for (let i = 0; i < prompts.length; i++) {
        console.log(`\n📝 生成文案 ${i+1}...`);
        const text = await generate(prompts[i]);
        results.push({ prompt: prompts[i], text });
        console.log(`\n✅ 结果 ${i+1}:\n${text}\n`);
    }

    // 保存结果
    const fs = require('fs');
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(`${OUTPUT_DIR}/larry_content.json`, JSON.stringify(results, null, 2));
    
    console.log(`\n✅ 已保存到 ${OUTPUT_DIR}/larry_content.json`);
}

main().catch(console.error);