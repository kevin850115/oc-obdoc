#!/bin/bash
# 每天 18:00 发送文章待读清单提醒（移动端优化版 - markdown 链接）

# 读取待读清单
LIST_FILE="/home/admin/doc/文章/待读清单.md"

if [ ! -f "$LIST_FILE" ]; then
    echo "待读清单文件不存在"
    exit 1
fi

# 提取待读文章数量
TODO_COUNT=$(grep -c "⏳ 待读" "$LIST_FILE" 2>/dev/null || echo "0")

if [ "$TODO_COUNT" -eq 0 ]; then
    MESSAGE="📚 阅读提醒
━━━━━━━━━━━━━━━━
✅ 太棒了！待读清单已清空～

继续保持学习的热情！🌟"
else
    # 提取待读文章信息
    ARTICLES=""
    INDEX=0
    while IFS='|' read -r num name type link source date status; do
        # 跳过表头
        [[ "$num" =~ ^[[:space:]]*序号 ]] && continue
        # 清理空白
        name=$(echo "$name" | xargs)
        type=$(echo "$type" | xargs)
        link=$(echo "$link" | xargs)
        [[ -z "$name" || "$name" == "-" ]] && continue
        
        INDEX=$((INDEX + 1))
        
        # 提取纯 URL（去掉 markdown 格式）
        URL=$(echo "$link" | grep -oP '(?<=\().*(?=\))' 2>/dev/null || echo "$link")
        
        # 类型图标
        case "$type" in
            *"技术"*) ICON="🔧" ;;
            *"新闻"*) ICON="📰" ;;
            *"教程"*) ICON="📖" ;;
            *"分析"*) ICON="💡" ;;
            *"产品"*) ICON="🚀" ;;
            *"微信"*) ICON="💬" ;;
            *) ICON="📄" ;;
        esac
        
        # 使用 markdown 链接格式
        ARTICLES+="━━━━━━━━━━━━━━━━
${INDEX}. ${ICON} ${name}
   类型：${type}
   👉 [点击阅读](${URL})
"
    done < <(grep "⏳ 待读" "$LIST_FILE" | head -5)
    
    MESSAGE="📚 阅读提醒时间到
━━━━━━━━━━━━━━━━
⏳ 待读：${TODO_COUNT} 篇

${ARTICLES}
━━━━━━━━━━━━━━━━
💡 小建议
• 每天阅读 1-2 篇
• 读后标记 ✅ 已完成
• 重要内容归档笔记

📁 清单：/home/admin/doc/文章/待读清单.md"
fi

# 发送到钉钉
openclaw message send \
    --channel dingtalk \
    --target "035500048153" \
    --message "$MESSAGE" \
    2>/dev/null

echo "提醒已发送：$(date)"
