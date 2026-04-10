#!/usr/bin/env python3
"""
HTML 动画转视频

流程：
1. 用 Selenium 打开 HTML 页面
2. 每隔一定时间截图
3. 用 imageio 合成视频
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import imageio.v2 as imageio
from pathlib import Path
from datetime import datetime
import time


class HTMLVideoGenerator:
    """HTML 动画转视频"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / "artifacts" / "douyin_videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = self.output_dir / "temp_frames"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_driver(self):
        """设置浏览器"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1080,1920')
        
        driver = webdriver.Chrome(options=options)
        return driver
    
    def capture_frames(self, html_file: str, fps: int = 2, duration: int = 60):
        """捕获帧"""
        
        print("\n📸 开始捕获帧...")
        
        driver = self.setup_driver()
        
        try:
            # 打开 HTML
            html_path = Path(html_file).absolute()
            driver.get(f"file://{html_path}")
            print(f"  ✅ 已打开：{html_path}")
            
            # 捕获帧
            frames = []
            total_frames = fps * duration
            
            for i in range(total_frames):
                # 截图
                screenshot_path = self.temp_dir / f"frame_{i:04d}.png"
                driver.save_screenshot(str(screenshot_path))
                
                # 读取图像
                img = imageio.imread(screenshot_path)
                frames.append(img)
                
                # 进度
                if (i + 1) % 10 == 0:
                    print(f"  进度：{i+1}/{total_frames} 帧")
                
                # 等待下一帧
                time.sleep(1 / fps)
            
            print(f"  ✅ 捕获 {len(frames)} 帧")
            return frames
            
        finally:
            driver.quit()
    
    def create_video(self, frames: list, fps: int = 2):
        """创建视频"""
        
        print("\n🎬 生成视频...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"html_video_{timestamp}.mp4"
        
        # 使用 imageio 生成视频
        imageio.mimwrite(str(output_file), frames, fps=fps)
        
        size_mb = output_file.stat().st_size / 1024 / 1024
        
        print(f"\n{'='*60}")
        print("✅ 视频生成完成！")
        print(f"{'='*60}")
        print(f"📁 文件：{output_file}")
        print(f"⏱️  时长：{len(frames)/fps:.1f}秒")
        print(f"📊 大小：{size_mb:.2f} MB")
        
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir)
        
        return {
            "file": str(output_file),
            "duration": len(frames) / fps,
            "size_mb": size_mb
        }
    
    def generate(self, html_file: str):
        """完整流程"""
        
        print("="*60)
        print("🎬 HTML 动画转视频")
        print("="*60)
        
        # 捕获帧
        frames = self.capture_frames(html_file, fps=2, duration=60)
        
        # 创建视频
        result = self.create_video(frames, fps=2)
        
        return result


if __name__ == "__main__":
    generator = HTMLVideoGenerator("/home/admin/openclaw/workspace")
    html_file = "/home/admin/openclaw/workspace/tasks/video_animation.html"
    
    result = generator.generate(html_file)
    
    if result:
        print(f"\n🎉 成功：{result['file']}")
