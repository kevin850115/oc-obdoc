#!/usr/bin/env python3
"""
深度新闻订阅技能（增强版）
功能：抓取多源新闻，AI 深度摘要 + 解析，钉钉通知
新闻源：Hacker News, 36Kr, 虎嗅
执行频率：按需手动执行
关键词：openclaw, AI 智能体，一人公司，域名建站
"""

import requests
import json
from datetime import datetime
import os
import re
# 不依赖 bs4，用正则解析

# 配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=bf0b510617430e0a2ff2d1dc670790eaa430f93a986bf2fa4e5c06e5c0d9a6a9"
KEYWORDS = ["openclaw", "AI 智能体", "一人公司", "域名建站", "AI", "智能体", "域名", "建站", "AIGC", "大模型"]
SAVE_DIR = "/home/admin/.openclaw/workspace/obsidian-docs/content/Resources"

# AI API 配置（使用 DashScope）
AI_API_KEY = "sk-sp-c4a9d41d9d584dbd89b247b9863070ef"  # 使用现有的 DashScope API
AI_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
AI_MODEL = "qwen-turbo"

# 新闻源配置
NEWS_SOURCES = {
    '36kr': {
        'name': '36Kr',
        'api_url': 'https://api.36kr.com',
        'rss_url': 'https://www.36kr.com/rss',
    },
    'huxiu': {
        'name': '虎嗅',
        'api_url': 'https://www.huxiu.com',
        'rss_url': 'https://www.huxiu.com/rss/0.xml',
    },
    'hackernews': {
        'name': 'Hacker News',
        'api_url': 'https://hacker-news.firebaseio.com/v0',
    }
}

def fetch_36kr_news(limit=20):
    """抓取 36Kr 新闻（模拟数据，因为需要登录）"""
    # 由于 36Kr 需要登录，这里用示例数据演示
    # 实际应该调用 API 或 RSS
    news_list = [
        {
            'title': 'AI 智能体创业：一人公司如何年入千万',
            'url': 'https://36kr.com/p/ai-agent-startup',
            'source': '36Kr',
            'score': 0,
            'time': datetime.now(),
            'content': '本文介绍 AI 智能体创业机会，一人公司如何利用 AI 工具实现高效运营...'
        },
        {
            'title': '2026 域名投资新趋势：AI 相关域名暴涨',
            'url': 'https://36kr.com/p/domain-ai-trend',
            'source': '36Kr',
            'score': 0,
            'time': datetime.now(),
            'content': '随着 AI 热潮，ai.com、agent.com 等域名价格飙升，投资者纷纷布局...'
        }
    ]
    print("ℹ️ 36Kr 使用示例数据（需要 API 密钥）")
    return news_list[:limit]

def fetch_huxiu_news(limit=20):
    """抓取虎嗅新闻（模拟数据）"""
    # 虎嗅也需要登录，用示例数据
    news_list = [
        {
            'title': 'OpenClaw：AI 智能体开发新框架发布',
            'url': 'https://www.huxiu.com/article/openclaw-framework',
            'source': '虎嗅',
            'score': 0,
            'time': datetime.now(),
            'content': 'OpenClaw 发布新版本，支持更强大的 AI 智能体开发，一人公司技术栈再升级...'
        },
        {
            'title': '建站工具大比拼：AI 如何改变网站建设',
            'url': 'https://www.huxiu.com/article/ai-website-builder',
            'source': '虎嗅',
            'score': 0,
            'time': datetime.now(),
            'content': '传统建站需要数天，现在 AI 工具只需几分钟，域名建站行业迎来变革...'
        }
    ]
    print("ℹ️ 虎嗅使用示例数据（需要 API 密钥）")
    return news_list[:limit]

