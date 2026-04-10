#!/usr/bin/env python3
"""
AuthenticityChecker Agent - 真人化检查 Agent

核心职责：
1. 检查内容是否像真人撰写
2. 检测 AI 痕迹
3. 提供修改建议
4. 评分并给出优化方案

检查维度：
- 语言层面（正式度、情绪词、句长）
- 内容层面（故事、细节、对比、缺点）
- 互动层面（称呼、提问、引导）
- 格式层面（emoji、标签、分段）
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents import AgentBase


class AuthenticityCheckerAgent(AgentBase):
    AGENT_NAME = "AuthenticityCheckerAgent"
    STAGE_NAME = "authenticity_checker"
    ROLE_DESCRIPTION = "真人化检查专家，确保内容像真人撰写"
    
    INPUT_FILES = ["content_to_check.json"]
    OUTPUT_FILES = ["authenticity_report.json"]
    
    # AI 味词汇库
    AI_WORDS = [
        "非常", "极其", "十分", "相当", "颇为",
        "显著", "明显", "有效", "优质", "卓越",
        "此外", "另外", "同时", "然而", "因此",
        "总之", "综上所述", "总而言之",
        "值得", "可以", "能够", "应该", "必须"
    ]
    
    # 真人化词汇库
    HUMAN_WORDS = [
        "真的", "太", "超", "巨", "绝了",
        "救命", "笑死", "无语", "真香",
        "姐妹们", "兄弟们", "家人们", "宝子们",
        "我", "我的", "我个人", "我自己",
        "说实话", "讲真", "不夸张", "亲测"
    ]
    
    # 情绪词库
    EMOTION_WORDS = [
        "😭", "😱", "💯", "✨", "🔥", "", "😍", "",
        "！！", "！！！", "？？", "？？？",
        "爱了", "哭了", "跪了", "服了", "绝了"
    ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行真人化检查"""
        
        content = input_data.get("content", "")
        platform = input_data.get("platform", "general")
        content_type = input_data.get("type", "text")  # text/script
        
        # 多维度检查
        checks = {
            "language": self._check_language(content),
            "content": self._check_content(content),
            "interaction": self._check_interaction(content),
            "format": self._check_format(content, platform)
        }
        
        # 计算总分
        total_score = sum(check["score"] for check in checks.values()) / len(checks)
        
        # 生成建议
        suggestions = self._generate_suggestions(checks, platform)
        
        # 生成报告
        report = {
            "checked_at": datetime.now().isoformat(),
            "platform": platform,
            "content_type": content_type,
            "total_score": round(total_score, 1),
            "level": self._score_to_level(total_score),
            "checks": checks,
            "suggestions": suggestions,
            "ai_probability": self._detect_ai_probability(content),
            "passed": total_score >= 7.0
        }
        
        return {
            "authenticity_report.json": report,
            "report": report
        }
    
    def _check_language(self, content: str) -> Dict:
        """语言层面检查"""
        
        score = 10.0
        issues = []
        
        # 检查 AI 词汇
        ai_count = sum(1 for word in self.AI_WORDS if word in content)
        if ai_count > 5:
            score -= 3
            issues.append(f"AI 词汇过多 ({ai_count}个)")
        elif ai_count > 2:
            score -= 1
            issues.append(f"有 AI 词汇 ({ai_count}个)")
        
        # 检查真人词汇
        human_count = sum(1 for word in self.HUMAN_WORDS if word in content)
        if human_count >= 3:
            score += 2
        elif human_count >= 1:
            score += 1
        else:
            score -= 2
            issues.append("缺少真人化词汇")
        
        # 检查句长
        sentences = re.split(r'[.!?！？。]', content)
        avg_len = sum(len(s) for s in sentences if s.strip()) / max(len(sentences), 1)
        
        if avg_len > 50:
            score -= 2
            issues.append("句子过长，真人喜欢短句")
        elif avg_len < 10:
            score -= 1
            issues.append("句子过短")
        
        # 检查情绪词
        emotion_count = sum(1 for word in self.EMOTION_WORDS if word in content)
        if emotion_count >= 5:
            score += 2
        elif emotion_count >= 2:
            score += 1
        else:
            score -= 1
            issues.append("缺少情绪表达")
        
        return {
            "dimension": "language",
            "score": max(0, min(10, score)),
            "issues": issues,
            "details": {
                "ai_words": ai_count,
                "human_words": human_count,
                "emotion_words": emotion_count,
                "avg_sentence_length": round(avg_len, 1)
            }
        }
    
    def _check_content(self, content: str) -> Dict:
        """内容层面检查"""
        
        score = 10.0
        issues = []
        
        # 检查个人故事
        has_story = any(phrase in content for phrase in [
            "我之前", "有一次", "那天", "记得", "想起",
            "我朋友", "我同事", "我家人"
        ])
        if has_story:
            score += 2
        else:
            score -= 2
            issues.append("缺少个人故事")
        
        # 检查具体细节
        has_details = any(phrase in content for phrase in [
            "凌晨", "地铁上", "办公室里", "回家后",
            "第一次", "第二天", "一周后", "一个月"
        ])
        if has_details:
            score += 2
        else:
            score -= 2
            issues.append("缺少具体细节")
        
        # 检查前后对比
        has_comparison = any(phrase in content for phrase in [
            "之前", "以前", "后来", "现在",
            "对比", "相比", "变化", "改善"
        ])
        if has_comparison:
            score += 2
        else:
            score -= 2
            issues.append("缺少前后对比")
        
        # 检查小缺点
        has_flaw = any(phrase in content for phrase in [
            "但是", "不过", "说实话", "唯一缺点",
            "小问题", "美中不足", "虽然", "尽管"
        ])
        if has_flaw:
            score += 2
        else:
            score -= 2
            issues.append("太完美，不真实")
        
        return {
            "dimension": "content",
            "score": max(0, min(10, score)),
            "issues": issues,
            "details": {
                "has_story": has_story,
                "has_details": has_details,
                "has_comparison": has_comparison,
                "has_flaw": has_flaw
            }
        }
    
    def _check_interaction(self, content: str) -> Dict:
        """互动层面检查"""
        
        score = 10.0
        issues = []
        
        # 检查称呼
        has_address = any(phrase in content for phrase in [
            "姐妹们", "兄弟们", "家人们", "宝子们",
            "大家", "你们", "朋友们"
        ])
        if has_address:
            score += 2
        else:
            score -= 1
            issues.append("缺少称呼")
        
        # 检查提问
        has_question = "?" in content or "？" in content
        if has_question:
            score += 2
        else:
            score -= 2
            issues.append("缺少互动提问")
        
        # 检查引导
        has_cta = any(phrase in content for phrase in [
            "评论区", "告诉我", "分享", "点赞",
            "收藏", "关注", "转发", "聊聊"
        ])
        if has_cta:
            score += 2
        else:
            score -= 2
            issues.append("缺少互动引导")
        
        return {
            "dimension": "interaction",
            "score": max(0, min(10, score)),
            "issues": issues,
            "details": {
                "has_address": has_address,
                "has_question": has_question,
                "has_cta": has_cta
            }
        }
    
    def _check_format(self, content: str, platform: str) -> Dict:
        """格式层面检查"""
        
        score = 10.0
        issues = []
        
        # 检查 emoji
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', content))
        
        emoji_requirements = {
            "xiaohongshu": (10, 30),  # (min, max)
            "douyin": (3, 10),
            "weibo": (3, 8),
            "wechat_official": (0, 5),
            "bilibili": (5, 15),
            "twitter": (1, 5),
            "linkedin": (0, 3)
        }
        
        min_emoji, max_emoji = emoji_requirements.get(platform, (3, 10))
        
        if min_emoji <= emoji_count <= max_emoji:
            score += 2
        elif emoji_count < min_emoji:
            score -= 2
            issues.append(f"emoji 太少 ({emoji_count}个，建议{min_emoji}-{max_emoji}个)")
        elif emoji_count > max_emoji * 2:
            score -= 1
            issues.append(f"emoji 过多 ({emoji_count}个)")
        
        # 检查标签
        tag_count = content.count("#")
        tag_requirements = {
            "xiaohongshu": (10, 20),  # 5-10 个标签，每个标签 2 个#
            "weibo": (2, 6),
            "twitter": (4, 6),
            "bilibili": (2, 8)
        }
        
        if platform in tag_requirements:
            min_tags, max_tags = tag_requirements[platform]
            if min_tags <= tag_count <= max_tags:
                score += 2
            elif tag_count < min_tags:
                score -= 1
                issues.append(f"标签太少")
        
        # 检查分段
        paragraphs = content.split("\n\n")
        if len(paragraphs) >= 3:
            score += 1
        else:
            score -= 1
            issues.append("分段太少")
        
        return {
            "dimension": "format",
            "score": max(0, min(10, score)),
            "issues": issues,
            "details": {
                "emoji_count": emoji_count,
                "tag_count": tag_count // 2,
                "paragraph_count": len(paragraphs)
            }
        }
    
    def _generate_suggestions(self, checks: Dict, platform: str) -> List[str]:
        """生成修改建议"""
        
        suggestions = []
        
        # 语言层面建议
        if checks["language"]["score"] < 7:
            suggestions.append("💡 语言优化:")
            if checks["language"]["details"]["ai_words"] > 2:
                suggestions.append("  - 替换 AI 词汇：非常→真的，显著→超")
            if checks["language"]["details"]["human_words"] < 3:
                suggestions.append("  - 添加真人词汇：绝了、真香、救命")
            if checks["language"]["details"]["emotion_words"] < 2:
                suggestions.append("  - 添加情绪词：😭、、💯")
            if checks["language"]["details"]["avg_sentence_length"] > 50:
                suggestions.append("  - 拆分长句，多用短句")
        
        # 内容层面建议
        if checks["content"]["score"] < 7:
            suggestions.append("📖 内容优化:")
            if not checks["content"]["details"]["has_story"]:
                suggestions.append("  - 添加个人故事：'我之前...有一次...'")
            if not checks["content"]["details"]["has_details"]:
                suggestions.append("  - 添加具体细节：时间、地点、场景")
            if not checks["content"]["details"]["has_comparison"]:
                suggestions.append("  - 添加前后对比：'之前...现在...'")
            if not checks["content"]["details"]["has_flaw"]:
                suggestions.append("  - 添加小缺点：'包装一般但效果好'")
        
        # 互动层面建议
        if checks["interaction"]["score"] < 7:
            suggestions.append("💬 互动优化:")
            if not checks["interaction"]["details"]["has_address"]:
                suggestions.append("  - 添加称呼：'姐妹们'、'家人们'")
            if not checks["interaction"]["details"]["has_question"]:
                suggestions.append("  - 添加提问：'你们觉得呢？'")
            if not checks["interaction"]["details"]["has_cta"]:
                suggestions.append("  - 添加引导：'评论区告诉我'")
        
        # 格式层面建议
        if checks["format"]["score"] < 7:
            suggestions.append("📐 格式优化:")
            emoji_info = checks["format"]["details"]
            if emoji_info["emoji_count"] < 5:
                suggestions.append(f"  - 添加 emoji (当前{emoji_info['emoji_count']}个)")
            if emoji_info["paragraph_count"] < 3:
                suggestions.append("  - 增加分段，提高可读性")
        
        # 平台特定建议
        platform_suggestions = {
            "xiaohongshu": "📕 小红书特化：姐妹语气 + 大量 emoji+ 标签",
            "douyin": "🎵 抖音特化：3 秒钩子 + 快节奏 + 互动",
            "wechat_official": "📝 公众号特化：深度内容 + 小标题 + 金句",
            "weibo": "🧣 微博特化：简短 + 热点 + 话题标签",
            "bilibili": "📺 B 站特化：玩梗 + 干货 + 弹幕互动点"
        }
        
        if platform in platform_suggestions:
            suggestions.append(f"\n{platform_suggestions[platform]}")
        
        return suggestions
    
    def _score_to_level(self, score: float) -> str:
        """分数转等级"""
        if score >= 9:
            return "🟢 完全真人"
        elif score >= 7:
            return "🟢 大部分真人"
        elif score >= 5:
            return "🟡 有明显 AI 痕迹"
        else:
            return "🔴 明显 AI 生成"
    
    def _detect_ai_probability(self, content: str) -> Dict:
        """检测 AI 生成概率"""
        
        ai_score = 0
        
        # AI 词汇密度
        ai_count = sum(len(re.findall(word, content)) for word in self.AI_WORDS)
        total_words = len(content) / 2  # 估算词数
        ai_density = ai_count / max(total_words, 1)
        
        if ai_density > 0.1:
            ai_score += 40
        elif ai_density > 0.05:
            ai_score += 20
        
        # 缺少真人特征
        if not any(word in content for word in self.HUMAN_WORDS):
            ai_score += 30
        
        # 过于完美
        if "但是" not in content and "不过" not in content:
            ai_score += 20
        
        # 没有情绪
        if not any(word in content for word in self.EMOTION_WORDS):
            ai_score += 10
        
        return {
            "probability": min(ai_score, 100),
            "level": "high" if ai_score > 70 else "medium" if ai_score > 40 else "low"
        }


