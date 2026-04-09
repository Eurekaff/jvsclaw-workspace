# Skills 和 Tools 集成使用指南

## 概述

所有 agents 现在都具备调用 **471 个 skills** 和 **多个 tools** 的能力，无需额外配置。

---

## 可用能力

### 🔮 Skills (471 个)

从 skills.sh 集成的大型能力库，包括：

**核心功能:**
- find-skills (731.2K 安装)
- skill-creator (105.5K)
- brainstorming (86.4K)
- ...

**前端开发:**
- frontend-design (214.1K)
- vercel-react-best-practices (229.8K)
- shadcn (68.6K)
- ...

**多媒体:**
- pdf (51.2K)
- pptx (48.0K)
- docx (46.9K)
- remotion-best-practices (181.0K)
- ...

**浏览器:**
- agent-browser (155.0K)
- browser-use (60.9K)
- ...

**企业工具:**
- Azure 系列 (56 个 skills)
- Supabase (75.3K)
- ...

### 🔧 Tools (内置)

| Tool | 功能 | 示例 |
|------|------|------|
| `file_read` | 读取文件 | `use_tool("file_read", path="file.txt")` |
| `file_write` | 写入文件 | `use_tool("file_write", path="file.txt", content="...")` |
| `file_list` | 列出目录 | `use_tool("file_list", path="./")` |
| `exec` | 执行命令 | `use_tool("exec", command="ls -la")` |
| `web_fetch` | 获取网页 | `use_tool("web_fetch", url="https://...")` |
| `search_skills` | 搜索 skills | `use_tool("search_skills", query="browser")` |

---

## 在 Agent 中使用

### 基础用法

```python
from agents import AgentBase

class MyAgent(AgentBase):
    def execute(self, input_data):
        # 使用 skill
        result = self.use_skill("find-skills")
        
        # 使用 tool
        files = self.use_tool("file_list", path="./workspace")
        
        # 组合使用
        content = self.use_tool("file_read", path="input.txt")
        processed = self.use_skill("brainstorming", input=content)
        self.use_tool("file_write", path="output.txt", content=processed)
        
        return {"result": processed}
```

### 查看可用 Skills/Tools

```python
class MyAgent(AgentBase):
    def execute(self, input_data):
        # 获取可用列表
        skills = self.get_available_skills()  # 471 个
        tools = self.get_available_tools()    # 6 个
        
        print(f"可用 skills: {len(skills)}")
        print(f"可用 tools: {len(tools)}")
        
        return {"skills": skills, "tools": tools}
```

### 高级用法 - 组合执行

```python
class MyAgent(AgentBase):
    def execute(self, input_data):
        # 使用多个 tools 执行任务
        result = self.execute_with_tools(
            task="处理文件",
            tools=["file_read", "file_write"]
        )
        
        return result
```

---

## 实际示例

### 示例 1: 使用 PDF skill

```python
from agents import AgentBase

class PDFAgent(AgentBase):
    AGENT_NAME = "PDFAgent"
    
    def execute(self, input_data):
        # 调用 PDF skill
        pdf_skill = self.use_skill("pdf")
        
        # 处理 PDF
        result = pdf_skill.process(input_data["file_path"])
        
        return result
```

### 示例 2: 使用浏览器自动化

```python
class BrowserAgent(AgentBase):
    AGENT_NAME = "BrowserAgent"
    
    def execute(self, input_data):
        # 调用 browser skill
        browser = self.use_skill("agent-browser")
        
        # 打开网页
        browser.navigate(input_data["url"])
        
        # 截图
        screenshot = browser.screenshot()
        
        return {"screenshot": screenshot}
```

### 示例 3: 搜索并使用 skill

```python
class DynamicAgent(AgentBase):
    AGENT_NAME = "DynamicAgent"
    
    def execute(self, input_data):
        # 搜索相关 skill
        search_result = self.use_tool(
            "search_skills",
            query=input_data["need"]
        )
        
        # 使用找到的 skill
        if search_result["count"] > 0:
            skill_name = search_result["results"][0]["name"]
            result = self.use_skill(skill_name)
            return result
        
        return {"error": "No suitable skill found"}
```

---

## 在现有 Agents 中使用

所有现有 agents 已自动获得 skill/tool 调用能力：