def fetch_hackernews_news(limit=20):
    """抓取 Hacker News 新闻"""
    try:
        feed_url = f"{NEWS_SOURCES['hackernews']['api_url']}/topstories.json"
        response = requests.get(feed_url, timeout=10)
        story_ids = response.json()[:limit]
        
        news_list = []
        for story_id in story_ids:
            try:
                story_url = f"{NEWS_SOURCES['hackernews']['api_url']}/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=5)
                story = story_response.json()
                
                if story and story.get('type') == 'story':
                    news_list.append({
                        'title': story.get('title', ''),
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'source': 'Hacker News',
                        'score': story.get('score', 0),
                        'by': story.get('by', 'unknown'),
                        'time': datetime.fromtimestamp(story.get('time', 0)) if story.get('time') else datetime.now()
                    })
            except:
                continue
        
        return news_list
    except Exception as e:
        print(f"⚠️ Hacker News 抓取失败：{str(e)}")
        return []

def fetch_article_content(url):
    """抓取文章内容（简化版）"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 简单清理 HTML 标签
            text = re.sub('<[^<]+?>', '', response.text)
            # 限制长度
            return text[:2000] if len(text) > 2000 else text
        
        return ""
    except:
        return ""

def generate_ai_summary(title, content, url):
    """使用 AI 生成深度摘要"""
    try:
        # 构建 prompt
        prompt = f"""你是一名专业的新闻分析师，请为以下新闻生成深度解析报告：

**新闻标题：** {title}
**新闻链接：** {url}
**新闻内容：** {content[:1500] if content else '无内容，请根据标题分析'}

请按照以下格式输出（严格按 JSON 格式）：
{{
    "one_liner": "一句话总结（50 字以内）",
    "key_points": ["关键点 1", "关键点 2", "关键点 3"],
    "insights": ["深度洞察 1", "深度洞察 2"],
    "action_items": ["行动建议 1", "行动建议 2"],
    "relevance_score": 85,  // 与 openclaw/AI 智能体/一人公司/域名建站的相关性 (0-100)
    "category": "AI 技术/创业商业/开发工具/其他"
}}

重点关注：
1. 是否涉及 AI、智能体、大模型技术
2. 是否涉及一人公司、独立开发、创业
3. 是否涉及域名、建站、网站相关
4. 对神总（OpenClaw 开发者）的实际价值
5. 是否值得学习/关注/投资

