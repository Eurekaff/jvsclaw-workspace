#!/usr/bin/env python3
"""
ContentCreator Agent - 内容创作主 Agent

核心职责：
1. 接收主题，生成核心内容
2. 调用 PlatformAdapter 进行多平台适配
3. 调用 AuthenticityChecker 进行真人化检查
4. 根据反馈优化内容
5. 输出最终版本

工作流程：
主题 → 核心内容生成 → 平台适配 → 真人化检查 → 优化 → 最终版本
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents import AgentBase


class ContentCreatorAgent(AgentBase):
    AGENT_NAME = "ContentCreatorAgent"
    STAGE_NAME = "content_creator"
    ROLE_DESCRIPTION = "社媒内容创作专家，生成真实有亮点的多平台内容"
    
    INPUT_FILES = ["content_request.json"]
    OUTPUT_FILES = ["final_content.json"]
    
    # 内容质量要求
    QUALITY_REQUIREMENTS = {
        "min_authenticity_score": 7.0,  # 最低真人化分数
        "max_ai_probability": 30,  # 最高 AI 概率
        "must_have": [
            "personal_story",  # 个人故事
            "specific_details",  # 具体细节
            "comparison",  # 前后对比
            "small_flaw",  # 小缺点
            "emotion",  # 情绪表达
            "interaction"  # 互动引导
        ]
    }
    
    def __init__(self, workspace_root: str, artifacts_dir: str = None):
        super().__init__(workspace_root, artifacts_dir)
        
        # 导入其他 Agent
        from agents.platform_adapter.agent import PlatformAdapterAgent
        from agents.authenticity_checker.agent import AuthenticityCheckerAgent
        
        self.platform_adapter = PlatformAdapterAgent(workspace_root, artifacts_dir)
        self.authenticity_checker = AuthenticityCheckerAgent(workspace_root, artifacts_dir)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行内容创作"""
        
        # 1. 解析需求
        topic = input_data.get("topic", "")
        target_audience = input_data.get("target_audience", "")
        selling_points = input_data.get("selling_points", [])
        platforms = input_data.get("platforms", ["xiaohongshu"])
        tone = input_data.get("tone", "authentic")
        
        print(f"\n🎨 开始创作内容...")
        print(f"   主题：{topic}")
        print(f"   平台：{', '.join(platforms)}")
        print(f"   受众：{target_audience}")
        
        # 2. 生成核心内容
        print(f"\n📝 生成核心内容...")
        core_content = self._generate_core_content(
            topic=topic,
            target_audience=target_audience,
            selling_points=selling_points
        )
        
        # 3. 平台适配
        print(f"\n📱 进行平台适配...")
        adapter_result = self.platform_adapter.execute({
            "core_content": core_content,
            "platforms": platforms
        })
        
        platform_versions = adapter_result.get("platform_versions", {})
        print(f"✅ 完成 {len(platform_versions)} 个平台适配")
        
        # 4. 真人化检查与优化
        print(f"\n🔍 真人化检查...")
        final_versions = {}
        
        for platform, version in platform_versions.items():
            print(f"\n   检查 {platform}...")
            
            content = version.get("content", {})
            text = content.get("text", content.get("script", ""))
            
            # 检查
            check_result = self.authenticity_checker.execute({
                "content": text,
                "platform": platform
            })
            
            report = check_result.get("authenticity_report.json", {})
            score = report.get("total_score", 0)
            passed = report.get("passed", False)
            
            print(f"   分数：{score} | 等级：{report.get('level', 'N/A')}")
            
            # 如果未通过，进行优化
            if not passed:
                print(f"   ⚠️  未通过，优化中...")
                suggestions = report.get("suggestions", [])
                optimized = self._optimize_content(text, suggestions, platform)
                version["content"]["text"] = optimized
                version["optimized"] = True
                
                # 再次检查
                recheck = self.authenticity_checker.execute({
                    "content": optimized,
                    "platform": platform
                })
                recheck_report = recheck.get("authenticity_report.json", {})
                print(f"   优化后分数：{recheck_report.get('total_score', 'N/A')}")
            
            final_versions[platform] = version
        
        # 5. 生成最终报告
        final_report = {
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "platforms": platforms,
            "versions": final_versions,
            "summary": {
                "total_platforms": len(final_versions),
                "optimized_count": sum(1 for v in final_versions.values() if v.get("optimized")),
                "avg_score": self._calculate_avg_score(final_versions)
            },
            "quality_check": {
                "all_passed": all(
                    v.get("content", {}).get("authenticity_score", {}).get("score", 0) >= self.QUALITY_REQUIREMENTS["min_authenticity_score"]
                    for v in final_versions.values()
                )
            }
        }
        
        return {
            "final_content.json": final_report,
            "final_report": final_report,
            "core_content": core_content,
            "platform_versions": final_versions
        }
    
    def _generate_core_content(self, topic: str, target_audience: str, 
                              selling_points: List) -> Dict:
        """生成核心内容"""
        
        # 使用学习循环提取的经验
        core_content = {
            "topic": topic,
            "content": self._write_core_content(topic, target_audience, selling_points),
            "selling_points": selling_points,
            "target_audience": target_audience,
            "tone": "authentic",
            "requirements": self.QUALITY_REQUIREMENTS["must_have"]
        }
        
        return core_content
    
    def _write_core_content(self, topic: str, target_audience: str, 
                           selling_points: List) -> str:
        """撰写核心内容（真人化）"""
        
        # 个人故事开头
        story = f"""
作为一个{target_audience}，
我之前也踩过很多坑。

记得有一次，为了解决这个问题，
我试了十几款产品/方法，
花了不少冤枉钱😢
""".strip()
        
        # 转折点
        turning_point = f"""
直到我遇到了{topic}！

说实话，刚开始我是抱着怀疑态度的。
但是用了一周后，我真的真香了！！
""".strip()
        
        # 卖点展示
        points_section = f"""
✨核心亮点：
"""
        for i, point in enumerate(selling_points[:3], 1):
            points_section += f"{i}. {point}\n"
        
        # 小缺点（增加真实感）
        flaw = f"""
说实话，它也不是完美的。
小缺点：包装/价格/学习曲线 一般般。
但是！！效果真的没话说！
""".strip()
        
        # 前后对比
        comparison = f"""
使用前：问题重重，效率低下
使用后：明显改善，效率翻倍

我身边的人都说我变了😂
""".strip()
        
        # 结尾互动
        cta = f"""
如果你也是{target_audience}，
真的可以试试！

你们有什么经验？
评论区告诉我！👇
""".strip()
        
        # 组合所有内容
        full_content = f"""
{story}

{turning_point}

{points_section}

{comparison}

{flaw}

{cta}
""".strip()
        
        return full_content
    
    def _optimize_content(self, content: str, suggestions: List, 
                         platform: str) -> str:
        """根据建议优化内容"""
        
        optimized = content
        
        # 处理语言优化建议
        if any("AI 词汇" in s for s in suggestions):
            ai_words = ["非常", "极其", "显著", "有效", "此外", "因此"]
            for word in ai_words:
                optimized = optimized.replace(word, "真的" if word in ["非常", "极其"] else word)
        
        # 处理真人词汇建议
        if any("真人词汇" in s for s in suggestions):
            human_words = ["真的", "绝了", "真香", "救命"]
            if not any(word in optimized for word in human_words):
                optimized = optimized.replace("。", "！！", 3)
        
        # 处理情绪词建议
        if any("情绪词" in s for s in suggestions):
            emojis = ["😭", "😱", "💯", "✨", ""]
            if not any(emoji in optimized for emoji in emojis):
                optimized = "😭 " + optimized + " 💯"
        
        # 处理个人故事建议
        if any("个人故事" in s for s in suggestions):
            if "我" not in optimized:
                optimized = "我个人" + optimized
        
        # 处理互动建议
        if any("提问" in s for s in suggestions):
            if "?" not in optimized and "？" not in optimized:
                optimized += "\n\n你们觉得呢？"
        
        if any("引导" in s for s in suggestions):
            if "评论" not in optimized:
                optimized += "\n\n评论区告诉我！"
        
        return optimized
    
    def _calculate_avg_score(self, versions: Dict) -> float:
        """计算平均分数"""
        scores = []
        for version in versions.values():
            score = version.get("content", {}).get("authenticity_score", {}).get("score", 0)
            if score:
                scores.append(score)
        
        return round(sum(scores) / max(len(scores), 1), 1)


if __name__ == "__main__":
    # 测试
    agent = ContentCreatorAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "topic": "AI 工具推荐",
        "target_audience": "打工人",
        "selling_points": [
            "提高效率 10 倍",
            "节省每天 2 小时",
            "上手简单，零基础可用"
        ],
        "platforms": ["xiaohongshu", "weibo", "twitter"]
    }
    
    result = agent.execute(test_input)
    
    print(f"\n✅ 内容创作完成")
    print(f"📱 平台数：{result['final_report']['summary']['total_platforms']}")
    print(f"⚙️  优化数：{result['final_report']['summary']['optimized_count']}")
    print(f"📊 平均分：{result['final_report']['summary']['avg_score']}")
    
    # 展示一个示例
    if result['platform_versions']:
        platform = list(result['platform_versions'].keys())[0]
        version = result['platform_versions'][platform]
        content = version.get('content', {})
        
        print(f"\n📝 {platform} 最终版本:")
        print("="*60)
        print(content.get('text', '')[:800])
        print("="*60)
