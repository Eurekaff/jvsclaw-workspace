#!/usr/bin/env python3
"""
Agent 工作流监控面板 - 后端服务

功能：
- 实时 agent 状态监控
- Token 用量统计
- 工作流可视化数据
- 历史记录查询
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path
import os

app = FastAPI(title="Agent Workflow Monitor API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Data Models ====================

class AgentStatus(BaseModel):
    name: str
    stage: str
    status: str  # idle, running, completed, error
    current_task: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    token_usage: int = 0
    message_count: int = 0

class WorkflowStage(BaseModel):
    name: str
    status: str  # pending, running, completed, skipped
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    artifacts: List[str] = []

class WorkflowRun(BaseModel):
    run_id: str
    project_name: str
    status: str
    current_stage: str
    created_at: str
    updated_at: str
    stages: List[WorkflowStage]
    total_tokens: int = 0
    total_messages: int = 0

class TokenUsage(BaseModel):
    date: str
    agent_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: float

class DashboardSummary(BaseModel):
    total_runs: int
    active_runs: int
    completed_runs: int
    total_agents: int
    active_agents: int
    total_tokens_today: int
    estimated_cost_today: float
    recent_runs: List[WorkflowRun]

# ==================== In-Memory Store ====================

# 实际应该用数据库，这里用内存存储演示
agent_statuses: Dict[str, AgentStatus] = {}
workflow_runs: Dict[str, WorkflowRun] = {}
token_usage_history: List[TokenUsage] = []

# ==================== Services ====================

def scan_workflow_runs() -> List[WorkflowRun]:
    """扫描 artifacts/runs 目录获取工作流运行记录"""
    runs_dir = Path("/home/admin/openclaw/workspace/artifacts/runs")
    runs = []
    
    if not runs_dir.exists():
        return runs
    
    for run_dir in runs_dir.iterdir():
        if run_dir.is_dir():
            state_file = run_dir / "project_state.json"
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # 转换为 WorkflowRun
                stages = []
                for artifact_key, artifact_info in state.get("artifacts_index", {}).items():
                    stage_name = artifact_key.split("/")[0]
                    if not any(s.name == stage_name for s in stages):
                        stages.append(WorkflowStage(
                            name=stage_name,
                            status="completed" if artifact_info.get("status") == "approved" else "running",
                            completed_at=artifact_info.get("created_at"),
                            artifacts=[artifact_key]
                        ))
                
                run = WorkflowRun(
                    run_id=run_dir.name,
                    project_name=state.get("project_name", "Unknown"),
                    status="completed" if state.get("current_stage") == "completed" else "running",
                    current_stage=state.get("current_stage", "unknown"),
                    created_at=state.get("metadata", {}).get("created_at", ""),
                    updated_at=state.get("metadata", {}).get("updated_at", ""),
                    stages=stages,
                    total_tokens=0,  # 需要从日志中统计
                    total_messages=0
                )
                runs.append(run)
    
    return sorted(runs, key=lambda x: x.created_at, reverse=True)

def scan_agent_status() -> Dict[str, AgentStatus]:
    """扫描当前 agent 状态"""
    # 从 sessions 或其他地方获取 agent 状态
    # 这里是示例实现
    agents_dir = Path("/home/admin/openclaw/workspace/agents")
    statuses = {}
    
    if agents_dir.exists():
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith("_"):
                agent_name = f"{agent_dir.name}_agent"
                statuses[agent_name] = AgentStatus(
                    name=agent_name,
                    stage=agent_dir.name,
                    status="idle",
                    token_usage=0,
                    message_count=0
                )
    
    return statuses

# ==================== API Endpoints ====================

@app.get("/api/dashboard", response_model=DashboardSummary)
def get_dashboard_summary():
    """获取仪表板摘要"""
    runs = scan_workflow_runs()
    agent_statuses = scan_agent_status()
    
    # 统计今天的 token 用量
    today = datetime.now().strftime("%Y-%m-%d")
    today_tokens = sum(t.total_tokens for t in token_usage_history if t.date == today)
    today_cost = sum(t.estimated_cost for t in token_usage_history if t.date == today)
    
    return DashboardSummary(
        total_runs=len(runs),
        active_runs=len([r for r in runs if r.status == "running"]),
        completed_runs=len([r for r in runs if r.status == "completed"]),
        total_agents=len(agent_statuses),
        active_agents=len([a for a in agent_statuses.values() if a.status == "running"]),
        total_tokens_today=today_tokens,
        estimated_cost_today=today_cost,
        recent_runs=runs[:10]
    )

@app.get("/api/workflows", response_model=List[WorkflowRun])
def list_workflows(limit: int = 20, status: str = None):
    """获取工作流列表"""
    runs = scan_workflow_runs()
    
    if status:
        runs = [r for r in runs if r.status == status]
    
    return runs[:limit]

@app.get("/api/workflows/{run_id}", response_model=WorkflowRun)
def get_workflow(run_id: str):
    """获取单个工作流详情"""
    runs = scan_workflow_runs()
    for run in runs:
        if run.run_id == run_id:
            return run
    raise HTTPException(status_code=404, detail="Workflow not found")

@app.get("/api/agents", response_model=List[AgentStatus])
def list_agents():
    """获取所有 agent 状态"""
    return list(scan_agent_status().values())

@app.get("/api/agents/{agent_name}", response_model=AgentStatus)
def get_agent(agent_name: str):
    """获取单个 agent 状态"""
    agents = scan_agent_status()
    if agent_name in agents:
        return agents[agent_name]
    raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/api/tokens", response_model=List[TokenUsage])
def get_token_usage(days: int = 7, agent_name: str = None):
    """获取 token 用量统计"""
    # 实际应该从数据库查询
    return token_usage_history[-days*24:] if not agent_name else [
        t for t in token_usage_history[-days*24:] if t.agent_name == agent_name
    ]

@app.post("/api/agents/{agent_name}/update")
def update_agent_status(agent_name: str, status: AgentStatus):
    """更新 agent 状态（用于 agent 自我报告）"""
    agent_statuses[agent_name] = status
    return {"status": "ok"}

@app.post("/api/tokens/record")
def record_token_usage(usage: TokenUsage):
    """记录 token 用量"""
    token_usage_history.append(usage)
    return {"status": "ok"}

@app.get("/api/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
