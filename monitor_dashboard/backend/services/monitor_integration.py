#!/usr/bin/env python3
"""
Monitor Integration - 工作流与监控面板的集成模块

功能：
- 自动向监控 API 报告 agent 状态
- 记录 token 用量
- 更新工作流进度
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import urllib.request
import urllib.error

MONITOR_API_BASE = os.environ.get("MONITOR_API_BASE", "http://localhost:8001")


class MonitorReporter:
    """监控报告器"""
    
    def __init__(self, api_base: str = MONITOR_API_BASE):
        self.api_base = api_base
    
    def _post(self, endpoint: str, data: dict) -> Optional[dict]:
        """发送 POST 请求"""
        try:
            req = urllib.request.Request(
                f"{self.api_base}{endpoint}",
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"[Monitor] 报告失败：{e}")
            return None
    
    def report_agent_status(
        self,
        agent_name: str,
        stage: str,
        status: str,
        current_task: str = None,
        token_usage: int = 0,
        message_count: int = 0,
    ):
        """报告 agent 状态"""
        data = {
            "name": agent_name,
            "stage": stage,
            "status": status,
            "current_task": current_task,
            "start_time": datetime.now().isoformat() if status == "running" else None,
            "end_time": datetime.now().isoformat() if status in ["completed", "error"] else None,
            "token_usage": token_usage,
            "message_count": message_count,
        }
        return self._post(f"/api/agents/{agent_name}/update", data)
    
    def record_token_usage(
        self,
        agent_name: str,
        input_tokens: int,
        output_tokens: int,
        estimated_cost: float = 0.0,
    ):
        """记录 token 用量"""
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "agent_name": agent_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "estimated_cost": estimated_cost,
        }
        return self._post("/api/tokens/record", data)
    
    def start_workflow(self, run_id: str, project_name: str):
        """标记工作流开始"""
        # 可以通过更新项目状态来实现
        pass
    
    def complete_stage(self, run_id: str, stage_name: str, artifacts: list):
        """标记阶段完成"""
        # 可以通过更新项目状态来实现
        pass


# 装饰器：自动报告 agent 状态
def monitor_agent(agent_class):
    """装饰器：为 agent 添加监控报告功能"""
    original_execute = agent_class.execute
    
    def monitored_execute(self, input_data: dict):
        reporter = MonitorReporter()
        
        # 报告开始
        reporter.report_agent_status(
            agent_name=self.AGENT_NAME,
            stage=self.STAGE_NAME,
            status="running",
            current_task="执行中...",
        )
        
        try:
            # 执行原方法
            result = original_execute(self, input_data)
            
            # 报告完成
            reporter.report_agent_status(
                agent_name=self.AGENT_NAME,
                stage=self.STAGE_NAME,
                status="completed",
                token_usage=getattr(self, '_last_token_usage', 0),
                message_count=getattr(self, '_last_message_count', 0),
            )
            
            return result
        except Exception as e:
            # 报告错误
            reporter.report_agent_status(
                agent_name=self.AGENT_NAME,
                stage=self.STAGE_NAME,
                status="error",
                current_task=str(e),
            )
            raise
    
    agent_class.execute = monitored_execute
    return agent_class


# 上下文管理器：记录 token 用量
class track_tokens:
    """上下文管理器：追踪并报告 token 用量"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.reporter = MonitorReporter()
        self.input_tokens = 0
        self.output_tokens = 0
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.input_tokens > 0 or self.output_tokens > 0:
            self.reporter.record_token_usage(
                agent_name=self.agent_name,
                input_tokens=self.input_tokens,
                output_tokens=self.output_tokens,
                estimated_cost=(self.input_tokens + self.output_tokens) * 0.000002,  # 假设价格
            )
    
    def record(self, input_tokens: int, output_tokens: int):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


# 便捷函数
def report_status(agent_name: str, stage: str, status: str, **kwargs):
    """快速报告状态"""
    reporter = MonitorReporter()
    return reporter.report_agent_status(agent_name, stage, status, **kwargs)


def record_usage(agent_name: str, input_tokens: int, output_tokens: int):
    """快速记录用量"""
    reporter = MonitorReporter()
    return reporter.record_token_usage(agent_name, input_tokens, output_tokens)
