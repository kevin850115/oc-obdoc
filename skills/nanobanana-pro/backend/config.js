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
