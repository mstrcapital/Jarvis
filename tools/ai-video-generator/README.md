# AI视频生成 - API接口完整方案

> **Date**: 2026-02-19
> **目标**: 批量自动化生成视频
> **状态**: 完整调研

---

## 🎯 可用API平台

### 1. Replicate (推荐)

```
官网: https://replicate.com
特点: 聚合多个视频生成模型，按需付费
```

**热门视频生成API**:

| 模型 | 公司 | 价格/次 | 质量 | 说明 |
|------|------|---------|------|------|
| **runwayml/gen-4.5** | Runway | $0.04-0.2 | 顶级 | 最新模型 |
| **runwayml/gen-4** | Runway | $0.02-0.1 | 高 | 稳定版 |
| **kwaivgi/kling-v3** | 快手 | $0.01-0.05 | 高 | 60秒长视频 |
| **kwaivgi/kling-o1** | 快手 | $0.01-0.03 | 中 | 快速版 |
| **xai/grok-imagine-video** | xAI | $0.01 | 中 | 新模型 |
| **pixverse/pixverse-v5.6** | Pixverse | $0.005 | 中 | 便宜 |
| **stable-video-diffusion** | Stability AI | $0.01 | 中 | 开源 |

### 2. Replicate 使用示例

```python
import replicate

# Runway Gen-4.5
output = replicate.run(
    "runwayml/gen-4.5",
    input={
        "prompt": "A stunning gold necklace sparkling under soft light, 4k, cinematic",
        "negative_prompt": "blurry, low quality, watermark",
        "num_frames": 24,
        "fps": 24,
        "width": 1024,
        "height": 576,
        "guidance_scale": 7.5,
        "num_inference_steps": 30
    }
)
print(output)  # 返回视频URL
```

### 3. Replicate 安装

```bash
pip install replicate
export REPLICATE_API_TOKEN=your_token
```

---

## 🇨🇳 国内平台API

### 1. 阿里云通义万相

```
官网: https://tongyi.aliyun.com/wanxiang
特点: 国内可用，价格便宜
```

### 2. 百度文心一言

```
官网: https://wenxin.baidu.com
特点: 国内稳定，需要申请
```

### 3. 字节Seedream

```
官网: https://www.seedream.cn
特点: 新发布，图像为主，视频待开放
```

---

## 💰 成本对比

### Replicate API 价格 (参考)

| 模型 | 时长 | 价格/次 | 100次 | 1000次 |
|------|------|---------|-------|--------|
| Gen-4.5 | 4秒 | $0.04 | $4 | $40 |
| Gen-4 | 4秒 | $0.02 | $2 | $20 |
| Kling v3 | 5秒 | $0.015 | $1.5 | $15 |
| Pixverse | 4秒 | $0.005 | $0.5 | $5 |
| SVD | 2秒 | $0.01 | $1 | $10 |

### 月成本估算

```
每天100条:
├── 低配 (Pixverse): ¥3.5/天 × 30 = ¥105/月
├── 中配 (Kling):    ¥10/天 × 30 = ¥300/月
└── 高配 (Gen-4.5):  ¥28/天 × 30 = ¥840/月

每天500条:
├── 低配: ¥525/月
├── 中配: ¥1,500/月
└── 高配: ¥4,200/月
```

---

## 🛠️ 自动化工作流

### 批量生成脚本

