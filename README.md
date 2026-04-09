# 项目总览 - Agent 工作流系统

## 🎯 项目目标

构建一个**自驱动、可监控、可扩展**的多 Agent 工程工作流系统，将软件项目从想法自动推进到可交付状态。

## 📦 核心组件

### 1. 工作流引擎 (`workflows/`)

```
workflows/
├── engineering_lifecycle_workflow.py  # 主工作流编排器
├── run_workflow.py                    # 运行脚本
└── README.md
```

**7 个核心阶段:**
```
idea → problem_definition → mvp_scope → context_pack → 
mainline_build → quality_correction → productization → retrospective
```

### 2. Agent 系统 (`agents/`)

```
agents/
├── problem_definition/     # 问题定义 Agent
├── mvp_scope/              # MVP 范围 Agent
├── context_pack/           # 上下文包 Agent
├── mainline_build/         # 主链路构建 Agent
├── quality_correction/     # 质量校正 Agent
├── productization/         # 产品化 Agent
├── retrospective/          # 复盘 Agent
└── github_research/        # GitHub 调研 Agent (新增)
```

### 3. 监控面板 (`monitor_dashboard/`)

```
monitor_dashboard/
├── backend/                # FastAPI 后端
│   ├── app/main.py        # API 服务
│   └── services/
│       └── monitor_integration.py  # 工作流集成
├── frontend/               # React 前端
│   └── src/
│       ├── pages/         # 5 个页面
│       ├── services/      # API 调用
│       └── store/         # 状态管理
└── docker-compose.yml     # 一键部署
```

**功能:**
- 📊 实时仪表板
- 🔄 工作流可视化
- 💰 Token 用量统计
- 🤖 Agent 状态监控
- 📈 历史趋势分析

## 🚀 快速开始

### 启动工作流

```bash
# 运行示例
python3 workflows/run_workflow.py --example

# 新项目
python3 workflows/run_workflow.py --brief "你的项目想法"
```

### 启动监控面板

```bash
# 方式 1: 快速启动脚本
./scripts/start-monitor.sh

# 方式 2: Docker Compose
cd monitor_dashboard && docker-compose up -d
```

访问：http://localhost:3000

### 集成监控到 Agent

```python
from monitor_dashboard.backend.services.monitor_integration import monitor_agent

@monitor_agent
class MyAgent(AgentBase):
    def execute(self, input_data):
        # 自动报告状态
        return result
```

## 📊 当前能力

| 能力 | 状态 | 说明 |
|------|------|------|
| 问题定义 | ✅ | 从想法提炼问题 |
| MVP 范围 | ✅ | 定义最小可交付范围 |
| 技术规划 | ✅ | 推荐技术栈和架构 |
| 代码骨架 | ✅ | 生成项目骨架 |
| 质量分析 | ✅ | 问题识别和修复建议 |
| 交付材料 | ✅ | 文档和部署说明 |
| 复盘迭代 | ✅ | 总结和下一轮计划 |
| 实时监控 | ✅ | Agent 状态和 Token 用量 |
| GitHub 调研 | ✅ | 开源项目分析 |
| 代码生成 | 🟡 | 骨架级别 |
| 自动测试 | 🟡 | 框架就绪 |
| 自动部署 | 🟡 | 配置就绪 |

## 📁 目录结构

```
workspace/
├── agents/                 # Agent 实现
├── workflows/              # 工作流编排
├── schemas/                # JSON Schema
├── prompts/                # Prompt 模板
├── monitor_dashboard/      # 监控面板
├── artifacts/              # 产出物
│   └── runs/              # 每次运行结果
├── docs/                   # 文档
│   ├── workflow_overview.md
│   ├── agent_contracts.md
│   ├── usage_guide.md
│   └── self_iteration_plan.md
├── tests/                  # 测试
└── scripts/                # 脚本
```

## 🔌 扩展指南

### 新增 Agent

1. 创建目录：`agents/my_agent/`
2. 继承基类：
```python
from agents import AgentBase

class MyAgent(AgentBase):
    AGENT_NAME = "MyAgent"
    STAGE_NAME = "my_stage"
    def execute(self, input_data):
        return {"output": "result"}
```
3. 在 `AGENT_MAP` 中注册

### 新增监控指标

1. 在 `backend/app/main.py` 添加数据模型
2. 添加 API 端点
3. 在 `frontend/src/pages/` 创建页面

### 自定义工作流

修改 `workflows/engineering_lifecycle_workflow.py`:
- 调整 `STAGES` 列表
- 修改阶段流转逻辑

## 📖 文档索引

| 文档 | 说明 |
|------|------|
| `workflows/README.md` | 工作流使用说明 |
| `docs/workflow_overview.md` | 工作流概览 |
| `docs/agent_contracts.md` | Agent 合同规范 |
| `docs/usage_guide.md` | 使用指南 |
| `docs/self_iteration_plan.md` | 自我迭代计划 |
| `monitor_dashboard/README.md` | 监控面板文档 |

## 🛠️ 技术栈

**工作流引擎:**
- Python 3.10+
- FastAPI (可选集成)

**监控面板:**
- Backend: FastAPI, Pydantic
- Frontend: React, TanStack Query, Zustand, Recharts
- Styling: TailwindCSS
- Deploy: Docker, Docker Compose

**开发工具:**
- Git + GitHub
- Docker
- Vite

## 📈 发展路线

### Phase 1 (已完成) ✅
- [x] 7 个核心 Agent
- [x] 工作流编排器
- [x] 监控面板 MVP
- [x] GitHub 调研 Agent

### Phase 2 (进行中) 🚧
- [ ] WebSocket 实时推送
- [ ] 告警系统
- [ ] 数据库持久化

### Phase 3 (计划中) 📋
- [ ] CodeGenerationAgent
- [ ] TestGenerationAgent
- [ ] DeploymentAgent
- [ ] 并行执行支持

### Phase 4 (愿景) 🔮
- [ ] Web UI 工作流编辑器
- [ ] 自然语言交互
- [ ] 自主学习和优化

## 🎓 学习资源

- **工作流设计**: `docs/workflow_overview.md`
- **Agent 开发**: `docs/agent_contracts.md`
- **监控集成**: `monitor_dashboard/README.md`
- **示例项目**: `artifacts/runs/<run_id>/`

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 📄 License

MIT

---

**最后更新**: 2026-04-09  
**版本**: v0.2.0  
**状态**: 🟢 活跃开发中
