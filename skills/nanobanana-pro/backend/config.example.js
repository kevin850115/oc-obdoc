// config.js - 配置文件示例
// ⚠️ 请勿提交真实 API Key 到 Git！
// 复制此文件为 config.js 并填入你的真实密钥

module.exports = {
  openai: {
    apiKey: process.env.OPENAI_API_KEY || 'your-api-key-here',
    baseURL: process.env.OPENAI_BASE_URL || 'https://idealab.alibaba-inc.com/api/openai/v1',
    model: process.env.OPENAI_MODEL || 'gemini-3-pro-image-preview',
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
