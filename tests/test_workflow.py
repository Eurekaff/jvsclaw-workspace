#!/usr/bin/env python3
"""
测试工作流 - 验证各 Agent 和编排器功能
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.problem_definition.agent import ProblemDefinitionAgent
from agents.mvp_scope.agent import MVPScopeAgent
from agents.context_pack.agent import ContextPackAgent
from workflows.engineering_lifecycle_workflow import WorkflowOrchestrator


def test_problem_definition_agent():
    """测试问题定义 Agent"""
    print("\n" + "="*60)
    print("测试 ProblemDefinitionAgent")
    print("="*60)
    
    agent = ProblemDefinitionAgent("/home/admin/openclaw/workspace")
    
    test_brief = """
    做一个面向合规分析员的企业批量查册原型系统。
    用户上传来源复杂、字段混乱的 Excel，系统自动识别企业主体并生成 entity 清单，
    再调用查册接口返回结构化结果，支持人工复核和导出。
    第一版不做登录权限和复杂报表。
    """
    
    result = agent.run({"raw_brief": test_brief})
    
    assert "problem_definition.md" in result
    assert "structured_problem_definition.json" in result
    
    # 验证 JSON 输出
    with open(result["structured_problem_definition.json"], 'r') as f:
        data = json.load(f)
        assert "target_users" in data
        assert "core_problem" in data
    
    print("✅ ProblemDefinitionAgent 测试通过")
    return True


def test_mvp_scope_agent():
    """测试 MVP 范围 Agent"""
    print("\n" + "="*60)
    print("测试 MVPScopeAgent")
    print("="*60)
    
    agent = MVPScopeAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "structured_problem_definition": {
            "target_users": ["合规分析员"],
            "core_problem": "企业查册效率低"
        }
    }
    
    result = agent.run(test_input)
    
    assert "mvp_scope.md" in result
    assert "mvp_scope.json" in result
    
    print("✅ MVPScopeAgent 测试通过")
    return True


def test_context_pack_agent():
    """测试上下文包 Agent"""
    print("\n" + "="*60)
    print("测试 ContextPackAgent")
    print("="*60)
    
    agent = ContextPackAgent("/home/admin/openclaw/workspace")
    result = agent.run({})
    
    assert "context_pack.md" in result
    assert "context_pack.json" in result
    
    print("✅ ContextPackAgent 测试通过")
    return True


def test_workflow_orchestrator():
    """测试工作流编排器"""
    print("\n" + "="*60)
    print("测试 WorkflowOrchestrator")
    print("="*60)
    
    try:
        orchestrator = WorkflowOrchestrator("/home/admin/openclaw/workspace")
        
        # 测试启动 (参数顺序：raw_brief, project_name)
        state = orchestrator.start("这是一个测试项目", "测试项目")
        assert state["project_name"] == "测试项目", f"Expected '测试项目', got {state['project_name']}"
        
        # 测试状态保存
        state.save(orchestrator.run_dir / "test_state.json")
        assert (orchestrator.run_dir / "test_state.json").exists(), "State file not saved"
        
        # 测试状态加载
        from workflows.engineering_lifecycle_workflow import ProjectState
        loaded_state = ProjectState.load(orchestrator.run_dir / "test_state.json")
        assert loaded_state["project_name"] == "测试项目", f"Load failed: {loaded_state['project_name']}"
        
        print("✅ WorkflowOrchestrator 测试通过")
        return True
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🧪 运行工作流测试套件")
    print("="*60)
    
    tests = [
        test_problem_definition_agent,
        test_mvp_scope_agent,
        test_context_pack_agent,
        test_workflow_orchestrator,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败：{e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
