# Nanobanana Pro 生图应用 🍌

通过此技能可以创建一个包含前后端的生图应用网站。使用 idealab 模型 API。

## 前置工作

用户需要提供 idealab 模型 ak，可以直接发送，或者说明暂不提供，稍后在代码中手动填写。

## 配置

```js
// config.js
module.exports = {
  openai: {
    apiKey: 'f678954b102a87dccd44bcccf673acc6',
    baseURL: 'https://idealab.alibaba-inc.com/api/openai/v1',
    model: 'gemini-3-pro-image-preview',
  },
  server: {
    port: process.env.PORT || 9000,
    env: process.env.NODE_ENV || 'development',
  },
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true,
  },
};
```

## 项目结构

```
nanobanana-pro/
├── backend/
│   ├── config.js
│   ├── server.js
│   ├── package.json
│   └── routes/
│       └── image.js
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   └── package.json
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd backend && npm install
cd ../frontend && npm install
```

### 2. 配置 API Key

编辑 `backend/config.js`，填入你的 API Key。

### 3. 启动服务

```bash
# 启动后端
cd backend && node server.js

# 启动前端（新终端）
cd frontend && npm start
```

### 4. 访问应用

打开浏览器访问：http://localhost:9000

## 功能

- ✅ 文本生成图片
- ✅ 多种尺寸选择
- ✅ 高清质量
- ✅ 历史记录
- ✅ 图片下载
- ✅ 响应式设计

## 作者

智小月 🌙
Created: 2026-03-03
