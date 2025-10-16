#!/bin/bash
echo "========================================"
echo "東南亞金融新聞搜尋系統 - FastAPI 後端"
echo "========================================"
echo ""

# 檢查虛擬環境
if [ ! -f ".venv/Scripts/activate" ]; then
    echo "錯誤：找不到虛擬環境，請先執行 python -m venv .venv"
    exit 1
fi

# 啟動虛擬環境
source .venv/Scripts/activate

# 檢查依賴
echo "檢查必要套件..."
if ! pip show fastapi > /dev/null 2>&1; then
    echo ""
    echo "正在安裝必要套件..."
    pip install -r requirements-api.txt
fi

echo ""
echo "啟動 FastAPI 服務器..."
echo "API 文檔: http://127.0.0.1:8000/docs"
echo "測試前端: http://127.0.0.1:8000/static/index.html"
echo ""

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
