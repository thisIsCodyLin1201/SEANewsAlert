@echo off
REM 東南亞金融新聞搜尋系統 - 啟動腳本 (Windows .bat)
echo.
echo ========================================
echo   東南亞金融新聞搜尋系統
echo ========================================
echo.
echo 正在啟動 Streamlit Web 介面...
echo.

REM 啟動應用
.venv\Scripts\python.exe -m streamlit run app.py

REM 如果啟動失敗，顯示錯誤訊息
if errorlevel 1 (
    echo.
    echo 啟動失敗！請確認：
    echo 1. 虛擬環境是否存在（.venv 目錄）
    echo 2. 依賴是否已安裝
    echo.
    pause
)
