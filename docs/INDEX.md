# 文档索引

**最后更新**: 2026-04-09 23:10

---

## 📚 文档分类

### 配置文档
系统配置和架构相关文档

- [工作流概览](配置文档/workflow_overview.md) - 工作流系统整体架构
- [Agent 合同规范](配置文档/agent_contracts.md) - Agent 开发规范
- [使用指南](配置文档/usage_guide.md) - 系统使用指南
- [README](../README.md) - 项目总览

### 技能文档
Skills 和 Tools 相关文档

- [Skills/Tools 使用指南](技能文档/skills_tools_usage_guide.md) - 471 个 skills 和 6 个 tools 的使用方法
- [Design.md 集成](技能文档/design_md_integration.md) - awesome-design-md 项目集成
- [Skills 测试报告](技能文档/skills_test_report.md) - Skills 测试结果
- [监控面板](../monitor_dashboard/README.md) - 监控面板文档

### 产出文档
任务执行和项目产出文档（按日期排序）

- [20260409_Skills.sh 集成_任务报告](产出文档/20260409_Skills.sh 集成_任务报告.md) - Skills.sh 集成任务报告
- [20260409_下一步建议_执行报告](产出文档/20260409_下一步建议_执行报告.md) - 下一步建议完成报告
- [20260409_Skills-Tools 集成_完成报告](产出文档/20260409_Skills-Tools 集成_完成报告.md) - Skills/Tools 集成完成报告
- [20260409_自我迭代_计划](产出文档/20260409_自我迭代_计划.md) - 自我迭代计划

### API 文档
API 和接口文档

- [监控面板 API](../monitor_dashboard/README.md) - 监控面板 API 文档
- [工作流 API](配置文档/usage_guide.md#编程接口) - 工作流编程接口

---

## 📁 目录结构

```
workspace/
├── README.md                    # 项目总览
├── docs/
│   ├── INDEX.md                 # 本文档（索引）
│   ├── 配置文档/
│   │   ├── workflow_overview.md    # 工作流概览
│   │   ├── agent_contracts.md      # Agent 合同
│   │   └── usage_guide.md          # 使用指南
│   ├── 技能文档/
│   │   ├── skills_tools_usage_guide.md  # Skills/Tools 使用
│   │   ├── design_md_integration.md     # Design.md 集成
│   │   └── skills_test_report.md        # Skills 测试
│   ├── 产出文档/
│   │   ├── skills_integration_report.md        # Skills 集成
│   │   ├── next_steps_completion_report.md     # 下一步执行
│   │   ├── skills_tools_integration_report.md  # Skills/Tools 集成
│   │   └── self_iteration_plan.md              # 自我迭代
│   └── API 文档/
│       └── (链接到各模块 README)
├── monitor_dashboard/
│   └── README.md                  # 监控面板文档
└── ...
```

---

## 🔍 快速查找

### 我想...

| 需求 | 查看文档 |
|------|----------|
| 了解系统整体架构 | [README](../README.md) → [工作流概览](配置文档/workflow_overview.md) |
| 开发新 Agent | [Agent 合同](配置文档/agent_contracts.md) |
| 使用系统 | [使用指南](配置文档/usage_guide.md) |
| 调用 Skills | [Skills/Tools 使用指南](技能文档/skills_tools_usage_guide.md) |
| 查看任务报告 | [产出文档/](产出文档/) |
| 查看 API | [监控面板 API](../monitor_dashboard/README.md) |

---

## 📊 文档统计

| 分类 | 文档数 | 总行数 |
|------|--------|--------|
| 配置文档 | 3 | ~400 |
| 技能文档 | 3 | ~800 |
| 产出文档 | 4 | ~1200 |
| API 文档 | 1 | ~300 |
| **总计** | **11** | **~2700** |

---

## 📝 命名规范

### 配置文档
- 使用小写英文命名
- 单词间用下划线分隔
- 示例：`workflow_overview.md`

### 技能文档
- 使用小写英文命名
- 包含技能名称
- 示例：`skills_tools_usage_guide.md`

### 产出文档
- 使用**标准中文命名**
- 包含日期和主题
- 格式：`YYYYMMDD_主题_报告.md`
- 示例：`20260409_Skills 集成_报告.md`

---

## 🔄 文档更新流程

1. **新增配置文档** → `docs/配置文档/`
2. **新增技能文档** → `docs/技能文档/`
3. **新增产出文档** → `docs/产出文档/` + 标准中文命名
4. **更新索引** → 更新本文档

---

**维护者**: TaskReportAgent  
**更新频率**: 每次任务完成后
