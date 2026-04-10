#!/usr/bin/env python3
"""
制作 AI 工具推荐示例视频

流程:
1. 准备素材（背景、BGM、字体）
2. 生成文字层
3. 合成视频
4. 添加配音和 BGM
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime


class AIVideoProducer:
    """AI 视频制作"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.assets_dir = self.workspace_root / "assets"
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        
        # 确保目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "backgrounds").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "bgm").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "fonts").mkdir(parents=True, exist_ok=True)
    
    def check_ffmpeg(self):
        """检查 FFmpeg"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def create_background(self, duration: int = 60):
        """创建科技背景"""
        print("\n🎨 创建科技背景...")
        
        output_file = self.assets_dir / "backgrounds" / "tech_bg.mp4"
        
        # 创建深色渐变背景
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c=#1a1a2e:s=1080x1920:d={duration}",
            "-vf", "gblur=sigma=20",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            print(f"  ✅ 背景已创建：{output_file}")
            return str(output_file)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            return None
    
    def add_text_scenes(self, video_file: str):
        """添加文字场景"""
        print("\n📝 添加文字场景...")
        
        output_file = Path(video_file).with_name("with_text.mp4")
        
        # 定义场景文字
        scenes = [
            {"text": "⚠️别再手动工作了！", "time": 3, "y": "h/2"},
            {"text": "每天加班到深夜？", "time": 7, "y": "h/2"},
            {"text": "工具 1：自动写文档", "time": 15, "y": "h/3"},
            {"text": "3 秒生成！", "time": 20, "y": "h/2"},
            {"text": "工具 2：自动做 PPT", "time": 25, "y": "h/3"},
            {"text": "效率翻倍！", "time": 30, "y": "h/2"},
            {"text": "之前 3 小时", "time": 40, "y": "h/3"},
            {"text": "现在 3 分钟", "time": 45, "y": "h/2"},
            {"text": "评论区领工具👇", "time": 50, "y": "h/2"},
        ]
        
        # 创建 FFmpeg 滤镜
        filter_complex = []
        for i, scene in enumerate(scenes):
            filter_complex.append(
                f"drawtext=text='{scene['text']}':fontsize=50:fontcolor=white:x=(w-text_w)/2:y={scene['y']}:enable='between(t,{sum(s['time'] for s in scenes[:i])},{sum(s['time'] for s in scenes[:i+1])})'"
            )
        
        filter_str = ",".join(filter_complex)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-vf", filter_str,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            print(f"  ✅ 文字已添加：{output_file}")
            return str(output_file)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            return video_file
    
    def add_bgm(self, video_file: str, bgm_file: str = None):
        """添加背景音乐"""
        print("\n🎵 添加 BGM...")
        
        # 使用默认 BGM 或提供的
        if bgm_file is None:
            bgm_file = self.assets_dir / "bgm" / "popular_bgm.mp3"
            if not bgm_file.exists():
                print(f"  ⚠️  BGM 文件不存在，跳过")
                return video_file
        
        output_file = Path(video_file).with_name("with_bgm.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-i", str(bgm_file),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            print(f"  ✅ BGM 已添加：{output_file}")
            return str(output_file)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            return video_file
    
    def create_example_video(self, topic: str = "AI 工具推荐"):
        """创建示例视频"""
        
        print("="*60)
        print("🎬 制作 AI 工具推荐示例视频")
        print("="*60)
        
        # 检查 FFmpeg
        if not self.check_ffmpeg():
            print("❌ FFmpeg 未安装")
            return None
        
        # 1. 创建背景
        background = self.create_background(duration=60)
        if not background:
            return None
        
        # 2. 添加文字场景
        with_text = self.add_text_scenes(background)
        
        # 3. 添加 BGM
        final_video = self.add_bgm(with_text)
        
        # 4. 生成信息
        video_info = {
            "topic": topic,
            "file": final_video,
            "duration": 60,
            "resolution": "1080x1920",
            "size_mb": final_video.stat().st_size / 1024 / 1024 if final_video and Path(final_video).exists() else 0,
            "created_at": datetime.now().isoformat()
        }
        
        # 5. 保存信息
        info_file = self.output_dir / "example_video_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(video_info, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print("✅ 示例视频制作完成")
        print(f"{'='*60}")
        print(f"📁 文件：{final_video}")
        print(f"⏱️  时长：{video_info['duration']}秒")
        print(f"📊 大小：{video_info['size_mb']:.2f} MB")
        print(f"📐 分辨率：{video_info['resolution']}")
        
        return video_info


if __name__ == "__main__":
    producer = AIVideoProducer("/home/admin/openclaw/workspace")
    
    if not producer.check_ffmpeg():
        print("❌ FFmpeg 未安装")
        print("\n安装方法:")
        print("  Linux: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
    else:
        print("✅ FFmpeg 已安装")
        
        # 创建示例视频
        info = producer.create_example_video("AI 工具推荐")
        
        if info:
            print(f"\n🎉 视频已生成：{info['file']}")