if __name__ == "__main__":
    # 测试
    agent = AuthenticityCheckerAgent("/home/admin/openclaw/workspace")
    
    # 测试 AI 味内容
    ai_content = """
    这款产品非常优秀，效果显著。
    使用后可以明显改善肤质。
    此外，价格也十分合理。
    综上所述，值得购买。
    """
    
    # 测试真人化内容
    human_content = """
    姐妹们！！我真的要按头安利这个！！💯
    
    作为一个常年熬夜的人
    我之前也踩过很多坑😢
    但是这个！！真的用一次就爱了！！
    
    说实话，包装一般般
    但是！！效果真的没话说！
    我已经回购第三瓶了！！
    
    姐妹们冲！不踩雷！！
    """
    
    print("="*60)
    print("测试 AI 味内容")
    print("="*60)
    result1 = agent.execute({
        "content": ai_content,
        "platform": "xiaohongshu"
    })
    report1 = result1.get("authenticity_report.json", result1)
    print(f"总分：{report1.get('total_score', 'N/A')}")
    print(f"等级：{report1.get('level', 'N/A')}")
    print(f"AI 概率：{report1.get('ai_probability', {}).get('probability', 'N/A')}%")
    print(f"建议：{len(report1.get('suggestions', []))}条")
    
    print("\n" + "="*60)
    print("测试真人化内容")
    print("="*60)
    result2 = agent.execute({
        "content": human_content,
        "platform": "xiaohongshu"
    })
    report2 = result2.get("authenticity_report.json", result2)
    print(f"总分：{report2.get('total_score', 'N/A')}")
    print(f"等级：{report2.get('level', 'N/A')}")
    print(f"AI 概率：{report2.get('ai_probability', {}).get('probability', 'N/A')}%")
    print(f"通过：{report2.get('passed', False)}")
