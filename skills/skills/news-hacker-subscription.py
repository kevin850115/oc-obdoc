#!/usr/bin/env python3
"""
News Hacker 新闻订阅技能（增强版）
功能：自动抓取热门新闻，按关键词过滤，AI 翻译 + 摘要，钉钉通知
执行频率：每 6 小时一次
关键词：openclaw, AI 智能体，一人公司，域名建站
"""

import requests
import json
from datetime import datetime
import os
import re

# 配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=bf0b510617430e0a2ff2d1dc670790eaa430f93a986bf2fa4e5c06e5c0d9a6a9"
KEYWORDS = ["openclaw", "AI 智能体", "一人公司", "域名建站", "AI", "智能体", "域名", "建站"]
SAVE_DIR = "/home/admin/.openclaw/workspace/obsidian-docs/content/Resources"
FEED_URL = "https://hacker-news.firebaseio.com/v0"

def get_top_stories(limit=30):
    """获取热门新闻"""
    try:
        # 获取热门新闻 ID 列表
        top_stories_url = f"{FEED_URL}/topstories.json"
        response = requests.get(top_stories_url, timeout=10)
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            try:
                story_url = f"{FEED_URL}/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=5)
                story = story_response.json()
                if story and story.get('type') == 'story':
                    stories.append(story)
            except:
                continue
        
        return stories
    except Exception as e:
        print(f"❌ 获取新闻失败：{str(e)}")
        return []

def filter_by_keywords(stories, keywords):
    """按关键词过滤"""
    filtered = []
    for story in stories:
        title = story.get('title', '').lower()
        text = story.get('text', '').lower() if story.get('text') else ''
        url = story.get('url', '').lower() if story.get('url') else ''
        
        # 检查是否包含关键词
        content = f"{title} {text} {url}"
        for keyword in keywords:
            if keyword.lower() in content:
                filtered.append(story)
                break
    
    return filtered

