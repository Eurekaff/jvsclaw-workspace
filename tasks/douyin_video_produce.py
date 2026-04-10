#!/usr/bin/env python3
"""
抖音视频自动制作

流程:
1. 读取脚本
2. 准备素材 (图片/视频片段)
3. 添加 BGM
4. 添加字幕
5. 导出视频

依赖:
- FFmpeg (必须安装)
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime


class DouyinVideoProducer:
    """抖音视频制作"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.assets_dir = self.workspace_root / "assets"
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        
        # 确保目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "bgm").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "fonts").mkdir(parents=True, exist_ok=True)
        (self.assets_dir / "templates").mkdir(parents=True, exist_ok=True)
    
    def check_ffmpeg(self):
        """检查 FFmpeg 是否安装"""
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
    
    def prepare_assets(self):
        """准备素材"""
        print("\n📦 准备素材...")
        
        # 检查必要素材
        required = {
            "bgm": self.assets_dir / "bgm" / "popular_bgm.mp3",
            "font": self.assets_dir / "fonts" / "simhei.ttf"
        }
        
        missing = []
        for name, path in required.items():
            if not path.exists():
                missing.append(name)
                print(f"  ⚠️  缺少：{path}")
        
        if missing:
            print(f"\n⚠️  需要准备的素材:")
            print(f"  1. BGM: {required['bgm']}")
            print(f"     下载无版权音乐放在这里")
            print(f"  2. 字体：{required['font']}")
            print(f"     下载思源黑体或类似字体")
            return False
        
        print(f"  ✅ 素材已准备")
        return True
    
    def create_video_from_script(self, script_file: str, output_name: str = None):
        """从脚本创建视频"""
        
        print(f"\n🎬 开始制作视频...")
        print(f"   脚本：{script_file}")
        
        # 检查 FFmpeg
        if not self.check_ffmpeg():
            print(f"  ❌ FFmpeg 未安装")
            print(f"  安装方法:")
            print(f"    sudo apt-get install ffmpeg  # Linux")
            print(f"    brew install ffmpeg  # macOS")
            return None
        
        # 准备素材
        if not self.prepare_assets():
            print(f"\n⚠️  使用简化模式 (无 BGM 和字幕)")
        
        # 读取脚本
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 生成视频 (简化版本)
        # 实际应该解析脚本，准备对应素材
        # 这里演示基本流程
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = output_name or f"douyin_video_{timestamp}"
        output_file = self.output_dir / f"{output_name}.mp4"
        
        # 创建测试视频 (黑屏 + 文字)
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:d=10",  # 黑屏 10 秒
            "-vf", "drawtext=text='抖音测试视频':fontsize=50:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264",
            "-t", "10",
            "-pix_fmt", "yuv420p",
            str(output_file)
        ]
        
        print(f"  执行 FFmpeg...")
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            print(f"  ✅ 视频已生成：{output_file}")
            print(f"  📊 大小：{output_file.stat().st_size / 1024 / 1024:.2f} MB")
            return str(output_file)
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 失败：{e}")
            return None
        except Exception as e:
            print(f"  ❌ 异常：{e}")
            return None
    
    def add_bgm(self, video_file: str, bgm_file: str):
        """添加背景音乐"""
        print(f"\n🎵 添加 BGM...")
        
        output_file = Path(video_file).with_name(
            Path(video_file).stem + "_with_bgm.mp4"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-i", bgm_file,
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
    
    def add_subtitles(self, video_file: str, subtitle_text: str):
        """添加字幕"""
        print(f"\n📝 添加字幕...")
        
        # 创建字幕文件
        srt_file = Path(video_file).with_name("temp.srt")
        with open(srt_file, 'w', encoding='utf-8') as f:
            f.write(f"1\n00:00:00,000 --> 00:00:10,000\n{subtitle_text}\n")
        
        output_file = Path(video_file).with_name(
            Path(video_file).stem + "_with_subs.mp4"
        )
        
        font_file = self.assets_dir / "fonts" / "simhei.ttf"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-vf", f"subtitles={srt_file}:fontsdir={font_file.parent}",
            "-c:a", "copy",
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            print(f"  ✅ 字幕已添加：{output_file}")
            srt_file.unlink()  # 删除临时文件
            return str(output_file)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            if srt_file.exists():
                srt_file.unlink()
            return video_file


if __name__ == "__main__":
    producer = DouyinVideoProducer("/home/admin/openclaw/workspace")
    
    # 检查 FFmpeg
    if not producer.check_ffmpeg():
        print("❌ FFmpeg 未安装")
        print("\n安装方法:")
        print("  Linux: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: 下载 https://ffmpeg.org/download.html")
    else:
        print("✅ FFmpeg 已安装")
        
        # 创建测试视频
        result = producer.create_video_from_script(
            "/home/admin/openclaw/workspace/artifacts/douyin_content/20260410_105529_douyin_script.md"
        )
        
        if result:
            print(f"\n✅ 视频制作完成：{result}")
