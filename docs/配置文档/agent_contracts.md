# Agent 合同说明

每个 Agent 必须遵守以下合同（Contract）。

## 基础合同

### 必须定义的属性

```python
AGENT_NAME: str       # Agent 名称
STAGE_NAME: str       # 阶段名称
ROLE_DESCRIPTION: str # 角色描述
INPUT_FILES: List[str]  # 输入文件列表
OUTPUT_FILES: List[str] # 输出文件列表
```

### 必须实现的方法

```python
def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行 Agent 任务
    
    Args:
        input_data: 输入数据字典
        
    Returns:
        输出数据字典，key 对应 OUTPUT_FILES 的文件名（不含扩展名）
    """
    pass
```

## 输入输出约定

### 输入文件命名
- Markdown: `{stage_name}.md`
- JSON: `{stage_name}.json`

### 输出文件命名
- Markdown: `{stage_name}.md`
- JSON: `{stage_name}.json`

### 数据格式
- JSON 输出必须是有效的 JSON 对象
- Markdown 输出应包含标题和结构化内容

## 各 Agent 详细合同

### ProblemDefinitionAgent

**职责**: 从原始简报提炼问题定义

**输入**:
- `raw_brief` (str): 用户原始输入

**输出**:
- `problem_definition.md`: 问题定义报告
- `structured_problem_definition.json`: 结构化问题定义

**JSON Schema**:
```json
{
  "target_users": ["string"],
  "core_problem": "string",
  "use_scenarios": ["string"],
  "existing_alternatives": ["string"],
  "priority_reason": "string",
  "success_criteria": ["string"],
  "assumptions": ["string"],
  "risks": ["string"]
}
```

### MVPScopeAgent

**职责**: 定义 MVP 范围

**输入**:
- `structured_problem_definition.json`

**输出**:
- `mvp_scope.md`: 范围定义报告
- `mvp_scope.json`: 结构化范围

**JSON Schema**:
```json
{
  "must_have": ["string"],
  "nice_to_have": ["string"],
  "out_of_scope": ["string"],
  "acceptance_criteria": ["string"],
  "constraints": ["string"],
  "timeline_estimate": "string"
}
```

### ContextPackAgent

**职责**: 整理上下文任务包

**输入**:
- `mvp_scope.json`

**输出**:
- `context_pack.md`: 上下文包报告
- `context_pack.json`: 结构化上下文

**JSON Schema**:
```json
{
  "project_goals": ["string"],
  "recommended_tech_stack": {
    "frontend": ["string"],
    "backend": ["string"],
    "database": ["string"],
    "deployment": ["string"]
  },
  "resources_needed": ["string"],
  "constraints": ["string"],
  "forbidden_practices": ["string"],
  "recommended_order": ["string"],
  "key_decisions": ["string"]
}
```

### MainlineBuildAgent

**职责**: 设计并实现主链路

**输入**:
- `context_pack.json`

**输出**:
- `implementation_plan.md`: 实现计划
- `architecture.json`: 架构设计
- 代码骨架文件

**JSON Schema**:
```json
{
  "project_structure": {},
  "modules": [{"name": "string", "responsibility": "string", "interface": "string"}],
  "api_endpoints": [{"method": "string", "path": "string", "description": "string"}],
  "data_models": [{"name": "string", "fields": ["string"]}]
}
```

### QualityCorrectionAgent

**职责**: 分析质量问题并给出修复方案

**输入**:
- `implementation_plan.md`
- `test_results.json` (可选)

**输出**:
- `issue_analysis.md`: 问题分析报告
- `fix_plan.json`: 修复计划

**JSON Schema**:
```json
{
  "fixes": [{
    "issue_id": "string",
    "priority": "number",
    "action": "string",
    "approach": "string",
    "estimate": "string",
    "test_required": "boolean"
  }],
  "total_estimate": "string",
  "recommendation": "string"
}
```

### ProductizationAgent

**职责**: 整理交付材料

**输入**:
- `architecture.json`
- `fix_plan.json`

**输出**:
- `delivery_summary.md`: 交付总结
- `runbook.md`: 部署说明
- `demo_script.md`: 演示脚本
- `known_issues.md`: 已知问题清单

### RetrospectiveAgent

**职责**: 复盘和规划下一轮迭代

**输入**:
- `delivery_summary.md`
- `known_issues.md`

**输出**:
- `retrospective.md`: 复盘报告
- `next_iteration_plan.json`: 下一轮计划

**JSON Schema**:
```json
{
  "iteration": "string",
  "timeline": "string",
  "goals": ["string"],
  "features": [{
    "name": "string",
    "priority": "number",
    "estimate": "string",
    "description": "string"
  }],
  "metrics": {},
  "risks": ["string"],
  "dependencies": ["string"]
}
```

## 测试要求

每个 Agent 必须包含：
1. `__main__` 测试入口
2. 最小测试样例
3. 可独立运行验证

## 扩展示例

创建新 Agent 的步骤：

```python
from agents import AgentBase

class NewAgent(AgentBase):
    AGENT_NAME = "NewAgent"
    STAGE_NAME = "new_stage"
    ROLE_DESCRIPTION = "新 Agent 的角色描述"
    INPUT_FILES = ["previous_stage_output.json"]
    OUTPUT_FILES = ["new_output.md", "new_output.json"]
    
    def execute(self, input_data: Dict) -> Dict:
        # 实现逻辑
        return {
            "new_output": {"key": "value"},
            "new_output": "# Markdown content"
        }
```

然后在 `AGENT_MAP` 中注册。
