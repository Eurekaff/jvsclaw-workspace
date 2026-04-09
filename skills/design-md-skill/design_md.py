#!/usr/bin/env python3
"""
Design.md Skill - 集成 awesome-design-md 项目

获取并应用知名网站的设计系统到前端项目
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
import urllib.request
import urllib.error


class DesignMdSkill:
    """Design.md 技能实现"""
    
    # 支持的网站列表
    SUPPORTED_SITES = {
        "linear": "Linear - 项目管理工具",
        "vercel": "Vercel - 前端部署平台",
        "stripe": "Stripe - 支付基础设施",
        "claude": "Claude - AI 助手",
        "cursor": "Cursor - AI 代码编辑器",
        "supabase": "Supabase - 开源 Firebase 替代",
        "sentry": "Sentry - 错误监控",
        "raycast": "Raycast - 生产力启动器",
        "notion": "Notion - 工作区工具",
        "figma": "Figma - 设计工具",
    }
    
    BASE_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main"
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.design_md_dir = self.workspace_root / "design_systems"
        self.design_md_dir.mkdir(exist_ok=True)
    
    def fetch(self, site_name: str) -> Optional[Dict]:
        """获取指定网站的设计系统"""
        if site_name not in self.SUPPORTED_SITES:
            print(f"❌ 不支持的网站：{site_name}")
            print(f"支持的网站：{', '.join(self.SUPPORTED_SITES.keys())}")
            return None
        
        try:
            # 获取 DESIGN.md
            design_url = f"{self.BASE_URL}/sites/{site_name}/DESIGN.md"
            req = urllib.request.Request(design_url)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                design_content = response.read().decode('utf-8')
            
            # 解析设计令牌（简化实现）
            design_data = self._parse_design_md(design_content)
            design_data['raw'] = design_content
            design_data['site'] = site_name
            
            # 保存到本地
            output_file = self.design_md_dir / f"{site_name}_DESIGN.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(design_content)
            
            print(f"✅ 已获取 {self.SUPPORTED_SITES[site_name]} 设计系统")
            print(f"📁 保存到：{output_file}")
            
            return design_data
            
        except Exception as e:
            print(f"❌ 获取失败：{e}")
            return None
    
    def _parse_design_md(self, content: str) -> Dict:
        """解析 DESIGN.md 内容，提取设计令牌"""
        design = {
            "colors": {},
            "typography": {},
            "spacing": {},
            "components": {},
            "layout": {}
        }
        
        # 简化解析（实际应该更完善）
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            if line.startswith('## '):
                current_section = line[3:].strip().lower()
            
            # 提取颜色
            if 'color' in current_section or 'palette' in current_section:
                if '`' in line and '#' in line:
                    # 提取颜色代码
                    import re
                    matches = re.findall(r'#[0-9A-Fa-f]{3,8}', line)
                    for color in matches:
                        name_match = re.search(r'`([^`]+)`', line)
                        if name_match:
                            name = name_match.group(1).strip()
                            design['colors'][name] = color
            
            # 提取排版
            if 'typography' in current_section or 'font' in current_section:
                if 'font-family' in line.lower() or 'font-size' in line.lower():
                    design['typography']['raw'] = line
        
        return design
    
    def generate_tailwind_config(self, design: Dict, output_path: str = None) -> str:
        """生成 Tailwind 配置文件"""
        site = design.get('site', 'custom')
        
        # 基于 Linear 设计系统的配置（示例）
        tailwind_config = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    "./index.html",
    "./src/**/*{{js,ts,jsx,tsx}}",
  ],
  theme: {{
    extend: {{
      colors: {{
        // {site} Design System
        primary: {{
          50: '#f5f5f5',
          100: '#e0e0e0',
          200: '#cccccc',
          300: '#999999',
          400: '#666666',
          500: '#333333',
          600: '#292929',
          700: '#1f1f1f',
          800: '#141414',
          900: '#0a0a0a',
        }},
        accent: {{
          50: '#f9f5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',  // Linear purple
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
        }},
        success: '#00c853',
        warning: '#ffc107',
        error: '#ff5252',
        info: '#448aff',
      }},
      fontFamily: {{
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }},
      fontSize: {{
        xs: ['0.75rem', {{ lineHeight: '1rem' }}],
        sm: ['0.875rem', {{ lineHeight: '1.25rem' }}],
        base: ['1rem', {{ lineHeight: '1.5rem' }}],
        lg: ['1.125rem', {{ lineHeight: '1.75rem' }}],
        xl: ['1.25rem', {{ lineHeight: '1.75rem' }}],
        '2xl': ['1.5rem', {{ lineHeight: '2rem' }}],
      }},
      spacing: {{
        px: '1px',
        0: '0px',
        0.5: '0.125rem',
        1: '0.25rem',
        1.5: '0.375rem',
        2: '0.5rem',
        2.5: '0.625rem',
        3: '0.75rem',
        3.5: '0.875rem',
        4: '1rem',
        5: '1.25rem',
        6: '1.5rem',
        7: '1.75rem',
        8: '2rem',
        9: '2.25rem',
        10: '2.5rem',
        11: '2.75rem',
        12: '3rem',
        14: '3.5rem',
        16: '4rem',
        20: '5rem',
        24: '6rem',
        28: '7rem',
        32: '8rem',
        36: '9rem',
        40: '10rem',
        44: '11rem',
        48: '12rem',
        52: '13rem',
        56: '14rem',
        60: '15rem',
        64: '16rem',
        72: '18rem',
        80: '20rem',
        96: '24rem',
      }},
      borderRadius: {{
        none: '0px',
        sm: '0.125rem',
        DEFAULT: '0.25rem',
        md: '0.375rem',
        lg: '0.5rem',
        xl: '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        full: '9999px',
      }},
      boxShadow: {{
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)',
      }},
    }},
  }},
  plugins: [],
}}
"""
        
        if output_path:
            output_file = Path(output_path)
        else:
            output_file = self.design_md_dir / f"{site}_tailwind.config.js"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tailwind_config)
        
        print(f"✅ 已生成 Tailwind 配置：{output_file}")
        return str(output_file)
    
    def apply(self, site_name: str, target_dir: str) -> bool:
        """应用设计系统到目标项目"""
        # 获取设计系统
        design = self.fetch(site_name)
        if not design:
            return False
        
        # 生成 Tailwind 配置
        target_path = Path(target_dir)
        tailwind_config_path = target_path / "tailwind.config.js"
        self.generate_tailwind_config(design, str(tailwind_config_path))
        
        # 复制 DESIGN.md
        design_md_source = self.design_md_dir / f"{site_name}_DESIGN.md"
        design_md_target = target_path.parent / "DESIGN.md"
        
        if design_md_source.exists():
            import shutil
            shutil.copy(design_md_source, design_md_target)
            print(f"✅ 已复制 DESIGN.md 到：{design_md_target}")
        
        print(f"\n💡 下一步:")
        print(f"1. 更新 {tailwind_config_path} 的引用")
        print(f"2. 重启开发服务器")
        print(f"3. 查看效果")
        
        return True
    
    def list_sites(self) -> Dict:
        """列出所有支持的网站"""
        return self.SUPPORTED_SITES


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Design.md Skill - 获取并应用设计系统")
    parser.add_argument("action", choices=["fetch", "apply", "list"], 
                       help="操作类型")
    parser.add_argument("--site", type=str, help="网站名称")
    parser.add_argument("--target", type=str, help="目标目录")
    parser.add_argument("--workspace", type=str, default="/home/admin/openclaw/workspace",
                       help="工作区根目录")
    
    args = parser.parse_args()
    
    skill = DesignMdSkill(args.workspace)
    
    if args.action == "list":
        print("支持的网站:")
        for site, desc in skill.list_sites().items():
            print(f"  - {site}: {desc}")
    
    elif args.action == "fetch":
        if not args.site:
            print("❌ 请指定网站名称 (--site)")
            return
        skill.fetch(args.site)
    
    elif args.action == "apply":
        if not args.site:
            print("❌ 请指定网站名称 (--site)")
            return
        if not args.target:
            print("❌ 请指定目标目录 (--target)")
            return
        skill.apply(args.site, args.target)


if __name__ == "__main__":
    main()
