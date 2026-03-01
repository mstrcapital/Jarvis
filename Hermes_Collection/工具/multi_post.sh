#!/bin/bash
# Larry Content Multi-Post Script
# 发布5个帖子到TikTok和Instagram

export POSTIZ_API_KEY="c18db8acb2e9d3520b007029baab376856e1c976e2cde5e13aa82b4b4d84841d"

echo "======================================"
echo "  Larry Content Multi-Post Script"
echo "======================================"
echo ""

# 图片和文案配置
declare -a IMAGES=(
    "https://uploads.postiz.com/ijHzLt7sDN.jpeg"
    "https://uploads.postiz.com/25iWgcmfD4.jpeg"
    "https://uploads.postiz.com/NZi3WskqPL.jpeg"
    "https://uploads.postiz.com/JB29dAuIPf.jpeg"
    "https://uploads.postiz.com/4MHBvhRWFz.jpeg"
)

declare -a CAPTIONS=(
    "I just spent \$45,000 on a bag and my bank account is SCREAMING 😬🖤\n\nThe Birkin 30 black leather is giving main character energy. Yes, it's expensive. Yes, it's worth it. Who's manifesting one with me? ✨🖤\n\n#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags #BagCollector #HermesCollection #InvestmentBag"
    "90% of buyers can't spot this fake detail 😬\n\nReal Hermès hardware tells a story. Every piece is solid brass—never lightweight, never plastic. The gold won't rub off. The font is crisp. The screws are flat-head and hand-finished. 💎\n\n#Hermès #LuxuryResale #AuthenticityCheck #Birkin #BagCollector"
    "The timeless classic\n\nBirkin 30 • Noir\n\n• Togo leather / Palladium hardware\n• The most versatile Birkin size\n\n'Black is never wrong. Birkin is always right.'\n\n#HermesBirkin #Birkin30 #BirkinNoir #LuxuryBags #HermesCollection"
    "Dream bag unlocked 🔓\n\nBirkin 30 in Black Togo\nThe bag that started it all\n\n#HermesBirkin #Birkin30 #LuxuryBags #BagCollector #HermesCollection"
    "POV: You finally got the call 📞\n\nAfter 9 months of waiting... my dream Birkin 30 is finally here. 😍\n\n#HermesBirkin #Birkin30 #DreamBag #LuxuryBags #BagCollector"
)

# 发布到TikTok
echo "📱 发布到 TikTok..."
for i in 0 1 2 3 4; do
    echo ""
    echo "  帖子 $((i+1))/5..."
    postiz posts:create \
        -c "${CAPTIONS[$i]}" \
        -m "${IMAGES[$i]}" \
        -i "cmlomzyp90166qf0y1qvcpzyh" \
        -s "2026-02-17T$((16+i)):00:00Z" \
        -t "schedule" \
        --settings '{"privacy_level":"PUBLIC_TO_EVERYONE","content_posting_method":"UPLOAD","duet":false,"stitch":false,"comment":true,"autoAddMusic":"no"}' 2>&1 | grep -E "(Post created|FAILED|Error)"
done

echo ""
echo "======================================"
echo "  完成!"
echo "======================================"