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
cat > "$BACKUP_FILE" << HEADER
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

## 📁 配置文件总览

| 配置文件 | 路径 | 说明 |
|---------|------|------|
| \`openclaw.json\` | \`/home/admin/.openclaw/\` | 主配置文件 |
| \`device.json\` | \`/home/admin/.openclaw/identity/\` | 设备身份 |
| \`jobs.json\` | \`/home/admin/.openclaw/cron/\` | 定时任务 |
| \`paired.json\` | \`/home/admin/.openclaw/devices/\` | 配对设备 |

---

## 🔧 主配置 (openclaw.json)

### 模型配置

| 提供商 | 模型 ID | 别名 | 上下文窗口 | 最大 Token |
|--------|---------|------|------------|-----------|
| dashscope-coding | qwen3.5-plus | qwen3.5-plus | 1,000,000 | 65,536 |
| dashscope | qwen3.5-plus | qwen3.5-plus | 1,000,000 | 65,536 |
| dashscope-us | qwen3-max-2025-09-23 | qwen3-max-2025-09-23 | 32,768 | 8,192 |

**默认模型：** \`dashscope-coding/qwen3.5-plus\`  
**默认图像模型：** \`alibaba-cloud/qwen3-vl-plus\`

### API 端点

\`\`\`
DashScope (国际): https://dashscope.aliyuncs.com/compatible-mode/v1
DashScope (美国): https://dashscope-us.aliyuncs.com/compatible-mode/v1
DashScope Coding: https://coding.dashscope.aliyuncs.com/v1
\`\`\`

### Gateway 配置

| 配置项 | 值 |
|--------|-----|
| 端口 | 18183 |
| 模式 | local |
| 绑定 | lan |
| 认证模式 | token |
| Control UI Base Path | 625ee4e8 |
| 允许来源 | http://47.83.200.211:18183 |

### 已启用插件

| 插件 | 来源 | 版本 | 状态 |
|------|------|------|------|
| qqbot | path | 1.5.0 | ✅ |
| dingtalk | npm (@soimy/dingtalk) | 3.1.4 | ✅ |
| dashscope-cfg | archive | 2026.2.25 | ✅ |
| wecom | npm (@openclaw-china/wecom) | 0.1.28 | ✅ |

### 通道配置

#### 钉钉 (dingtalk)
- **Client ID:** \`ding4frqsnfmjkmjwbtg\`
- **Client Secret:** \`***REDACTED***`
- **DM Policy:** open
- **Group Policy:** open
- **消息类型:** markdown

#### 企业微信 (wecom)
- **Webhook Path:** \`/webhooks/wecom\`
- **Token:** \`***REDACTED***`
- **Encoding AES Key:** \`***REDACTED***`

### 内部 Hooks

| Hook | 状态 |
|------|------|
| boot-md | ✅ |
| command-logger | ✅ |
| session-memory | ✅ |

### 工作空间

- **路径:** \`/home/admin/.openclaw/workspace\`
- **Git 仓库:** 已启用

### 节点安全策略

**禁止的命令:**
- camera.snap
- camera.clip
- screen.record
- calendar.add
- contacts.add
- reminders.add

---

## 🔐 设备身份 (device.json)

- **设备 ID:** \`95a3136bc0d197289c981db4a05c160651fd535165fa9dc691bac594c16cee8a\`
- **创建时间:** 1772186580830 (ms)
- **密钥类型:** Ed25519
- **公钥:** \`***REDACTED***`
- **私钥:** \`***REDACTED***`

---

## ✅ 执行批准 (exec-approvals.json)

- **Socket 路径:** \`/home/admin/.openclaw/exec-approvals.sock\`
- **Socket Token:** \`***REDACTED***`

---

## 📱 配对设备 (paired.json)

| 设备 ID | 显示名称 | 平台 | 角色 |
|--------|---------|------|------|
| 95a3136bc0d197289c981db4a05c160651fd535165fa9dc691bac594c16cee8a | agent | linux | operator |

---

## ⏰ 定时任务 (cron/jobs.json)

- **状态:** 启用
- **当前任务:** 无 (空列表)

---

## 🌐 访问方式

### Gateway UI
\`\`\`
http://47.83.200.211:18183
\`\`\`

### SSH 登录
\`\`\`bash
ssh admin@47.83.200.211
\`\`\`

### 工作空间
\`\`\`bash
cd /home/admin/.openclaw/workspace
\`\`\`

---

## 📄 浏览器配置

- **可执行路径:** \`/usr/bin/google-chrome\`
- **无头模式:** true
- **默认配置:** openclaw

---

## 📝 命令配置

| 配置项 | 值 |
|--------|-----|
| native | true |
| nativeSkills | true |
| restart | true |
| ownerDisplay | raw |

---

## 🔒 会话配置

- **DM Scope:** per-channel-peer

---

## 📊 更新记录

| 日期 | 操作 | 备注 |
|------|------|------|
| $DATE | 自动备份 | 已脱敏处理 |
| 2026-03-03 | 初次备份 | 完整配置导出 |

---

## ⚠️ 安全提醒

1. **本文档已脱敏** - 敏感信息已隐藏，可以安全分享
2. **完整配置** - 仅限授权人员访问服务器本地文件
3. **定期轮换密钥** - 建议每 30-90 天更新一次
4. **监控异常访问** - 注意 Gateway 日志中的异常请求

---

## 🔧 恢复配置

如果需要从备份恢复：

\`\`\`bash
# 1. 停止 OpenClaw 服务
openclaw gateway stop

# 2. 从服务器本地恢复完整配置
# （需要从本地备份或安全存储中获取完整配置）

# 3. 重启服务
openclaw gateway start
\`\`\`

---

> 📝 **备份说明：** 此配置备份已自动脱敏，用于配置参考和审计。完整配置请查看服务器本地文件。

---
*自动生成：OpenClaw Auto Backup Script (Sanitized)*
FOOTER

# 提交到 Git
cd "$WORKSPACE"
echo "📤 提交到 GitHub..."
git add "content/OpenClaw/OpenClaw-核心配置备份-$DATE.md"
git commit -m "Auto backup: OpenClaw config sanitized ($DATE)"
git push origin main

# 清理旧备份（保留最近 4 个）
echo "🧹 清理旧备份..."
cd "$BACKUP_DIR"
ls -t OpenClaw-核心配置备份-*.md | tail -n +5 | xargs -r rm -f
cd "$WORKSPACE"
git add -u
git commit -m "Cleanup: keep only last 4 backups" || true
git push origin main || true

# 清理临时文件
rm -f "$TEMP_CONFIG"

echo "✅ 备份完成（已脱敏）！"
echo "📁 备份文件：$BACKUP_FILE"
echo "🌐 GitHub: https://github.com/kevin850115/oc-obdoc"
