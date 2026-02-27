# 🚀 部署到 GitHub Pages 指南

## 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：例如 `my-digital-garden` 或 `notes`
3. 设为 **Public**（GitHub Pages 免费托管需要公开仓库）
4. **不要** 初始化 README、.gitignore 或 license
5. 点击 "Create repository"

## 第二步：推送代码到 GitHub

```bash
cd ~/doc

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Obsidian digital garden"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送
git push -u origin main
```

## 第三步：启用 GitHub Pages

1. 进入 GitHub 仓库的 **Settings** → **Pages**
2. 在 **Build and deployment** 部分：
   - Source: 选择 **GitHub Actions**
3. 等待 Actions 自动运行（大约 2-5 分钟）

## 第四步：访问你的网站

部署完成后，你的网站将在：
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

## 📝 日常使用

### 添加新笔记
1. 在 Obsidian 中写笔记
2. 保存到 `~/doc/content/` 对应目录
3. 提交并推送：
   ```bash
   cd ~/doc
   git add .
   git commit -m "Add new note"
   git push
   ```
4. GitHub Actions 会自动部署（约 2-5 分钟）

### 本地预览
```bash
cd ~/doc
npm install  # 首次需要
npx quartz-cli@latest serve
```
然后访问 http://localhost:8080

## ⚙️ 自定义配置

编辑 `quartz.config.ts` 可以修改：
- 网站标题
- 主题颜色
- 功能开关（图谱视图、搜索等）

编辑 `quartz.layout.ts` 可以修改页面布局。

## 🎨 主题

Quartz 支持多种主题，在 `quartz.config.ts` 中修改 `theme` 配置。

---
有问题？查看 Quartz 文档：https://quartz.jzhao.xyz/
