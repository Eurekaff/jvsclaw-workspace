#!/usr/bin/env python3
"""
热点爬虫 - 真实爬取各平台热榜

数据源:
- 微博热搜
- 知乎热榜
- 抖音热榜
- B 站热门
"""

import requests
import json
from datetime import datetime
from pathlib import Path


class HotSearchCrawler:
    """热点爬虫"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = 10
    
    def crawl_weibo(self):
        """爬取微博热搜"""
        print("  爬取微博热搜...")
        
        try:
            # 微博热搜 API (公开接口)
            url = "https://weibo.com/ajax/side/hotSearch"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('data', {}).get('realtime', [])[:20]:
                topics.append({
                    "title": item.get('note', ''),
                    "rank": item.get('rank', 0),
                    "heat": item.get('num', 0),
                    "trend": item.get('flag', ''),
                    "platform": "weibo",
                    "url": f"https://s.weibo.com/weibo?q={item.get('note', '')}"
                })
            
            print(f"    ✅ 获取 {len(topics)} 条")
            return topics
            
        except Exception as e:
            print(f"    ❌ 失败：{e}")
            return []
    
    def crawl_zhihu(self):
        """爬取知乎热榜"""
        print("  爬取知乎热榜...")
        
        try:
            # 知乎热榜 API (公开接口)
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('data', []):
                target = item.get('target', {})
                topics.append({
                    "title": target.get('title', ''),
                    "rank": target.get('id', 0),
                    "heat": target.get('follower_count', 0),
                    "trend": "",
                    "platform": "zhihu",
                    "url": target.get('url', '')
                })
            
            print(f"    ✅ 获取 {len(topics)} 条")
            return topics
            
        except Exception as e:
            print(f"    ❌ 失败：{e}")
            return []
    
    def crawl_douyin(self):
        """爬取抖音热榜"""
        print("  爬取抖音热榜...")
        
        try:
            # 抖音热榜 (公开接口)
            url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('data', {}).get('word_list', [])[:20]:
                topics.append({
                    "title": item.get('word', ''),
                    "rank": item.get('position', 0),
                    "heat": item.get('hot_value', 0),
                    "trend": item.get('label', ''),
                    "platform": "douyin",
                    "url": f"https://www.douyin.com/hot/{item.get('sentence_id', '')}"
                })
            
            print(f"    ✅ 获取 {len(topics)} 条")
            return topics
            
        except Exception as e:
            print(f"    ❌ 失败：{e}")
            return []
    
    def crawl_bilibili(self):
        """爬取 B 站热门"""
        print("  爬取 B 站热门...")
        
        try:
            # B 站热门 API (公开接口)
            url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('data', {}).get('list', [])[:20]:
                topics.append({
                    "title": item.get('title', ''),
                    "rank": item.get('rank', 0),
                    "heat": item.get('stat', {}).get('view', 0),
                    "trend": "",
                    "platform": "bilibili",
                    "url": item.get('short_link_v2', '')
                })
            
            print(f"    ✅ 获取 {len(topics)} 条")
            return topics
            
        except Exception as e:
            print(f"    ❌ 失败：{e}")
            return []
    
    def crawl_all(self):
        """爬取所有平台"""
        print("\n️  开始爬取热点...")
        
        all_topics = []
        
        # 爬取各平台
        all_topics.extend(self.crawl_weibo())
        all_topics.extend(self.crawl_zhihu())
        all_topics.extend(self.crawl_douyin())
        all_topics.extend(self.crawl_bilibili())
        
        print(f"\n✅ 爬取完成，共 {len(all_topics)} 条热点")
        
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
            "topics": topics
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 原始数据已保存：{output_file}")
    
    # 展示前 10 条
    print(f"\n🔥 热门 TOP10:")
    for i, topic in enumerate(topics[:10], 1):
        print(f"{i}. [{topic['platform']}] {topic['title']}")