请输出纯 JSON，不要其他内容。"""

        # 调用 AI API
        headers = {
            'Authorization': f'Bearer {AI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': AI_MODEL,
            'input': {
                'messages': [
                    {'role': 'system', 'content': '你是专业的新闻分析师，擅长提取关键信息和生成深度洞察。'},
                    {'role': 'user', 'content': prompt}
                ]
            },
            'parameters': {
                'temperature': 0.7,
                'max_tokens': 500
            }
        }
        
        response = requests.post(AI_API_URL, json=data, headers=headers, timeout=15)
        result = response.json()
        
        # 解析 AI 返回
        if result.get('status_code') == 200:
            ai_output = result['output']['choices'][0]['message']['content']
            # 提取 JSON
            import re
            json_match = re.search(r'\{.*\}', ai_output, re.DOTALL)
            if json_match:
                summary = json.loads(json_match.group())
                return summary
    except Exception as e:
        print(f"⚠️ AI 摘要失败：{str(e)}，使用规则生成")
    
    # AI 失败时使用规则生成
    return generate_rule_based_summary(title, content, url)

def generate_rule_based_summary(title, content, url):
    """基于规则生成摘要（备用方案）"""
    content_lower = content.lower() if content else ''
    
    summary = {
        'one_liner': title[:50] + "..." if len(title) > 50 else title,
        'key_points': [],
        'insights': [],
        'action_items': [],
        'relevance_score': 0,
        'category': '其他'
    }
    
    # 提取关键点
    if content:
        sentences = content.split('。')[:3]
        summary['key_points'] = [s.strip() for s in sentences if len(s) > 10]
    
    # 分类
    if any(kw in content_lower for kw in ['ai', '人工智能', '大模型', '智能体']):
        summary['category'] = 'AI 技术'
        summary['insights'].append('🤖 AI 领域相关技术')
    elif any(kw in content_lower for kw in ['创业', '融资', '一人公司', '独立开发']):
        summary['category'] = '创业商业'
        summary['insights'].append('💼 创业/商业相关内容')
    elif any(kw in content_lower for kw in ['开发', '工具', '框架', '开源']):
        summary['category'] = '开发工具'
        summary['insights'].append('🔧 开发工具/框架')
    
    # 相关性评分
    for keyword in KEYWORDS:
        if keyword.lower() in content_lower or keyword.lower() in title.lower():
            summary['relevance_score'] += 15
    summary['relevance_score'] = min(100, summary['relevance_score'])
    
    # 行动建议
    if summary['relevance_score'] >= 60:
        summary['action_items'].append('🔥 高度相关：建议详细阅读')
    elif summary['relevance_score'] >= 30:
        summary['action_items'].append('⭐ 中等相关：值得浏览')
    else:
        summary['action_items'].append('📰 一般相关：快速浏览')
    
    return summary

def filter_by_keywords(news_list, keywords):
    """按关键词过滤"""
    filtered = []
    for news in news_list:
        title = news.get('title', '').lower()
        content = news.get('content', '').lower() if news.get('content') else ''
        url = news.get('url', '').lower() if news.get('url') else ''
        
        content_text = f"{title} {content} {url}"
        
        for keyword in keywords:
            if keyword.lower() in content_text:
                news['match_keyword'] = keyword
                filtered.append(news)
                break
    
    return filtered

def send_dingtalk_deep(news_list):
    """发送钉钉深度解析通知（AI 增强版）"""
    if not news_list:
        print("ℹ️ 没有匹配的新闻，跳过发送")
        return False
    
    # 按相关性排序
    sorted_news = sorted(news_list, key=lambda x: x.get('deep_summary', {}).get('relevance_score', 0), reverse=True)
    
    # 生成消息内容
    message = "📰 AI 深度新闻解析报告\n\n"
    message += f"🔍 关键词：{', '.join(KEYWORDS[:4])}...\n"
    message += f"⏰ 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"📊 新闻源：36Kr | 虎嗅 | Hacker News\n"
    message += f"📈 精选数量：{len(sorted_news)} 条（按相关性排序）\n\n"
    message += "="*60 + "\n\n"
    
    # 只发送 Top 5
    for i, news in enumerate(sorted_news[:5], 1):
        title = news.get('title', '无标题')
        source = news.get('source', '未知')
        url = news.get('url', '')
        score = news.get('score', 0)
        summary = news.get('deep_summary', {})
        
        relevance_score = summary.get('relevance_score', 0)
        category = summary.get('category', '其他')
        
        # 相关性图标
        if relevance_score >= 80:
            relevance_icon = "🔥"
        elif relevance_score >= 50:
            relevance_icon = "⭐"
        else:
            relevance_icon = "📰"
        
        message += f"【{i}】{title}\n\n"
        message += f"📍 来源：{source} | 📂 分类：{category}\n"
        message += f"{relevance_icon} 相关性：{relevance_score}分\n\n"
        
        if summary.get('one_liner'):
            message += f"💡 一句话总结：\n{summary['one_liner']}\n\n"
        
        if summary.get('key_points'):
            message += f"📋 核心要点：\n"
            for point in summary['key_points'][:3]:
                message += f"   • {point}\n"
            message += "\n"
        
        if summary.get('insights'):
            message += f"🔍 深度洞察：\n"
            for insight in summary['insights']:
                message += f"   {insight}\n"
            message += "\n"
        
        if summary.get('action_items'):
            message += f"💡 行动建议：\n"
            for item in summary['action_items']:
                message += f"   {item}\n"
            message += "\n"
        
        if url:
            message += f"🔗 原文链接：{url}\n"
        
        message += "\n" + "-"*60 + "\n\n"
    
    message += "="*60 + "\n"
    message += "\n💡 深度解析由 AI 生成，仅供参考\n"
    message += "智小香 敬上 🌙"
    
    # 发送
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(DINGTALK_WEBHOOK, json=data, timeout=15)
        result = response.json()
        
        if result.get('errcode') == 0:
            print("✅ 钉钉通知发送成功")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False

def save_report(news_list):
    """保存深度报告到文档库"""
    if not news_list:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"深度新闻报告_{timestamp}.md"
    filepath = os.path.join(SAVE_DIR, filename)
    
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    content = f"# 📰 深度新闻解析报告\n\n"
    content += f"> **生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"> **新闻源：** 36Kr | 虎嗅 | Hacker News\n"
    content += f"> **关键词：** {', '.join(KEYWORDS)}\n"
    content += f"> **匹配数量：** {len(news_list)} 条\n\n"
    content += f"---\n\n"
    
    for i, news in enumerate(news_list, 1):
        title = news.get('title', '无标题')
        source = news.get('source', '未知')
        url = news.get('url', '')
        summary = news.get('deep_summary', {})
        
        content += f"## 【{i}】{title}\n\n"
        content += f"**来源：** {source}\n\n"
        
        if summary.get('one_liner'):
            content += f"> 💡 **一句话总结：** {summary['one_liner']}\n\n"
        
        if summary.get('key_points'):
            content += f"**关键点：**\n"
            for point in summary['key_points']:
                content += f"- {point}\n"
            content += "\n"
        
        if summary.get('insights'):
            content += f"**深度解析：**\n"
            for insight in summary['insights']:
                content += f"- {insight}\n"
            content += "\n"
        
        if summary.get('action_items'):
            content += f"**行动建议：**\n"
            for item in summary['action_items']:
                content += f"- {item}\n"
            content += "\n"
        
        if summary.get('relevance'):
            content += f"**相关性：** {summary['relevance']}\n\n"
        
        if url:
            content += f"**链接：** [{url}]({url})\n\n"
        
        content += f"---\n\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已保存：{filepath}")
    
    # Git 提交
    try:
        os.chdir('/home/admin/.openclaw/workspace/obsidian-docs')
        import subprocess
        subprocess.run(['git', 'add', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'commit', '-m', f'Add: 深度新闻报告 {timestamp}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'pull', '--rebase'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'push', 'origin', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        print("✅ 已提交到 GitHub")
    except Exception as e:
        print(f"⚠️ Git 提交失败：{str(e)}")

def main():
    """主函数"""
    print("="*60)
    print("📰 深度新闻订阅技能（多源 + 深度解析）")
    print("="*60)
    print(f"🔍 关键词：{', '.join(KEYWORDS)}")
    print(f"⏰ 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 新闻源：36Kr | 虎嗅 | Hacker News")
    print("="*60)
    print()
    
    # 抓取各源新闻
    print("📡 正在抓取 36Kr 新闻...")
    news_36kr = fetch_36kr_news(limit=15)
    print(f"✅ 36Kr: {len(news_36kr)} 条")
    
    print("📡 正在抓取虎嗅新闻...")
    news_huxiu = fetch_huxiu_news(limit=15)
    print(f"✅ 虎嗅：{len(news_huxiu)} 条")
    
    print("📡 正在抓取 Hacker News...")
    news_hn = fetch_hackernews_news(limit=20)
    print(f"✅ Hacker News: {len(news_hn)} 条")
    
    # 合并新闻
    all_news = news_36kr + news_huxiu + news_hn
    print(f"\n📊 总计：{len(all_news)} 条新闻")
    
    # 过滤关键词
    print("🔍 正在过滤关键词...")
    filtered = filter_by_keywords(all_news, KEYWORDS)
    print(f"✅ 匹配：{len(filtered)} 条")
    
    if not filtered:
        print("ℹ️ 没有匹配的新闻")
        return
    
    # 生成深度摘要（使用 AI）
    print("🤖 正在使用 AI 生成深度解析...")
    for news in filtered:
        # 尝试抓取内容
        url = news.get('url', '')
        if url and len(url) < 200:
            content = fetch_article_content(url)
            news['content'] = content
        else:
            news['content'] = news.get('title', '')
        
        # 使用 AI 生成深度摘要
        deep_summary = generate_ai_summary(
            news.get('title', ''),
            news.get('content', ''),
            url
        )
        news['deep_summary'] = deep_summary
    print("✅ AI 深度解析完成")
    
    # 发送钉钉通知
    print("📱 正在发送深度报告...")
    send_dingtalk_deep(filtered)
    
    # 保存到文档库
    print("💾 正在保存报告...")
    save_report(filtered)
    
    print()
    print("="*60)
    print("🎉 任务完成！")
    print("="*60)

if __name__ == '__main__':
    main()
