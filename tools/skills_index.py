#!/usr/bin/env python3
"""
Skills Index Generator - Skills 索引生成器

扫描本地 skills 目录，生成可搜索的索引数据库
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SkillsIndexGenerator:
    """Skills 索引生成器"""
    
    def __init__(self, skills_dir: str = None):
        self.skills_dir = Path(skills_dir) if skills_dir else Path.home() / ".openclaw" / "skills"
        self.index_file = self.skills_dir / "skills_index.json"
        self.index = {
            "metadata": {
                "generated_at": "",
                "total_skills": 0,
                "total_repos": 0
            },
            "repositories": [],
            "skills": [],
            "categories": {}
        }
    
    def scan(self) -> Dict:
        """扫描 skills 目录"""
        print(f"🔍 扫描 skills 目录：{self.skills_dir}")
        
        repos = []
        all_skills = []
        categories = {}
        
        # 扫描所有目录
        for item in self.skills_dir.iterdir():
            if not item.is_dir() or item.name.startswith('.'):
                continue
            
            repo_info = self._scan_repository(item)
            if repo_info:
                repos.append(repo_info)
                all_skills.extend(repo_info['skills'])
                
                # 按分类整理
                category = repo_info.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].extend(repo_info['skills'])
        
        # 更新索引
        self.index['metadata']['generated_at'] = datetime.now().isoformat()
        self.index['metadata']['total_repos'] = len(repos)
        self.index['metadata']['total_skills'] = len(all_skills)
        self.index['repositories'] = repos
        self.index['skills'] = all_skills
        self.index['categories'] = categories
        
        return self.index
    
    def _scan_repository(self, repo_path: Path) -> Dict:
        """扫描单个仓库"""
        repo_info = {
            "name": repo_path.name,
            "path": str(repo_path),
            "scanned_at": datetime.now().isoformat(),
            "skills": [],
            "category": "other"
        }
        
        # 尝试读取 README 或 SKILL.md
        readme_path = repo_path / "README.md"
        skill_md_path = repo_path / "SKILL.md"
        
        description = ""
        if readme_path.exists():
            description = self._extract_description(readme_path)
        elif skill_md_path.exists():
            description = self._extract_description(skill_md_path)
            repo_info['category'] = self._detect_category(skill_md_path)
        
        # 扫描 skill 文件
        skill_files = list(repo_path.glob("**/SKILL.md")) + \
                     list(repo_path.glob("**/skill.md"))
        
        for skill_file in skill_files:
            skill_info = self._parse_skill_file(skill_file, repo_path)
            if skill_info:
                repo_info['skills'].append(skill_info)
        
        # 如果没有找到 SKILL.md，但有子目录，可能是集合仓库
        if not repo_info['skills']:
            subdirs = [d for d in repo_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            if subdirs:
                for subdir in subdirs:
                    skill_info = {
                        "name": f"{repo_path.name}/{subdir.name}",
                        "path": str(subdir),
                        "description": f"Skill from {repo_path.name}",
                        "tags": [repo_path.name]
                    }
                    repo_info['skills'].append(skill_info)
        
        repo_info['skills_count'] = len(repo_info['skills'])
        
        print(f"  📦 {repo_path.name}: {repo_info['skills_count']} skills")
        return repo_info
    
    def _extract_description(self, file_path: Path) -> str:
        """从文件提取描述"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # 读取前 2000 字符
                
                # 提取第一个标题后的内容
                lines = content.split('\n')
                description_lines = []
                in_description = False
                
                for line in lines:
                    if line.startswith('# ') or line.startswith('## '):
                        in_description = True
                        continue
                    if in_description and line.startswith('#'):
                        break
                    if in_description and line.strip():
                        description_lines.append(line.strip())
                
                return ' '.join(description_lines[:5])[:500]
        except:
            return ""
    
    def _detect_category(self, file_path: Path) -> str:
        """检测 skill 分类"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
                if 'frontend' in content or 'react' in content or 'css' in content:
                    return 'frontend'
                elif 'backend' in content or 'database' in content or 'api' in content:
                    return 'backend'
                elif 'browser' in content or 'web' in content:
                    return 'browser'
                elif 'pdf' in content or 'docx' in content or 'pptx' in content:
                    return 'document'
                elif 'video' in content or 'remotion' in content:
                    return 'multimedia'
                elif 'search' in content or 'find' in content:
                    return 'search'
                elif 'report' in content or 'task' in content:
                    return 'reporting'
                else:
                    return 'other'
        except:
            return 'other'
    
    def _parse_skill_file(self, skill_file: Path, repo_path: Path) -> Dict:
        """解析 SKILL.md 文件"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read(3000)
                
            # 提取基本信息
            lines = content.split('\n')
            name = skill_file.parent.name
            
            # 提取描述
            description = ""
            for i, line in enumerate(lines):
                if line.startswith('## ') or line.startswith('### '):
                    if '描述' in line.lower() or 'description' in line.lower():
                        # 提取后续非空行
                        for j in range(i+1, min(i+5, len(lines))):
                            if lines[j].strip() and not lines[j].startswith('#'):
                                description += lines[j].strip() + ' '
                        break
            
            if not description:
                description = self._extract_description(skill_file)
            
            return {
                "name": name,
                "path": str(skill_file),
                "repo": repo_path.name,
                "description": description[:300],
                "tags": [repo_path.name],
                "category": self._detect_category(skill_file)
            }
        except Exception as e:
            print(f"    ⚠️  解析失败 {skill_file}: {e}")
            return None
    
    def save(self) -> str:
        """保存索引到文件"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 索引已保存到：{self.index_file}")
        return str(self.index_file)
    
    def search(self, query: str, category: str = None) -> List:
        """搜索 skills"""
        if not self.index['skills']:
            self.scan()
        
        results = []
        query_lower = query.lower()
        
        for skill in self.index['skills']:
            # 检查分类
            if category and skill.get('category') != category:
                continue
            
            # 搜索名称、描述、标签
            searchable = f"{skill.get('name', '')} {skill.get('description', '')} {' '.join(skill.get('tags', []))}".lower()
            
            if query_lower in searchable:
                results.append(skill)
        
        return results
    
    def list_categories(self) -> Dict:
        """列出所有分类"""
        if not self.index['categories']:
            self.scan()
        
        return {
            cat: len(skills) 
            for cat, skills in self.index['categories'].items()
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Skills Index Generator")
    parser.add_argument("action", choices=["scan", "search", "list"], 
                       help="操作类型")
    parser.add_argument("--query", type=str, help="搜索关键词")
    parser.add_argument("--category", type=str, help="分类过滤")
    parser.add_argument("--skills-dir", type=str, 
                       default=str(Path.home() / ".openclaw" / "skills"),
                       help="Skills 目录")
    
    args = parser.parse_args()
    
    generator = SkillsIndexGenerator(args.skills_dir)
    
    if args.action == "scan":
        index = generator.scan()
        generator.save()
        
        print(f"\n📊 统计:")
        print(f"  仓库数：{index['metadata']['total_repos']}")
        print(f"  Skills 数：{index['metadata']['total_skills']}")
        print(f"  分类数：{len(index['categories'])}")
    
    elif args.action == "search":
        if not args.query:
            print("❌ 请指定搜索关键词 (--query)")
            return
        
        results = generator.search(args.query, args.category)
        
        print(f"\n🔍 搜索结果：{len(results)} 个")
        for skill in results[:10]:
            print(f"  - {skill['name']} ({skill.get('category', 'other')})")
            print(f"    {skill['description'][:100]}...")
    
    elif args.action == "list":
        categories = generator.list_categories()
        
        print("\n📂 分类:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} skills")


if __name__ == "__main__":
    main()
