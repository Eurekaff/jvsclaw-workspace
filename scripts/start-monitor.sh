#!/bin/bash
# 快速启动监控面板

set -e

echo "🚀 启动 Agent 工作流监控面板..."

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请安装 Docker 后重试"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请安装后重试"
    exit 1
fi

cd monitor_dashboard

# 启动服务
echo "📦 启动 Docker 容器..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo ""
echo "✅ 服务已启动！"
echo ""
echo "📊 访问地址:"
echo "   前端：http://localhost:3000"
echo "   API:   http://localhost:8001"
echo "   API 文档：http://localhost:8001/docs"
echo ""
echo "📝 查看日志:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose down"
echo ""
