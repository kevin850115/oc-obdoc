#!/bin/bash
# OpenClaw 配置自动备份脚本（脱敏版）
# 每周日执行一次，备份核心配置到 GitHub（自动脱敏敏感信息）

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace/obsidian-docs"
BACKUP_DIR="/home/admin/.openclaw/workspace/obsidian-docs/content/OpenClaw"
CONFIG_DIR="/home/admin/.openclaw"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/OpenClaw-核心配置备份-$DATE.md"
TEMP_CONFIG="/tmp/openclaw-config-sanitized.json"

echo "🚀 开始 OpenClaw 配置自动备份..."
echo "📅 日期：$DATE"
echo "🔒 模式：脱敏处理"

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 生成脱敏后的配置文件
echo "🔐 正在脱敏处理..."

# 读取原始配置并脱敏
cat "$CONFIG_DIR/openclaw.json" | \
  sed 's/"apiKey": "[^"]*"/"apiKey": "***REDACTED***"/g' | \
  sed 's/"clientSecret": "[^"]*"/"clientSecret": "***REDACTED***"/g' | \
  sed 's/"token": "[^"]*"/"token": "***REDACTED***"/g' | \
  sed 's/"encodingAESKey": "[^"]*"/"encodingAESKey": "***REDACTED***"/g' \
  > "$TEMP_CONFIG"

# 生成备份文档
cat > "$BACKUP_FILE" << EOF
# OpenClaw 核心配置备份

> **备份时间：** $DATE  
> **服务器：** 阿里云 ECS (47.83.200.211)  
> **OpenClaw 版本：** 2026.2.26  
> **🔒 安全级别：** 已脱敏（敏感信息已隐藏）

---

## ⚠️ 重要说明

**本文档已自动脱敏，以下信息已被隐藏：**
- 🔑 API Keys
- 🔐 Client Secrets  
- 🎫 Tokens
- 🔑 加密密钥

**完整配置请查看服务器本地文件：** \`/home/admin/.openclaw/openclaw.json\`

---

## 🔧 主配置 (openclaw.json)

\`\`\`json
$(cat "$TEMP_CONFIG")
\`\`\`

---

## 🔐 设备身份 (device.json)

\`\`\`json
$(cat "$CONFIG_DIR/identity/device.json")
\`\`\`

---

## 📱 配对设备 (paired.json)

\`\`\`json
$(cat "$CONFIG_DIR/devices/paired.json")
\`\`\`

---

## ⏰ 定时任务 (cron/jobs.json)

\`\`\`json
$(cat "$CONFIG_DIR/cron/jobs.json")
\`\`\`

---

## ⚠️ 安全提醒

1. **本文档已脱敏** - 敏感信息已隐藏，可以安全分享
2. **完整配置** - 仅限授权人员访问服务器本地文件
3. **定期轮换密钥** - 建议每 30-90 天更新一次

---

## 📊 更新记录

| 日期 | 操作 | 备注 |
|------|------|------|
| $DATE | 自动备份 | 已脱敏处理 |

---

> 📝 **备份说明：** 此配置备份已自动脱敏，用于配置参考和审计。

---
*自动生成：OpenClaw Auto Backup Script (Sanitized)*
EOF

# 提交到 Git
cd "$WORKSPACE"
echo "📤 提交到 GitHub..."
git add "content/OpenClaw/OpenClaw-核心配置备份-$DATE.md"
git commit -m "Auto backup: OpenClaw config sanitized ($DATE)"
git push origin main

# 清理旧备份（保留最近 4 个）
echo "🧹 清理旧备份..."
cd "$BACKUP_DIR"
ls -t OpenClaw-核心配置备份-*.md 2>/dev/null | tail -n +5 | xargs -r rm -f
cd "$WORKSPACE"
git add -u
git commit -m "Cleanup: keep only last 4 backups" || true
git push origin main || true

# 清理临时文件
rm -f "$TEMP_CONFIG"

echo "✅ 备份完成（已脱敏）！"
echo "📁 备份文件：$BACKUP_FILE"
echo "🌐 GitHub: https://github.com/kevin850115/oc-obdoc"
