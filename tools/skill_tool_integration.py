#!/usr/bin/env python3
"""
Skill & Tool Integration System - Skill 和 Tool 集成系统

确保 agents 能够调用 skills 和 tools 来优化任务执行
"""

import json
import importlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime


class SkillLoader:
    """Skill 加载器"""
    
    def __init__(self, skills_dir: str = None):
        self.skills_dir = Path(skills_dir) if skills_dir else Path.home() / ".openclaw" / "skills"
        self.index_file = self.skills_dir / "skills_index.json"
        self.loaded_skills = {}
        self.skills_index = {}
    
    def load_index(self) -> Dict:
        """加载 skills 索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.skills_index = json.load(f)
            print(f"📚 已加载 skills 索引：{self.skills_index['metadata']['total_skills']} skills")
            return self.skills_index
        else:
            print("⚠️  Skills 索引不存在，请先运行 skills_index.py scan")
            return {}
    
    def find_skill(self, skill_name: str) -> Optional[Dict]:
        """查找 skill"""
        if not self.skills_index:
            self.load_index()
        
        for skill in self.skills_index.get('skills', []):
            if skill['name'] == skill_name or skill_name in skill.get('path', ''):
                return skill
        
        return None
    
    def load_skill(self, skill_name: str) -> Optional[Callable]:
        """加载 skill 模块"""
        if skill_name in self.loaded_skills:
            return self.loaded_skills[skill_name]
        
        skill_info = self.find_skill(skill_name)
        if not skill_info:
            print(f"❌ 未找到 skill: {skill_name}")
            return None
        
        try:
            skill_path = Path(skill_info['path'])
            
            # 尝试不同的加载方式
            # 1. 如果是 Python 模块
            if (skill_path / "__init__.py").exists():
                spec = importlib.util.spec_from_file_location(
                    skill_name, 
                    skill_path / "__init__.py"
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.loaded_skills[skill_name] = module
                print(f"✅ 已加载 skill: {skill_name}")
                return module
            
            # 2. 如果有 SKILL.md，返回路径
            elif (skill_path / "SKILL.md").exists():
                self.loaded_skills[skill_name] = {
                    "type": "skill_file",
                    "path": str(skill_path),
                    "skill_md": str(skill_path / "SKILL.md")
                }
                print(f"✅ 已加载 skill 文件：{skill_name}")
                return self.loaded_skills[skill_name]
            
            # 3. 返回目录路径
            else:
                self.loaded_skills[skill_name] = {
                    "type": "directory",
                    "path": str(skill_path)
                }
                print(f"✅ 已加载 skill 目录：{skill_name}")
                return self.loaded_skills[skill_name]
                
        except Exception as e:
            print(f"❌ 加载 skill 失败：{skill_name} - {e}")
            return None
    
    def execute_skill(self, skill_name: str, **kwargs) -> Any:
        """执行 skill"""
        skill = self.load_skill(skill_name)
        
        if not skill:
            return None
        
        # 如果是 Python 模块，尝试调用 execute 或 main
        if hasattr(skill, 'execute'):
            return skill.execute(**kwargs)
        elif hasattr(skill, 'main'):
            return skill.main(**kwargs)
        # 如果是文件类型，返回信息
        elif isinstance(skill, dict):
            return skill
        
        return None
    
    def list_loaded_skills(self) -> List[str]:
        """列出已加载的 skills"""
        return list(self.loaded_skills.keys())


class ToolRegistry:
    """Tool 注册表"""
    
    def __init__(self):
        self.tools = {}
        self._register_builtin_tools()
    
    def _register_builtin_tools(self):
        """注册内置 tools"""
        # 文件操作 tools
        self.register("file_read", self._file_read, "读取文件内容")
        self.register("file_write", self._file_write, "写入文件内容")
        self.register("file_list", self._file_list, "列出目录文件")
        
        # 执行 tools
        self.register("exec", self._exec, "执行 shell 命令")
        
        # 网络 tools
        self.register("web_fetch", self._web_fetch, "获取网页内容")
        
        # 搜索 tools
        self.register("search_skills", self._search_skills, "搜索 skills")
    
    def register(self, name: str, func: Callable, description: str = ""):
        """注册 tool"""
        self.tools[name] = {
            "func": func,
            "description": description,
            "registered_at": datetime.now().isoformat()
        }
        print(f"🔧 已注册 tool: {name}")
    
    def get(self, name: str) -> Optional[Callable]:
        """获取 tool"""
        if name in self.tools:
            return self.tools[name]["func"]
        return None
    
    def call(self, name: str, **kwargs) -> Any:
        """调用 tool"""
        tool = self.get(name)
        if tool:
            try:
                return tool(**kwargs)
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Tool not found: {name}"}
    
    def list_tools(self) -> List[Dict]:
        """列出所有 tools"""
        return [
            {"name": name, "description": info["description"]}
            for name, info in self.tools.items()
        ]
    
    # 内置 tools 实现
    def _file_read(self, path: str) -> Dict:
        """读取文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _file_write(self, path: str, content: str) -> Dict:
        """写入文件"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "path": path}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _file_list(self, path: str) -> Dict:
        """列出目录"""
        try:
            p = Path(path)
            if p.exists():
                files = [str(f) for f in p.iterdir()]
                return {"files": files, "success": True}
            return {"error": "Path not found", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _exec(self, command: str, cwd: str = None) -> Dict:
        """执行命令"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd,
                capture_output=True, 
                text=True,
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _web_fetch(self, url: str) -> Dict:
        """获取网页"""
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as response:
                return {
                    "content": response.read().decode('utf-8'),
                    "success": True
                }
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _search_skills(self, query: str) -> Dict:
        """搜索 skills"""
        try:
            from tools.skills_index import SkillsIndexGenerator
            generator = SkillsIndexGenerator()
            results = generator.search(query)
            return {"results": results, "count": len(results), "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}


class AgentIntegration:
    """Agent 集成层 - 让 agents 能够调用 skills 和 tools"""
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.skill_loader = SkillLoader()
        self.tool_registry = ToolRegistry()
        
        # 加载 skills 索引
        self.skill_loader.load_index()
    
    def get_available_skills(self) -> List[str]:
        """获取可用 skills 列表"""
        return [skill['name'] for skill in self.skill_loader.skills_index.get('skills', [])]
    
    def get_available_tools(self) -> List[str]:
        """获取可用 tools 列表"""
        return [tool['name'] for tool in self.tool_registry.list_tools()]
    
    def call_skill(self, skill_name: str, **kwargs) -> Any:
        """调用 skill"""
        print(f"🔮 调用 skill: {skill_name}")
        return self.skill_loader.execute_skill(skill_name, **kwargs)
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """调用 tool"""
        print(f"🔧 调用 tool: {tool_name}")
        return self.tool_registry.call(tool_name, **kwargs)
    
    def execute_with_skills(self, task: str, skills: List[str] = None) -> Dict:
        """使用 skills 执行任务"""
        result = {
            "task": task,
            "skills_used": skills or [],
            "results": {},
            "timestamp": datetime.now().isoformat()
        }
        
        if skills:
            for skill_name in skills:
                print(f"🚀 执行 skill: {skill_name}")
                skill_result = self.call_skill(skill_name)
                result["results"][skill_name] = skill_result
        
        return result
    
    def create_agent_context(self, agent_name: str) -> Dict:
        """为 agent 创建上下文（包含可用的 skills 和 tools）"""
        return {
            "agent_name": agent_name,
            "available_skills": self.get_available_skills(),
            "available_tools": self.get_available_tools(),
            "call_skill": self.call_skill,
            "call_tool": self.call_tool,
            "workspace": str(self.workspace_root),
            "skills_dir": str(self.skill_loader.skills_dir)
        }


# 全局实例
_integration = None

def get_integration(workspace_root: str = None) -> AgentIntegration:
    """获取集成实例"""
    global _integration
    if not _integration:
        _integration = AgentIntegration(workspace_root)
    return _integration


def main():
    """测试"""
    print("="*60)
    print("Skill & Tool Integration Test")
    print("="*60)
    
    integration = AgentIntegration("/home/admin/openclaw/workspace")
    
    # 测试 tools
    print("\n🔧 可用 tools:")
    for tool in integration.get_available_tools():
        print(f"  - {tool}")
    
    # 测试 skills
    print("\n🔮 可用 skills (前 10 个):")
    skills = integration.get_available_skills()[:10]
    for skill in skills:
        print(f"  - {skill}")
    
    # 测试调用 tool
    print("\n🧪 测试调用 tool:")
    result = integration.call_tool("file_list", path="/home/admin/openclaw/workspace")
    print(f"  文件数：{len(result.get('files', []))}")
    
    # 测试调用 skill
    print("\n🧪 测试调用 skill:")
    result = integration.call_skill("find-skills")
    print(f"  结果：{result}")
    
    # 创建 agent 上下文
    print("\n🧪 创建 agent 上下文:")
    context = integration.create_agent_context("test_agent")
    print(f"  Agent: {context['agent_name']}")
    print(f"  Skills: {len(context['available_skills'])} available")
    print(f"  Tools: {len(context['available_tools'])} available")


if __name__ == "__main__":
    main()
