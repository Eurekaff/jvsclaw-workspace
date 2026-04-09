# 工作流概览

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Orchestrator                    │
│  - 管理 ProjectState                                        │
│  - 定义阶段流转                                             │
│  - 保存中间产物                                             │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Problem     │    │    MVP        │    │   Context     │
│ Definition    │ →  │    Scope      │ →  │    Pack       │
│   Agent       │    │    Agent      │    │    Agent      │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Mainline     │    │   Quality     │    │  Producti-    │
│    Build      │ →  │  Correction   │ →  │   zation      │
│    Agent      │    │    Agent      │    │    Agent      │
└───────────────┘    └───────────────┘    └───────────────┘
                              │
                              ▼
                     ┌───────────────┐
                     │ Retrospective │
                     │    Agent      │
                     └───────────────┘
```

## 阶段流转

```
idea_input → problem_definition → mvp_scope → context_pack → 
mainline_build → quality_correction → productization → retrospective → completed
```

## 核心概念

### ProjectState
全局状态对象，贯穿整个工作流生命周期，包含：
- 项目基本信息
- 当前阶段
- 产出物索引
- 待确认问题
- 验证结果

### Agent
每个阶段对应一个 Agent，负责：
- 接收输入（前置阶段产出）
- 执行特定任务
- 生成结构化输出

### Artifact
每个阶段的产出物，包括：
- Markdown 文档（人类可读）
- JSON 数据（机器可读）
- 代码文件（如适用）

## 使用场景

### 场景 1: 从想法启动
```bash
python3 workflows/run_workflow.py --brief "你的项目想法"
```

### 场景 2: 运行示例
```bash
python3 workflows/run_workflow.py --example
```

### 场景 3: 从中间阶段恢复
```bash
python3 workflows/run_workflow.py --resume <run_id>
```

## 扩展方式

### 新增 Agent
1. 在 `agents/` 创建新目录
2. 继承 `AgentBase` 类
3. 实现 `execute()` 方法
4. 在 `AGENT_MAP` 中注册

### 新增阶段
1. 创建新的 Agent
2. 在 `STAGES` 列表中添加到合适位置
3. 定义输入输出文件

详见 `docs/agent_contracts.md`
