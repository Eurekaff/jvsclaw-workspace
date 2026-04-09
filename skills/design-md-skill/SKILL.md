# Design.md Skill

## 描述

集成 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 项目，为监控面板和其他前端项目提供专业的设计系统。

## 功能

1. **获取 DESIGN.md** - 从 awesome-design-md 仓库获取知名网站的设计系统
2. **应用设计令牌** - 将设计令牌应用到 React/Tailwind 项目
3. **生成主题配置** - 自动生成 Tailwind 配置文件
4. **组件样式指南** - 生成组件样式参考

## 使用方法

### 1. 获取设计系统

```bash
python3 -m skills.design_md fetch --site linear
```

支持的网站：
- **AI & ML**: Claude, Cohere, ElevenLabs, Mistral AI, Ollama, xAI 等
- **开发者工具**: Cursor, Linear, Vercel, Supabase, Sentry, Raycast 等
- **云服务**: Stripe, MongoDB, HashiCorp, Sanity 等
- **设计工具**: Figma, Framer, Notion, Miro, Webflow 等
- **其他**: Airbnb, Apple, Spotify, Uber, Tesla 等

### 2. 应用到项目

```bash
python3 -m skills.design_md apply --site linear --target ./monitor_dashboard/frontend
```

### 3. 生成 Tailwind 配置

```bash
python3 -m skills.design_md generate-tailwind --site linear --output ./tailwind.config.js
```

## 输出文件

- `DESIGN.md` - 设计系统文档
- `preview.html` - 视觉预览
- `tailwind-theme.js` - Tailwind 主题配置
- `components/` - 组件样式示例

## 集成到监控面板

1. 获取 Linear 设计系统（工程师最爱的项目管理工具）
2. 应用到前端项目
3. 更新组件样式
4. 重启前端服务

## 示例

```python
from skills.design_md import DesignMdSkill

skill = DesignMdSkill()

# 获取 Linear 设计系统
design = skill.fetch("linear")

# 应用到项目
skill.apply(design, target="./monitor_dashboard/frontend")

# 生成预览
skill.generate_preview(design)
```

## 设计系统参考

每个 DESIGN.md 包含：
1. 视觉主题和氛围
2. 颜色调色板和角色
3. 排版规则
4. 组件样式
5. 布局原则
6. 深度和海拔
7. Do's and Don'ts
8. 响应式行为
9. Agent Prompt 指南

## 资源

- [awesome-design-md GitHub](https://github.com/VoltAgent/awesome-design-md)
- [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/)
- [getdesign.md](https://getdesign.md/)
