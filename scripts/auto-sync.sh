#!/bin/bash
# GitHub Workspace Auto-Sync Script
# 检查 workspace 变更并自动推送

WORKSPACE="/home/admin/openclaw/workspace"
cd "$WORKSPACE" || exit 1

# 检查是否有变更
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 没有变更，跳过同步"
    exit 0
fi

# 有变更，执行推送
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到变更，开始同步..."

# 添加所有变更
git add -A

# 提交
git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 同步成功"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 同步失败"
    exit 1
fi
