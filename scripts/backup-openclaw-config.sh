#!/bin/bash
# OpenClaw 配置自动备份脚本
# 每周日执行一次，备份核心配置到 GitHub

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace/obsidian-docs"
BACKUP_DIR="/home/admin/.openclaw/workspace/obsidian-docs/content/OpenClaw"
CONFIG_DIR="/home/admin/.openclaw"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/OpenClaw-核心配置备份-$DATE.md"

echo "🚀 开始 OpenClaw 配置自动备份..."
echo "📅 日期：$DATE"

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 生成备份文档
cat > "$BACKUP_FILE" << 'HEADER'
# OpenClaw 核心配置备份

> **备份时间：** DATE_PLACEHOLDER  
> **服务器：** 阿里云 ECS (47.83.200.211)  
> **OpenClaw 版本：** 2026.2.26  
> **⚠️ 安全警告：** 本文档包含敏感配置信息，请妥善保管！

---

## 📁 配置文件总览

| 配置文件 | 路径 | 说明 |
|---------|------|------|
| `openclaw.json` | `/home/admin/.openclaw/` | 主配置文件 |
| `device.json` | `/home/admin/.openclaw/identity/` | 设备身份 |
| `jobs.json` | `/home/admin/.openclaw/cron/` | 定时任务 |
| `exec-approvals.json` | `/home/admin/.openclaw/` | 执行批准 |
| `paired.json` | `/home/admin/.openclaw/devices/` | 配对设备 |

---

HEADER

# 替换日期占位符
sed -i "s/DATE_PLACEHOLDER/$DATE/" "$BACKUP_FILE"

# 读取并添加主配置
echo "📝 备份 openclaw.json..."
echo '## 🔧 主配置 (openclaw.json)' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"
echo '```json' >> "$BACKUP_FILE"
cat "$CONFIG_DIR/openclaw.json" >> "$BACKUP_FILE"
echo '```' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"

# 读取设备身份
echo "📝 备份 device.json..."
echo '## 🔐 设备身份 (device.json)' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"
echo '```json' >> "$BACKUP_FILE"
cat "$CONFIG_DIR/identity/device.json" >> "$BACKUP_FILE"
echo '```' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"

# 读取定时任务
echo "📝 备份 jobs.json..."
echo '## ⏰ 定时任务 (cron/jobs.json)' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"
echo '```json' >> "$BACKUP_FILE"
cat "$CONFIG_DIR/cron/jobs.json" >> "$BACKUP_FILE"
echo '```' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"

# 读取配对设备
echo "📝 备份 paired.json..."
echo '## 📱 配对设备 (paired.json)' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"
echo '```json' >> "$BACKUP_FILE"
cat "$CONFIG_DIR/devices/paired.json" >> "$BACKUP_FILE"
echo '```' >> "$BACKUP_FILE"
echo '' >> "$BACKUP_FILE"

# 添加安全提醒
cat >> "$BACKUP_FILE" << 'FOOTER'
---

## ⚠️ 安全提醒

1. **不要公开分享此文档** - 包含 API Key、Token 等敏感信息
2. **定期轮换密钥** - 建议每 30-90 天更新一次
3. **限制访问权限** - 只有授权人员可以查看
4. **监控异常访问** - 注意 Gateway 日志中的异常请求

---

## 📊 自动备份信息

- **备份频率：** 每周日自动执行
- **保留策略：** 保留最近 4 次备份
- **存储位置：** GitHub Private Repository

---

> 📝 **备份说明：** 此配置备份由 OpenClaw 自动备份脚本生成，用于灾难恢复和配置迁移。

---
*自动生成：OpenClaw Auto Backup Script*
FOOTER

# 提交到 Git
cd "$WORKSPACE"
echo "📤 提交到 GitHub..."
git add "content/OpenClaw/OpenClaw-核心配置备份-$DATE.md"
git commit -m "Auto backup: OpenClaw config ($DATE)"
git push origin main

# 清理旧备份（保留最近 4 个）
echo "🧹 清理旧备份..."
cd "$BACKUP_DIR"
ls -t OpenClaw-核心配置备份-*.md | tail -n +5 | xargs -r rm -f
cd "$WORKSPACE"
git add -u
git commit -m "Cleanup: keep only last 4 backups" || true
git push origin main || true

echo "✅ 备份完成！"
echo "📁 备份文件：$BACKUP_FILE"
echo "🌐 GitHub: https://github.com/kevin850115/oc-obdoc"
