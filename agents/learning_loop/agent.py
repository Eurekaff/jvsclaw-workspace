#!/usr/bin/env python3
"""
Learning Loop Agent - 学习循环 Agent

核心职责：
1. 从任务执行中提取经验
2. 创建或更新技能
3. 优化工作流程
4. 自我迭代改进

学习循环：
执行 → 反思 → 抽象 → 应用 → 改进
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents import AgentBase


class LearningLoopAgent(AgentBase):
    AGENT_NAME = "LearningLoopAgent"
    STAGE_NAME = "learning_loop"
    ROLE_DESCRIPTION = "学习循环专家，从经验中提取知识并创建可复用的技能"
    
    INPUT_FILES = ["task_report.json"]
    OUTPUT_FILES = ["learning_report.md", "skill_updates.json"]
    
    def __init__(self, workspace_root: str, artifacts_dir: str = None):
        super().__init__(workspace_root, artifacts_dir)
        self.skills_dir = self.workspace_root / "skills"
        self.learnings_dir = self.workspace_root / "artifacts" / "learnings"
        self.learnings_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行学习循环"""
        
        # 1. 分析任务报告
        task_report = input_data.get("task_report", {})
        task_name = task_report.get("task_name", "未知任务")
        success = task_report.get("success", False)
        complexity = task_report.get("complexity", 1)
        steps_taken = task_report.get("steps_taken", [])
        challenges = task_report.get("challenges", [])
        solutions = task_report.get("solutions", [])
        
        # 2. 提取学习点
        learnings = self._extract_learnings(task_report)
        
        # 3. 判断是否需要创建/更新技能
        skill_actions = []
        if success and complexity >= 5:
            # 复杂且成功的任务 → 创建技能
            skill_action = self._create_skill_suggestion(task_report, learnings)
            if skill_action:
                skill_actions.append(skill_action)
        
        if challenges:
            # 遇到挑战 → 创建改进建议
            improvement = self._create_improvement_suggestion(challenges, solutions)
            if improvement:
                skill_actions.append(improvement)
        
        # 4. 优化工作流程
        workflow_optimizations = self._optimize_workflow(steps_taken)
        
        # 5. 生成学习报告
        learning_report = self._generate_learning_report(
            task_name, learnings, skill_actions, workflow_optimizations
        )
        
        # 6. 保存学习记录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        learning_file = self.learnings_dir / f"{timestamp}_{self._slugify(task_name)}.json"
        
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "task_name": task_name,
            "success": success,
            "complexity": complexity,
            "learnings": learnings,
            "skill_actions": skill_actions,
            "workflow_optimizations": workflow_optimizations,
            "next_actions": self._generate_next_actions(learnings, skill_actions)
        }
        
        with open(learning_file, 'w', encoding='utf-8') as f:
            json.dump(learning_data, f, ensure_ascii=False, indent=2)
        
        # 7. 如果有技能创建，实际执行
        created_skills = []
        for action in skill_actions:
            if action.get("action") == "create_skill" and action.get("auto_create", False):
                skill_path = self._actually_create_skill(action)
                created_skills.append(skill_path)
        
        return {
            "learning_report.md": learning_report,
            "skill_updates.json": learning_data,
            "learnings_count": len(learnings),
            "skills_created": len(created_skills),
            "learning_file": str(learning_file)
        }
    
    def _extract_learnings(self, task_report: Dict) -> List[Dict]:
        """从任务报告中提取学习点"""
        learnings = []
        
        # 提取成功的模式
        if task_report.get("success"):
            steps = task_report.get("steps_taken", [])
            if len(steps) > 3:
                learnings.append({
                    "type": "success_pattern",
                    "description": f"发现了有效的执行模式：{len(steps)} 步完成",
                    "pattern": steps,
                    "confidence": 0.8,
                    "reusable": True
                })
        
        # 提取挑战和解决方案
        challenges = task_report.get("challenges", [])
        solutions = task_report.get("solutions", [])
        
        for i, challenge in enumerate(challenges):
            if i < len(solutions):
                learnings.append({
                    "type": "challenge_solution",
                    "challenge": challenge,
                    "solution": solutions[i],
                    "confidence": 0.9,
                    "reusable": True
                })
        
        # 提取效率改进点
        metrics = task_report.get("metrics", {})
        if metrics.get("token_usage", 0) > 10000:
            learnings.append({
                "type": "efficiency",
                "description": "Token 用量较高，可能需要优化",
                "current_usage": metrics["token_usage"],
                "suggestion": "考虑使用更小的模型或优化 prompt",
                "confidence": 0.7,
                "reusable": False
            })
        
        return learnings
    
    def _create_skill_suggestion(self, task_report: Dict, learnings: List) -> Optional[Dict]:
        """创建技能建议"""
        task_name = task_report.get("task_name", "")
        steps = task_report.get("steps_taken", [])
        
        # 判断是否值得创建技能
        if len(steps) < 3:
            return None
        
        # 提取可复用的步骤
        reusable_steps = []
        for step in steps:
            if any(kw in step.lower() for kw in ["使用", "调用", "创建", "生成", "分析"]):
                reusable_steps.append(step)
        
        if len(reusable_steps) < 2:
            return None
        
        skill_name = self._generate_skill_name(task_name)
        
        return {
            "action": "create_skill",
            "skill_name": skill_name,
            "description": f"从任务'{task_name}'中提取的技能",
            "steps": reusable_steps,
            "learnings": [l for l in learnings if l.get("reusable")],
            "auto_create": True,  # 自动创建
            "confidence": 0.8
        }
    
    def _create_improvement_suggestion(self, challenges: List, solutions: List) -> Dict:
        """创建改进建议"""
        return {
            "action": "improve_workflow",
            "description": f"解决 {len(challenges)} 个挑战",
            "challenges": challenges,
            "solutions": solutions,
            "priority": "high" if len(challenges) > 2 else "medium",
            "auto_create": False
        }
    
    def _optimize_workflow(self, steps: List[str]) -> List[Dict]:
        """优化工作流程"""
        optimizations = []
        
        # 检测重复步骤
        step_counts = {}
        for step in steps:
            # 简化步骤用于计数
            simplified = step.split("→")[0].strip() if "→" in step else step
            step_counts[simplified] = step_counts.get(simplified, 0) + 1
        
        for step, count in step_counts.items():
            if count > 1:
                optimizations.append({
                    "type": "deduplication",
                    "description": f"步骤'{step}'重复 {count} 次，可以合并",
                    "impact": "medium",
                    "effort": "low"
                })
        
        # 检测可以并行的步骤
        if len(steps) > 5:
            optimizations.append({
                "type": "parallelization",
                "description": f"长流程 ({len(steps)} 步)，考虑并行执行",
                "suggestion": "使用 sessions_spawn 创建子 agent 并行处理",
                "impact": "high",
                "effort": "medium"
            })
        
        return optimizations
    
    def _generate_learning_report(self, task_name: str, learnings: List, 
                                  skill_actions: List, optimizations: List) -> str:
        """生成学习报告"""
        report = f"""# 学习报告：{task_name}

**生成时间**: {datetime.now().isoformat()}

---

## 📚 提取的学习点 ({len(learnings)})

"""
        for i, learning in enumerate(learnings, 1):
            emoji = {"success_pattern": "✅", "challenge_solution": "💡", "efficiency": "⚡"}.get(
                learning.get("type", ""), "📌"
            )
            report += f"""
### {emoji} {learning.get('type', '学习点')} #{i}

**描述**: {learning.get('description', learning.get('challenge', 'N/A'))}
**可复用**: {'✅ 是' if learning.get('reusable') else '❌ 否'}
**置信度**: {learning.get('confidence', 0) * 100:.0f}%

"""
            if learning.get("solution"):
                report += f"**解决方案**: {learning['solution']}\n"
        
        report += f"""
---

## 🛠️ 技能操作 ({len(skill_actions)})

"""
        for action in skill_actions:
            action_emoji = {"create_skill": "🆕", "improve_workflow": "🔧"}.get(
                action.get("action", ""), "📌"
            )
            report += f"""
### {action_emoji} {action.get('action', '操作')}

**描述**: {action.get('description', 'N/A')}
**自动执行**: {'✅ 是' if action.get('auto_create') else '❌ 否'}
**置信度**: {action.get('confidence', 0) * 100:.0f}%

"""
        
        report += f"""
---

## ⚡ 流程优化建议 ({len(optimizations)})

"""
        for opt in optimizations:
            impact_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                opt.get("impact", ""), "⚪"
            )
            report += f"""
### {impact_emoji} {opt.get('type', '优化')}

**描述**: {opt.get('description', 'N/A')}
**影响**: {opt.get('impact', 'unknown')}
**工作量**: {opt.get('effort', 'unknown')}

"""
        
        report += """
---

## 🎯 下一步行动

1. 审查自动创建的技能
2. 应用流程优化建议
3. 在下次任务中验证学习点

---

*Generated by LearningLoopAgent v1.0*
"""
        return report
    
    def _generate_next_actions(self, learnings: List, skill_actions: List) -> List[str]:
        """生成下一步行动"""
        actions = []
        
        if any(l.get("reusable") for l in learnings):
            actions.append("在类似任务中应用提取的学习点")
        
        if any(a.get("auto_create") for a in skill_actions):
            actions.append("审查新创建的技能")
        
        actions.append("在下一次任务执行后进行新的学习循环")
        
        return actions
    
    def _generate_skill_name(self, task_name: str) -> str:
        """生成技能名称"""
        # 简化任务名称作为技能名
        name = task_name.lower()
        name = name.replace(" ", "_").replace("-", "_")
        name = "".join(c for c in name if c.isalnum() or c == "_")
        return f"auto_{name[:30]}"
    
    def _slugify(self, text: str) -> str:
        """转换为文件名友好的格式"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]
    
    def _actually_create_skill(self, action: Dict) -> str:
        """实际创建技能文件"""
        skill_name = action.get("skill_name", "unknown_skill")
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 SKILL.md
        skill_md = f"""# {skill_name}

