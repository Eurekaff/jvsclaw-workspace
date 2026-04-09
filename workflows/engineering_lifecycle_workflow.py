#!/usr/bin/env python3
"""
Workflow Orchestrator - 工程生命周期工作流编排器

负责：
1. 管理全局状态 ProjectState
2. 定义阶段流转规则
3. 支持从指定阶段启动/恢复
4. 记录每一阶段输入输出
5. 保存所有中间产物
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 导入所有 agent
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.problem_definition.agent import ProblemDefinitionAgent
from agents.mvp_scope.agent import MVPScopeAgent
from agents.context_pack.agent import ContextPackAgent
from agents.mainline_build.agent import MainlineBuildAgent
from agents.quality_correction.agent import QualityCorrectionAgent
from agents.productization.agent import ProductizationAgent
from agents.retrospective.agent import RetrospectiveAgent


# 阶段定义
STAGES = [
    "problem_definition",
    "mvp_scope",
    "context_pack",
    "mainline_build",
    "quality_correction",
    "productization",
    "retrospective"
]

# Agent 映射
AGENT_MAP = {
    "problem_definition": ProblemDefinitionAgent,
    "mvp_scope": MVPScopeAgent,
    "context_pack": ContextPackAgent,
    "mainline_build": MainlineBuildAgent,
    "quality_correction": QualityCorrectionAgent,
    "productization": ProductizationAgent,
    "retrospective": RetrospectiveAgent,
}


class ProjectState:
    """项目状态管理"""
    
    def __init__(self, project_name: str = None, raw_brief: str = None):
        self.state = {
            "project_name": project_name or "Unnamed Project",
            "raw_brief": raw_brief or "",
            "current_stage": "idea_input",
            "approved_scope": None,
            "tech_stack": [],
            "constraints": [],
            "artifacts_index": {},
            "pending_questions": [],
            "validation_results": {},
            "next_actions": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "0.1.0"
            }
        }
    
    def update_stage(self, stage: str):
        """更新当前阶段"""
        self.state["current_stage"] = stage
        self.state["metadata"]["updated_at"] = datetime.now().isoformat()
    
    def add_artifact(self, stage: str, filename: str, path: str, status: str = "pending"):
        """添加产出物索引"""
        self.state["artifacts_index"][f"{stage}/{filename}"] = {
            "path": path,
            "created_at": datetime.now().isoformat(),
            "status": status
        }
    
    def approve_stage(self, stage: str):
        """确认阶段完成"""
        if stage == "mvp_scope":
            self.state["approved_scope"] = self.state.get("validation_results", {}).get(stage)
    
    def save(self, filepath: str):
        """保存状态到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'ProjectState':
        """从文件加载状态"""
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        instance = cls()
        instance.state = state
        return instance
    
    def __getitem__(self, key):
        return self.state[key]
    
    def __setitem__(self, key, value):
        self.state[key] = value


