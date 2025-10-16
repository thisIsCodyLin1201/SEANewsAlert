# 東南亞金融新聞搜尋系統 - FastAPI 後端版本

## 📋 專案概述

本專案將原有的 Streamlit 版本改寫為「前後端分離 + RESTful API」架構，後端採用 FastAPI。

### 主要功能
- ✅ RESTful API 架構（FastAPI）
- ✅ 背景任務執行（非阻塞）
- ✅ 任務進度追蹤與輪詢
- ✅ 新聞搜尋、分析、報告生成
- ✅ PDF + Excel 報告輸出
- ✅ 郵件附件自動發送
- ✅ 極簡測試前端頁面
- ✅ 來源多樣性優化（建議導向）
- ✅ 多語言支援（英文、中文、越南文等）

## 🏗️ 專案結構

```
SEANewsAlert/
├── app/                          # FastAPI 後端
│   ├── main.py                   # 主應用程式
│   ├── routers/                  # API 路由
│   │   └── tasks.py              # 任務相關 API
│   └── services/                 # 服務層
│       ├── workflow.py           # 工作流程封裝
│       └── progress.py           # 任務狀態管理
├── agents/                       # AI Agents（沿用既有）
│   ├── research_agent.py         # 搜尋代理
│   ├── analyst_agent.py          # 分析代理
│   ├── report_agent.py           # 報告生成代理
│   └── email_agent.py            # 郵件代理
├── public/                       # 靜態前端
│   └── index.html                # 極簡測試頁面
├── reports/                      # 報告輸出目錄
├── config.py                     # 設定檔
├── .env                          # 環境變數（需自行建立）
├── .env.example                  # 環境變數範例
├── requirements-api.txt          # 後端依賴套件
├── start-api.bat                 # Windows 啟動腳本
├── start-api.sh                  # Linux/Mac 啟動腳本
└── README-API.md                 # 本說明文件
```

## 🚀 快速開始

### 1. 環境需求

- Python 3.11+
- Windows 10/11（或 Linux/Mac）
- OpenAI API Key
- SMTP 郵件帳號（如 Gmail）

### 2. 安裝依賴

```bash
# 建立虛擬環境（如果還沒有）
python -m venv .venv

# 啟動虛擬環境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安裝依賴
pip install -r requirements-api.txt
```

### 3. 設定環境變數

複製 `.env.example` 為 `.env` 並填入實際設定：

```bash
cp .env.example .env
```

編輯 `.env` 文件：

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Application Configuration
APP_NAME=東南亞金融新聞搜尋系統
APP_VERSION=2.0.0
DEBUG=false

# Agno Configuration
AGNO_TELEMETRY=false

