# Pepe Quick Start Script
# Created: 2026-02-19

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       🐸🔥 Welcome to Pepe - Crypto Degen Agent!          ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Gateway status
echo "📡 Checking Gateway status..."
if ! openclaw gateway status 2>/dev/null | grep -q "running"; then
    echo "   🔄 Starting Gateway..."
    openclaw gateway start
    sleep 5
fi
echo "   ✅ Gateway running"
echo ""

# Create Pepe agent
echo "👑 Creating Pepe agent..."
openclaw agents add pepe \
  --workspace "/root/.openclaw/workspace/subagents/pepe" \
  --model "openrouter/minimax/minimax-m2.1"
echo "   ✅ Pepe agent created"
echo ""

# Verify
echo "📊 Verifying Pepe configuration..."
openclaw agents list | grep pepe
echo ""

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       ✅ Pepe is ready to degen!                             ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Usage:"
echo ""
echo "1️⃣  Via Telegram:"
echo "   @Jarvis /subagents spawn pepe"
echo "   or just say 'Hey Pepe' in the chat"
echo ""
echo "2️⃣  Via CLI:"
echo "   openclaw agents list"
echo "   openclaw agents delete pepe"
echo ""
echo "3️⃣  Personality:"
echo "   - Airdrop hunting expert 🐸"
echo "   - Pump.fun PVP trader 🔥"
echo "   - Meme lord 💰"
echo "   - Chaos ambassador 😂"
echo ""
echo "💾 Memory: /root/.openclaw/workspace/subagents/pepe/memory/"
echo "📖 Docs: /root/.openclaw/workspace/subagents/pepe/README.md"
echo ""