class WorkflowOrchestrator:
    """工作流编排器"""
    
    def __init__(self, workspace_root: str, run_id: str = None):
        self.workspace_root = Path(workspace_root)
        self.run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = self.workspace_root / "artifacts" / "runs" / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        self.state: Optional[ProjectState] = None
        self.agents: Dict[str, Any] = {}
        
        # 初始化 agents
        for stage_name, agent_class in AGENT_MAP.items():
            self.agents[stage_name] = agent_class(
                str(self.workspace_root),
                str(self.run_dir)
            )
    
    def start(self, raw_brief: str, project_name: str = None) -> ProjectState:
        """启动新工作流"""
        self.state = ProjectState(project_name, raw_brief)
        
        # 保存原始输入
        brief_file = self.run_dir / "raw_brief.md"
        with open(brief_file, 'w', encoding='utf-8') as f:
            f.write(f"# {self.state['project_name']}\n\n{raw_brief}")
        
        self.state.add_artifact("idea_input", "raw_brief.md", str(brief_file), "approved")
        self.state.save(self.run_dir / "project_state.json")
        
        print(f"✅ 工作流启动：{self.state['project_name']}")
        print(f"📁 运行目录：{self.run_dir}")
        
        return self.state
    
    def resume(self, run_id: str) -> ProjectState:
        """从已有运行恢复"""
        self.run_id = run_id
        self.run_dir = self.workspace_root / "artifacts" / "runs" / run_id
        
        if not self.run_dir.exists():
            raise ValueError(f"Run directory not found: {self.run_dir}")
        
        self.state = ProjectState.load(self.run_dir / "project_state.json")
        
        # 重新初始化 agents 指向正确的目录
        for stage_name, agent_class in AGENT_MAP.items():
            self.agents[stage_name] = agent_class(
                str(self.workspace_root),
                str(self.run_dir)
            )
        
        print(f"🔄 恢复工作流：{self.state['project_name']}")
        print(f"📍 当前阶段：{self.state['current_stage']}")
        
        return self.state
    
    def run_stage(self, stage_name: str, input_data: Dict = None, auto_approve: bool = True) -> Dict:
        """运行指定阶段"""
        if stage_name not in AGENT_MAP:
            raise ValueError(f"Unknown stage: {stage_name}")
        
        print(f"\n{'='*60}")
        print(f"🚀 执行阶段：{stage_name}")
        print(f"{'='*60}")
        
        agent = self.agents[stage_name]
        
        # 准备输入数据
        if input_data is None:
            input_data = self._gather_stage_input(stage_name)
        
        # 执行 agent
        output_files = agent.run(input_data)
        
        # 更新状态
        self.state.update_stage(stage_name)
        for filename, filepath in output_files.items():
            self.state.add_artifact(stage_name, filename, filepath, "pending")
        
        # 自动确认（或等待人工确认）
        if auto_approve:
            for filename in output_files:
                # 更新 artifact 状态为 approved
                for key in self.state["artifacts_index"]:
                    if key.endswith(filename):
                        self.state["artifacts_index"][key]["status"] = "approved"
        
        # 保存状态
        self.state.save(self.run_dir / "project_state.json")
        
        # 打印输出
        print(f"\n✅ 阶段完成：{stage_name}")
        print(f"📄 产出文件:")
        for filename, filepath in output_files.items():
            print(f"   - {filename}")
        
        return output_files
    
    def _gather_stage_input(self, stage_name: str) -> Dict:
        """收集阶段输入数据"""
        input_data = {}
        
        # 根据阶段收集前置阶段的输出
        stage_index = STAGES.index(stage_name)
        
        for i in range(stage_index):
            prev_stage = STAGES[i]
            prev_agent = self.agents[prev_stage]
            
            for filename in prev_agent.OUTPUT_FILES:
                content = prev_agent.load_input(filename)
                if content:
                    key = filename.replace('.md', '').replace('.json', '')
                    if filename.endswith('.json'):
                        input_data[key] = json.loads(content)
                    else:
                        input_data[key] = content
        
        # 添加原始简报
        if stage_name == "problem_definition":
            input_data["raw_brief"] = self.state["raw_brief"]
        
        return input_data
    
    def run_full_workflow(self, raw_brief: str, project_name: str = None, 
                         start_from: str = None, stop_at: str = None) -> ProjectState:
        """运行完整工作流"""
        # 启动或恢复
        if start_from is None:
            self.start(raw_brief, project_name)
        else:
            # 从指定阶段开始
            self.start(raw_brief, project_name)
        
        # 确定阶段范围
        stages_to_run = STAGES
        if start_from:
            start_idx = STAGES.index(start_from)
            stages_to_run = STAGES[start_idx:]
        if stop_at:
            stop_idx = STAGES.index(stop_at)
            stages_to_run = STAGES[:stop_idx + 1]
        
        # 依次执行各阶段
        for stage in stages_to_run:
            self.run_stage(stage, auto_approve=True)
        
        # 完成
        self.state.update_stage("completed")
        self.state.save(self.run_dir / "project_state.json")
        
        print(f"\n{'='*60}")
        print(f"🎉 工作流完成！")
        print(f"{'='*60}")
        print(f"📊 产出物目录：{self.run_dir}")
        print(f"📈 阶段数：{len(stages_to_run)}")
        
        return self.state
    
    def get_status(self) -> Dict:
        """获取工作流状态"""
        return {
            "project_name": self.state["project_name"] if self.state else None,
            "current_stage": self.state["current_stage"] if self.state else None,
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "artifacts_count": len(self.state["artifacts_index"]) if self.state else 0
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Engineering Lifecycle Workflow")
    parser.add_argument("--brief", type=str, help="项目简述")
    parser.add_argument("--example", action="store_true", help="运行示例项目")
    parser.add_argument("--resume", type=str, help="从指定 run_id 恢复")
    parser.add_argument("--start-from", type=str, help="从指定阶段开始")
    parser.add_argument("--workspace", type=str, default="/home/admin/openclaw/workspace",
                       help="工作区根目录")
    
    args = parser.parse_args()
    
    orchestrator = WorkflowOrchestrator(args.workspace)
    
    if args.example:
        # 运行示例项目
        example_brief = """
        做一个面向合规分析员的企业批量查册原型系统。
        用户上传来源复杂、字段混乱的 Excel，系统自动识别企业主体并生成 entity 清单，
        再调用查册接口返回结构化结果，支持人工复核和导出。
        第一版不做登录权限和复杂报表。
        """
        orchestrator.run_full_workflow(example_brief, "企业批量查册系统")
        
    elif args.resume:
        # 恢复已有运行
        orchestrator.resume(args.resume)
        current_stage = orchestrator.state["current_stage"]
        if current_stage != "completed":
            # 继续执行下一阶段
            current_idx = STAGES.index(current_stage)
            if current_idx < len(STAGES) - 1:
                next_stage = STAGES[current_idx + 1]
                orchestrator.run_stage(next_stage)
        
    elif args.brief:
        # 从原始简报启动
        orchestrator.run_full_workflow(args.brief, "新项目")
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
