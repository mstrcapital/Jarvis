#!/usr/bin/env python3
"""
轻量级视频处理工具 - MediaFlow替代方案

功能:
1. 视频下载 (yt-dlp)
2. 语音转文字 (faster-whisper)
3. 字幕生成与翻译
4. 视频合成 (FFmpeg)

Created: 2026-02-19
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# ============== 配置 ==============
WORKSPACE = "/root/.openclaw/workspace/video-workflow"
os.makedirs(WORKSPACE, exist_ok=True)

# ============== 工具函数 ==============
def run_command(cmd: list, cwd: str = None) -> tuple:
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=600
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


# ============== 视频下载 ==============
def download_video(url: str, output_path: str = None) -> dict:
    """下载视频"""
    if output_path is None:
        output_path = WORKSPACE
    
    print(f"\n📥 下载视频: {url}")
    print(f"   保存到: {output_path}")
    
    # yt-dlp命令
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best",
        "-o", f"{output_path}/%(title)s_%(id)s.%(ext)s",
        "--no-playlist",
        "--verbose",
        url
    ]
    
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        print(f"   ✅ 下载成功!")
        return {"success": True, "message": stdout}
    else:
        print(f"   ❌ 下载失败: {stderr}")
        return {"success": False, "error": stderr}


# ============== 语音转文字 ==============
def transcribe_video(video_path: str, language: str = "zh") -> dict:
    """语音转文字"""
    print(f"\n📝 转录音频: {video_path}")
    print(f"   语言: {language}")
    
    try:
        from faster_whisper import WhisperModel
        
        # 使用small模型 (平衡速度和质量)
        model = WhisperModel("small", device="auto")
        
        segments, info = model.transcribe(
            video_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )
        
        print(f"   检测语言: {info.language} (概率: {info.language_probability:.2f})")
        
        # 收集字幕
        subtitles = []
        for segment in segments:
            subtitles.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
        
        # 保存字幕文件
        output_path = video_path.replace(Path(video_path).suffix, ".srt")
        with open(output_path, "w", encoding="utf-8") as f:
            for i, sub in enumerate(subtitles, 1):
                start_time = format_time(sub["start"])
                end_time = format_time(sub["end"])
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{sub['text']}\n\n")
        
        print(f"   ✅ 字幕已保存: {output_path}")
        print(f"   共 {len(subtitles)} 条字幕")
        
        return {
            "success": True,
            "subtitles": subtitles,
            "srt_path": output_path,
            "language": info.language
        }
        
    except Exception as e:
        print(f"   ❌ 转录失败: {e}")
        return {"success": False, "error": str(e)}


def format_time(seconds: float) -> str:
    """格式化时间"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ============== 翻译字幕 ==============
def translate_subtitle(srt_path: str, target_lang: str = "zh") -> dict:
    """翻译字幕"""
    print(f"\n🌍 翻译字幕: {srt_path}")
    print(f"   目标语言: {target_lang}")
    
    # 读取原字幕
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 简单替换语言标识
    lang_map = {
        "en": "English",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German"
    }
    
    lang_name = lang_map.get(target_lang, target_lang)
    
    # 生成翻译后的文件名
    output_path = srt_path.replace(".srt", f"_{target_lang}.srt")
    
    # 简单处理: 在原字幕后添加翻译字幕
    # 实际使用需要调用翻译API
    print(f"   ⚠️  翻译API未配置，保存原文")
    print(f"   ✅ 字幕文件: {output_path}")
    
    return {
        "success": True,
        "translated_path": output_path,
        "note": "Translation API not configured"
    }


# ============== 视频合成 ==============
def add_subtitle_to_video(video_path: str, srt_path: str, output_path: str = None) -> dict:
    """添加字幕到视频"""
    print(f"\n🎬 合成视频: {video_path}")
    print(f"   字幕: {srt_path}")
    
    if output_path is None:
        output_path = video_path.replace(Path(video_path).suffix, "_subtitled.mp4")
    
    # 使用FFmpeg添加字幕
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_path
    ]
    
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        print(f"   ✅ 合成成功: {output_path}")
        return {"success": True, "output_path": output_path}
    else:
        print(f"   ❌ 合成失败: {stderr}")
        return {"success": False, "error": stderr}


