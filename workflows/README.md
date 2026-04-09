# Multi-Agent Engineering Lifecycle Workflow

一个面向 vibe coding 的多 agent 工程工作流系统，用于将软件项目从想法推进到可验证、可交付、可复盘的状态。

## 核心特性

- **生命周期驱动**：显式区分项目阶段，每轮只推进一个阶段
- **产物驱动**：每个 agent 有明确输入/输出/完成标准
- **可中断、可检查、可重入**：任一阶段完成后留下中间产物
- **人类确认点**：关键节点保留人工修订能力

## 快速开始

```bash
# 运行示例工作流
python3 workflows/run_workflow.py --example

# 从原始想法启动
python3 workflows/run_workflow.py --brief "你的项目想法"

# 从指定阶段恢复
python3 workflows/run_workflow.py --resume --stage mvp_scope
```

## 目录结构

```
workspace/
├── agents/              # 7 个核心 agent
├── workflows/           # 编排层
├── schemas/             # 数据结构定义
├── prompts/             # prompt 模板
├── artifacts/           # 产出物
├── tests/               # 测试
└── docs/                # 文档
```

## 主流程

```
idea_input → problem_definition → mvp_scope → context_pack → 
mainline_build → quality_correction → productization → retrospective
```

详细文档见 `docs/` 目录。
