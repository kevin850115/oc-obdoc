---
created: 2026-02-28
updated: 2026-02-28
tags: [#资源, #AI, #文生图, #配图技能, #OpenClaw]
para-folder: Resources
---

# 文生图配图 Skills 清单

**创建日期:** 2026-02-28  
**用途:** 为文章自动配图、智能 Mass 云推荐配图  
**适用场景:** 博客文章、公众号推文、技术文档、营销文案

---

## 🎨 推荐 Skills 清单

### 1. **ai-image-generation** ⭐⭐⭐⭐⭐ 强烈推荐

**功能最全面的文生图技能**

| 项目 | 详情 |
|------|------|
| **支持模型** | FLUX、Gemini 3 Pro、Grok Imagine、Seedream 4.5、Reve 等 50+ 模型 |
| **核心能力** | 文生图、图生图、局部重绘、图像编辑、超分辨率放大 |
| **适用场景** | AI 艺术、产品 mockup、概念图、社交媒体配图、营销视觉、插图 |
| **触发词** | `flux`, `image generation`, `ai image`, `text to image`, `stable diffusion`, `generate image` |
| **依赖** | inference.sh CLI |

**安装方式:**
```bash
# 安装 CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# 安装技能
npx skills add inference-sh/skills@ai-image-generation
```

**快速使用:**
```bash
# 生成文章配图
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional blog illustration about AI and cloud computing, modern style"
}'
```

**推荐模型:**
| 模型 | 适用场景 |
|------|---------|
| FLUX Dev LoRA | 高质量通用配图 |
| FLUX.2 Klein | 快速生成 |
| Gemini 3 Pro | Google 最新模型 |
| Seedream 4.5 | 2K-4K 电影级质量 |
| Reve | 文字渲染（海报、标题图） |

---

### 2. **openai-image-gen** ⭐⭐⭐⭐

**OpenAI 官方图像生成**

| 项目 | 详情 |
|------|------|
| **支持模型** | OpenAI Images API (DALL-E 3) |
| **核心能力** | 批量生成、随机提示词采样、HTML 画廊预览 |
| **适用场景** | 快速生成多张配图、A/B 测试 |
| **触发词** | `openai image`, `dall-e`, `generate image` |

**安装方式:**
```bash
openclaw skills install clawhub/openai-image-gen
```

**特点:**
- ✅ 质量稳定，风格一致
- ✅ 支持批量生成
- ✅ 自动生成 HTML 预览页面
- ⚠️ 需要 OpenAI API key

---

### 3. **imagegen** ⭐⭐⭐⭐

**OpenAI 图像编辑增强版**

| 项目 | 详情 |
|------|------|
| **支持模型** | OpenAI Image API |
| **核心能力** | 图像生成、编辑、局部重绘、背景移除/替换、透明背景 |
| **适用场景** | 产品图、概念艺术、封面图、批量变体 |
| **触发词** | `generate image`, `edit`, `inpaint`, `background removal` |

**安装方式:**
```bash
openclaw skills install clawhub/imagegen
```

**特点:**
- ✅ 支持图像编辑和修改
- ✅ 背景移除/替换
- ✅ 产品摄影优化

---

### 4. **best-stable-diffusion-prompts-guide** ⭐⭐⭐

**Stable Diffusion 提示词指南**

| 项目 | 详情 |
|------|------|
| **类型** | 提示词模板库 |
| **核心能力** | 艺术家风格模仿、提示词配方、参数推荐 |
| **适用场景** | 学习提示词工程、生成特定风格图像 |

**安装方式:**
```bash
openclaw skills install clawhub/best-stable-diffusion-prompts-guide
```

**特点:**
- ✅ 提供提示词模板
- ✅ 艺术家风格参考
- ✅ 参数优化建议

---

## 🚀 针对阿里云 MaaS 文章的配图方案

### 推荐工作流

**方案 A: 使用 ai-image-generation (推荐)**

```bash
# 1. 安装技能
curl -fsSL https://cli.inference.sh | sh && infsh login
npx skills add inference-sh/skills@ai-image-generation

# 2. 为 MaaS 文章生成配图
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "professional cloud computing architecture diagram, AI model deployment, modern tech illustration, blue and white color scheme, clean minimalist style"
}'
```

**方案 B: 批量生成多张配图**

```bash
# 使用 openai-image-gen 批量生成
openclaw skills install clawhub/openai-image-gen

# 生成 4 张备选图，选择最佳
```

---

## 📝 文章配图提示词模板

### 技术文章通用模板

```
professional blog illustration about [主题], 
modern tech style, clean minimalist design, 
blue and white color scheme, 
high quality, 16:9 aspect ratio
```

### AI/云计算主题

```
AI artificial intelligence cloud computing concept, 
neural network visualization, data flow, 
futuristic technology background, 
professional corporate style, 4K
```

### 产品推荐文章

```
product showcase [产品名], 
professional product photography, 
studio lighting, clean background, 
marketing material quality
```

---

## 💰 成本对比

| Skill | 模型 | 成本/张 | 推荐用途 |
|-------|------|--------|---------|
| ai-image-generation | FLUX | ~$0.02 | 日常配图 |
| ai-image-generation | Seedream 4.5 | ~$0.05 | 高质量配图 |
| ai-image-generation | Gemini 3 Pro | ~$0.03 | 通用配图 |
| openai-image-gen | DALL-E 3 | ~$0.04 | 稳定质量 |
| imagegen | OpenAI | ~$0.04 | 编辑修改 |

---

## ✅ 安装检查清单

- [ ] 选择主要使用的 skill（推荐 ai-image-generation）
- [ ] 安装必要的 CLI 工具
- [ ] 配置 API key（如需要）
- [ ] 测试生成一张图片
- [ ] 创建提示词模板库
- [ ] 集成到文章发布流程

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| ClawHub 技能市场 | https://clawhub.ai |
| inference.sh 文档 | https://inference.sh/docs |
| Awesome OpenClaw Skills | https://github.com/VoltAgent/awesome-openclaw-skills |
| FLUX.1 介绍 | https://stable-diffusion-art.com/flux/ |

---

*最后更新：2026-02-28 23:15*
