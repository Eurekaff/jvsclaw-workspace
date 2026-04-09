#!/bin/bash
# Skills 更新脚本

set -e

SKILLS_DIR="$HOME/.openclaw/skills"

echo "🔄 更新所有 skills 仓库..."
cd "$SKILLS_DIR"

# 获取所有 git 仓库
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "📦 更新 $repo..."
        cd "$repo"
        git pull --rebase --quiet 2>&1 || echo "  ⚠️  更新失败"
        cd ..
    fi
done

echo ""
echo "✅ 所有 skills 更新完成"
echo ""
echo "📊 重新生成索引..."
python3 /home/admin/openclaw/workspace/tools/skills_index.py scan
