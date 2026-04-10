#!/usr/bin/env python3
"""
AI 工具推荐视频生成 - 含实际工具信息

使用 PPT 方案，生成有实际内容的视频
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
from pathlib import Path
from datetime import datetime
import numpy as np


class AIToolsVideoGenerator:
    """AI 工具推荐视频生成"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_text_frame(self, text, subtext="", size=(1080, 1920), fontsize=70):
        """创建文字帧"""
        
        # 创建图像
        img = Image.new('RGB', size, color=(26, 26, 46))
        draw = ImageDraw.Draw(img)
        
        # 加载中文字体
        try:
            font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", fontsize)
            small_font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 40)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/arphic/ukai.ttc", fontsize)
                small_font = ImageFont.truetype("/usr/share/fonts/arphic/ukai.ttc", 40)
            except:
                font = ImageFont.load_default()
                small_font = font
        
        # 绘制主文字
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] // 2) - text_height - 20
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        # 绘制副标题
        if subtext:
            bbox = draw.textbbox((0, 0), subtext, font=small_font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            draw.text((x, y + text_height + 20), subtext, font=small_font, fill=(200, 200, 200))
        
        return np.array(img)
    
    def create_scene(self, text, subtext="", duration=5):
        """创建场景"""
        
        frame = self.create_text_frame(text, subtext)
        frames = [frame] * (duration * 2)  # 2fps
        
        return frames
    
    def create_full_video(self):
        """创建完整视频"""
        
        print("="*60)
        print("🎬 生成 AI 工具推荐视频（含实际工具）")
        print("="*60)
        
        # 定义场景（含实际工具信息）
        scenes = [
            ("⚠️ 别再加班了！", "是不是经常加班到深夜？", 3),
            ("这 5 个 AI 工具", "让你准时下班！", 5),
            ("工具 1：Notion AI", "自动写文档/做总结/效率提升 10 倍", 8),
            ("工具 2：Gamma", "3 分钟生成 PPT/支持中文", 8),
            ("工具 3：Tome", "AI 生成演示文稿/设计师都失业了", 8),
            ("工具 4：剪映", "自动字幕/智能剪辑/视频制作简单", 8),
            ("工具 5：通义千问", "国产 AI 助手/写代码写文章", 8),
            ("从每天加班 3 小时", "到准时下班", 5),
            ("评论区扣'AI'领取👇", "想要工具链接？", 7),
        ]
        
        print("\n📝 生成场景...")
        all_frames = []
        
        for text, subtext, duration in scenes:
            print(f"  生成：{text} ({duration}秒)")
            frames = self.create_scene(text, subtext, duration)
            all_frames.extend(frames)
        
        # 生成视频
        print(f"\n🎬 生成视频...")
        print(f"  总帧数：{len(all_frames)}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"ai_tools_video_{timestamp}.mp4"
        
        imageio.mimwrite(str(output_file), all_frames, fps=2)
        
        size_mb = output_file.stat().st_size / 1024 / 1024
        
        print(f"\n{'='*60}")
        print("✅ 视频生成完成！")
        print(f"{'='*60}")
        print(f"📁 文件：{output_file}")
        print(f"⏱️  时长：{len(all_frames)/2:.1f}秒")
        print(f"📊 大小：{size_mb:.2f} MB")
        print(f"📐 分辨率：1080x1920（抖音竖屏）")
        
        return {
            "file": str(output_file),
            "duration": len(all_frames) / 2,
            "size_mb": size_mb,
            "tools_count": 5,
            "created_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    generator = AIToolsVideoGenerator("/home/admin/openclaw/workspace")
    result = generator.create_full_video()
    
    if result:
        print(f"\n🎉 成功：{result['file']}")
        print(f"\n视频包含 5 个实际 AI 工具:")
        print("1. Notion AI - 自动写文档")
        print("2. Gamma - 3 分钟 PPT")
        print("3. Tome - AI 演示文稿")
        print("4. 剪映 - 智能剪辑")
        print("5. 通义千问 - 国产 AI 助手")
