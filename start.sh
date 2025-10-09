#!/bin/bash
# 東南亞金融新聞搜尋系統 - 啟動腳本 (Linux/macOS)

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║    🌏 東南亞金融新聞智能搜尋與報告系統               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 檢查虛擬環境
if [ ! -d ".venv" ]; then
    echo "❌ 找不到虛擬環境"
    echo ""
    echo "請先執行安裝："
    echo "  uv venv && source .venv/bin/activate && uv pip install -e ."
    exit 1
fi

echo "✅ 虛擬環境檢查通過"
echo ""
echo "🚀 正在啟動 Web 介面..."
echo ""
echo "📍 訪問網址："
echo "   http://localhost:8501"
echo "   http://127.0.0.1:8501"
echo ""
echo "💡 按 Ctrl+C 停止服務"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 啟動應用
./.venv/bin/python -m streamlit run app.py