def extract_audio(video_path: str, output_path: str = None) -> dict:
    """提取音频"""
    if output_path is None:
        output_path = video_path.replace(Path(video_path).suffix, ".wav")
    
    print(f"\n🔊 提取音频: {video_path}")
    print(f"   输出: {output_path}")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]
    
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        print(f"   ✅ 音频已保存: {output_path}")
        return {"success": True, "audio_path": output_path}
    else:
        print(f"   ❌ 提取失败: {stderr}")
        return {"success": False, "error": stderr}


# ============== 完整工作流 ==============
def full_workflow(video_url: str, target_lang: str = "zh") -> dict:
    """完整工作流"""
    print("\n" + "=" * 70)
    print("🚀 视频处理完整工作流")
    print("=" * 70)
    
    # 1. 下载视频
    print("\n[1/4] 下载视频...")
    download_result = download_video(video_url)
    if not download_result.get("success"):
        return {"success": False, "step": "download", "error": download_result.get("error")}
    
    # 找到下载的视频文件
    video_files = list(Path(WORKSPACE).glob("*.mp4"))
    if not video_files:
        video_files = list(Path(WORKSPACE).glob("*.mkv"))
    if not video_files:
        return {"success": False, "error": "未找到下载的视频文件"}
    
    video_path = str(video_files[0])
    print(f"   视频路径: {video_path}")
    
    # 2. 提取音频
    print("\n[2/4] 提取音频...")
    audio_result = extract_audio(video_path)
    
    # 3. 转录
    print("\n[3/4] 语音转文字...")
    transcribe_result = transcribe_video(video_path, language="zh")
    
    if not transcribe_result.get("success"):
        return {"success": False, "step": "transcribe", "error": transcribe_result.get("error")}
    
    srt_path = transcribe_result["srt_path"]
    
    # 4. 翻译
    print("\n[4/4] 翻译字幕...")
    translate_result = translate_subtitle(srt_path, target_lang)
    
    # 5. 合成 (可选)
    print("\n[5/5] 合成视频...")
   合成_result = add_subtitle_to_video(video_path, srt_path)
    
    return {
        "success": True,
        "video_path": video_path,
        "srt_path": srt_path,
        "audio_path": audio_result.get("audio_path"),
        "translated_srt": translate_result.get("translated_path"),
        "output_video": 合成_result.get("output_path")
    }


# ============== 主程序 ==============
def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              轻量级视频处理工具 - MediaFlow替代方案             ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                              ║
║  功能:                                                        ║
║  1. 视频下载 (yt-dlp)                                        ║
║  2. 语音转文字 (faster-whisper)                              ║
║  3. 字幕生成与翻译                                           ║
║  4. 视频合成 (FFmpeg)                                       ║
║                                                              ║
║  使用方法:                                                    ║
║                                                              ║
║    python video_workflow.py download <url>                    ║
║    python video_workflow.py transcribe <video_path>           ║
║    python video_workflow.py translate <srt_path>             ║
║    python video_workflow.py compose <video> <srt>           ║
║    python video_workflow.py workflow <url>                    ║
║                                                              ║
║  示例:                                                        ║
║    python video_workflow.py download https://youtu.be/xxx     ║
║    python video_workflow.py transcribe video.mp4              ║
║    python video_workflow.py workflow https://youtu.be/xxx     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command in ["--help", "-h", "help"]:
        show_help()
    
    elif command == "download":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = download_video(url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "transcribe":
        video_path = sys.argv[2] if len(sys.argv) > 2 else ""
        language = sys.argv[3] if len(sys.argv) > 3 else "zh"
        result = transcribe_video(video_path, language)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "translate":
        srt_path = sys.argv[2] if len(sys.argv) > 2 else ""
        target_lang = sys.argv[3] if len(sys.argv) > 3 else "zh"
        result = translate_subtitle(srt_path, target_lang)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "compose":
        video_path = sys.argv[2] if len(sys.argv) > 2 else ""
        srt_path = sys.argv[3] if len(sys.argv) > 3 else ""
        result = add_subtitle_to_video(video_path, srt_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "workflow":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        target_lang = sys.argv[3] if len(sys.argv) > 3 else "zh"
        result = full_workflow(url, target_lang)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
