/**
 * Nanobanana Pro - 生图应用后端服务
 */

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const config = require('./config');

const app = express();
const PORT = config.server.port;

// 中间件
app.use(cors(config.cors));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 静态文件服务（前端）
app.use(express.static(path.join(__dirname, '../frontend/public')));

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 生图接口
app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt, size = '1024x1024', quality = 'hd' } = req.body;

    // 验证输入
    if (!prompt || typeof prompt !== 'string' || prompt.trim().length === 0) {
      return res.status(400).json({ error: '请提供有效的图像描述' });
    }

    if (prompt.length > 1000) {
      return res.status(400).json({ error: '图像描述过长，请控制在 1000 字符以内' });
    }

    // 记录请求信息
    console.log('🎨 图像生成请求:', {
      prompt: prompt.substring(0, 100) + (prompt.length > 100 ? '...' : ''),
      size,
      quality,
      timestamp: new Date().toISOString(),
    });

    // 调用 OpenAI API 生成图像
    console.log('📡 正在调用 API 生成图像...', {
      model: config.openai.model,
      baseURL: config.openai.baseURL,
      prompt: prompt.substring(0, 50),
    });

    const response = await axios.post(
      `${config.openai.baseURL}/chat/completions`,
      {
        model: config.openai.model,
        messages: [
          {
            role: 'user',
            content: `Generate an image: ${prompt}`,
          },
        ],
        max_tokens: 1000,
      },
      {
        headers: {
          'Authorization': `Bearer ${config.openai.apiKey}`,
          'Content-Type': 'application/json',
        },
        timeout: 120000, // 2 分钟超时
      }
    );

    console.log('✅ API 响应成功');

    if (!response.data.choices || response.data.choices.length === 0) {
      throw new Error('API 返回空结果');
    }

    // 从响应中提取图像内容
    let imageContent = response.data.choices[0].message.content;
    let imageUrl;

    console.log('📄 原始响应内容类型:', typeof imageContent);
    console.log('📄 原始响应内容 (前 100 字符):', imageContent && typeof imageContent === 'string' ? imageContent.substring(0, 100) : imageContent);

    // 检查是否是数组格式的响应（包含 image_url 对象）
    if (Array.isArray(imageContent) && imageContent.length > 0) {
      const imageItem = imageContent[0];
      console.log('🔍 检测到数组格式响应:', imageItem);

      if (imageItem.image_url && imageItem.image_url.url) {
        imageContent = imageItem.image_url.url;
        console.log('✅ 提取到图片 URL:', imageContent.substring(0, 100));
      } else if (imageItem.type === 'image_url' && imageItem.image_url) {
        imageContent = imageItem.image_url.url;
        console.log('✅ 从 image_url 对象提取图片数据');
      }
    }

    // 按优先级检查图片格式：HTTP URL > data URL > 纯 base64
    if (imageContent && typeof imageContent === 'string') {
      console.log('📐 处理图片内容，长度:', imageContent.length);

      // 1. 优先检查是否是 HTTP/HTTPS URL
      if (imageContent.startsWith('http://') || imageContent.startsWith('https://')) {
        console.log('✅ 检测到 HTTP/HTTPS URL');
        imageUrl = imageContent;
      }
      // 2. 检查是否已经有 data: 前缀
      else if (imageContent.startsWith('data:image/')) {
        console.log('✅ 检测到完整的 data URL');
        imageUrl = imageContent;
      }
      // 3. 检查是否是纯 base64 字符串（没有 data: 前缀）
      else if (imageContent.match(/^[A-Za-z0-9+/]+=*$/) && imageContent.length > 100) {
        console.log('✅ 检测到纯 base64 格式，添加前缀');
        imageUrl = `data:image/png;base64,${imageContent}`;
      }
      // 4. 其他情况记录详细信息并使用占位符
      else {
        console.log('⚠️ 未识别的内容格式');
        console.log('📊 内容详情:', {
          startsWithHttp: imageContent.startsWith('http'),
          startsWithHttps: imageContent.startsWith('https'),
          startsWithData: imageContent.startsWith('data:'),
          isBase64Match: !!imageContent.match(/^[A-Za-z0-9+/]+=*$/),
          length: imageContent.length,
          firstChars: imageContent.substring(0, 50),
        });
        imageUrl = 'https://via.placeholder.com/1024x1024?text=Generated+Image';
      }
    } else {
      console.log('⚠️ 图像内容为空或非字符串类型');
      imageUrl = 'https://via.placeholder.com/1024x1024?text=Generated+Image';
    }

    console.log('🖼️ 最终图像 URL 类型:', imageUrl && typeof imageUrl === 'string' && imageUrl.startsWith('data:') ? 'base64' : 'url');

    res.json({
      success: true,
      imageUrl,
      prompt,
      size,
      quality,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ 图像生成失败:', error.message);

    // 处理不同类型的错误
    if (error.code === 'content_policy_violation') {
      return res.status(400).json({
        error: '您的描述违反了内容政策，请修改后重试',
      });
    }

    if (error.code === 'rate_limit_exceeded') {
      return res.status(429).json({
        error: '请求过于频繁，请稍后再试',
      });
    }

    if (error.code === 'insufficient_quota') {
      return res.status(503).json({
        error: '服务暂时不可用，请稍后再试',
      });
    }

    // 通用错误处理
    res.status(500).json({
      error: '图像生成失败，请稍后重试',
      details: config.server.env === 'development' ? error.message : undefined,
    });
  }
});

// 前端路由 - 所有其他请求返回 index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/public/index.html'));
});

// 启动服务器
app.listen(PORT, () => {
  console.log('🚀 Nanobanana Pro 服务已启动');
  console.log(`📡 服务地址：http://localhost:${PORT}`);
  console.log(`🎨 生图接口：POST /api/generate-image`);
  console.log(`📊 健康检查：GET /api/health`);
});

module.exports = app;
