# Self-Improvement Skill 技能说明

> **技能名称：** self-improvement  
> **用途：** 持续改进代理能力，记录错误、纠正和学习  
> **安装日期：** 2026-03-04  
> **来源：** ~/.agents/skills/self-improvement

---

## 📋 技能概述

这个技能使 AI 助手能够通过记录学习、错误和改进建议来实现自我提升。核心原则是 **"不靠脑子，靠文件"** —— 所有重要经验必须写入文件才能持久保存。

---

## 🎯 使用场景

| 情况 | 记录位置 | 类别 |
|------|----------|------|
| 命令/操作意外失败 | `.learnings/ERRORS.md` | error |
| 用户纠正你 ("不对...") | `.learnings/LEARNINGS.md` | correction |
| 用户请求不存在功能 | `.learnings/FEATURE_REQUESTS.md` | feature |
| API/外部工具失败 | `.learnings/ERRORS.md` | integration |
| 知识过时/错误 | `.learnings/LEARNINGS.md` | knowledge_gap |
| 发现更好方法 | `.learnings/LEARNINGS.md` | best_practice |

---

## 📁 文件结构

```
~/.openclaw/workspace/
├── AGENTS.md              # 多代理工作流、委托模式
├── SOUL.md                # 行为准则、性格、原则
├── TOOLS.md               # 工具能力、集成注意事项
├── MEMORY.md              # 长期记忆 (仅主会话)
├── memory/                # 每日记忆文件
│   └── YYYY-MM-DD.md
└── .learnings/            # 自改进日志
    ├── LEARNINGS.md       # 纠正、知识缺口、最佳实践
    ├── ERRORS.md          # 命令失败、异常
    └── FEATURE_REQUESTS.md # 用户请求的功能
```

---

## 📝 记录格式

### Learning 条目

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到了什么

### Details
完整上下文：发生了什么、什么是错的、什么是正确的

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (如相关)

---
```

### Error 条目

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述什么失败了

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 环境细节 (如相关)

### Suggested Fix
如果可识别，什么可能解决这个问题

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (如重复出现)

---
```

### Feature Request 条目

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要做什么

### User Context
为什么需要，解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何构建，可能扩展什么

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

---

## 🔖 ID 生成规则

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (学习), `ERR` (错误), `FEAT` (功能)
- YYYYMMDD: 当前日期
- XXX: 顺序号或随机 3 字符 (如 `001`, `A7B`)

示例：`LRN-20250115-001`, `ERR-20250115-A3F`, `FEAT-20250115-002`

---

## 📤 提升机制 (Promotion)

当学习被证明具有广泛适用性时，应提升到永久项目记忆：

| 学习类型 | 提升到 | 示例 |
|----------|--------|------|
| 行为模式 | `SOUL.md` | "简洁，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "长任务生成子代理" |
| 工具注意事项 | `TOOLS.md` | "Git push 需要先配置认证" |

### 提升流程

1. **提炼** 学习内容为简洁规则或事实
2. **添加** 到目标文件的适当部分
3. **更新** 原始条目：
   - `**Status**: pending` → `**Status**: promoted`
   - `**Promoted**: AGENTS.md` (或其他文件)

---

## 🔄 解决条目

当问题修复后，更新条目：

1. 更改 `**Status**: pending` → `**Status**: resolved`
2. 添加解决块：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 或 #42
- **Notes**: 简要描述完成的操作
```

其他状态值：
- `in_progress` - 正在处理
- `wont_fix` - 决定不处理 (在 Resolution 中说明原因)
- `promoted` - 已提升到项目记忆

---

## 🎯 优先级指南

| 优先级 | 使用场景 |
|--------|----------|
| `critical` | 阻塞核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常见工作流、重复问题 |
| `medium` | 中等影响、存在变通方案 |
| `low` | 轻微不便、边缘情况、锦上添花 |

---

## 🏷️ 区域标签

| 区域 | 范围 |
|------|------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务端代码 |
| `infra` | CI/CD、部署、Docker、云 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

---

## ✅ 最佳实践

1. **立即记录** - 问题发生后上下文最新鲜
2. **具体明确** - 未来代理需要快速理解
3. **包含复现步骤** - 特别是错误
4. **链接相关文件** - 使修复更容易
5. **建议具体修复** - 不只是"调查"
6. **使用一致类别** - 支持过滤
7. **积极提升** - 如有疑问，添加到 AGENTS.md
8. **定期审查** - 过时的学习失去价值

---

## 🔍 检测触发器

以下情况自动触发记录：

**纠正** (→ learning, category=correction):
- "不，那不对..."
- "实际上，应该是..."
- "你错了..."
- "那过时了..."

**功能请求** (→ feature request):
- "你还能..."
- "我希望你可以..."
- "有没有办法..."
- "为什么你不能..."

**知识缺口** (→ learning, category=knowledge_gap):
- 用户提供你不知道的信息
- 引用的文档过时
- API 行为与理解不同

**错误** (→ error entry):
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外输出或行为
- 超时或连接失败

---

## 📊 快速状态检查

```bash
# 统计待处理项目
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# 列出待处理高优先级项目
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# 查找特定区域的学习
grep -l "Area\*\*: backend" .learnings/*.md
```

---

## 🤖 OpenClaw 集成

### 工作空间注入

OpenClaw 自动将这些文件注入每个会话：
- `AGENTS.md` - 多代理工作流
- `SOUL.md` - 行为准则
- `TOOLS.md` - 工具使用
- `MEMORY.md` - 长期记忆 (仅主会话)
- `memory/YYYY-MM-DD.md` - 每日笔记

### 跨会话通信

OpenClaw 提供工具在不同会话间分享学习：
- `sessions_list` - 查看活跃/最近会话
- `sessions_history` - 读取另一会话的转录
- `sessions_send` - 发送学习到另一会话
- `sessions_spawn` - 生成子代理进行后台工作

---

## 📚 相关文档

- [SKILL.md](../../../.agents/skills/self-improvement/SKILL.md) - 完整技能说明
- [AGENTS.md](../AGENTS.md) - 工作区代理工作流
- [SOUL.md](../SOUL.md) - 行为准则和原则
- [TOOLS.md](../TOOLS.md) - 工具使用和本地配置

---

**安装者：** 智小月  
**安装日期：** 2026-03-04  
**版本：** 1.0.1  
**维护者：** peterskoett
