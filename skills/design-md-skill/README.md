# Design.md Skill - 集成 awesome-design-md

## 概述

本 skill 集成了 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 项目，为前端项目提供专业的设计系统。

## 什么是 DESIGN.md

DESIGN.md 是 Google Stitch 推出的概念：一个纯文本的设计系统文档，AI agents 读取它来生成一致的 UI。

| 文件 | 谁读取 | 定义内容 |
|------|--------|----------|
| `AGENTS.md` | 编码 agents | 如何构建项目 |
| `DESIGN.md` | 设计 agents | 项目应该如何外观和感觉 |

## 功能

### 1. 获取设计系统

从 awesome-design-md 仓库获取 58+ 个知名网站的设计系统：

**AI & 机器学习:**
- Claude, Cohere, ElevenLabs, Mistral AI, Ollama, xAI

**开发者工具:**
- Linear, Cursor, Vercel, Supabase, Sentry, Raycast, Mintlify

**云服务:**
- Stripe, MongoDB, HashiCorp, Sanity, ClickHouse

**设计工具:**
- Figma, Framer, Notion, Miro, Webflow, Intercom

**其他:**
- Airbnb, Apple, Spotify, Uber, Tesla, SpaceX

### 2. 应用设计令牌

将设计令牌应用到 TailwindCSS 项目：
- 颜色系统
- 排版规则
- 间距比例
- 圆角半径
- 阴影系统
- 动画效果

### 3. 生成预览

生成视觉预览页面，展示：
- 颜色色板
- 字体比例
- 按钮样式
- 卡片组件

## 使用方法

### 命令行

```bash
# 列出所有支持的网站
python3 skills/design-md-skill/design_md.py list

# 获取指定网站的设计系统
python3 skills/design-md-skill/design_md.py fetch --site linear

# 应用到项目
python3 skills/design-md-skill/design_md.py apply --site linear --target ./monitor_dashboard/frontend
```

### Python API

```python
from skills.design_md_skill.design_md import DesignMdSkill

skill = DesignMdSkill()

# 获取设计系统
design = skill.fetch("linear")

# 生成 Tailwind 配置
skill.generate_tailwind_config(design, "./tailwind.config.js")

# 应用到项目
skill.apply("linear", "./monitor_dashboard/frontend")
```

## 已应用的设计系统

### Linear Design System ✅

已应用到监控面板：

**特点:**
- 深色主题
- 紫色强调色 (#a855f7)
- 精确的间距系统
- 微妙的阴影
- 平滑的动画

**文件:**
- `monitor_dashboard/frontend/tailwind.config.js`
- `monitor_dashboard/frontend/src/index.css`
- `monitor_dashboard/demo-linear.html`

## 设计系统结构

每个 DESIGN.md 包含：

1. **视觉主题和氛围** - Mood, density, design philosophy
2. **颜色调色板和角色** - Semantic name + hex + functional role
3. **排版规则** - Font families, full hierarchy table
4. **组件样式** - Buttons, cards, inputs, navigation with states
5. **布局原则** - Spacing scale, grid, whitespace philosophy
6. **深度和海拔** - Shadow system, surface hierarchy
7. **Do's and Don'ts** - Design guardrails and anti-patterns
8. **响应式行为** - Breakpoints, touch targets, collapsing strategy
9. **Agent Prompt Guide** - Quick color reference, ready-to-use prompts

## 下一步

### 计划支持的设计系统

- [x] Linear - 项目管理工具
- [ ] Vercel - 前端部署平台
- [ ] Stripe - 支付基础设施
- [ ] Sentry - 错误监控
- [ ] Supabase - 开源 Firebase 替代

### 功能扩展

- [ ] 自动从 URL 提取设计令牌
- [ ] 支持更多 CSS 框架（CSS Modules, Styled Components）
- [ ] 生成组件库
- [ ] Figma 插件集成

## 资源

- [awesome-design-md GitHub](https://github.com/VoltAgent/awesome-design-md)
- [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/)
- [getdesign.md](https://getdesign.md/) - 请求自定义 DESIGN.md

## 贡献

欢迎贡献新的设计系统或改进现有的实现！
