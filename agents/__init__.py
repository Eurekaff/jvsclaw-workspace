#!/usr/bin/env python3
"""
Agent Base Class - 所有工程生命周期 agent 的基类

集成 Skills 和 Tools 调用能力
"""

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

# 导入 skill 和 tool 集成
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from skill_tool_integration import AgentIntegration, get_integration


class AgentBase(ABC):
    """
    Agent 基类
    
    每个 agent 必须有：
    - 角色说明 (role_description)
    - 输入 schema (input_schema)
    - 输出 schema (output_schema)
    - prompt 模板 (prompt_template)
    - 最小测试样例
    """
    
    # 子类必须覆盖
    AGENT_NAME: str = "BaseAgent"
    STAGE_NAME: str = "base"
    ROLE_DESCRIPTION: str = "Base agent role"
    
    # 输入输出文件约定
    INPUT_FILES: List[str] = []
    OUTPUT_FILES: List[str] = []
    
    def __init__(self, workspace_root: str, artifacts_dir: str = None):
        self.workspace_root = Path(workspace_root)
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else self.workspace_root / "artifacts" / "runs"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 skill 和 tool 集成
        self.integration = get_integration(str(workspace_root))
        self.skills_context = self.integration.create_agent_context(self.AGENT_NAME)
        
    def load_input(self, filename: str) -> Optional[str]:
        """加载输入文件"""
        filepath = self.artifacts_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def load_json_input(self, filename: str) -> Optional[Dict]:
        """加载 JSON 输入"""
        content = self.load_input(filename)
        if content:
            return json.loads(content)
        return None
    
    def save_output(self, filename: str, content: str) -> str:
        """保存输出文件"""
        filepath = self.artifacts_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(filepath)
    
    # ========== Skill 和 Tool 调用方法 ==========
    
    def use_skill(self, skill_name: str, **kwargs) -> Any:
        """
        调用 skill
        
        Args:
            skill_name: skill 名称
            **kwargs: skill 参数
            
        Returns:
            skill 执行结果
        """
        print(f"🔮 [{self.AGENT_NAME}] 使用 skill: {skill_name}")
        return self.integration.call_skill(skill_name, **kwargs)
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """
        调用 tool
        
        Args:
            tool_name: tool 名称
            **kwargs: tool 参数
            
        Returns:
            tool 执行结果
        """
        print(f"🔧 [{self.AGENT_NAME}] 使用 tool: {tool_name}")
        return self.integration.call_tool(tool_name, **kwargs)
    
    def get_available_skills(self) -> List[str]:
        """获取可用 skills 列表"""
        return self.skills_context['available_skills']
    
    def get_available_tools(self) -> List[str]:
        """获取可用 tools 列表"""
        return self.skills_context['available_tools']
    
    def execute_with_tools(self, task: str, tools: List[str] = None) -> Dict:
        """
        使用 tools 执行任务
        
        Args:
            task: 任务描述
            tools: 要使用的 tools 列表
            
        Returns:
            执行结果
        """
        result = {
            "task": task,
            "tools_used": tools or [],
            "results": {},
            "timestamp": datetime.now().isoformat()
        }
        
        if tools:
            for tool_name in tools:
                print(f"🔧 [{self.AGENT_NAME}] 使用 tool: {tool_name}")
                tool_result = self.use_tool(tool_name)
                result["results"][tool_name] = tool_result
        
        return result
    
    def save_json_output(self, filename: str, data: Dict) -> str:
        """保存 JSON 输出"""
        content = json.dumps(data, ensure_ascii=False, indent=2)
        return self.save_output(filename, content)
    
    def load_prompt(self, prompt_name: str = None) -> str:
        """
        加载 prompt 模板
        默认从 prompts/{stage_name}_prompt.md 加载
        """
        prompt_file = prompt_name or f"{self.STAGE_NAME}_prompt"
        prompt_path = self.workspace_root / "prompts" / f"{prompt_file}.md"
        
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # 返回默认 prompt
        return self.get_default_prompt()
    
    def get_default_prompt(self) -> str:
        """默认 prompt 模板"""
        return f"""# {self.AGENT_NAME}

## Role
{self.ROLE_DESCRIPTION}

## Input
{{input}}

## Task
请根据输入完成你的任务，输出结构化的结果。

## Output Format
请以 JSON 格式输出，包含必要的字段。
"""
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 agent 任务
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            输出数据字典
        """
        pass
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, str]:
        """
        运行 agent，保存输出
        
        Args:
            input_data: 可选的输入数据
            
        Returns:
            输出文件路径字典
        """
        # 执行任务
        output_data = self.execute(input_data or {})
        
        # 保存输出
        output_files = {}
        for filename in self.OUTPUT_FILES:
            # 尝试带扩展名的 key，然后尝试不带扩展名的 key
            key_with_ext = filename
            key_without_ext = filename.replace('.json', '').replace('.md', '')
            
            content = output_data.get(key_with_ext) or output_data.get(key_without_ext)
            
            if content is not None:
                if filename.endswith('.json'):
                    output_files[filename] = self.save_json_output(filename, content)
                else:
                    output_files[filename] = self.save_output(filename, content)
        
        return output_files
    
    def get_status(self) -> Dict:
        """返回 agent 状态信息"""
        return {
            "name": self.AGENT_NAME,
            "stage": self.STAGE_NAME,
            "role": self.ROLE_DESCRIPTION,
            "input_files": self.INPUT_FILES,
            "output_files": self.OUTPUT_FILES
        }
