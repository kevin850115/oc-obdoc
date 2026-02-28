# aidomain Skill 开发总结

**创建日期:** 2026-02-28  
**最后更新:** 2026-02-28  
**标签:** #aidomain #skill #开发总结 #阿里云 #域名

---

## 📋 项目概述

aidomain 是一个基于阿里云万小域 AI 的域名智能体 Skill，提供域名推荐、价格查询、可用性检查、WHOIS 查询等功能。

---

## 🎯 核心功能

### 1. 域名推荐
- 根据关键词推荐相关域名
- 支持多种后缀选择
- 提供品牌建议

### 2. 价格查询
- 查询域名注册价格
- 显示续费价格
- 提供转入价格

### 3. 可用性查询
- 检查域名是否可注册
- 提供替代建议
- 支持批量查询

### 4. WHOIS 查询
- 查询域名所有者信息
- 显示注册商信息
- 提供到期时间

### 5. 自由对话
- 域名相关知识问答
- 注册流程指导
- 问题咨询

---

## 🔧 技术实现

### API 调用

**端点:** `https://aidomain.msea.aliyun.com/sse/agent/chat`

**请求方法:** POST

**请求头:**
```javascript
{
  'Content-Type': 'application/json',
  'Cookie': '[用户 Cookie]',
  'Referer': 'https://wanwang.aliyun.com/webdesign/aidomain',
  'User-Agent': 'Mozilla/5.0...',
  'Accept': '*/*',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Pragma': 'no-cache',
  'Origin': 'https://wanwang.aliyun.com',
  'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'priority': 'u=1, i',
}
```

**请求体:**
```json
{
  "botId": "Zero3",
  "messages": [{
    "conversationId": "",
    "botId": "Zero3",
    "contentType": "text",
    "content": "用户问题",
    "role": "user",
    "type": "question"
  }]
}
```

**响应格式:** SSE (Server-Sent Events)

```
event:chat.processing
data:{"status":"processing",...}

event:message.delta
data:{"content":"部","type":"answer",...}

event:message.completed
data:{"content":"完整回复","type":"answer",...}

event:chat.completed
data:{"status":"success",...}

event:done
data:"[DONE]"
```

---

## 📁 文件结构

```
aidomain/
├── aidomain.js              # 主程序（Node.js）
├── aidomain.sh              # Bash 命令行工具
├── batch-query.js           # 批量查询工具
├── cookies.json             # Cookie 配置（纯文本）
├── manifest.json            # OpenClaw 集成配置
├── SKILL.md                 # Skill 说明文档
├── README.md                # 使用指南
├── 配置教程.md               # Cookie 配置教程
├── 命令行使用指南.md          # Bash 命令使用
├── bash 集成报告.md           # Bash 集成测试
├── Cookie 配置说明.md         # Cookie 格式说明
├── API 修复报告.md            # API 调用修复记录
├── 域名注册测试报告.md         # 域名注册功能测试
├── 测试总结.md                # 总体测试总结
├── debug.js                 # 调试脚本
├── test-parse.js            # 解析测试脚本
└── .gitignore              # Git 忽略配置
```

---

## 🚀 使用方法

### 方式 1: Node.js 直接调用

```bash
cd /home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain

# 域名推荐
node aidomain.js query "AI 科技"

# 价格查询
node aidomain.js price "example.com"

# 可用性查询
node aidomain.js check "test.com"

# WHOIS 查询
node aidomain.js whois "google.com"

# 自由对话
node aidomain.js chat "我想注册域名"
```

### 方式 2: Bash 命令

```bash
# 加载配置
source ~/.bashrc

# 使用快捷命令
ad status
ad query "AI 科技"
ad price "example.com"
ad check "test.com"
ad whois "google.com"
ad chat "域名推荐"

# 批量查询
ad batch domains.txt results.json
```

### 方式 3: OpenClaw 自动集成

在 OpenClaw 中直接调用 aidomain skill。

---

## ⚙️ 配置说明

### Cookie 配置

**文件位置:** `/home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/cookies.json`

**格式:** 纯文本（直接粘贴 Cookie 字符串）

**获取步骤:**
1. 访问 https://wanwang.aliyun.com/webdesign/aidomain
2. 登录阿里云账号
3. F12 打开开发者工具
4. Network 标签找到请求
5. 复制 Cookie 请求头
6. 粘贴到 cookies.json

