#!/usr/bin/env python3
"""
MiniMax OpenAI API 集成工具 - 官方推荐方式

使用方法:
1. 设置环境变量
2. 运行工具

文档: https://platform.minimaxi.com/docs/api-reference/text-openai-api
"""

import os
import sys
import json
from datetime import datetime

# ============== 配置 ==============
# 官方推荐方式
OPENAI_BASE_URL = "https://api.minimaxi.com/v1"
API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# ============== 提示词库 ==============
TEXT_PROMPTS = {
    "crypto_alpha": "What's the best crypto airdrop hunting strategy in 2024?",
    "pump_fun": "Explain pump.fun trading strategy in simple terms",
    "meme_coins": "What makes a good meme coin? Give 3 examples",
    "hermes_birkin": "Describe the allure of Hermès Birkin bag",
    "luxury_jewelry": "Why do people love gold jewelry? Give 3 reasons",
    "lifestyle": "Write a short paragraph about luxury lifestyle"
}

# ============== OpenAI SDK集成 ==============
def create_client():
    """创建OpenAI客户端 (MiniMax兼容版)"""
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=API_KEY,
            base_url=OPENAI_BASE_URL
        )
        return client
    except ImportError:
        print("❌ 请安装openai: pip install openai")
        return None


def generate_text(prompt_key: str, model: str = "MiniMax-M2.5", reasoning: bool = False):
    """生成文本 (官方推荐方式)"""
    
    if prompt_key not in TEXT_PROMPTS:
        print(f"❌ 未知提示词: {prompt_key}")
        print(f"可用提示词: {list(TEXT_PROMPTS.keys())}")
        return None
    
    prompt = TEXT_PROMPTS[prompt_key]
    
    print(f"\n📝 生成文本: {prompt_key}")
    print(f"   模型: {model}")
    print(f"   内容: {prompt[:50]}...")
    
    client = create_client()
    if not client:
        return None
    
    try:
        # 构建参数
        kwargs = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        # 如果需要分离思考过程
        if reasoning:
            kwargs["extra_body"] = {"reasoning_split": True}
        
        # 调用API
        response = client.chat.completions.create(**kwargs)
        
        # 解析响应
        if reasoning and hasattr(response.choices[0].message, 'reasoning_details'):
            reasoning_content = response.choices[0].message.reasoning_details
            print(f"   🧠 思考: {str(reasoning_content)[:100]}...")
        
        content = response.choices[0].message.content
        print(f"   ✅ 成功: {content[:100]}...")
        
        return {
            "success": True,
            "content": content,
            "model": model,
            "prompt_key": prompt_key
        }
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def stream_response(prompt_key: str, model: str = "MiniMax-M2.5"):
    """流式输出响应"""
    
    if prompt_key not in TEXT_PROMPTS:
        print(f"❌ 未知提示词: {prompt_key}")
        return
    
    prompt = TEXT_PROMPTS[prompt_key]
    
    print(f"\n🌊 流式响应: {prompt_key}")
    print(f"   模型: {model}")
    
    client = create_client()
    if not client:
        return
    
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"reasoning_split": True},
            stream=True
        )
        
        print("\n🧠 思考过程:")
        print("-" * 60)
        
        reasoning_buffer = ""
        text_buffer = ""
        
        for chunk in stream:
            # 处理思考内容
            if (hasattr(chunk.choices[0].delta, 'reasoning_details') and 
                chunk.choices[0].delta.reasoning_details):
                for detail in chunk.choices[0].delta.reasoning_details:
                    if "text" in detail:
                        reasoning_text = detail["text"]
                        new_reasoning = reasoning_text[len(reasoning_buffer):]
                        if new_reasoning:
                            print(new_reasoning, end="", flush=True)
                            reasoning_buffer = reasoning_text
            
            # 处理实际内容
            if chunk.choices[0].delta.content:
                content_text = chunk.choices[0].delta.content
                new_text = content_text[len(text_buffer):] if text_buffer else content_text
                if new_text:
                    text_buffer += new_text
        
        print("\n" + "-" * 60)
        print("\n📝 最终回复:")
        print("-" * 60)
        print(text_buffer)
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ 错误: {e}")