**自动创建**: {datetime.now().isoformat()}
**来源**: {action.get('description', '未知')}
**置信度**: {action.get('confidence', 0) * 100:.0f}%

## 描述

{action.get('description', '自动生成的技能')}

## 步骤

"""
        for i, step in enumerate(action.get("steps", []), 1):
            skill_md += f"{i}. {step}\n"
        
        skill_md += """
## 使用方法

```python
from agents import AgentBase

class AutoSkill(AgentBase):
    def execute(self, input_data):
        # 实现技能逻辑
        pass
```

---

*Auto-generated by LearningLoopAgent*
"""
        
        skill_file = skill_dir / "SKILL.md"
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(skill_md)
        
        # 创建 __init__.py
        init_file = skill_dir / "__init__.py"
        init_file.touch()
        
        return str(skill_dir)


if __name__ == "__main__":
    # 测试
    agent = LearningLoopAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "task_report": {
            "task_name": "集成 awesome-design-md 设计系统",
            "success": True,
            "complexity": 7,
            "steps_taken": [
                "浏览 skills.sh 网站",
                "研究 awesome-design-md 项目",
                "获取 Linear 设计令牌",
                "更新 Tailwind 配置",
                "创建演示页面",
                "提交到 Git"
            ],
            "challenges": ["GitHub 路径结构变化"],
            "solutions": ["手动创建 Linear 设计令牌"],
            "metrics": {"token_usage": 15000, "api_calls": 25}
        }
    }
    
    result = agent.execute(test_input)
    print(f"\n✅ 学习循环完成")
    print(f"📚 学习点：{result.get('learnings_count', 0)}")
    print(f"🛠️ 创建技能：{result.get('skills_created', 0)}")
    print(f"📁 学习文件：{result.get('learning_file', 'N/A')}")
