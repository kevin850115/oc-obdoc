# OpenClaw 核心配置备份

> **备份时间：** 2026-03-03  
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

## 🔧 主配置 (openclaw.json)

### 模型配置

| 提供商 | 模型 ID | 别名 | 上下文窗口 | 最大 Token |
|--------|---------|------|------------|-----------|
| dashscope-coding | qwen3.5-plus | qwen3.5-plus | 1,000,000 | 65,536 |
| dashscope | qwen3.5-plus | qwen3.5-plus | 1,000,000 | 65,536 |
| dashscope-us | qwen3-max-2025-09-23 | qwen3-max-2025-09-23 | 32,768 | 8,192 |

**默认模型：** `dashscope-coding/qwen3.5-plus`  
**默认图像模型：** `alibaba-cloud/qwen3-vl-plus`

### API 端点

```
DashScope (国际): https://dashscope.aliyuncs.com/compatible-mode/v1
DashScope (美国): https://dashscope-us.aliyuncs.com/compatible-mode/v1
DashScope Coding: https://coding.dashscope.aliyuncs.com/v1
```

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
- **Client ID:** `ding4frqsnfmjkmjwbtg`
- **DM Policy:** open
- **Group Policy:** open
- **消息类型:** markdown

#### 企业微信 (wecom)
- **Webhook Path:** `/webhooks/wecom`
- **Token:** `tE7JlFgmb1M762EHK7eJsgF2nyH21`

### 内部 Hooks

| Hook | 状态 |
|------|------|
| boot-md | ✅ |
| command-logger | ✅ |
| session-memory | ✅ |

### 工作空间

- **路径:** `/home/admin/.openclaw/workspace`
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

- **设备 ID:** `95a3136bc0d197289c981db4a05c160651fd535165fa9dc691bac594c16cee8a`
- **创建时间:** 1772186580830 (ms)
- **密钥类型:** Ed25519

---

## 🔑 设备认证 (device-auth.json)

### Operator Token
- **Token:** `qg_-OMSGDDQr6Ap4wCKzsI4dZD0E2kULQ1uQ0p0OxX4`
- **角色:** operator
- **权限范围:**
  - operator.admin
  - operator.approvals
  - operator.pairing
  - operator.read
  - operator.write
- **更新时间:** 1772247377021 (ms)

---

## ✅ 执行批准 (exec-approvals.json)

- **Socket 路径:** `/home/admin/.openclaw/exec-approvals.sock`
- **Socket Token:** `u94dcdRcdcxFEEvM1tnV6NI7XwzidavA`

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
```
http://47.83.200.211:18183
```

### SSH 登录
```bash
ssh admin@47.83.200.211
```

### 工作空间
```bash
cd /home/admin/.openclaw/workspace
```

---

## 📄 浏览器配置

- **可执行路径:** `/usr/bin/google-chrome`
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
| 2026-03-03 | 初次备份 | 完整配置导出 |
| 2026-03-03 | 同步到 GitHub | obsidian-docs 仓库 |

---

## ⚠️ 安全提醒

1. **不要公开分享此文档** - 包含 API Key、Token 等敏感信息
2. **定期轮换密钥** - 建议每 30-90 天更新一次
3. **限制访问权限** - 只有授权人员可以查看
4. **监控异常访问** - 注意 Gateway 日志中的异常请求

---

## 🔧 恢复配置

如果需要从备份恢复：

```bash
# 1. 停止 OpenClaw 服务
openclaw gateway stop

# 2. 恢复配置文件
cp OpenClaw-配置备份.md /home/admin/.openclaw/openclaw.json

# 3. 重启服务
openclaw gateway start
```

---

> 📝 **备份说明：** 此配置备份由 智小月 🌙 自动生成，用于灾难恢复和配置迁移。

---
*最后更新：2026-03-03*
