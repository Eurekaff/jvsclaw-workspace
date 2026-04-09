#!/usr/bin/env python3
"""
TaskReportAgent - 任务报告撰写 agent

职责：
- 在任务完成后自动生成任务报告
- 记录任务执行过程、结果、经验教训
- 存档到本地供后续参考
- 支持多种报告格式（Markdown、JSON）

输出：
- task_report.md - 任务报告（人类可读）
- task_report.json - 任务报告（结构化）
- 存档到 artifacts/task_reports/
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents import AgentBase


class TaskReportAgent(AgentBase):
    AGENT_NAME = "TaskReportAgent"
    STAGE_NAME = "task_report"
    ROLE_DESCRIPTION = "任务报告专家，擅长总结任务执行过程并生成结构化报告"
    
    INPUT_FILES = []
    OUTPUT_FILES = ["task_report.md", "task_report.json"]
    
    def __init__(self, workspace_root: str, artifacts_dir: str = None):
        super().__init__(workspace_root, artifacts_dir)
        self.reports_dir = self.workspace_root / "artifacts" / "task_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成任务报告"""
        # 提取任务信息
        task_name = input_data.get("task_name", "未命名任务")
        task_description = input_data.get("task_description", "")
        start_time = input_data.get("start_time", "")
        end_time = input_data.get("end_time", datetime.now().isoformat())
        status = input_data.get("status", "completed")
        
        # 任务执行详情
        steps_taken = input_data.get("steps_taken", [])
        artifacts_created = input_data.get("artifacts_created", [])
        challenges = input_data.get("challenges", [])
        solutions = input_data.get("solutions", [])
        
        # 统计信息
        metrics = input_data.get("metrics", {})
        token_usage = metrics.get("token_usage", 0)
        api_calls = metrics.get("api_calls", 0)
        files_modified = metrics.get("files_modified", 0)
        
        # 经验教训
        lessons_learned = input_data.get("lessons_learned", [])
        next_steps = input_data.get("next_steps", [])
        
        # 生成报告
        report_data = {
            "task_name": task_name,
            "task_description": task_description,
            "status": status,
            "timing": {
                "start_time": start_time,
                "end_time": end_time,
                "duration": self._calculate_duration(start_time, end_time)
            },
            "execution": {
                "steps_taken": steps_taken,
                "artifacts_created": artifacts_created,
                "challenges": challenges,
                "solutions": solutions
            },
            "metrics": {
                "token_usage": token_usage,
                "api_calls": api_calls,
                "files_modified": files_modified
            },
            "learnings": {
                "lessons_learned": lessons_learned,
                "next_steps": next_steps
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "agent_version": "1.0.0",
                "report_id": self._generate_report_id(task_name)
            }
        }
        
        # 生成 Markdown 报告
        md_content = self._generate_markdown(report_data)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{timestamp}_{self._slugify(task_name)}"
        
        # 保存 JSON
        json_path = self.reports_dir / f"{report_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # 保存 Markdown
        md_path = self.reports_dir / f"{report_filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return {
            "task_report.md": md_content,
            "task_report.json": report_data,
            "report_path": str(self.reports_dir),
            "report_filename": report_filename
        }
    
    def _calculate_duration(self, start: str, end: str) -> str:
        """计算任务持续时间"""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            duration = end_dt - start_dt
            total_seconds = int(duration.total_seconds())
            
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            if hours > 0:
                return f"{hours}小时 {minutes}分钟 {seconds}秒"
            elif minutes > 0:
                return f"{minutes}分钟 {seconds}秒"
            else:
                return f"{seconds}秒"
        except:
            return "未知"
    
    def _generate_report_id(self, task_name: str) -> str:
        """生成报告 ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        slug = self._slugify(task_name)[:20]
        return f"TR_{timestamp}_{slug}"
    
    def _slugify(self, text: str) -> str:
        """将文本转换为文件名友好的格式"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text
    
    def _generate_markdown(self, report: Dict) -> str:
        """生成 Markdown 格式报告"""
        md = f"""# 任务报告：{report['task_name']}

**报告 ID**: `{report['metadata']['report_id']}`  
**生成时间**: {report['metadata']['generated_at']}  
**状态**: {'✅ 完成' if report['status'] == 'completed' else '🟡 进行中' if report['status'] == 'running' else '❌ 失败'}

---

## 📋 任务概述

**任务描述**: {report['task_description']}

**时间信息**:
- 开始时间：{report['timing']['start_time']}
- 结束时间：{report['timing']['end_time']}
- 持续时间：{report['timing']['duration']}

---

## 🚀 执行过程

### 采取的步骤

"""
        for i, step in enumerate(report['execution']['steps_taken'], 1):
            md += f"{i}. {step}\n"
        
        md += "\n### 创建的产物\n\n"
        if report['execution']['artifacts_created']:
            for artifact in report['execution']['artifacts_created']:
                md += f"- 📄 {artifact}\n"
        else:
            md += "无\n"
        
        md += "\n### 遇到的挑战\n\n"
        if report['execution']['challenges']:
            for i, challenge in enumerate(report['execution']['challenges'], 1):
                md += f"{i}. ⚠️ {challenge}\n"
        else:
            md += "无重大挑战\n"
        
        md += "\n### 解决方案\n\n"
        if report['execution']['solutions']:
            for i, solution in enumerate(report['execution']['solutions'], 1):
                md += f"{i}. ✅ {solution}\n"
        else:
            md += "无需特殊解决方案\n"
        
        md += f"""
---

## 📊 统计指标

| 指标 | 数值 |
|------|------|
| Token 用量 | {report['metrics']['token_usage']:,} |
| API 调用次数 | {report['metrics']['api_calls']} |
| 修改文件数 | {report['metrics']['files_modified']} |

---

## 💡 经验教训

### 学到的经验

"""
        if report['learnings']['lessons_learned']:
            for lesson in report['learnings']['lessons_learned']:
                md += f"- {lesson}\n"
        else:
            md += "暂无\n"
        
        md += "\n### 下一步行动\n\n"
        if report['learnings']['next_steps']:
            for step in report['learnings']['next_steps']:
                md += f"- [ ] {step}\n"
        else:
            md += "无\n"
        
        md += """
---

## 📁 存档信息

**报告存储位置**: `""" + str(report.get('report_path', 'N/A')) + "/" + str(report.get('report_filename', 'N/A')) + """`

**文件列表**:
- `{report['report_filename']}.md` - Markdown 格式报告
- `{report['report_filename']}.json` - JSON 格式报告

---

*Generated by TaskReportAgent v1.0.0*
"""
        return md


