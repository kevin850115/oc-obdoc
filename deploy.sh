#!/bin/bash

# Quartz 部署脚本 - 部署到 GitHub Pages

set -e

echo "🔨 构建 Quartz 站点..."
npx quartz-cli@latest build

echo "🚀 部署到 gh-pages 分支..."

# 创建临时构建目录
cd public

# 初始化 git 并推送
git init
git add .
git commit -m "Deploy site [skip ci]"
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u --force origin main

echo "✅ 部署完成!"
echo "🌐 访问：https://YOUR_USERNAME.github.io/YOUR_REPO/"