### ProblemDefinitionAgent
```python
# 自动可用
self.use_skill("brainstorming")
self.use_tool("web_fetch", url="...")
```

### MainlineBuildAgent
```python
# 自动可用
self.use_skill("frontend-design")
self.use_skill("vercel-react-best-practices")
self.use_tool("exec", command="npm init")
```

### TaskReportAgent
```python
# 自动可用
self.use_tool("file_write", path="report.md", content=report)
```

---

## 最佳实践

### 1. 优先使用 Skills

```python
# ✅ 好：使用现成 skill
result = self.use_skill("pdf")

# ❌ 差：重新实现
def parse_pdf(...):
    # 重复造轮子
```

### 2. 组合使用

```python
# 搜索 → 加载 → 执行
results = self.use_tool("search_skills", query="react")
if results["count"] > 0:
    skill = self.use_skill(results["results"][0]["name"])
```

### 3. 错误处理

```python
try:
    result = self.use_skill("nonexistent")
    if result:
        # 处理结果
        pass
except Exception as e:
    # 降级处理
    return self.fallback_method()
```

### 4. 记录使用情况

```python
def execute(self, input_data):
    skills_used = []
    
    result = self.use_skill("pdf")
    skills_used.append("pdf")
    
    # 记录到报告
    self.report["skills_used"] = skills_used
    
    return result
```

---

## 添加新 Skills

### 1. 下载 skill

```bash
cd ~/.openclaw/skills
git clone https://github.com/owner/repo.git
```

### 2. 重新生成索引

```bash
python3 tools/skills_index.py scan
```

### 3. 立即可用

```python
# 所有 agents 立即可以使用新 skill
result = self.use_skill("new-skill")
```

---

## 添加新 Tools

```python
from tools.skill_tool_integration import ToolRegistry

# 获取注册表
registry = ToolRegistry()

# 注册新 tool
def my_custom_tool(param1, param2):
    # 实现逻辑
    return {"result": "success"}

registry.register("my_tool", my_custom_tool, "自定义工具")

# 现在所有 agents 都可以使用
# self.use_tool("my_tool", param1="...", param2="...")
```

---

## 调试和监控

### 查看已加载 Skills

```python
from tools.skill_tool_integration import get_integration

integration = get_integration()
print(f"已加载：{integration.skill_loader.loaded_skills.keys()}")
```

### 查看 Skill 详情

```bash
cat ~/.openclaw/skills/skills_index.json | jq '.skills[] | select(.name == "pdf")'
```

### 监控使用情况

所有 skill/tool 调用都会打印日志：
```
🔮 [AgentName] 使用 skill: skill-name
🔧 [AgentName] 使用 tool: tool-name
```

---

## 性能优化

### 1. 缓存已加载 Skills

```python
# Skill 自动缓存，无需重复加载
result1 = self.use_skill("pdf")  # 加载
result2 = self.use_skill("pdf")  # 使用缓存
```

### 2. 批量操作

```python
# ✅ 好：批量处理
files = self.use_tool("file_list", path="./")

# ❌ 差：逐个处理
for f in os.listdir("./"):
    ...
```

### 3. 异步执行（未来）

```python
# 计划支持
results = await self.use_skills_async(["skill1", "skill2"])
```

---

## 故障排除

### Q: Skill 找不到？

```python
# 检查索引
python3 tools/skills_index.py search --query "skill-name"

# 重新扫描
python3 tools/skills_index.py scan
```

### Q: Tool 调用失败？

```python
# 检查 tool 是否存在
tools = self.get_available_tools()
print(tools)

# 检查参数
result = self.use_tool("tool-name", **correct_params)
```

### Q: Skills 未更新？

```bash
# 更新所有 skills
./tools/update_skills.sh
```

---

## 统计信息

| 指标 | 数值 |
|------|------|
| 总 Skills | 471 |
| 总 Tools | 6 |
| 已集成 Agents | 9 |
| Skills 仓库 | 31 |

---

## 资源链接

- [Skills 索引](file:///home/admin/.openclaw/skills/skills_index.json)
- [Skill 测试报告](file:///home/admin/openclaw/workspace/docs/skills_test_report.md)
- [Integration 代码](file:///home/admin/openclaw/workspace/tools/skill_tool_integration.py)

---

**最后更新**: 2026-04-09 22:45  
**版本**: v1.0.0
