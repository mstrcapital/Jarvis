#!/usr/bin/env node
/**
 * Postiz Multi-Post Script v2.0
 * 批量发布Larry风格内容到TikTok/Instagram
 */

const axios = require('axios');
const fs = require('fs');

// 配置
const API_KEY = 'c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d';
const API_BASE = 'https://api.postiz.com/public/v1';

// 图片和文案
const POSTS = [
    {
        image: 'https://uploads.postiz.com/ijHzLt7sDN.jpeg',
        caption: "I just spent $45,000 on a bag and my bank account is SCREAMING 😬🖤\n\nThe Birkin 30 black leather is giving main character energy. Yes, it's expensive. Yes, it's worth it.\n\n#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags #BagCollector #HermesCollection #InvestmentBag"
    },
    {
        image: 'https://uploads.postiz.com/25iWgcmfD4.jpeg',
        caption: "90% of buyers can't spot this fake detail 😬\n\nReal Hermès hardware tells a story. Every piece is solid brass. The gold won't rub off. The font is crisp. The screws are flat-head and hand-finished. 💎\n\n#Hermès #LuxuryResale #AuthenticityCheck #Birkin #BagCollector"
    },
    {
        image: 'https://uploads.postiz.com/NZi3WskqPL.jpeg',
        caption: "The timeless classic\n\nBirkin 30 • Noir\n\n• Togo leather / Palladium hardware\n• The most versatile Birkin size\n\n#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags #HermesCollection"
    },
    {
        image: 'https://uploads.postiz.com/JB29dAuIPf.jpeg',
        caption: "Dream bag unlocked 🔓\n\nBirkin 30 in Black Togo\nThe bag that started it all\n\n#HermesBirkin #Birkin30 #LuxuryBags #BagCollector #HermesCollection"
    }
];

// TikTok Channel
const TIKTOK_CHANNEL = 'cmlomzyp90166qf0y1qvcpzyh';
// Instagram Channel
const INSTAGRAM_CHANNEL = 'cmlon7x9a016jqf0y440vzy3d';

async function createPost(content, imageUrl, channelId, scheduledAt) {
    try {
        const payload = {
            posts: [{
                content: content,
                media: [{ url: imageUrl }],
                settings: {
                    privacy_level: 'PUBLIC_TO_EVERYONE',
                    content_posting_method: 'UPLOAD',
                    duet: false,
                    stitch: false,
                    comment: true,
                    autoAddMusic: 'no',
                    brand_content_toggle: false,
                    brand_organic_toggle: false
                }
            }],
            integration_ids: [channelId],
            scheduled_at: scheduledAt,
            type: 'schedule'
        };

        const response = await axios.post(`${API_BASE}/posts`, payload, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        return null;
    }
}

async function main() {
    console.log('======================================');
    console.log('  Larry Content Multi-Post v2.0');
    console.log('======================================\n');

    let tiktokCount = 0;
    let instagramCount = 0;

    // 发布到TikTok
    console.log('📱 发布到 TikTok...');
    for (let i = 0; i < POSTS.length; i++) {
        const scheduledAt = new Date(Date.now() + (i + 1) * 2 * 60 * 60 * 1000).toISOString(); // 每2小时一个帖子
        
        console.log(`\n  帖子 ${i + 1}/4: ${POSTS[i].caption.substring(0, 50)}...`);
        const result = await createPost(POSTS[i].caption, POSTS[i].image, TIKTOK_CHANNEL, scheduledAt);
        
        if (result) {
            console.log('    ✅ 成功!');
            tiktokCount++;
        } else {
            console.log('    ❌ 失败');
        }
    }

    // 发布到Instagram
    console.log('\n\n📷 发布到 Instagram...');
    for (let i = 0; i < POSTS.length; i++) {
        const scheduledAt = new Date(Date.now() + (i + 1) * 2.5 * 60 * 60 * 1000).toISOString();
        
        console.log(`\n  帖子 ${i + 1}/4...`);
        const result = await createPost(POSTS[i].caption, POSTS[i].image, INSTAGRAM_CHANNEL, scheduledAt);
        
        if (result) {
            console.log('    ✅ 成功!');
            instagramCount++;
        } else {
            console.log('    ❌ 失败');
        }
    }

    console.log('\n======================================');
    console.log(`  完成!`);
    console.log(`  TikTok: ${tiktokCount} 帖子`);
    console.log(`  Instagram: ${instagramCount} 帖子`);
    console.log('======================================');
}

main().catch(console.error);