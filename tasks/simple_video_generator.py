#!/usr/bin/env python3
"""
全自动抖音视频生成 - 简化版

使用 ColorClip + TextClip，更快更稳定
"""

from moviepy import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from pathlib import Path
from datetime import datetime


class SimpleVideoGenerator:
    """简化版视频生成"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_scene(self, text, duration=5, fontsize=80):
        """创建场景"""
        
        # 背景
        bg = ColorClip(size=(1080, 1920), color=(26, 26, 46)).with_duration(duration)
        
        # 文字
        try:
            txt = TextClip(
                text=text,
                font="DejaVu-Sans-Bold",
                fontsize=fontsize,
                color='white',
                size=(1080, None),
                method='caption',
                align='center'
            ).with_duration(duration).with_position('center')
        except:
            # 字体加载失败，用默认
            txt = ColorClip(size=(1080, 1920), color=(26, 26, 46)).with_duration(duration)
        
        # 合成
        clip = CompositeVideoClip([bg, txt])
        return clip
    
    def create_full_video(self):
        """创建完整视频"""
        
        print("="*60)
        print("🎬 全自动生成抖音视频（简化版）")
        print("="*60)
        
        # 定义场景
        scenes = [
            ("⚠️别再手动工作了！", 3),
            ("每天加班到深夜？", 7),
            ("工具 1：自动写文档", 10),
            ("3 秒生成！", 5),
            ("工具 2：自动做 PPT", 10),
            ("效率翻倍！", 5),
            ("之前 3 小时", 5),
            ("现在 3 分钟", 5),
            ("评论区领工具👇", 10),
        ]
        
        print("\n📝 生成场景...")
        clips = []
        
        for text, duration in scenes:
            print(f"  生成：{text} ({duration}秒)")
            clip = self.create_scene(text, duration=duration)
            clips.append(clip)
        
        # 合并
        print("\n✂️  合并场景...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"simple_video_{timestamp}.mp4"
        
        print(f"\n💾 导出视频：{output_file}")
        
        try:
            final_video.write_videofile(
                str(output_file),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                logger=None
            )
            
            size_mb = output_file.stat().st_size / 1024 / 1024
            
            print(f"\n{'='*60}")
            print("✅ 视频生成完成！")
            print(f"{'='*60}")
            print(f"📁 文件：{output_file}")
            print(f"⏱️  时长：{final_video.duration:.1f}秒")
            print(f"📊 大小：{size_mb:.2f} MB")
            
            return {
                "file": str(output_file),
                "duration": final_video.duration,
                "size_mb": size_mb
            }
            
        except Exception as e:
            print(f"\n❌ 导出失败：{e}")
            return None


if __name__ == "__main__":
    generator = SimpleVideoGenerator("/home/admin/openclaw/workspace")
    result = generator.create_full_video()
    
    if result:
        print(f"\n🎉 成功：{result['file']}")
