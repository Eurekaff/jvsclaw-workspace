#!/usr/bin/env python3
"""
PlatformAdapter Agent - 平台适配 Agent

核心职责：
1. 将核心内容适配到不同平台
2. 调整语气、格式、emoji、标签
3. 确保符合各平台风格
4. 生成多平台版本

支持平台：
- 小红书 (xiaohongshu)
- 抖音 (douyin)
- 公众号 (wechat_official)
- 微博 (weibo)
- B 站 (bilbili)
- Twitter (twitter)
- LinkedIn (linkedin)
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


class PlatformAdapterAgent(AgentBase):
    AGENT_NAME = "PlatformAdapterAgent"
    STAGE_NAME = "platform_adapter"
    ROLE_DESCRIPTION = "平台适配专家，将内容精准适配到各社交媒体平台"
    
    INPUT_FILES = ["core_content.json"]
    OUTPUT_FILES = ["platform_versions.json"]
    
    # 各平台风格配置
    PLATFORM_STYLES = {
        "xiaohongshu": {
            "name": "小红书",
            "max_length": 800,
            "min_length": 300,
            "title_max_length": 20,
            "emoji_level": "high",  # high/medium/low
            "tone": "sister_chat",  # 姐妹聊天式
            "structure": "pain_point + experience + comparison + recommend",
            "tags_count": (5, 10),
            "format": "markdown",
            "features": [
                "emoji 开头",
                "姐妹称呼",
                "情绪化表达",
                "个人体验",
                "前后对比",
                "小缺点",
                "标签"
            ]
        },
        "douyin": {
            "name": "抖音",
            "max_length": 300,  # 脚本字数
            "duration": 60,  # 秒
            "hook_time": 3,  # 开头钩子时间
            "emoji_level": "medium",
            "tone": "dramatic",  # 戏剧化
            "structure": "hook + pain_amplify + solution + demo + cta",
            "format": "script",
            "features": [
                "3 秒钩子",
                "快节奏",
                "镜头标注",
                "BGM 建议",
                "字幕",
                "互动引导"
            ]
        },
        "wechat_official": {
            "name": "公众号",
            "max_length": 3000,
            "min_length": 1500,
            "title_max_length": 30,
            "emoji_level": "low",
            "tone": "professional_friendly",  # 专业且亲和
            "structure": "story + analysis + advice + quote",
            "format": "markdown",
            "features": [
                "深度内容",
                "小标题",
                "个人故事",
                "实用建议",
                "金句总结",
                "引导关注"
            ]
        },
        "weibo": {
            "name": "微博",
            "max_length": 140,
            "emoji_level": "medium",
            "tone": "casual",  # 随意
            "structure": "topic + opinion + emotion + question",
            "tags_count": (1, 3),
            "format": "text",
            "features": [
                "蹭热点",
                "话题标签",
                "简短",
                "互动提问"
            ]
        },
        "bilibili": {
            "name": "B 站",
            "duration": 600,  # 秒 (10 分钟)
            "emoji_level": "high",
            "tone": "fun_educational",  # 有趣 + 干货
            "structure": "funny_opening + content + meme + emotion + cta",
            "format": "script",
            "features": [
                "玩梗开头",
                "干货内容",
                "弹幕互动点",
                "情感共鸣",
                "三连引导"
            ]
        },
        "twitter": {
            "name": "Twitter",
            "max_length": 280,  # 字符
            "emoji_level": "low",
            "tone": "direct",  # 直接
            "structure": "highlight + details + link + hashtags",
            "tags_count": (2, 3),
            "format": "text",
            "features": [
                "简洁",
                "直接",
                "链接",
                "英文标签"
            ]
        },
        "linkedin": {
            "name": "LinkedIn",
            "max_length": 1000,
            "min_length": 500,
            "emoji_level": "low",
            "tone": "professional",  # 专业
            "structure": "hook + insights + list + question",
            "format": "text",
            "features": [
                "职场相关",
                "专业洞察",
                "列表式",
                "互动提问"
            ]
        }
    }
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行平台适配"""
        
        # 获取核心内容
        core_content = input_data.get("core_content", {})
        topic = core_content.get("topic", "")
        content = core_content.get("content", "")
        selling_points = core_content.get("selling_points", [])
        target_audience = core_content.get("target_audience", "")
        
        # 获取目标平台
        target_platforms = input_data.get("platforms", ["xiaohongshu", "weibo", "twitter"])
        
        # 为每个平台生成适配版本
        platform_versions = {}
        
        for platform in target_platforms:
            if platform not in self.PLATFORM_STYLES:
                print(f"⚠️ 不支持的平台：{platform}")
                continue
            
            print(f"\n📱 适配 {self.PLATFORM_STYLES[platform]['name']}...")
            
            # 生成适配内容
            adapted = self._adapt_to_platform(
                content=content,
                topic=topic,
                selling_points=selling_points,
                target_audience=target_audience,
                platform_style=self.PLATFORM_STYLES[platform]
            )
            
            platform_versions[platform] = adapted
        
        # 保存结果
        result = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "platforms": target_platforms,
            "versions": platform_versions,
            "summary": {
                "total_platforms": len(platform_versions),
                "platforms_done": list(platform_versions.keys())
            }
        }
        
        return {
            "platform_versions.json": result,
            "platform_versions": platform_versions
        }
    
    def _adapt_to_platform(self, content: str, topic: str, 
                          selling_points: List, target_audience: str,
                          platform_style: Dict) -> Dict:
        """适配到特定平台"""
        
        platform_name = platform_style["name"]
        
        # 根据平台类型调用不同的适配方法
        format_type = platform_style.get("format", "text")
        
        if format_type == "script":
            # 视频脚本类 (抖音、B 站)
            adapted = self._adapt_script(content, topic, selling_points, platform_style)
        else:
            # 文本类 (小红书、微博、公众号等)
            adapted = self._adapt_text(content, topic, selling_points, platform_style)
        
        # 真人化检查
        authenticity_score = self._check_authenticity(adapted, platform_style)
        
        return {
            "platform": platform_name,
            "content": adapted,
            "style": platform_style,
            "authenticity_score": authenticity_score,
            "word_count": len(adapted.get("text", adapted.get("script", ""))),
            "generated_at": datetime.now().isoformat()
        }
    
    def _adapt_text(self, content: str, topic: str, 
                   selling_points: List, style: Dict) -> Dict:
        """适配文本内容"""
        
        emoji_level = style.get("emoji_level", "medium")
        tone = style.get("tone", "neutral")
        max_length = style.get("max_length", 500)
        
        # 生成标题
        title = self._generate_title(topic, style)
        
        # 生成正文
        text = self._generate_text(content, selling_points, style)
        
        # 生成标签
        tags = self._generate_tags(topic, style)
        
        # 生成 emoji
        if emoji_level != "low":
            text = self._add_emojis(text, emoji_level)
        
        # 截断到合适长度
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        
        return {
            "type": "text",
            "title": title,
            "text": text,
            "tags": tags,
            "format": style.get("format", "text")
        }
    
    def _adapt_script(self, content: str, topic: str, 
                     selling_points: List, style: Dict) -> Dict:
        """适配视频脚本"""
        
        duration = style.get("duration", 60)
        platform_name = style.get("name", "")
        
        # 抖音脚本结构
        if "抖音" in platform_name:
            script = self._generate_douyin_script(content, selling_points, duration)
        # B 站脚本结构
        elif "B 站" in platform_name:
            script = self._generate_bilibili_script(content, selling_points, duration)
        else:
            script = self._generate_generic_script(content, selling_points, duration)
        
        return {
            "type": "script",
            "script": script,
            "duration": duration,
            "format": "script"
        }
    
    def _generate_title(self, topic: str, style: Dict) -> str:
        """生成标题"""
        
        emoji_level = style.get("emoji_level", "medium")
        max_length = style.get("title_max_length", 30)
        
        # 小红书标题风格
        if style.get("tone") == "sister_chat":
            emojis = ["😭", "😱", "💯", "✨", "🔥"] if emoji_level == "high" else ["✨"]
            emoji = emojis[0] if emojis else ""
            title = f"{emoji} {topic}！真的绝了！！"
        
        # 公众号标题风格
        elif style.get("tone") == "professional_friendly":
            title = f"我花了 3 万块，买了这个教训：关于{topic}的深度思考"
        
        # 微博标题风格
        elif style.get("tone") == "casual":
            title = f"# {topic}# 用了 1 个月，说点真话"
        
        else:
            title = topic
        
        # 截断
        if len(title) > max_length:
            title = title[:max_length]
        
        return title
    
    def _generate_text(self, content: str, selling_points: List, style: Dict) -> str:
        """生成正文"""
        
        tone = style.get("tone", "neutral")
        
        # 小红书风格
        if tone == "sister_chat":
            text = self._generate_xiaohongshu_style(content, selling_points)
        # 微博风格
        elif tone == "casual":
            text = self._generate_weibo_style(content, selling_points)
        # 公众号风格
        elif tone == "professional_friendly":
            text = self._generate_wechat_style(content, selling_points)
        # LinkedIn 风格
        elif tone == "professional":
            text = self._generate_linkedin_style(content, selling_points)
        else:
            text = content
        
        return text
    
    def _generate_xiaohongshu_style(self, content: str, selling_points: List) -> str:
        """小红书风格文案"""
        
        text = """
姐妹们！！我真的要按头安利这个！！💯

作为一个常年{audience}的人
我之前也踩过很多坑😢
但是这个！！真的用一次就爱了！！

✨使用感受：
{selling_points}

说实话，{small_flaw}
但是！！效果真的没话说！
我已经回购第三瓶了！！

姐妹们冲！不踩雷！！
""".format(
            audience="熬夜/追求品质",
            selling_points="\n".join([f"- {sp}" for sp in selling_points[:3]]),
            small_flaw="包装一般般/价格小贵"
        )
        
        return text.strip()
    
    def _generate_weibo_style(self, content: str, selling_points: List) -> str:
        """微博风格文案"""
        
        text = """
# {topic}# 用了 1 个月，说点真话：

1. 确实有效果
2. 但需要坚持
3. 性价比还行

你们觉得呢？评论区聊聊👇
""".format(topic="AI 工具")
        
        return text.strip()
    
    def _generate_wechat_style(self, content: str, selling_points: List) -> str:
        """公众号风格文案"""
        
        text = """
## 开头

去年这个时候，我也和很多人一样迷茫...

## 我的经历

那是一个普通的周一，我接到了改变想法的电话...

## 深度分析

为什么会出现这种情况？我总结了 3 点：

1. **第一点**：{point1}
2. **第二点**：{point2}
3. **第三点**：{point3}

## 实用建议

如果你也遇到类似问题，建议这样做：

- 建议 1
- 建议 2
- 建议 3

## 结尾

成长，就是不断试错的过程。

愿我们都能成为更好的自己。
""".format(
            point1=selling_points[0] if selling_points else "...",
            point2=selling_points[1] if len(selling_points) > 1 else "...",
            point3=selling_points[2] if len(selling_points) > 2 else "..."
        )
        
        return text.strip()
    
    def _generate_linkedin_style(self, content: str, selling_points: List) -> str:
        """LinkedIn 风格文案"""
        
        text = """
【3 个洞察，让我从{role}晋升为{target}】

{years}年职场生涯，我总结了几个关键习惯：

1️⃣ {habit1}

2️⃣ {habit2}

3️⃣ {habit3}

职场没有捷径，但有方法。

你在实践中有什么心得？欢迎分享👇

#职场 #成长 #领导力
""".format(
            role="工程师",
            target="总监",
            years="15",
            habit1=selling_points[0] if selling_points else "持续学习",
            habit2=selling_points[1] if len(selling_points) > 1 else "主动承担",
            habit3=selling_points[2] if len(selling_points) > 2 else "建立人脉"
        )
        
        return text.strip()
    
    def _generate_douyin_script(self, content: str, selling_points: List, 
                                duration: int) -> str:
        """抖音脚本"""
        
        script = """
【0-3s】钩子
⚠️千万别买这个！除非你想...

【3-10s】痛点
是不是经常...？
用了很多方法都没用？

【10-30s】解决方案
试试这个！我用了{days}天
（展示使用过程）

【30-50s】效果
看！这是之前...
这是现在...

【50-60s】互动
想知道是什么吗？
评论区告诉我！

BGM 建议：热门轻快节奏
字幕：关键词高亮
""".format(days=7)
        
        return script.strip()
    
    def _generate_bilibili_script(self, content: str, selling_points: List,
                                  duration: int) -> str:
        """B 站脚本"""
        
        script = """
【0-30s】有趣开头
（玩梗/鬼畜）
"前方高能！非战斗人员撤离！"

【30s-2min】内容引入
今天要给大家深度测评...

【2min-8min】干货内容
1. 第一点...
   （弹幕互动点："懂了"）
   
2. 第二点...
   （弹幕互动点："真实"）
   
3. 第三点...
   （弹幕互动点："泪目"）

【8min-9min】情感共鸣
其实...（走心时刻）

【9min-10min】结尾
求点赞！投币！收藏！
三连走一波！

BGM：根据情绪变化
字幕：大字体 + 关键词高亮
""".strip()
        
        return script
    
    def _generate_generic_script(self, content: str, selling_points: List,
                                duration: int) -> str:
        """通用脚本"""
        return self._generate_douyin_script(content, selling_points, duration)
    
    def _generate_tags(self, topic: str, style: Dict) -> List[str]:
        """生成标签"""
        
        tags_count = style.get("tags_count", (3, 5))
        min_tags, max_tags = tags_count
        
        # 基础标签
        base_tags = [topic.replace(" ", ""), "推荐", "分享"]
        
        # 平台特定标签
        if "小红书" in style.get("name", ""):
            platform_tags = ["好物分享", "种草", "测评", "必备", "安利"]
        elif "微博" in style.get("name", ""):
            platform_tags = ["热点", "讨论"]
        elif "Twitter" in style.get("name", ""):
            platform_tags = ["AI", "Tech"]
        else:
            platform_tags = []
        
        all_tags = base_tags + platform_tags
        return all_tags[:max_tags]
    
    def _add_emojis(self, text: str, level: str) -> str:
        """添加 emoji"""
        
        emoji_map = {
            "high": ["😭", "😱", "💯", "✨", "🔥", "💖", "😍", "", "✅", "❌"],
            "medium": ["✨", "💯", "", "👍", "✅"],
            "low": ["✨", "👍"]
        }
        
        emojis = emoji_map.get(level, emoji_map["medium"])
        
        # 简单实现：在句首和句尾添加
        lines = text.split("\n")
        enhanced_lines = []
        
        for line in lines:
            if line.strip() and len(line) > 5:
                import random
                emoji = random.choice(emojis)
                enhanced_lines.append(f"{emoji} {line}")
            else:
                enhanced_lines.append(line)
        
        return "\n".join(enhanced_lines)
    
    def _check_authenticity(self, adapted: Dict, style: Dict) -> Dict:
        """检查真人化程度（简化版）"""
        
        text = adapted.get("text", adapted.get("script", ""))
        
        score = 10  # 基础分
        
        # 检查个人故事
        if any(word in text for word in ["我", "我的", "我个人"]):
            score += 2
        
        # 检查情绪词
        if any(word in text for word in ["真的", "绝了", "太", "超级"]):
            score += 2
        
        # 检查互动
        if "?" in text or "？" in text:
            score += 1
        
        # 检查 emoji
        if style.get("emoji_level") == "high" and "✨" in text:
            score += 1
        
        # 检查小缺点
        if any(word in text for word in ["但是", "不过", "说实话"]):
            score += 2
        
        # 上限 10 分
        score = min(score, 10)
        
        return {
            "score": score,
            "level": "high" if score >= 8 else "medium" if score >= 6 else "low",
            "suggestions": [] if score >= 7 else ["增加个人故事", "添加情绪词", "增加互动"]
        }


if __name__ == "__main__":
    # 测试
    agent = PlatformAdapterAgent("/home/admin/openclaw/workspace")
    
    test_input = {
        "core_content": {
            "topic": "AI 工具推荐",
            "content": "这是一款非常好用的 AI 工具，可以提高工作效率。",
            "selling_points": [
                "提高效率 10 倍",
                "节省时间",
                "易于上手"
            ],
            "target_audience": "打工人"
        },
        "platforms": ["xiaohongshu", "douyin", "weibo", "twitter"]
    }
    
    result = agent.execute(test_input)
    
    print(f"\n✅ 平台适配完成")
    versions = result.get('platform_versions', {})
    print(f"📱 适配平台：{len(versions)}")
    
    # 展示一个示例
    if versions:
        platform = list(versions.keys())[0]
        version = versions[platform]
        print(f"\n📝 {version.get('platform', '')} 示例:")
        content = version.get('content', {})
        print(content.get('text', content.get('script', ''))[:500])