```python
#!/usr/bin/env python3
"""
AI视频批量生成器
使用Replicate API批量生成视频
"""

import replicate
import os
import json
from datetime import datetime

# 配置
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 提示词库
PROMPTS = {
    "gold_necklace": "A stunning gold necklace with pendant sparkling under soft light, luxurious jewelry showcase, 4k, slow motion, cinematic",
    "platinum_ring": "Close-up of platinum ring, silver-white metallic sheen, minimalist design, luxury aesthetic, 4k, studio lighting",
    "stacked_jewelry": "Layered gold and silver jewelry on a hand, stacked rings and necklaces, fashion magazine style, 4k, elegant",
    "abstract_background": "Flowing gradient background with soft purple and blue tones, gentle motion, 4k, abstract, smooth, ethereal",
    "luxury_box": "Luxury jewelry box opening reveal shot, premium packaging, velvet interior, elegant unboxing, 4k, cinematic"
}

def generate_video(prompt_key, output_dir="./output"):
    """生成单个视频"""
    prompt = PROMPTS[prompt_key]
    
    print(f"🎬 Generating: {prompt_key}")
    
    output = client.run(
        "runwayml/gen-4.5",
        input={
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, watermark, text, logo",
            "num_frames": 24,
            "fps": 24,
            "width": 1024,
            "height": 576,
            "guidance_scale": 7.5,
            "num_inference_steps": 25
        }
    )
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prompt_key}_{timestamp}.mp4"
    
    # 下载视频
    import urllib.request
    urllib.request.urlretrieve(output[0], f"{output_dir}/{filename}")
    
    print(f"✅ Saved: {filename}")
    return filename

def batch_generate(count_per_prompt=10):
    """批量生成"""
    os.makedirs("./output", exist_ok=True)
    
    results = []
    for prompt_key in PROMPTS.keys():
        for i in range(count_per_prompt):
            try:
                filename = generate_video(prompt_key)
                results.append({
                    "prompt": prompt_key,
                    "file": filename,
                    "time": datetime.now().isoformat()
                })
            except Exception as e:
                print(f"❌ Error: {e}")
    
    # 保存日志
    with open("generation_log.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Total generated: {len(results)} videos")

if __name__ == "__main__":
    batch_generate(5)  # 每个提示词生成5个
```

### 使用方法

```bash
# 1. 安装依赖
pip install replicate

# 2. 设置API Token
export REPLICATE_API_TOKEN=your_token_here

# 3. 运行
python video_generator.py
```

---

## 📊 完整方案对比

### 方案1: Replicate API

```
优点:
├── 质量最高 (Runway官方)
├── 模型选择多
├── 按需付费
└── 支持批量

缺点:
├── 需要海外支付方式
├── 网络可能不稳定
└── 全部英文文档

适合: 高质量需求, 预算充足
```

### 方案2: Runway官方API

```
官网: https://runwayml.com/enterprise
价格: 联系销售
特点:
├── 企业级支持
├── 私有部署选项
├── SLA保证
└── 团队协作

适合: 企业用户, 大批量需求
```

### 方案3: 国内平台

```
平台: 阿里云, 百度, 字节
优点:
├── 国内网络稳定
├── 人民币支付
├── 中文支持
└── 备案合规

缺点:
├── 模型质量略逊
├── 视频生成能力待完善
└── 价格不一定更便宜

适合: 合规要求高, 国内客户
```

---

## 🔧 集成到现有系统

### OpenClaw集成

```yaml
# openclaw配置
tools:
  video_generator:
    provider: replicate
    model: runwayml/gen-4.5
    params:
      prompt: "${input.prompt}"
      width: 1024
      height: 576
```

### Cron定时任务

```bash
# 每天早上8点生成100个视频
0 8 * * * cd /root/.openclaw/workspace && python video_generator.py --count 100
```

---

## 📁 文件结构

```
ai-video-generator/
├── video_generator.py      # 主脚本
├── prompts.json            # 提示词库
├── config.yaml             # 配置文件
├── requirements.txt        # 依赖
├── output/                 # 输出目录
└── README.md               # 说明文档
```

---

## 🚀 下一步

### 立即执行

- [ ] 注册Replicate账号: https://replicate.com
- [ ] 申请API Token
- [ ] 测试单个视频生成

### 本周内

- [ ] 部署批量生成脚本
- [ ] 建立提示词库
- [ ] 设置定时任务

### 本月内

- [ ] 集成到内容工作流
- [ ] 优化成本效率
- [ ] 建立素材库 (1000+)

---

*AI Video API Guide v1.0*
*Created: 2026-02-19*
*Source: Replicate, Runway, 国内平台*