if __name__ == "__main__":
    # 测试样例
    agent = TaskReportAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "task_name": "集成 awesome-design-md 设计系统",
        "task_description": "研究并集成 Linear 设计系统到监控面板",
        "start_time": "2026-04-09T22:00:00",
        "status": "completed",
        "steps_taken": [
            "浏览 skills.sh 网站",
            "研究 awesome-design-md 项目",
            "获取 Linear 设计令牌",
            "更新 Tailwind 配置",
            "创建演示页面",
            "提交到 Git"
        ],
        "artifacts_created": [
            "monitor_dashboard/frontend/tailwind.config.js",
            "monitor_dashboard/frontend/src/index.css",
            "monitor_dashboard/demo-linear.html",
            "skills/design-md-skill/"
        ],
        "challenges": [
            "GitHub 路径结构变化",
            "浏览器暂时不可用"
        ],
        "solutions": [
            "手动创建 Linear 设计令牌",
            "使用备用方式启动服务"
        ],
        "metrics": {
            "token_usage": 15000,
            "api_calls": 25,
            "files_modified": 7
        },
        "lessons_learned": [
            "Linear 设计系统非常适合开发者工具",
            "深色主题需要精细的阴影处理",
            "设计令牌应该集中管理"
        ],
        "next_steps": [
            "添加更多设计系统支持",
            "实现设计系统切换功能",
            "优化移动端显示"
        ]
    }
    
    result = agent.run(test_input)
    print(f"✅ 报告已生成：{result}")
    print(f"📁 存储位置：{result.get('report_path')}")
