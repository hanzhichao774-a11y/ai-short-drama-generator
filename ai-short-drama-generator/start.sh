#!/bin/bash

echo "🎬 AI短剧剧本生成器 - 启动脚本"
echo "=================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python3 环境检测通过"

# 检查依赖
echo ""
echo "📦 检查依赖..."
pip install -q -r requirements.txt

echo ""
echo "🚀 启动 Web 界面..."
echo "浏览器将自动打开 http://localhost:8501"
echo ""

streamlit run app.py