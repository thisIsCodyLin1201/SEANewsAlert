# 東南亞金融新聞搜尋系統 - 啟動腳本

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║    🌏 東南亞金融新聞智能搜尋與報告系統               ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# 檢查虛擬環境
if (-not (Test-Path ".venv")) {
    Write-Host "❌ 找不到虛擬環境" -ForegroundColor Red
    Write-Host ""
    Write-Host "請先執行安裝：" -ForegroundColor Yellow
    Write-Host "  uv venv && .\.venv\Scripts\Activate.ps1 && uv pip install -e ." -ForegroundColor Green
    exit 1
}

Write-Host "✅ 虛擬環境檢查通過" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 正在啟動 Web 介面..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 訪問網址：" -ForegroundColor Yellow
Write-Host "   http://localhost:8501" -ForegroundColor White
Write-Host "   http://127.0.0.1:8501" -ForegroundColor White
Write-Host ""
Write-Host "💡 按 Ctrl+C 停止服務" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# 啟動應用
& ".\.venv\Scripts\python.exe" -m streamlit run app.py
