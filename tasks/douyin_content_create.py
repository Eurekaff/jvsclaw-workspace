#!/usr/bin/env python3
"""
抖音内容创作脚本

功能：
1. 读取热点报告
2. 生成抖音脚本
3. 生成配图 (可选)
4. 制作视频 (需要 FFmpeg)
5. 准备发布

使用方式：
python3 tasks/douyin_content_create.py --topic "AI 工具推荐"
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.content_creator.agent import ContentCreatorAgent


def create_douyin_content(topic: str, selling_points: list = None):
    """创作抖音内容"""
    
    print("="*60)
    print("🎬 抖音内容创作")
    print("="*60)
    print(f"主题：{topic}")
    print(f"时间：{datetime.now().isoformat()}")
    
    # 默认卖点
    if not selling_points:
        selling_points = [
            "实用性强",
            "容易上手",
            "效率高"
        ]
    
    # 创建内容创作 Agent
    agent = ContentCreatorAgent("/home/admin/openclaw/workspace")
    
    # 执行创作
    result = agent.execute({
        "topic": topic,
        "target_audience": "想提升效率的年轻人",
        "selling_points": selling_points,
        "platforms": ["douyin"],
        "tone": "authentic"
    })
    
    # 获取抖音版本
    douyin_version = result["platform_versions"]["douyin"]
    content = douyin_version.get("content", {})
    script = content.get("script", "")
    text = content.get("text", "")
    
    # 保存脚本
    output_dir = Path("/home/admin/openclaw/workspace/artifacts/douyin_content")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存脚本文件
    script_file = output_dir / f"{timestamp}_douyin_script.md"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(f"# 抖音脚本：{topic}\n\n")
        f.write(f"**生成时间**: {datetime.now().isoformat()}\n\n")
        f.write(f"## 口播文案\n\n```\n{text}\n```\n\n")
        f.write(f"## 分镜脚本\n\n```\n{script}\n```\n")
    
    # 保存纯文本版本 (用于配音)
    text_file = output_dir / f"{timestamp}_douyin_text.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"\n✅ 内容创作完成")
    print(f"📝 脚本：{script_file}")
    print(f"📄 文案：{text_file}")
    
    # 展示内容
    print(f"\n{'='*60}")
    print("📱 抖音口播文案")
    print(f"{'='*60}")
    print(text)
    print(f"{'='*60}")
    
    return {
        "topic": topic,
        "script_file": str(script_file),
        "text_file": str(text_file),
        "text": text,
        "script": script
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='抖音内容创作')
    parser.add_argument('--topic', type=str, required=True, help='创作主题')
    parser.add_argument('--selling-points', nargs='+', help='卖点列表')
    
    args = parser.parse_args()
    
    create_douyin_content(args.topic, args.selling_points)
