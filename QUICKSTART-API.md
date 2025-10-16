# 🚀 快速啟動指南 - FastAPI 版本

## 前置要求

- ✅ Python 3.11 或以上
- ✅ OpenAI API Key
- ✅ Gmail 帳號（或其他 SMTP 郵件服務）

## 步驟 1：安裝依賴

### Windows (CMD or PowerShell)

```bash
# 如果還沒有虛擬環境
python -m venv .venv

# 啟動虛擬環境
.venv\Scripts\activate

# 安裝依賴
pip install -r requirements-api.txt
```

### Linux / Mac

```bash
# 如果還沒有虛擬環境
python3 -m venv .venv

# 啟動虛擬環境
source .venv/bin/activate

# 安裝依賴
pip install -r requirements-api.txt
```

## 步驟 2：設定環境變數

複製 `.env.example` 為 `.env`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

編輯 `.env` 文件，填入你的設定：

```env
# OpenAI API Key（必填）
OPENAI_API_KEY=sk-your-api-key-here

# Gmail 設定（必填）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your-app-password-here

# 其他設定（選填）
APP_NAME=東南亞金融新聞搜尋系統
APP_VERSION=2.0.0
DEBUG=false
```

### 📧 Gmail 應用程式密碼設定

1. 前往 https://myaccount.google.com/security
2. 啟用「兩步驟驗證」
3. 搜尋「應用程式密碼」
4. 選擇「郵件」和「Windows 電腦」（或其他）
5. 生成密碼並複製到 `.env` 的 `EMAIL_PASSWORD`

## 步驟 3：啟動服務

### 方式一：使用啟動腳本（推薦）

**Windows (CMD):**
```bash
start-api.bat
```

**Windows (PowerShell):**
```powershell
.\START-API.ps1
```

**Linux/Mac:**
```bash
chmod +x start-api.sh
./start-api.sh
```

### 方式二：手動啟動

```bash
# 確保虛擬環境已啟動
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# 啟動服務
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## 步驟 4：測試服務

服務啟動後，在瀏覽器中訪問：

1. **首頁**: http://127.0.0.1:8000/
2. **API 文檔**: http://127.0.0.1:8000/docs
3. **測試前端**: http://127.0.0.1:8000/static/index.html

## 步驟 5：使用測試前端

1. 訪問 http://127.0.0.1:8000/static/index.html
2. 在「搜尋需求」欄位輸入查詢，例如：
   - 「新加坡金融科技發展趨勢」
   - 「越南股市最近動態」
   - 「泰國經濟政策變化」
3. 輸入你的郵箱地址
4. 選擇語言、時間範圍、數量（可選）
5. 點擊「開始搜尋」
6. 等待任務完成（約 1-3 分鐘）
7. 檢查你的郵箱，會收到 PDF 和 Excel 報告

## 步驟 6（選用）：使用測試腳本

```bash
# 確保服務正在運行
# 然後在另一個終端執行：

python test_api.py
```

## 常見問題

### Q1: 啟動時提示找不到模組

**A**: 確保虛擬環境已啟動，並重新安裝依賴：
```bash
pip install -r requirements-api.txt
```

### Q2: 郵件發送失敗

**A**: 檢查 `.env` 中的郵件設定：
- 確認使用「應用程式密碼」而非帳號密碼
- 確認 Gmail 已啟用「兩步驟驗證」
- 嘗試使用其他 SMTP 服務

### Q3: OpenAI API 錯誤

**A**: 檢查：
- API Key 是否正確
- 帳戶是否有餘額
- 是否有網路連線

### Q4: 前端頁面無法連接後端

**A**: 確認：
- 後端服務是否正在運行（http://127.0.0.1:8000）
- 瀏覽器控制台是否有 CORS 錯誤
- 防火牆是否阻擋連線

### Q5: 任務一直顯示「執行中」

**A**: 檢查後端終端的日誌輸出，可能原因：
- OpenAI API 請求失敗
- 網路連線問題
- 搜尋結果為空

## 下一步

- 📖 閱讀完整文檔：`README-API.md`
- 🔧 自訂 API：編輯 `app/routers/tasks.py`
- 🎨 修改前端：編輯 `public/index.html`
- 🤖 調整 Agents：編輯 `agents/` 目錄下的文件

## 技術支援

如遇到問題，請：
1. 檢查終端的錯誤訊息
2. 查看 API 文檔：http://127.0.0.1:8000/docs
3. 檢查 `.env` 設定是否正確

---

**祝使用愉快！** 🎉
