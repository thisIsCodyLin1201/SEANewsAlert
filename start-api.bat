@echo off
echo ========================================
echo 東南亞金融新聞搜尋系統 - FastAPI 後端
echo ========================================
echo.

REM 檢查虛擬環境
if not exist ".venv\Scripts\activate.bat" (
    echo 錯誤：找不到虛擬環境，請先執行 python -m venv .venv
    pause
    exit /b 1
)

REM 啟動虛擬環境
call .venv\Scripts\activate.bat

REM 檢查依賴
echo 檢查必要套件...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo.
    echo 正在安裝必要套件...
    pip install -r requirements-api.txt
)

echo.
echo 啟動 FastAPI 服務器...
echo API 文檔: http://127.0.0.1:8000/docs
echo 測試前端: http://127.0.0.1:8000/static/index.html
echo.

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
