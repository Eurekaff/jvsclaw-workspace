# Hermes Agent 架构学习报告

**调研时间**: 2026-04-10  
**项目**: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)  
**Stars**: 44.7k | **Forks**: 5.8k | **Commits**: 3,614  
**语言**: Python (主要), TypeScript, Shell

---

## 🎯 项目概述

**Hermes Agent** 是一个**自我进化的 AI 智能体**，核心特点是内置学习循环：

- ✅ 从经验中创建技能
- ✅ 在使用过程中改进技能
- ✅ 跨会话持久化知识
- ✅ 自主搜索历史对话
- ✅ 构建用户模型

**关键优势**:
- 可运行在 $5 VPS、GPU 集群或 serverless 环境
- 支持 Telegram、Discord、Slack、WhatsApp、Signal 等多平台
- 内置 cron 调度器
- 支持子智能体并行工作
- 6 种终端后端（本地、Docker、SSH、Daytona、Singularity、Modal）

---

## 📁 项目架构

### 核心目录结构

```
hermes-agent/
├── agent/                    # 核心 Agent 逻辑
├── gateway/                  # 消息网关（Telegram/Discord 等）
├── skills/                   # 技能系统
├── tools/                    # 工具库（40+ 工具）
├── environments/             # RL 训练环境
├── plugins/                  # 插件系统
├── cron/                     # 定时任务调度
├── acp_adapter/              # ACP 适配器
├── acp_registry/             # ACP 注册表
├── hermes_cli/               # CLI 工具
├── website/                  # 文档网站
├── docker/                   # Docker 配置
├── tests/                    # 测试套件
└── docs/                     # 文档
```

### 核心组件

| 组件 | 职责 | 文件位置 |
|------|------|----------|
| **Agent Core** | 智能体核心循环 | `agent/` |
| **Gateway** | 多平台消息网关 | `gateway/` |
| **Skills** | 技能系统（agentskills.io 标准） | `skills/` |
| **Tools** | 40+ 工具库 | `tools/` |
| **CLI** | 命令行界面 | `hermes_cli/`, `cli.py` |
| **Cron** | 定时任务调度 | `cron/` |
| **Plugins** | 插件系统 | `plugins/` |
| **Environments** | RL 训练环境 | `environments/` |

---

## 🏗️ 架构设计

### 1. 核心 Agent 循环

```
用户输入 → 解析命令 → 选择工具 → 执行 → 输出 → 学习
    ↑                                        ↓
    └──────────── 记忆/技能更新 ─────────────
```

**关键文件**:
- `agent/` - Agent 核心逻辑
- `model_tools.py` - 工具调用
- `hermes_state.py` - 状态管理

### 2. 消息网关架构

```
                  ┌─────────────────┐
                  │   Gateway       │
                  │   (统一入口)     │
                  └────────┬────────┘
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │Telegram │      │ Discord │      │  Slack  │
    └─────────┘      └─────────┘      └─────────┘
```

**关键文件**:
- `gateway/` - 网关主目录
- `cron/` - 定时任务交付

### 3. 技能系统

