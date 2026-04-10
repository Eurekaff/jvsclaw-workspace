#!/usr/bin/env python3
"""
TrendHunter Agent - 热点发现 Agent

核心职责：
1. 扫描各平台热点榜单
2. 分析和分类热点
3. 生成选题建议
4. 评估热点价值

数据源：
- 微博热搜
- 知乎热榜
- Twitter Trends
- 抖音热榜
- B 站热门
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from agents import AgentBase


class TrendHunterAgent(AgentBase):
    AGENT_NAME = "TrendHunterAgent"
    STAGE_NAME = "trend_hunter"
    ROLE_DESCRIPTION = "热点发现专家，扫描全网热点并生成选题建议"
    
    INPUT_FILES = []
    OUTPUT_FILES = ["trending_report.json"]
    
    # 平台配置
    PLATFORMS = {
        "weibo": {
            "name": "微博",
            "url": "https://s.weibo.com/top/summary",
            "update_frequency": 10,  # 分钟
            "heat_levels": ["爆", "热", "沸", "新"]
        },
        "zhihu": {
            "name": "知乎",
            "url": "https://www.zhihu.com/hot",
            "update_frequency": 30,
            "heat_levels": []
        },
        "twitter": {
            "name": "Twitter",
            "url": "https://twitter.com/explore/tabs/trending",
            "update_frequency": 15,
            "heat_levels": []
        },
        "douyin": {
            "name": "抖音",
            "url": "https://www.douyin.com/hot",
            "update_frequency": 30,
            "heat_levels": []
        },
        "bilibili": {
            "name": "B 站",
            "url": "https://www.bilibili.com/v/popular/rank/all",
            "update_frequency": 60,
            "heat_levels": []
        }
    }
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行热点发现"""
        
        # 获取目标平台
        platforms = input_data.get("platforms", list(self.PLATFORMS.keys()))
        category = input_data.get("category", "all")  # all/tech/lifestyle/entertainment
        limit = input_data.get("limit", 20)
        
        print(f"\n🔍 开始扫描热点...")
        print(f"   平台：{', '.join(platforms)}")
        print(f"   分类：{category}")
        
        # 扫描各平台热点
        all_trends = {}
        
        for platform in platforms:
            if platform not in self.PLATFORMS:
                print(f"⚠️ 不支持的平台：{platform}")
                continue
            
            print(f"\n📱 扫描 {self.PLATFORMS[platform]['name']}...")
            
            # 模拟扫描 (实际应该调用 API 或爬虫)
            trends = self._scan_platform(platform, category)
            all_trends[platform] = trends
        
        # 分析和排序
        print(f"\n📊 分析热点...")
        analyzed_trends = self._analyze_trends(all_trends)
        
        # 生成选题建议
        print(f"\n💡 生成选题建议...")
        recommendations = self._generate_recommendations(analyzed_trends, limit)
        
        # 生成报告
        report = {
            "scanned_at": datetime.now().isoformat(),
            "platforms": platforms,
            "category": category,
            "trends": analyzed_trends,
            "recommendations": recommendations,
            "summary": {
                "total_trends": sum(len(t) for t in analyzed_trends.values()),
                "platforms_scanned": len(all_trends),
                "top_topics": len(recommendations)
            }
        }
        
        return {
            "trending_report.json": report,
            "report": report,
            "trends": analyzed_trends,
            "recommendations": recommendations
        }
    
    def _scan_platform(self, platform: str, category: str) -> List[Dict]:
        """扫描平台热点 (模拟实现)"""
        
        # 实际应该：
        # 1. 调用平台 API
        # 2. 或网页爬虫
        # 3. 或第三方数据服务
        
        # 这里使用模拟数据
        mock_trends = {
            "weibo": [
                {"title": "AI 技术发展", "heat": "爆", "rank": 1, "category": "tech"},
                {"title": "打工人日常", "heat": "热", "rank": 2, "category": "lifestyle"},
                {"title": "效率工具推荐", "heat": "沸", "rank": 3, "category": "tech"},
            ],
            "zhihu": [
                {"title": "有哪些相见恨晚的 AI 工具？", "heat": "", "rank": 1, "category": "tech"},
                {"title": "如何提高工作效率？", "heat": "", "rank": 2, "category": "lifestyle"},
            ],
            "twitter": [
                {"title": "#AI", "heat": "", "rank": 1, "category": "tech"},
                {"title": "#Productivity", "heat": "", "rank": 2, "category": "tech"},
            ],
            "douyin": [
                {"title": "AI 工具实测", "heat": "", "rank": 1, "category": "tech"},
            ],
            "bilibili": [
                {"title": "AI 工具横评", "heat": "", "rank": 1, "category": "tech"},
            ]
        }
        
        trends = mock_trends.get(platform, [])
        
        # 过滤分类
        if category != "all":
            trends = [t for t in trends if t.get("category") == category]
        
        return trends
    
    def _analyze_trends(self, all_trends: Dict) -> Dict:
        """分析热点"""
        
        analyzed = {}
        
        for platform, trends in all_trends.items():
            analyzed[platform] = []
            
            for trend in trends:
                # 计算热度分数
                heat_score = self._calculate_heat_score(trend, platform)
                
                # 分析关键词
                keywords = self._extract_keywords(trend["title"])
                
                # 评估选题价值
                topic_value = self._evaluate_topic_value(trend["title"], keywords)
                
                analyzed[platform].append({
                    "title": trend["title"],
                    "heat_score": heat_score,
                    "keywords": keywords,
                    "topic_value": topic_value,
                    "platform": platform,
                    "rank": trend.get("rank", 0),
                    "category": trend.get("category", "other")
                })
        
        return analyzed
    
    def _calculate_heat_score(self, trend: Dict, platform: str) -> float:
        """计算热度分数"""
        
        base_score = 100 - trend.get("rank", 50)
        
        # 微博特殊处理
        heat_level = trend.get("heat", "")
        if heat_level == "爆":
            base_score += 50
        elif heat_level == "热":
            base_score += 30
        elif heat_level == "沸":
            base_score += 20
        
        return min(base_score, 100)
    
    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        
        # 简单实现：分词 + 去停用词
        # 实际应该用 NLP 模型
        
        keywords = []
        
        # 提取 hashtag
        import re
        hashtags = re.findall(r'#(\w+)#', title)
        keywords.extend(hashtags)
        
        # 提取关键词 (简单分词)
        words = title.split()
        keywords.extend([w for w in words if len(w) > 1])
        
        return keywords[:5]  # 最多 5 个关键词
    
    def _evaluate_topic_value(self, title: str, keywords: List) -> Dict:
        """评估选题价值"""
        
        score = 0
        reasons = []
        
        # 包含 AI/技术关键词
        tech_keywords = ["AI", "工具", "效率", "技术", "软件"]
        if any(kw in title for kw in tech_keywords):
            score += 30
            reasons.append("技术热点")
        
        # 包含情感词
        emotion_keywords = ["相见恨晚", "绝了", "必看", "推荐"]
        if any(kw in title for kw in emotion_keywords):
            score += 20
            reasons.append("情感共鸣")
        
        # 问题形式
        if "?" in title or "？" in title:
            score += 10
            reasons.append("问题形式")
        
        # 列表形式
        if any(kw in title for kw in ["哪些", "如何", "怎么", "X 个"]):
            score += 15
            reasons.append("列表形式")
        
        return {
            "score": min(score, 100),
            "level": "high" if score >= 60 else "medium" if score >= 30 else "low",
            "reasons": reasons
        }
    
    def _generate_recommendations(self, analyzed_trends: Dict, limit: int) -> List[Dict]:
        """生成选题建议"""
        
        # 收集所有热点
        all_topics = []
        
        for platform, trends in analyzed_trends.items():
            for trend in trends:
                all_topics.append(trend)
        
        # 排序 (热度分数 + 选题价值)
        all_topics.sort(
            key=lambda x: x["heat_score"] + x["topic_value"]["score"],
            reverse=True
        )
        
        # 生成建议
        recommendations = []
        
        for i, topic in enumerate(all_topics[:limit]):
            recommendation = {
                "topic": topic["title"],
                "priority": "high" if i < 5 else "medium" if i < 10 else "low",
                "heat_score": topic["heat_score"],
                "topic_value": topic["topic_value"]["score"],
                "keywords": topic["keywords"],
                "platforms": [topic["platform"]],
                "suggested_formats": self._suggest_formats(topic),
                "reason": " + ".join(topic["topic_value"]["reasons"])
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _suggest_formats(self, topic: Dict) -> List[str]:
        """建议内容格式"""
        
        formats = []
        
        # 根据关键词建议
        keywords = topic.get("keywords", [])
        
        if any(kw in keywords for kw in ["工具", "软件", "APP"]):
            formats.extend(["文章", "视频", "图文"])
        
        if any(kw in keywords for kw in ["如何", "怎么", "教程"]):
            formats.extend(["教程视频", "图文教程"])
        
        if any(kw in keywords for kw in ["推荐", "测评", "横评"]):
            formats.extend(["测评视频", "对比文章"])
        
        return formats if formats else ["文章", "图文"]


if __name__ == "__main__":
    # 测试
    agent = TrendHunterAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "platforms": ["weibo", "zhihu", "twitter"],
        "category": "all",
        "limit": 10
    }
    
    result = agent.execute(test_input)
    
    print(f"\n✅ 热点扫描完成")
    print(f"📊 扫描平台：{result['report']['summary']['platforms_scanned']}")
    print(f"📈 总热点数：{result['report']['summary']['total_trends']}")
    print(f"💡 推荐选题：{result['report']['summary']['top_topics']}")
    
    # 展示前 3 个推荐
    print(f"\n🔥 热门选题 TOP3:")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"\n{i}. {rec['topic']}")
        print(f"   优先级：{rec['priority']}")
        print(f"   热度：{rec['heat_score']}")
        print(f"   价值：{rec['topic_value']}")
        print(f"   原因：{rec['reason']}")
