@echo off
chcp 65001 > nul
echo ========================================
echo 完全重建虛擬環境
echo ========================================
echo.
echo [警告] 這會刪除現有的 .venv 目錄
echo.
pause

echo [1/3] 刪除舊的虛擬環境...
if exist ".venv" (
    rmdir /s /q .venv
    echo     已刪除
) else (
    echo     不存在舊環境
)

echo [2/3] 創建新的虛擬環境...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [錯誤] 創建失敗，請檢查 Python 安裝
    pause
    exit /b 1
)
echo     創建成功

echo [3/3] 安裝基礎套件...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install fastapi uvicorn[standard] pydantic[email]

echo.
echo ========================================
echo 虛擬環境重建完成！
echo ========================================
echo.
echo 現在請執行: START-API-FIX.bat
echo.
pause
