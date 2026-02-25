#!/bin/bash

# AI短剧剧本生成器 - 外网访问启动脚本

echo "🎬 AI短剧剧本生成器 - 外网访问启动"
echo "======================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查streamlit
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 正在安装Streamlit..."
    python3 -m pip install -q streamlit
fi

echo "✅ 环境检查通过"
echo ""

# 获取服务器IP
EXTERNAL_IP=$(curl -s ifconfig.me)
INTERNAL_IP=$(hostname -I | awk '{print $1}')

echo "🌐 服务器信息："
echo "   外网IP: $EXTERNAL_IP"
echo "   内网IP: $INTERNAL_IP"
echo "   端口: 8501"
echo ""

echo "📋 访问地址："
echo "   外网: http://$EXTERNAL_IP:8501"
echo "   内网: http://$INTERNAL_IP:8501"
echo ""

echo "🚀 正在启动 Streamlit 服务..."
echo ""

# 启动Streamlit
python3 -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501

echo ""
echo "✅ 服务已停止"