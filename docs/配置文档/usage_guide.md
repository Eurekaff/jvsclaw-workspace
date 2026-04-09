# 使用指南

## 快速开始

### 1. 运行示例

```bash
cd /home/admin/openclaw/workspace
python3 workflows/run_workflow.py --example
```

这会运行一个完整的企业查册系统示例，产出所有阶段的文件。

### 2. 启动新项目

```bash
python3 workflows/run_workflow.py --brief "你的项目想法"
```

### 3. 从中间阶段恢复

```bash
# 查看已有运行
ls artifacts/runs/

# 恢复指定运行
python3 workflows/run_workflow.py --resume 20260409_151300
```

## 目录结构

```
workspace/
├── agents/                      # Agent 实现
│   ├── __init__.py             # Agent 基类
│   ├── problem_definition/     # 问题定义 Agent
│   ├── mvp_scope/              # MVP 范围 Agent
│   └── ...
├── workflows/                   # 工作流编排
│   ├── engineering_lifecycle_workflow.py  # 主工作流
│   ├── run_workflow.py         # 运行脚本
│   └── README.md
├── schemas/                     # JSON Schema 定义
├── prompts/                     # Prompt 模板
├── artifacts/                   # 产出物
│   ├── runs/                   # 每次运行的产出
│   └── examples/               # 示例产出
├── tests/                       # 测试
└── docs/                        # 文档
```

## 产出物说明

每次运行会在 `artifacts/runs/<run_id>/` 生成：

```
<run_id>/
├── project_state.json          # 项目状态
├── raw_brief.md                # 原始简报
├── problem_definition.md       # 问题定义
├── structured_problem_definition.json
├── mvp_scope.md               # MVP 范围
├── mvp_scope.json
├── context_pack.md            # 上下文包
├── context_pack.json
├── implementation_plan.md     # 实现计划
├── architecture.json          # 架构设计
├── backend/                   # 代码骨架
├── frontend/
├── docker-compose.yml
├── issue_analysis.md          # 问题分析
├── fix_plan.json
├── delivery_summary.md        # 交付总结
├── runbook.md                 # 部署说明
├── demo_script.md             # 演示脚本
├── known_issues.md            # 已知问题
├── retrospective.md           # 复盘报告
└── next_iteration_plan.json   # 下一轮计划
```

## 编程接口

### Python API

```python
from workflows.engineering_lifecycle_workflow import WorkflowOrchestrator

# 创建编排器
orchestrator = WorkflowOrchestrator("/path/to/workspace")

# 启动新工作流
state = orchestrator.start("项目想法", "项目名称")

# 运行单个阶段
orchestrator.run_stage("problem_definition")

# 运行完整工作流
final_state = orchestrator.run_full_workflow(
    raw_brief="项目想法",
    project_name="项目名称"
)

# 获取状态
status = orchestrator.get_status()
```

### 恢复运行

```python
# 恢复已有运行
orchestrator.resume("20260409_151300")

# 继续执行下一阶段
current_stage = orchestrator.state["current_stage"]
# ... 执行下一阶段
```

## 自定义 Agent

### 创建新 Agent

1. 创建目录：
```bash
mkdir agents/new_stage
```

2. 创建 `agents/new_stage/agent.py`:
```python
from agents import AgentBase

class NewStageAgent(AgentBase):
    AGENT_NAME = "NewStageAgent"
    STAGE_NAME = "new_stage"
    ROLE_DESCRIPTION = "角色描述"
    INPUT_FILES = ["input.json"]
    OUTPUT_FILES = ["output.md", "output.json"]
    
    def execute(self, input_data):
        # 实现逻辑
        return {"output": {...}}
```

3. 在 `workflows/engineering_lifecycle_workflow.py` 中注册:
```python
from agents.new_stage.agent import NewStageAgent

AGENT_MAP["new_stage"] = NewStageAgent
STAGES.append("new_stage")  # 或插入到合适位置
```

### 自定义 Prompt

在 `prompts/` 目录创建 `{stage_name}_prompt.md`。

## 集成 LLM

当前实现使用简化的启发式逻辑。要集成真实 LLM：

1. 在每个 Agent 的 `execute()` 方法中调用 LLM
2. 使用 `prompts/` 中的模板
3. 解析 LLM 返回的结构化输出

示例：
```python
def execute(self, input_data):
    prompt = self.load_prompt()
    prompt = prompt.replace("{{input}}", json.dumps(input_data))
    
    # 调用 LLM
    response = call_llm(prompt)
    
    # 解析输出
    result = parse_llm_response(response)
    
    return result
```

## 调试技巧

### 查看日志

```bash
# 查看运行日志
tail -f artifacts/runs/<run_id>/project_state.json
```

### 单步执行

```python
orchestrator = WorkflowOrchestrator("/path/to/workspace")
orchestrator.start("想法", "项目")

# 逐个阶段执行
orchestrator.run_stage("problem_definition")
input()  # 暂停，检查输出
orchestrator.run_stage("mvp_scope")
```

### 检查状态

```python
print(orchestrator.get_status())
print(orchestrator.state["artifacts_index"])
```

## 常见问题

### Q: 如何跳过某个阶段？
A: 修改 `STAGES` 列表，或使用 `start_from` 参数。

### Q: 如何修改产出物格式？
A: 修改对应 Agent 的 `OUTPUT_FILES` 和 `execute()` 方法。

### Q: 如何添加人工确认点？
A: 在 `run_stage()` 方法中添加确认逻辑，设置 `auto_approve=False`。

### Q: 产出物在哪里？
A: `artifacts/runs/<run_id>/` 目录。

## 下一步

- 集成真实 LLM 调用
- 添加 Web UI
- 支持并行执行
- 添加更多 Agent（测试、部署等）
