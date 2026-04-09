# Agent 工作流监控面板

实时监控 Agent 执行状态、Token 用量和工作流进度的可视化面板。

## 功能特性

- 📊 **实时仪表板** - 概览所有运行中的工作流和 Agent 状态
- 🔄 **工作流可视化** - 图形化展示工作流各阶段进度
- 💰 **Token 用量监测** - 统计和可视化 token 消耗及成本
- 🤖 **Agent 状态** - 查看每个 Agent 的实时工作状态
- 📈 **历史趋势** - 分析 token 用量和工作流执行趋势
- 🔌 **可扩展架构** - 轻松集成新的 Agent 和工作流

## 快速开始

### 方式 1: Docker Compose (推荐)

```bash
cd monitor_dashboard
docker-compose up -d
```

访问：
- 前端：http://localhost:3000
- 后端 API: http://localhost:8001

### 方式 2: 本地运行

**后端:**
```bash
cd monitor_dashboard/backend
pip install -r requirements.txt
python app/main.py
```

**前端:**
```bash
cd monitor_dashboard/frontend
npm install
npm run dev
```

## 集成到现有工作流

### 1. 在 Agent 中添加监控

```python
from monitor_dashboard.backend.services.monitor_integration import (
    monitor_agent,
    track_tokens,
)

@monitor_agent  # 自动报告状态
class MyAgent(AgentBase):
    def execute(self, input_data):
        with track_tokens(self.AGENT_NAME) as tracker:
            # 调用 LLM
            response = call_llm(prompt)
            
            # 记录 token 用量
            tracker.record(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
            )
            
            return result
```

### 2. 手动报告状态

```python
from monitor_dashboard.backend.services.monitor_integration import report_status, record_usage

# 报告 Agent 状态
report_status(
    agent_name="problem_definition_agent",
    stage="problem_definition",
    status="running",
    current_task="分析问题定义...",
)

# 记录 token 用量
record_usage(
    agent_name="problem_definition_agent",
    input_tokens=1000,
    output_tokens=500,
)
```

## API 文档

启动后端后访问：http://localhost:8001/docs

### 主要端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/dashboard` | GET | 获取仪表板摘要 |
| `/api/workflows` | GET | 获取工作流列表 |
| `/api/workflows/{run_id}` | GET | 获取工作流详情 |
| `/api/agents` | GET | 获取 Agent 状态列表 |
| `/api/agents/{name}/update` | POST | 更新 Agent 状态 |
| `/api/tokens` | GET | 获取 token 用量统计 |
| `/api/tokens/record` | POST | 记录 token 用量 |

## 目录结构

```
monitor_dashboard/
├── backend/
│   ├── app/
│   │   └── main.py           # FastAPI 主应用
│   ├── services/
│   │   └── monitor_integration.py  # 工作流集成模块
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/            # 页面组件
│   │   ├── components/       # 通用组件
│   │   ├── services/         # API 服务
│   │   └── store/            # 状态管理
│   └── package.json
└── docker-compose.yml
```

## 扩展指南

### 添加新的监控指标

1. 在 `backend/app/main.py` 中添加数据模型
2. 添加 API 端点
3. 在 `frontend/src/pages/` 创建新页面
4. 更新导航栏

### 集成新的 Agent

1. 在 Agent 代码中导入 `monitor_integration`
2. 使用 `@monitor_agent` 装饰器
3. 或使用 `track_tokens` 上下文管理器

### 自定义仪表板

编辑 `frontend/src/pages/Dashboard.jsx` 调整布局和组件。

## 技术栈

**后端:**
- FastAPI
- Pydantic
- Uvicorn

**前端:**
- React 18
- React Router
- TanStack Query
- Zustand (状态管理)
- Recharts (图表)
- TailwindCSS

## 开发

### 后端开发

```bash
cd monitor_dashboard/backend
uvicorn app.main:app --reload --port 8001
```

### 前端开发

```bash
cd monitor_dashboard/frontend
npm run dev
```

## 配置

环境变量：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MONITOR_API_BASE` | http://localhost:8001 | 监控 API 地址 |
| `WORKSPACE_PATH` | /workspace | Workspace 路径 |

## License

MIT
