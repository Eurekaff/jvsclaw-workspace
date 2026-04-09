#!/usr/bin/env python3
"""
MainlineBuildAgent - 主链路构建 agent

职责：
- 根据 context pack 输出最小可运行主链路方案
- 生成目录结构建议、模块划分、接口草案、关键实现步骤
- 如果当前项目允许，应直接落代码骨架

输出：
- implementation_plan.md
- architecture.json
- scaffold files / starter code
"""

import json
from typing import Any, Dict
from pathlib import Path
from agents import AgentBase


class MainlineBuildAgent(AgentBase):
    AGENT_NAME = "MainlineBuildAgent"
    STAGE_NAME = "mainline_build"
    ROLE_DESCRIPTION = "架构师 + 全栈工程师，擅长设计并实现最小可运行主链路"
    
    INPUT_FILES = ["context_pack.json"]
    OUTPUT_FILES = ["implementation_plan.md", "architecture.json"]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context_pack = input_data.get("context_pack", {})
        
        # 生成架构设计
        architecture = self._design_architecture(context_pack)
        
        # 生成实现计划
        impl_plan = self._generate_impl_plan(architecture)
        
        # 生成代码骨架
        scaffold = self._generate_scaffold(architecture)
        
        # 生成 markdown 报告
        md_content = self._generate_markdown(impl_plan, architecture)
        
        # 保存代码骨架
        for filepath, content in scaffold.items():
            full_path = self.artifacts_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            "implementation_plan": md_content,
            "architecture": architecture
        }
    
    def _design_architecture(self, context_pack: Dict) -> Dict:
        """设计系统架构"""
        return {
            "project_structure": {
                "frontend/": {
                    "src/": {
                        "components/": ["UploadForm.tsx", "EntityList.tsx", "ReviewPanel.tsx"],
                        "pages/": ["Home.tsx", "Review.tsx"],
                        "services/": ["api.ts"],
                        "types/": ["index.ts"]
                    },
                    "package.json": "",
                    "vite.config.ts": ""
                },
                "backend/": {
                    "app/": {
                        "main.py": "",
                        "api/": ["upload.py", "recognition.py", "search.py", "export.py"],
                        "services/": ["excel_parser.py", "entity_recognizer.py", "registry_api.py"],
                        "models/": ["entity.py", "search_result.py"]
                    },
                    "requirements.txt": "",
                    "Dockerfile": ""
                },
                "docker-compose.yml": ""
            },
            "modules": [
                {
                    "name": "Excel Parser",
                    "responsibility": "解析用户上传的 Excel 文件，处理各种格式变体",
                    "interface": "parse_excel(file) -> List[RawRecord]"
                },
                {
                    "name": "Entity Recognizer",
                    "responsibility": "从原始记录中识别企业主体",
                    "interface": "recognize(raw_records) -> List[Entity]"
                },
                {
                    "name": "Registry API Client",
                    "responsibility": "调用查册接口获取企业信息",
                    "interface": "search(entities) -> List[SearchResult]"
                },
                {
                    "name": "Review Manager",
                    "responsibility": "管理人工复核流程",
                    "interface": "submit_review(entity_id, decision, notes)"
                },
                {
                    "name": "Export Service",
                    "responsibility": "导出结果为 CSV/Excel",
                    "interface": "export(results, format) -> file"
                }
            ],
            "api_endpoints": [
                {"method": "POST", "path": "/api/upload", "description": "上传 Excel 文件"},
                {"method": "GET", "path": "/api/entities", "description": "获取识别后的实体列表"},
                {"method": "POST", "path": "/api/search", "description": "批量查册"},
                {"method": "GET", "path": "/api/results", "description": "获取查册结果"},
                {"method": "POST", "path": "/api/review", "description": "提交复核决定"},
                {"method": "GET", "path": "/api/export", "description": "导出结果"}
            ],
            "data_models": [
                {
                    "name": "Entity",
                    "fields": ["id", "name", "registration_number", "status", "confidence_score"]
                },
                {
                    "name": "SearchResult",
                    "fields": ["entity_id", "company_name", "registration_info", "status", "raw_data"]
                }
            ]
        }
    
    def _generate_impl_plan(self, architecture: Dict) -> Dict:
        """生成实现计划"""
        return {
            "phases": [
                {
                    "phase": 1,
                    "name": "项目骨架",
                    "tasks": ["创建目录结构", "配置开发环境", "设置 Docker"],
                    "estimate": "0.5 天"
                },
                {
                    "phase": 2,
                    "name": "Excel 解析",
                    "tasks": ["实现文件上传", "解析 Excel", "数据清洗"],
                    "estimate": "1 天"
                },
                {
                    "phase": 3,
                    "name": "企业识别",
                    "tasks": ["实现识别算法", "处理边界情况", "添加置信度评分"],
                    "estimate": "1 天"
                },
                {
                    "phase": 4,
                    "name": "查册集成",
                    "tasks": ["集成 API", "错误处理", "结果存储"],
                    "estimate": "1 天"
                },
                {
                    "phase": 5,
                    "name": "前端界面",
                    "tasks": ["上传界面", "列表展示", "复核界面"],
                    "estimate": "2 天"
                },
                {
                    "phase": 6,
                    "name": "导出功能",
                    "tasks": ["实现 CSV 导出", "实现 Excel 导出"],
                    "estimate": "0.5 天"
                },
                {
                    "phase": 7,
                    "name": "测试和修复",
                    "tasks": ["端到端测试", "Bug 修复", "性能优化"],
                    "estimate": "1 天"
                }
            ],
            "total_estimate": "7 天"
        }
    
    def _generate_scaffold(self, architecture: Dict) -> Dict:
        """生成代码骨架"""
        scaffold = {}
        
        # Backend main.py
        scaffold["backend/app/main.py"] = '''from fastapi import FastAPI
from app.api import upload, recognition, search, export

app = FastAPI(title="Enterprise Registry Search System")

app.include_router(upload.router, prefix="/api/upload")
app.include_router(recognition.router, prefix="/api/recognition")
app.include_router(search.router, prefix="/api/search")
app.include_router(export.router, prefix="/api/export")

@app.get("/health")
def health_check():
    return {"status": "ok"}
'''
        
        # Backend requirements.txt
        scaffold["backend/requirements.txt"] = '''fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
openpyxl==3.1.2
python-multipart==0.0.6
'''
        
        # Backend Dockerfile
        scaffold["backend/Dockerfile"] = '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        
        # Frontend package.json
        scaffold["frontend/package.json"] = '''{
  "name": "registry-search-frontend",
  "version": "0.1.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "axios": "^1.6.0"
  }
}
'''
        
        # docker-compose.yml
        scaffold["docker-compose.yml"] = '''version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
'''
        
        return scaffold
    
    def _generate_markdown(self, impl_plan: Dict, architecture: Dict) -> str:
        """生成 markdown 格式"""
        phases_md = '\n'.join(
            f"### Phase {p['phase']}: {p['name']}\n"
            f"- 任务：{', '.join(p['tasks'])}\n"
            f"- 估算：{p['estimate']}\n"
            for p in impl_plan['phases']
        )
        
        modules_md = '\n'.join(
            f"- **{m['name']}**: {m['responsibility']}\n  - 接口：`{m['interface']}`"
            for m in architecture['modules']
        )
        
        api_md = '\n'.join(
            f"- `{e['method']} {e['path']}`: {e['description']}"
            for e in architecture['api_endpoints']
        )
        
        md = f"""# 实现计划

## 总体估算
{impl_plan['total_estimate']}

## 开发阶段

{phases_md}

## 模块划分

{modules_md}

## API 接口

{api_md}

## 目录结构

```
{json.dumps(architecture['project_structure'], indent=2)}
```

---
*Generated by MainlineBuildAgent*
"""
        return md


if __name__ == "__main__":
    agent = MainlineBuildAgent("/home/admin/openclaw/workspace")
    result = agent.run({})
    print(f"Generated files: {result}")