**特点**:
- 符合 [agentskills.io](https://agentskills.io) 开放标准
- 自主创建技能
- 技能自我改进
- 技能搜索和发现

**目录**:
- `skills/` - 技能库
- `optional-skills/` - 可选技能

### 4. 工具系统

**40+ 内置工具**:
- 文件操作
- 网络搜索
- 代码执行
- 浏览器自动化
- 多平台消息

**关键文件**:
- `tools/` - 工具库
- `model_tools.py` - 工具定义

### 5. 记忆系统

**特点**:
- 持久化记忆
- 用户建模（Honcho 方言）
- 跨会话搜索（FTS5 全文搜索）
- LLM 总结

**关键文件**:
- `hermes_state.py` - 状态和记忆
- `hermes_logging.py` - 日志系统

---

## 🔧 技术栈

### 后端

| 技术 | 用途 |
|------|------|
| **Python** | 主要语言 |
| **FastAPI?** | API 服务（推测） |
| **SQLite** | 本地数据库（FTS5 搜索） |
| **Docker** | 容器化部署 |

### 前端/CLI

| 技术 | 用途 |
|------|------|
| **Textual/Rich** | TUI 终端界面 |
| **React?** | Landing page |
| **TypeScript** | 部分工具 |

### 基础设施

| 技术 | 用途 |
|------|------|
| **Nix** | 包管理（flake.nix） |
| **Docker** | 容器部署 |
| **Modal/Daytona** | Serverless 后端 |

---

## 🎨 核心特性对比

| 特性 | Hermes | OpenClaw (我们) | 差距 |
|------|--------|-----------------|------|
| **多平台网关** | ✅ 6+ 平台 | ✅ JVSCLaw | 相当 |
| **技能系统** | ✅ agentskills.io | ✅ 自有技能 | 需对接标准 |
| **自我改进** | ✅ 内置学习循环 | ❌ 无 | **需学习** |
| **记忆系统** | ✅ Honcho 用户建模 | ✅ MEMORY.md | 相当 |
| **定时任务** | ✅ cron + 交付 | ✅ cron | 相当 |
| **子智能体** | ✅ 并行工作流 | ✅ sessions_spawn | 相当 |
| **终端后端** | ✅ 6 种 | ❌ 本地 | **需学习** |
| **RL 训练** | ✅ Atropos 环境 | ❌ 无 | 研究向 |
| **MCP 集成** | ✅ | ❌ | **需学习** |

---

## 📚 可借鉴的设计

### 1. ✅ 学习循环系统

**Hermes 的做法**:
```
执行任务 → 成功/失败 → 创建/更新技能 → 下次使用 → 改进
```

**我们可以**:
- 在 TaskReportAgent 中添加技能创建逻辑
- 任务完成后询问"是否创建技能"
- 技能版本管理和自我改进

### 2. ✅ 多终端后端

**Hermes 支持**:
- Local (本地)
- Docker (容器)
- SSH (远程)
- Daytona (serverless)
- Singularity (HPC)
- Modal (serverless)

**我们可以**:
- 添加 Docker 后端支持
- 添加 SSH 远程执行
- 考虑 serverless 部署

### 3. ✅ 技能标准化

**Hermes**: 遵循 [agentskills.io](https://agentskills.io) 标准

**我们可以**:
- 将现有 skills 转换为标准格式
- 发布到 agentskills.io
- 复用社区 skills

### 4. ✅ MCP 集成

**Hermes**: 支持 Model Context Protocol (MCP)

**我们可以**:
- 研究 MCP 协议
- 实现 MCP server
- 连接更多工具

### 5. ✅ CLI 设计

**Hermes CLI**:
```bash
hermes              # 交互式 CLI
hermes model        # 选择模型
hermes tools        # 配置工具
hermes gateway      # 启动网关
hermes setup        # 设置向导
hermes claw migrate # 从 OpenClaw 迁移！
hermes update       # 更新
hermes doctor       # 诊断
```

**我们可以**:
- 统一 CLI 命令风格
- 添加 `hermes doctor` 诊断功能
- 改进设置向导

---

## 🚀 实施建议

### 短期（1-2 周）

1. **学习循环** - 增强 TaskReportAgent
   - 任务完成后自动询问是否创建技能
   - 技能版本管理

2. **CLI 改进** - 统一命令风格
   - 添加诊断命令
   - 改进设置向导

3. **技能标准化** - 对接 agentskills.io
   - 转换现有 skills 格式
   - 发布到社区

### 中期（1 个月）

4. **Docker 后端** - 容器化支持
   - 添加 Docker 执行后端
   - 容器隔离

5. **MCP 集成** - 协议实现
   - 研究 MCP 协议
   - 实现 MCP client/server

### 长期（2-3 个月）

6. **Serverless 部署** - 降低成本
   - 集成 Modal/Daytona
   - 闲置时几乎零成本

7. **RL 训练** - 研究向
   - 集成 Atropos 环境
   - 轨迹生成和压缩

---

## 📖 关键资源

| 资源 | 链接 |
|------|------|
| **GitHub** | https://github.com/NousResearch/hermes-agent |
| **文档** | https://hermes-agent.nousresearch.com/docs/ |
| **Discord** | https://discord.gg/NousResearch |
| **技能标准** | https://agentskills.io |
| **MCP 协议** | https://modelcontextprotocol.io |

---

## 🎯 总结

### Hermes 的核心优势

1. **学习循环** - 真正的自我改进
2. **多后端** - 灵活部署
3. **标准化** - agentskills.io
4. **生态** - 44.7k stars, 活跃社区

### 我们的优势

1. **简洁** - 更易于理解和维护
2. **灵活** - 不受历史包袱
3. **快速** - 决策链短
4. **本地化** - 中文友好

### 学习重点

1. ✅ 学习循环设计
2. ✅ 多终端后端架构
3. ✅ 技能标准化
4. ✅ MCP 协议集成

---

**报告生成者**: TaskReportAgent  
**生成时间**: 2026-04-10 09:45  
**状态**: ✅ 完成