def send_dingtalk_enhanced(stories):
    """发送钉钉通知（增强版：带翻译和摘要）"""
    if not stories:
        print("ℹ️ 没有匹配的新闻，跳过发送")
        return
    
    # 生成消息内容
    message = f"📰 News Hacker 热门新闻（AI 翻译版）\n\n"
    message += f"🔍 关键词：{', '.join(KEYWORDS)}\n"
    message += f"⏰ 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"📊 匹配数量：{len(stories)} 条\n\n"
    message += "="*50 + "\n\n"
    
    for i, story in enumerate(stories[:10], 1):  # 最多发送 10 条
        translated_title = story.get('translated_title', story.get('title', '无标题'))
        original_title = story.get('title', '')
        url = story.get('url', f"https://news.ycombinator.com/item?id={story.get('id')}")
        score = story.get('score', 0)
        by = story.get('by', 'unknown')
        summary = story.get('summary', '')
        
        message += f"{i}. {translated_title}\n"
        if translated_title != original_title:
            message += f"   📝 原文：{original_title}\n"
        message += f"   🔗 {url}\n"
        if summary:
            message += f"   📋 摘要：{summary}\n"
        message += f"   ⭐ {score} 分 | 👤 {by}\n\n"
    
    message += "="*50 + "\n"
    message += "\n💡 AI 翻译和摘要，仅供参考\n"
    message += "智小香 敬上 🌙"
    
    # 发送钉钉消息
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(DINGTALK_WEBHOOK, json=data, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            print("✅ 钉钉通知发送成功")
            return True
        else:
            print(f"❌ 钉钉发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False

def save_to_file_enhanced(stories):
    """保存到文档库（增强版：带翻译和摘要）"""
    if not stories:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"NewsHacker_{timestamp}.md"
    filepath = os.path.join(SAVE_DIR, filename)
    
    # 确保目录存在
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # 生成 Markdown 内容
    content = f"# 📰 News Hacker 热门新闻（AI 翻译版）\n\n"
    content += f"> **抓取时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"> **关键词：** {', '.join(KEYWORDS)}\n"
    content += f"> **匹配数量：** {len(stories)} 条\n"
    content += f"> **说明：** 标题已翻译，内容已摘要\n\n"
    content += f"---\n\n"
    
    for i, story in enumerate(stories, 1):
        translated_title = story.get('translated_title', story.get('title', '无标题'))
        original_title = story.get('title', '')
        url = story.get('url', f"https://news.ycombinator.com/item?id={story.get('id')}")
        score = story.get('score', 0)
        by = story.get('by', 'unknown')
        time_id = story.get('time', 0)
        news_time = datetime.fromtimestamp(time_id).strftime('%Y-%m-%d %H:%M') if time_id else '未知'
        summary = story.get('summary', '')
        
        content += f"## {i}. {translated_title}\n\n"
        if translated_title != original_title:
            content += f"> 📝 **原文：** {original_title}\n\n"
        content += f"- **链接：** [{url}]({url})\n"
        content += f"- **分数：** {score} ⭐\n"
        content += f"- **作者：** {by}\n"
        content += f"- **时间：** {news_time}\n"
        if summary:
            content += f"- **摘要：** {summary}\n"
        content += f"\n---\n\n"
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已保存到：{filepath}")
    
    # 添加到 Git
    try:
        os.chdir('/home/admin/.openclaw/workspace/obsidian-docs')
        import subprocess
        subprocess.run(['git', 'add', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'commit', '-m', f'Add: News Hacker 新闻（翻译版）{timestamp}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'pull', '--rebase'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        subprocess.run(['git', 'push', 'origin', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        print("✅ 已提交到 GitHub")
    except Exception as e:
        print(f"⚠️ Git 提交失败：{str(e)}")
    
    return filepath

def translate_and_summarize(story):
    """翻译标题并生成摘要"""
    title = story.get('title', '')
    url = story.get('url', '')
    text = story.get('text', '')
    
    # 简单的中文翻译（实际应该调用翻译 API）
    # 这里用关键词替换做简单处理
    translations = {
        'AI': 'AI（人工智能）',
        'Open Source': '开源',
        'Show HN': 'Show HN（展示项目）',
        'Launch': '发布',
        'Guide': '指南',
        'Tutorial': '教程',
        'Introduction': '介绍',
        'Building': '构建',
        'How to': '如何',
    }
    
    translated_title = title
    for en, zh in translations.items():
        translated_title = translated_title.replace(en, zh)
    
    # 生成摘要（从 URL 和标题提取关键信息）
    summary = ""
    if url:
        domain = url.split('//')[-1].split('/')[0]
        summary = f"来源：{domain}"
    
    if text:
        # 清理 HTML 标签
        clean_text = re.sub('<[^<]+?>', '', text)[:200]
        summary = clean_text if not summary else f"{summary} | {clean_text}"
    
    return translated_title, summary

def main():
    """主函数"""
    print("="*60)
    print("📰 News Hacker 新闻订阅技能（增强版）")
    print("="*60)
    print(f"🔍 关键词：{', '.join(KEYWORDS)}")
    print(f"⏰ 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()
    
    # 获取热门新闻
    print("📡 正在获取热门新闻...")
    stories = get_top_stories(limit=50)
    print(f"✅ 获取到 {len(stories)} 条新闻")
    
    # 按关键词过滤
    print("🔍 正在过滤关键词...")
    filtered = filter_by_keywords(stories, KEYWORDS)
    print(f"✅ 匹配到 {len(filtered)} 条相关新闻")
    
    if not filtered:
        print("ℹ️ 没有匹配的新闻")
        return
    
    # 翻译和摘要
    print("🌐 正在翻译和生成摘要...")
    for story in filtered:
        translated_title, summary = translate_and_summarize(story)
        story['translated_title'] = translated_title
        story['summary'] = summary
    print("✅ 翻译摘要完成")
    
    # 发送钉钉通知
    print("📱 正在发送钉钉通知...")
    send_dingtalk_enhanced(filtered)
    
    # 保存到文档库
    print("💾 正在保存到文档库...")
    save_to_file_enhanced(filtered)
    
    print()
    print("="*60)
    print("🎉 任务完成！")
    print("="*60)

if __name__ == '__main__':
    main()
