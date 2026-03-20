#!/bin/bash
# 安装 Vercel CLI
npm install -g vercel

# 登录 Vercel（需要先手动登录一次）
# vercel login

# 部署到 Vercel
vercel --prod --confirm
