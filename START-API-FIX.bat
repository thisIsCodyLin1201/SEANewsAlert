@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo 東南亞金融新聞搜尋系統 - 一鍵啟動
echo ========================================
echo.

REM 檢查 Python 是否安裝
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請先安裝 Python 3.11+
    pause
    exit /b 1
)

echo [1/4] 檢查虛擬環境...

REM 檢查虛擬環境是否存在且正常
if exist ".venv\Scripts\python.exe" (
    echo     虛擬環境已存在，檢查 pip...
    .venv\Scripts\python.exe -m pip --version > nul 2>&1
    if !errorlevel! neq 0 (
        echo     [警告] 虛擬環境損壞，重新創建...
        rmdir /s /q .venv
        goto create_venv
    ) else (
        echo     虛擬環境正常
        goto install_deps
    )
) else (
    echo     虛擬環境不存在，創建中...
    goto create_venv
)

:create_venv
echo [2/4] 創建虛擬環境...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [錯誤] 創建虛擬環境失敗
    pause
    exit /b 1
)
echo     虛擬環境創建成功

:install_deps
echo [3/4] 安裝套件...

REM 升級 pip
echo     升級 pip...
.venv\Scripts\python.exe -m pip install --upgrade pip -q

REM 安裝 FastAPI 相關套件
echo     安裝 FastAPI 套件...
.venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] pydantic[email] -q

REM 檢查 requirements-api.txt 是否存在
if exist "requirements-api.txt" (
    echo     安裝其他依賴...
    .venv\Scripts\python.exe -m pip install -r requirements-api.txt -q
)

echo     所有套件安裝完成

:start_server
echo [4/4] 啟動 FastAPI 服務器...
echo.
echo ========================================
echo 服務啟動成功！
echo ========================================
echo API 文檔:   http://127.0.0.1:8000/docs
echo 測試前端:   http://127.0.0.1:8000/static/index.html
echo 健康檢查:   http://127.0.0.1:8000/health
echo ========================================
echo 按 Ctrl+C 停止服務
echo ========================================
echo.

.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