# FastAPI Configuration
BASE_URL=http://127.0.0.1:8000
```

### 4. 啟動後端服務

#### 方式一：使用啟動腳本（推薦）

**Windows:**
```bash
start-api.bat
```

**Linux/Mac:**
```bash
chmod +x start-api.sh
./start-api.sh
```

#### 方式二：直接使用 uvicorn

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. 訪問服務

服務啟動後，可以訪問：

- 🏠 **首頁**: http://127.0.0.1:8000/
- 📖 **API 文檔（Swagger UI）**: http://127.0.0.1:8000/docs
- 📄 **API 文檔（ReDoc）**: http://127.0.0.1:8000/redoc
- 🎨 **測試前端頁面**: http://127.0.0.1:8000/static/index.html

## 📡 API 使用說明

### 1. 創建新聞報告任務

**端點**: `POST /api/tasks/news-report`

**請求體**:
```json
{
  "user_prompt": "新加坡金融科技發展趨勢",
  "email": "user@example.com",
  "language": "English",
  "time_range": "最近 7 天內",
  "count_hint": "5-10篇"
}
```

**響應** (201 Created):
```json
{
  "task_id": "uuid-string",
  "message": "Task started"
}
```

### 2. 查詢任務狀態

**端點**: `GET /api/tasks/{task_id}`

**響應** (200 OK):
```json
{
  "task_id": "uuid-string",
  "status": "running",
  "progress": 45,
  "error": null,
  "artifacts": {
    "pdf_path": null,
    "xlsx_path": null
  },
  "current_step": "analyzing",
  "step_message": "📊 正在分析並結構化資訊..."
}
```

**狀態值**:
- `queued`: 任務排隊中
- `running`: 任務執行中
- `succeeded`: 任務成功完成
- `failed`: 任務失敗

### 3. 健康檢查

**端點**: `GET /health`

**響應**:
```json
{
  "status": "healthy",
  "service": "SEA News Alert API",
  "version": "2.0.0"
}
```

## 🎨 前端測試頁面使用

1. 訪問 http://127.0.0.1:8000/static/index.html
2. 輸入搜尋需求（例如：「新加坡金融科技發展趨勢」）
3. 輸入收件者信箱
4. 選擇進階選項（語言、時間範圍、數量）
5. 點擊「開始搜尋」
6. 等待任務完成（頁面會自動輪詢狀態）
7. 完成後檢查信箱，會收到 PDF + Excel 報告

## 🔧 進階功能

### 語言支援

系統支援以下語言的新聞來源：
- `English`（英文，預設）
- `Chinese`（中文）
- `Vietnamese`（越南文）
- `Thai`（泰文）
- `Malay`（馬來文）
- `Indonesian`（印尼文）

### 來源多樣性

系統會自動優化新聞來源多樣性：
- 建議使用 3-4 個以上不同來源
- 優先考慮新聞品質與相關性
- 非強制比例限制

### 白名單來源（18個）

系統僅從以下可信來源搜尋新聞：
- VietJo, Cafef, VNExpress, Vietnam Finance, VIR, Vietnambiz, Tap Chi Tai chinh
- Bangkok Post, Techsauce
- Fintech Singapore, Fintech Philippines
- Khmer Times, 柬中時報, The Phnom Penh Post
- Deal Street Asia, Tech in Asia, Nikkei Asia, Heaptalk

## 📊 報告格式

### PDF 報告

包含：
- 報告摘要
- 搜尋主題與日期
- 新聞詳情（標題、來源、日期、摘要、重點分析）
- 市場洞察
- 資料來源連結

### Excel 報告

欄位順序（固定）：
1. 新聞標題（中文）
2. 來源國家
3. 來源網站連結
4. 發布日期
5. 摘要
6. 重點分析

## 🐛 錯誤處理

- API 會回傳標準 HTTP 錯誤碼（4xx/5xx）
- 任務失敗時，`error` 欄位會包含錯誤訊息
- 可透過 `GET /api/tasks/{task_id}` 查看錯誤詳情

## 📝 開發說明

### 新增 API 端點

1. 在 `app/routers/` 下建立新的路由文件
2. 在 `app/main.py` 中註冊路由：
   ```python
   from app.routers import your_router
   app.include_router(your_router.router)
   ```

### 修改工作流程

編輯 `app/services/workflow.py` 中的 `execute_task` 方法。

### 修改任務狀態管理

編輯 `app/services/progress.py` 中的 `TaskProgress` 類別。

## 🔒 安全性建議

1. **不要將 `.env` 文件提交到版本控制**
2. **使用應用程式專用密碼**（如 Gmail App Password）
3. **生產環境建議**：
   - 使用 Redis 或資料庫儲存任務狀態
   - 使用訊息佇列（如 RabbitMQ、Celery）處理背景任務
   - 啟用 HTTPS
   - 加入身份驗證（JWT 等）

## 🆚 與 Streamlit 版本的差異

| 功能 | Streamlit 版本 | FastAPI 版本 |
|------|---------------|-------------|
| 架構 | 單體應用 | 前後端分離 |
| API | 無 | RESTful API |
| 並發處理 | 阻塞 | 非阻塞（背景任務）|
| 前端 | Streamlit UI | 靜態 HTML |
| 擴展性 | 受限 | 易於擴展 |
| 部署 | 簡單 | 靈活 |

## 📞 支援與問題

如有問題，請：
1. 檢查 `.env` 設定是否正確
2. 查看 API 文檔：http://127.0.0.1:8000/docs
3. 檢查終端機的錯誤訊息

## 📜 授權

本專案僅供內部使用。

---

**版本**: 2.0.0  
**最後更新**: 2025-01-16
