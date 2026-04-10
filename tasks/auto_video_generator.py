#!/usr/bin/env python3
"""
全自动抖音视频生成 - 使用 MoviePy 2.x

完全自动化，无需手动操作
"""

from moviepy import ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
from datetime import datetime


class AutoVideoGenerator:
    """全自动视频生成"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_text_clip(self, text, size=(1080, 1920), fontsize=80, 
                        duration=5, color='white', bg_color=(26, 26, 46)):
        """创建文字片段"""
        
        # 创建图像
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # 尝试加载字体
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except:
            font = ImageFont.load_default()
        
        # 计算文字位置（居中）
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=color)
        
        # 转换为 numpy 数组
        frame = np.array(img)
        
        # 创建片段
        clip = ImageClip(frame).with_duration(duration)
        
        return clip
    
    def create_full_video(self):
        """创建完整视频"""
        
        print("="*60)
        print("🎬 全自动生成抖音视频")
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
            clip = self.create_text_clip(text, duration=duration)
            clips.append(clip)
        
        # 合并所有场景
        print("\n✂️  合并场景...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # 添加背景音乐（如果有）
        bgm_file = self.workspace_root / "assets" / "bgm" / "popular_bgm.mp3"
        if bgm_file.exists():
            print("\n🎵 添加 BGM...")
            try:
                bgm = AudioFileClip(str(bgm_file))
                # 循环 BGM 直到视频结束
                bgm = bgm.with_duration(final_video.duration)
                # 调整音量
                bgm = bgm.with_volume_scaled(0.3)
                # 设置音频
                final_video = final_video.with_audio(bgm)
                print("  ✅ BGM 已添加")
            except Exception as e:
                print(f"  ⚠️  BGM 添加失败：{e}")
        else:
            print("\n⚠️  无 BGM，跳过")
        
        # 保存视频
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"auto_video_{timestamp}.mp4"
        
        print(f"\n💾 导出视频：{output_file}")
        print(f"   时长：{final_video.duration:.1f}秒")
        print(f"   分辨率：1080x1920")
        
        # 写入文件
        final_video.write_videofile(
            str(output_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            logger=None
        )
        
        # 显示结果
        size_mb = output_file.stat().st_size / 1024 / 1024
        
        print(f"\n{'='*60}")
        print("✅ 视频生成完成！")
        print(f"{'='*60}")
        print(f"📁 文件：{output_file}")
        print(f"⏱️  时长：{final_video.duration:.1f}秒")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"📐 分辨率：1080x1920（抖音竖屏）")
        
        return {
            "file": str(output_file),
            "duration": final_video.duration,
            "size_mb": size_mb,
            "resolution": "1080x1920",
            "created_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    generator = AutoVideoGenerator("/home/admin/openclaw/workspace")
    result = generator.create_full_video()
    
    if result:
        print(f"\n🎉 成功生成视频：{result['file']}")
        print(f"\n下一步:")
        print(f"1. 查看视频：ls -lh {result['file']}")
        print(f"2. 发布到抖音：手动上传视频文件")
