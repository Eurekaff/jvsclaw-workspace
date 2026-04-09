#!/usr/bin/env python3
"""
GitHubResearchAgent - GitHub 项目调研 agent

职责：
- 根据项目需求搜索 GitHub 上的相关项目
- 分析热门项目的技术栈、架构、实现模式
- 提取可参考的设计模式和最佳实践
- 生成调研报告和推荐方案

输出：
- github_research.md - 调研报告
- github_recommendations.json - 推荐方案
"""

import json
from typing import Any, Dict, List
from agents import AgentBase


class GitHubResearchAgent(AgentBase):
    AGENT_NAME = "GitHubResearchAgent"
    STAGE_NAME = "github_research"
    ROLE_DESCRIPTION = "技术调研专家，擅长分析 GitHub 项目并提供可参考的实现方案"
    
    INPUT_FILES = ["context_pack.json"]
    OUTPUT_FILES = ["github_research.md", "github_recommendations.json"]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context_pack = input_data.get("context_pack", {})
        tech_stack = context_pack.get("recommended_tech_stack", {})
        
        # 生成调研结果（简化实现，实际应调用 GitHub API）
        research = self._generate_research(tech_stack)
        
        # 生成 markdown 报告
        md_content = self._generate_markdown(research)
        
        return {
            "github_research.md": md_content,
            "github_recommendations.json": research
        }
    
    def _generate_research(self, tech_stack: Dict) -> Dict:
        """生成调研报告"""
        return {
            "search_queries": [
                "fastapi react dashboard template",
                "agent workflow orchestration",
                "workflow monitoring dashboard",
                "fastapi realtime monitoring",
            ],
            "recommended_projects": [
                {
                    "name": "fastapi-dashboard-template",
                    "url": "https://github.com/example/fastapi-dashboard",
                    "stars": 1200,
                    "tech_stack": ["FastAPI", "React", "TailwindCSS"],
                    "key_features": [
                        "实时数据更新",
                        "可复用的图表组件",
                        "Docker 部署配置"
                    ],
                    "reference_points": [
                        "后端 API 结构设计",
                        "前端状态管理方案",
                        "Docker Compose 配置"
                    ]
                },
                {
                    "name": "workflow-orchestrator",
                    "url": "https://github.com/example/workflow-orchestrator",
                    "stars": 850,
                    "tech_stack": ["Python", "PostgreSQL", "Redis"],
                    "key_features": [
                        "DAG 工作流定义",
                        "任务重试机制",
                        "进度追踪"
                    ],
                    "reference_points": [
                        "工作流状态管理",
                        "任务队列设计",
                        "错误处理模式"
                    ]
                },
                {
                    "name": "agent-monitoring-system",
                    "url": "https://github.com/example/agent-monitor",
                    "stars": 620,
                    "tech_stack": ["FastAPI", "Vue3", "WebSocket"],
                    "key_features": [
                        "实时 Agent 状态推送",
                        "Token 用量统计",
                        "历史数据分析"
                    ],
                    "reference_points": [
                        "WebSocket 实时通信",
                        "数据聚合查询",
                        "可视化图表实现"
                    ]
                }
            ],
            "design_patterns": [
                {
                    "name": "Repository Pattern",
                    "description": "数据访问层抽象",
                    "applicable_to": ["数据模型管理", "数据库操作"],
                    "example": "backend/models/*.py"
                },
                {
                    "name": "Observer Pattern",
                    "description": "状态变更通知",
                    "applicable_to": ["Agent 状态更新", "工作流进度推送"],
                    "example": "WebSocket 广播"
                },
                {
                    "name": "Factory Pattern",
                    "description": "动态创建 Agent 实例",
                    "applicable_to": ["Agent 注册和加载"],
                    "example": "AGENT_MAP 工厂"
                }
            ],
            "best_practices": [
                "使用 Docker Compose 统一管理开发环境",
                "前后端分离，通过 API 通信",
                "使用 Zustand 进行轻量级状态管理",
                "实现健康检查端点",
                "添加 CORS 中间件支持跨域",
                "使用 Pydantic 进行数据验证"
            ],
            "warnings": [
                "避免在前端存储敏感信息",
                "生产环境需要添加认证和授权",
                "大规模数据需要数据库而非内存存储",
                "实时通信考虑使用 WebSocket 而非轮询"
            ]
        }
    
    def _generate_markdown(self, research: Dict) -> str:
        """生成 markdown 格式"""
        md = f"""# GitHub 调研报告

## 搜索关键词
{chr(10).join(f'- `{q}`' for q in research['search_queries'])}

## 推荐参考项目

"""
        for i, project in enumerate(research['recommended_projects'], 1):
            md += f"""
### {i}. {project['name']}

- **URL**: {project['url']}
- **Stars**: ⭐ {project['stars']}
- **技术栈**: {', '.join(project['tech_stack'])}

**核心功能**:
{chr(10).join(f'- {f}' for f in project['key_features'])}

**可参考点**:
{chr(10).join(f'- {p}' for p in project['reference_points'])}

---
"""
        
        md += """
## 设计模式推荐

"""
        for pattern in research['design_patterns']:
            md += f"""
### {pattern['name']}

- **描述**: {pattern['description']}
- **适用场景**: {', '.join(pattern['applicable_to'])}
- **示例**: `{pattern['example']}`

"""
        
        md += f"""
## 最佳实践

{chr(10).join(f'✅ {p}' for p in research['best_practices'])}

## 注意事项

{chr(10).join(f'⚠️ {w}' for w in research['warnings'])}

---
*Generated by GitHubResearchAgent*
"""
        return md


if __name__ == "__main__":
    agent = GitHubResearchAgent("/home/admin/openclaw/workspace")
    test_input = {
        "context_pack": {
            "recommended_tech_stack": {
                "frontend": ["React", "TailwindCSS"],
                "backend": ["Python", "FastAPI"]
            }
        }
    }
    result = agent.run(test_input)
    print(f"Generated files: {result}")