def list_models():
    """列出支持的模型"""
    print("\n📦 支持的模型:")
    print("-" * 60)
    models = [
        ("MiniMax-M2.5", "204,800", "60tps", "顶尖性能与极致性价比"),
        ("MiniMax-M2.5-highspeed", "204,800", "100tps", "极速版，更快更敏捷"),
        ("MiniMax-M2.1", "204,800", "60tps", "强大多语言编程能力"),
        ("MiniMax-M2.1-highspeed", "204,800", "100tps", "极速版"),
        ("MiniMax-M2", "204,800", "-", "专为高效编码与Agent工作流"),
    ]
    
    for model, tokens, speed, desc in models:
        print(f"  ✅ {model:<25} {tokens:>10} tokens | {speed:>5} | {desc}")
    print()


def test_connection():
    """测试API连接"""
    print("\n🔍 测试API连接...")
    print(f"   URL: {OPENAI_BASE_URL}")
    print(f"   Key: {API_KEY[:20] if API_KEY else '❌ 未设置'}...")
    
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        return False
    
    client = create_client()
    if not client:
        return False
    
    try:
        response = client.chat.completions.create(
            model="MiniMax-M2.5",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        
        content = response.choices[0].message.content
        print(f"   ✅ API连接成功!")
        print(f"   回复: {content}")
        return True
        
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return False


def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              MiniMax OpenAI API 集成工具                       ║
║              官方推荐方式: https://platform.minimaxi.com         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  使用方法:                                                     ║
║                                                              ║
║    1. 设置环境变量:                                           ║
║       export MINIMAX_API_KEY="your_api_key"                   ║
║                                                              ║
║    2. 运行命令:                                               ║
║                                                              ║
║  命令:                                                        ║
║    python minimax_openai.py test       # 测试连接              ║
║    python minimax_openai.py list       # 列出模型              ║
║    python minimax_openai.py text <key>  # 生成文本              ║
║    python minimax_openai.py stream <key> # 流式输出             ║
║    python minimax_openai.py demo        # 完整演示             ║
║                                                              ║
║  可用提示词:                                                  ║
║    crypto_alpha, pump_fun, meme_coins, hermes_birkin         ║
║    luxury_jewelry, lifestyle                                  ║
║                                                              ║
║  示例:                                                        ║
║    python minimax_openai.py text crypto_alpha                 ║
║    python minimax_openai.py stream hermes_birkin               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def main():
    if not API_KEY:
        print("❌ 请设置环境变量: export MINIMAX_API_KEY=\"your_key\"")
        show_help()
        sys.exit(1)
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command in ["--help", "-h", "help"]:
        show_help()
    
    elif command == "test":
        test_connection()
    
    elif command == "list":
        list_models()
    
    elif command == "text":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "crypto_alpha"
        model = sys.argv[3] if len(sys.argv) > 3 else "MiniMax-M2.5"
        result = generate_text(prompt_key, model)
        if result:
            print("\n📊 结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "stream":
        prompt_key = sys.argv[2] if len(sys.argv) > 2 else "crypto_alpha"
        model = sys.argv[3] if len(sys.argv) > 3 else "MiniMax-M2.5"
        stream_response(prompt_key, model)
    
    elif command == "demo":
        print("\n" + "=" * 70)
        print("🎯 MiniMax OpenAI API 完整演示")
        print("=" * 70)
        
        # 测试连接
        test_connection()
        
        # 列出模型
        list_models()
        
        # 生成示例
        print("\n📝 文本生成示例:")
        generate_text("crypto_alpha")
        generate_text("hermes_birkin")
        
        print("\n" + "=" * 70)
        print("✅ 演示完成!")
        print("=" * 70)
    
    else:
        print(f"❌ 未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
