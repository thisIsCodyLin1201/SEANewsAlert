# 東南亞金融新聞搜尋系統 - FastAPI 後端啟動腳本 (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "東南亞金融新聞搜尋系統 - FastAPI 後端" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查虛擬環境
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "錯誤：找不到虛擬環境，請先執行 python -m venv .venv" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 啟動虛擬環境
Write-Host "啟動虛擬環境..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 檢查依賴
Write-Host "檢查必要套件..." -ForegroundColor Yellow
$fastApiInstalled = & python -m pip show fastapi 2>$null
if (-not $fastApiInstalled) {
    Write-Host ""
    Write-Host "正在安裝必要套件..." -ForegroundColor Yellow
    python -m pip install -r requirements-api.txt
}

# 確認 uvicorn 已安裝
$uvicornInstalled = & python -m pip show uvicorn 2>$null
if (-not $uvicornInstalled) {
    Write-Host "正在安裝 uvicorn..." -ForegroundColor Yellow
    python -m pip install "uvicorn[standard]"
}

Write-Host ""
Write-Host "啟動 FastAPI 服務器..." -ForegroundColor Green
Write-Host "API 文檔: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "測試前端: http://127.0.0.1:8000/static/index.html" -ForegroundColor Cyan
Write-Host ""

# 使用 python -m 啟動服務（更可靠）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
