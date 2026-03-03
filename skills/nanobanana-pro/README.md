# Nanobanana Pro - AI 生图应用 🍌

完整的文生图 Web 应用，基于 idealab API。

## 🚀 快速开始

### 1. 安装后端依赖

```bash
cd /home/admin/.openclaw/workspace/skills/nanobanana-pro/backend
npm install
```

### 2. 配置 API Key

编辑 `backend/config.js`：

```js
module.exports = {
  openai: {
    apiKey: 'your-api-key-here',  // 替换为你的 API Key
    baseURL: 'https://idealab.alibaba-inc.com/api/openai/v1',
    model: 'gemini-3-pro-image-preview',
  },
  // ...
};
```

### 3. 启动后端服务

```bash
cd backend
node server.js
```

服务启动后访问：http://localhost:9000

### 4. （可选）单独启动前端

```bash
cd frontend
npm install
npm start
```

## 📁 项目结构

```
nanobanana-pro/
├── backend/
│   ├── config.js       # 配置文件
│   ├── server.js       # Express 服务器
│   └── package.json
├── frontend/
│   └── public/
│       ├── index.html  # 主页面
│       ├── style.css   # 样式
│       └── app.js      # 前端逻辑
└── SKILL.md
```

## ✨ 功能

- ✅ 文本生成图片
- ✅ 多种尺寸选择
- ✅ 高清/标准质量
- ✅ 历史记录（本地存储）
- ✅ 图片下载
- ✅ 响应式设计（支持手机）

## 🎨 使用示例

### 提示词示例

- "一只可爱的卡通猫咪，粉色背景，简约风格"
- "赛博朋克风格的城市夜景，霓虹灯，未来感"
- "中国风山水画，云雾缭绕，意境深远"
- "梦幻的星空，银河，流星，紫色调"

## ⚠️ 注意事项

1. **API Key**: 需要有效的 idealab API Key
2. **提示词长度**: 最多 1000 字符
3. **生成时间**: 通常 10-30 秒
4. **内容政策**: 不要生成违规内容

## 🔧 配置选项

### backend/config.js

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `openai.apiKey` | API 密钥 | 必填 |
| `openai.baseURL` | API 端点 | idealab |
| `openai.model` | 模型名称 | gemini-3-pro-image-preview |
| `server.port` | 服务端口 | 9000 |
| `server.env` | 运行环境 | development |

## 📝 API 接口

### POST /api/generate-image

生成图片

**请求体:**
```json
{
  "prompt": "一只可爱的猫咪",
  "size": "1024x1024",
  "quality": "hd"
}
```

**响应:**
```json
{
  "success": true,
  "imageUrl": "data:image/png;base64,...",
  "prompt": "一只可爱的猫咪",
  "size": "1024x1024",
  "timestamp": "2026-03-03T05:00:00.000Z"
}
```

### GET /api/health

健康检查

**响应:**
```json
{
  "status": "ok",
  "timestamp": "2026-03-03T05:00:00.000Z"
}
```

## 🛠️ 开发

### 本地开发

```bash
# 后端（端口 9000）
cd backend && node server.js

# 前端（端口 3000，可选）
cd frontend && npm start
```

### 生产部署

1. 设置环境变量
2. 修改 `server.env` 为 `production`
3. 使用 PM2 等进程管理器

## 📄 License

MIT

## 👤 Author

智小月 🌙  
Created: 2026-03-03
