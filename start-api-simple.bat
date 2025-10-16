@echo off
REM 東南亞金融新聞搜尋系統 - FastAPI 後端啟動腳本
REM 使用系統 Python 而非虛擬環境

echo ========================================
echo 東南亞金融新聞搜尋系統 - FastAPI 後端
echo ========================================
echo.

echo 檢查必要套件...
python -m pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo.
    echo 正在安裝 FastAPI...
    python -m pip install fastapi "uvicorn[standard]" python-multipart
)

python -m pip show uvicorn >nul 2>&1
if errorlevel 1 (
    echo.
    echo 正在安裝 Uvicorn...
    python -m pip install "uvicorn[standard]"
)

echo.
echo 啟動 FastAPI 服務器...
echo API 文檔: http://127.0.0.1:8000/docs
echo 測試前端: http://127.0.0.1:8000/static/index.html
echo.
echo 按 Ctrl+C 停止服務
echo.

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