**配置命令:**
```bash
ad config
```

### 快捷命令配置

**文件:** `~/.bashrc`

**配置内容:**
```bash
# 快捷指令：yf - 进入工作区
yf() {
    cd /home/admin/.openclaw/workspace-wecom-dm-yefeng
    echo "✅ 已进入工作区目录 (yf)"
    echo "当前目录：$(pwd)"
}

# aidomain 命令行工具
alias ad='/home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/aidomain.sh'
```

**使配置生效:**
```bash
source ~/.bashrc
```

---

## 🐛 已知问题

### 1. API 响应慢

**现象:** API 调用需要 6-30 秒

**原因:** 
- 阿里云 API 响应本身较慢
- SSE 流式响应需要等待完整内容
- 网络延迟

**解决方案:**
- 增加超时时间到 60 秒
- 添加重试机制
- 添加进度提示

### 2. Cookie 有效期

**现象:** Cookie 会过期（30 天 -1 年）

**解决方案:**
- 定期检查状态：`ad status`
- 发现失效重新配置：`ad config`

---

## 📊 版本历史

### v2.1 (2026-02-28) - API 修复

- ✅ 修复 HTTP Headers
- ✅ 修复 SSE 响应解析
- ✅ 修复 conversationId 处理
- ✅ 添加调试脚本

### v2.0 (2026-02-28) - Cookie 格式简化

- ✅ Cookie 改为纯文本格式
- ✅ 支持 JSON 格式（向后兼容）
- ✅ 添加 Cookie 配置说明

### v1.2 (2026-02-28) - Bash 集成

- ✅ 创建 aidomain.sh
- ✅ 添加 ad 快捷命令
- ✅ 集成到 PATH
- ✅ 交互式配置 Cookie

### v1.1 (2026-02-28) - 功能增强

- ✅ 命令模式（query/price/check/whois/chat）
- ✅ 批量查询工具
- ✅ 详细配置教程
- ✅ 文档重构

### v1.0 (2026-02-28) - 初始版本

- ✅ aidomain skill 发布
- ✅ 基础域名查询功能
- ✅ OpenClaw 集成

---

## 📞 相关资源

### 文档

- [README.md](file:///home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/README.md) - 完整使用指南
- [配置教程.md](file:///home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/配置教程.md) - Cookie 配置步骤
- [命令行使用指南.md](file:///home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/命令行使用指南.md) - Bash 命令使用
- [API 修复报告.md](file:///home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/API 修复报告.md) - API 调用修复记录

### 链接

- [阿里云万小域](https://wanwang.aliyun.com/webdesign/aidomain)
- [阿里云域名注册](https://wanwang.aliyun.com/domain)
- [GitHub Pages](https://kevin850115.github.io/oc-obdoc/)

---

## 💡 最佳实践

### 1. 定期备份 Cookie

```bash
cp /home/admin/.openclaw/workspace-wecom-dm-yefeng/skills/aidomain/cookies.json ~/backup/cookie-$(date +%Y%m%d).txt
```

### 2. 使用快捷命令

```bash
# 快速进入工作区
yf

# 快速查询
ad q "AI"
ad p "ex.com"
ad c "test.com"
```

### 3. 批量查询域名

```bash
# 创建域名列表
cat > domains.txt << EOF
example.com
test.com
demo.com
EOF

# 批量查询并保存结果
ad batch domains.txt results.json
```

### 4. 定期检查状态

```bash
# 每周检查一次
ad status
```

---

## 🎯 下一步计划

### 短期（1-2 周）

- [ ] 优化 SSE 解析逻辑
- [ ] 增加超时时间到 60 秒
- [ ] 添加重试机制
- [ ] 添加进度提示

### 中期（1-2 月）

- [ ] Web 界面
- [ ] API 接口
- [ ] 域名投资组合管理

### 长期（3-6 月）

- [ ] 域名自动抢注
- [ ] AI 域名估值
- [ ] 域名交易市场集成

---

**最后更新:** 2026-02-28  
**维护者:** aidomain 开发团队  
**状态:** ✅ 可用

---

*本文档会自动同步到 GitHub Pages*
