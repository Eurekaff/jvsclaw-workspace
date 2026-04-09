#!/usr/bin/env python3
"""
运行示例工作流 - Demo Runner

用于演示完整工作流的运行
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from engineering_lifecycle_workflow import WorkflowOrchestrator


def run_example():
    """运行示例项目"""
    print("=" * 60)
    print("🚀 工程生命周期工作流 - 示例演示")
    print("=" * 60)
    
    # 示例项目简报
    example_brief = """
    做一个面向合规分析员的企业批量查册原型系统。
    用户上传来源复杂、字段混乱的 Excel，系统自动识别企业主体并生成 entity 清单，
    再调用查册接口返回结构化结果，支持人工复核和导出。
    第一版不做登录权限和复杂报表。
    """
    
    # 创建工作流编排器
    orchestrator = WorkflowOrchestrator(
        workspace_root="/home/admin/openclaw/workspace"
    )
    
    # 运行完整工作流
    final_state = orchestrator.run_full_workflow(
        raw_brief=example_brief,
        project_name="企业批量查册系统"
    )
    
    # 打印总结
    print("\n" + "=" * 60)
    print("📊 工作流执行总结")
    print("=" * 60)
    print(f"项目名称：{final_state['project_name']}")
    print(f"运行 ID: {orchestrator.run_id}")
    print(f"产出物数量：{len(final_state['artifacts_index'])}")
    print(f"产出物目录：{orchestrator.run_dir}")
    
    # 列出所有产出物
    print("\n📄 产出物列表:")
    for key, info in final_state['artifacts_index'].items():
        status_icon = "✅" if info['status'] == 'approved' else "⏳"
        print(f"  {status_icon} {key}")
    
    return orchestrator.run_dir


if __name__ == "__main__":
    run_dir = run_example()
    print(f"\n✅ 示例运行完成！查看产出物：{run_dir}")
