#!/usr/bin/env python3
"""
热点爬虫 - 使用第三方 API

方案：
1. B 站直接爬取 (可用)
2. 微博/知乎/抖音使用模拟数据 + 用户手动补充
3. 或集成第三方聚合 API (如聚合数据、天行数据)
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class HotSearchCrawler:
    """热点爬虫 (混合模式)"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl_bilibili(self):
        """爬取 B 站热门 (真实)"""
        print("  爬取 B 站热门...")
        
        try:
            import requests
            url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('data', {}).get('list', [])[:15]:
                topics.append({
                    "title": item.get('title', ''),
                    "rank": item.get('rank', 0),
                    "heat": item.get('stat', {}).get('view', 0),
                    "platform": "bilibili",
                    "url": item.get('short_link_v2', ''),
                    "real": True
                })
            
            print(f"    ✅ 获取 {len(topics)} 条 (真实数据)")
            return topics
            
        except Exception as e:
            print(f"    ❌ 失败：{e}")
            return []
    
    def get_simulated_trends(self):
        """获取模拟热点 (知识类)"""
        print("  生成知识类热点 (模拟)...")
        
        # 知识类话题模板
        templates = [
            "有哪些相见恨晚的{topic}？",
            "如何{action}？",
            "{topic}推荐，亲测有效！",
            "用了{time}的{topic}，说点真话",
            "别再{wrong_way}了，试试这个{topic}",
            "{topic}避坑指南",
            "零基础如何入门{topic}？",
            "提升{aspect}的{num}个方法",
        ]
        
        topics_data = {
            "topic": ["AI 工具", "效率工具", "学习工具", "时间管理", "知识管理"],
            "action": ["提高工作效率", "快速学习", "管理时间", "做好笔记"],
            "time": ["一周", "一个月", "一年", "3 个月"],
            "wrong_way": ["加班", "死记硬背", "拖延", "盲目学习"],
            "aspect": ["效率", "学习能力", "专注力", "记忆力"],
            "num": ["5", "7", "10", "3"]
        }
        
        topics = []
        for i in range(15):
            template = random.choice(templates)
            topic = template.format(
                topic=random.choice(topics_data["topic"]),
                action=random.choice(topics_data["action"]),
                time=random.choice(topics_data["time"]),
                wrong_way=random.choice(topics_data["wrong_way"]),
                aspect=random.choice(topics_data["aspect"]),
                num=random.choice(topics_data["num"])
            )
            
            topics.append({
                "title": topic,
                "rank": i + 1,
                "heat": random.randint(50, 100),
                "platform": "simulated",
                "url": "",
                "real": False
            })
        
        print(f"    ✅ 生成 {len(topics)} 条 (知识类)")
        return topics
    
    def crawl_all(self):
        """获取所有热点"""
        print("\n🕷️  开始获取热点...")
        
        all_topics = []
        
        # 真实爬取
        all_topics.extend(self.crawl_bilibili())
        
        # 模拟知识类热点
        all_topics.extend(self.get_simulated_trends())
        
        # 排序 (热度优先)
        all_topics.sort(key=lambda x: x.get('heat', 0), reverse=True)
        
        print(f"\n✅ 获取完成，共 {len(all_topics)} 条热点")
        print(f"   真实数据：{sum(1 for t in all_topics if t.get('real'))}")
        print(f"   模拟数据：{sum(1 for t in all_topics if not t.get('real'))}")
        
        return all_topics


if __name__ == "__main__":
    crawler = HotSearchCrawler()
    topics = crawler.crawl_all()
    
    # 保存结果
    output_dir = Path("/home/admin/openclaw/workspace/artifacts/raw_trends")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{timestamp}_raw_trends.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "crawled_at": datetime.now().isoformat(),
            "total": len(topics),
            "real_count": sum(1 for t in topics if t.get('real')),
            "simulated_count": sum(1 for t in topics if not t.get('real')),
            "topics": topics
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 原始数据已保存：{output_file}")
    
    # 展示 TOP10
    print(f"\n🔥 热门 TOP10:")
    for i, topic in enumerate(topics[:10], 1):
        real_flag = "🔴" if topic.get('real') else "🟡"
        print(f"{i}. {real_flag} [{topic['platform']}] {topic['title']}")
    
    print(f"\n💡 说明:")
    print(f"   🔴 = 真实爬取")
    print(f"   🟡 = 模拟数据 (知识类)")
    print(f"\n⚠️  如需真实数据，需要:")
    print(f"   1. 微博：登录 Cookie")
    print(f"   2. 知乎：API Token")
    print(f"   3. 抖音：官方 API 权限")
