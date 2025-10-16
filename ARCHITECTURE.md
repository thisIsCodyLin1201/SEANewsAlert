# 🏗️ FastAPI 後端架構圖

## 系統整體架構

```
┌─────────────────────────────────────────────────────────────┐
│                         使用者                              │
│                    (Web Browser)                           │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ HTTP Request/Response
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                     前端層                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Static Frontend (public/index.html)                │   │
│  │  - 使用者輸入表單                                    │   │
│  │  - 任務提交                                         │   │
│  │  - 狀態輪詢                                         │   │
│  │  - 進度顯示                                         │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ REST API Calls
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                    FastAPI 後端                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  app/main.py                                        │   │
│  │  - FastAPI Application                             │   │
│  │  - CORS Middleware                                 │   │
│  │  - Static Files Serving                            │   │
│  │  - Router Registration                             │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                        │
│  ┌─────────────────▼───────────────────────────────────┐   │
│  │  app/routers/tasks.py                              │   │
│  │  - POST /api/tasks/news-report                     │   │
│  │  - GET  /api/tasks/{task_id}                       │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                        │
│  ┌─────────────────▼───────────────────────────────────┐   │
│  │  app/services/                                      │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ progress.py                                  │  │   │
│  │  │ - TaskProgress (狀態管理)                   │  │   │
│  │  │ - create_task()                             │  │   │
│  │  │ - get_task()                                │  │   │
│  │  │ - update_task()                             │  │   │
│  │  │ - set_running/succeeded/failed()            │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ workflow.py                                  │  │   │
│  │  │ - NewsReportWorkflow                        │  │   │
│  │  │ - execute_task() (背景任務)                 │  │   │
│  │  │ - _parse_prompt()                           │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────┬───────────────────────────────────┘   │
└────────────────────┼─────────────────────────────────────────┘
                     │
                     │ 調用既有 Agents
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                   Agent 層 (既有)                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  agents/research_agent.py                           │   │
│  │  - ResearchAgent                                    │   │
│  │  - search() - 搜尋新聞                              │   │
│  │  - 18 個白名單來源                                  │   │
│  │  - 多樣性建議                                       │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                        │
│  ┌─────────────────▼───────────────────────────────────┐   │
│  │  agents/analyst_agent.py                           │   │
│  │  - AnalystAgent                                    │   │
│  │  - analyze() - 分析與結構化                         │   │
│  │  - Markdown 報告生成                               │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                        │
│  ┌─────────────────▼───────────────────────────────────┐   │
│  │  agents/report_agent.py                            │   │
│  │  - ReportGeneratorAgent                            │   │
│  │  - generate_pdf() - PDF 生成                       │   │
│  │  - generate_excel() - Excel 生成                   │   │
│  └─────────────────┬───────────────────────────────────┘   │
│                    │                                        │
│  ┌─────────────────▼───────────────────────────────────┐   │
│  │  agents/email_agent.py                             │   │
│  │  - EmailAgent                                      │   │
│  │  - send_report() - 郵件發送                         │   │
│  │  - PDF + Excel 附件                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                     │
                     │ 輸出
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                   輸出與外部服務                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  reports/ 目錄                                      │   │
│  │  - PDF 報告                                         │   │
│  │  - Excel 報告                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SMTP 郵件服務 (Gmail)                              │   │
│  │  - 發送郵件                                         │   │
│  │  - 附加 PDF + Excel                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  OpenAI API                                         │   │
│  │  - GPT-4 深度搜尋                                   │   │
│  │  - 需求解析                                         │   │
│  │  - 新聞分析                                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## API 流程圖

### 創建任務流程

```
使用者                前端              FastAPI           服務層            Agents
  │                    │                  │                 │                 │
  │─── 填寫表單 ─────>│                  │                 │                 │
  │                    │                  │                 │                 │
  │                    │── POST /api/tasks/news-report ──>│                 │
  │                    │                  │                 │                 │
  │                    │                  │── create_task()─>│                │
  │                    │                  │                 │                 │
  │                    │                  │<── task_id ─────│                │
  │                    │                  │                 │                 │
  │                    │                  │── add_task(background) ─────────>│
  │                    │                  │                 │                 │
  │                    │<── 201 Created (task_id) ────────│                 │
  │                    │                  │                 │                 │
  │<── 顯示任務已創建 ─│                  │                 │                 │
  │                    │                  │                 │   (背景執行)    │
  │                    │                  │                 │<── execute_task()│
  │                    │                  │                 │                 │
  │                    │                  │                 │   1. 解析需求   │
  │                    │                  │                 │─────────────────>│
  │                    │                  │                 │   (LLM)         │
  │                    │                  │                 │                 │
  │                    │                  │                 │   2. 搜尋新聞   │
  │                    │                  │                 │─────────────────>│
  │                    │                  │                 │   (Research)    │
  │                    │                  │                 │                 │
  │                    │                  │                 │   3. 分析報告   │
  │                    │                  │                 │─────────────────>│
  │                    │                  │                 │   (Analyst)     │
  │                    │                  │                 │                 │
  │                    │                  │                 │   4. 生成文件   │
  │                    │                  │                 │─────────────────>│
  │                    │                  │                 │   (Report)      │
  │                    │                  │                 │                 │
  │                    │                  │                 │   5. 發送郵件   │
  │                    │                  │                 │─────────────────>│
  │                    │                  │                 │   (Email)       │
  │                    │                  │                 │                 │
  │                    │                  │                 │<── 完成 ─────────│
  │                    │                  │                 │                 │
  │                    │                  │<── set_succeeded()─┘              │
```

### 輪詢狀態流程

```
前端                FastAPI           服務層
  │                  │                 │
  │── GET /api/tasks/{task_id} ─────>│
  │                  │                 │
  │                  │── get_task() ──>│
  │                  │                 │
  │                  │<── task_status ─│
  │                  │                 │
  │<── 200 OK (狀態資訊) ──────────────│
  │                  │                 │
  │   (2 秒後)       │                 │
  │                  │                 │
  │── GET /api/tasks/{task_id} ─────>│
  │                  │                 │
  │   ... 重複直到 succeeded/failed
```

## 資料流

### 請求資料流

```
JSON Request Body
{
  "user_prompt": "新加坡金融科技發展趨勢",
  "email": "user@example.com",
  "language": "English",
  "time_range": "最近 7 天內",
  "count_hint": "5-10篇"
}
        │
        ▼
  Pydantic 驗證
  (NewsReportRequest)
        │
        ▼
  TaskProgress.create_task()
  建立任務紀錄
        │
        ▼
  BackgroundTasks.add_task()
  加入背景任務佇列
        │
        ▼
  返回 task_id
```

### 任務執行資料流

```
Task 執行
    │
    ├─> 1. 解析 Prompt (LLM)
    │       └─> keywords, time, count, language
    │
    ├─> 2. 搜尋新聞 (ResearchAgent)
    │       └─> search_results (含 URL、標題、內容)
    │
    ├─> 3. 分析報告 (AnalystAgent)
    │       └─> markdown_report + structured_news
    │
    ├─> 4. 生成報告 (ReportGeneratorAgent)
    │       ├─> generate_pdf() → PDF 檔案
    │       └─> generate_excel() → Excel 檔案
    │
    └─> 5. 發送郵件 (EmailAgent)
            └─> SMTP 發送 (PDF + Excel 附件)
```

## 狀態管理

### 任務狀態流轉

```
            創建任務
                │
                ▼
          ┌─────────┐
          │ queued  │ (排隊中)
          └────┬────┘
               │ 開始執行
               ▼
          ┌─────────┐
          │ running │ (執行中)
          └────┬────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
  ┌──────────┐    ┌──────────┐
  │succeeded │    │  failed  │
  └──────────┘    └──────────┘
   (成功)           (失敗)
```

### 進度追蹤

```
Progress: 0%    - queued
Progress: 10%   - running (開始)
Progress: 15%   - prompt_parsing
Progress: 20%   - prompt_parsing (完成)
Progress: 25%   - searching
Progress: 40%   - searching (完成)
Progress: 45%   - analyzing
Progress: 60%   - analyzing (完成)
Progress: 65%   - generating_report
Progress: 80%   - generating_report (完成)
Progress: 85%   - sending_email
Progress: 95%   - sending_email (完成)
Progress: 100%  - succeeded (完成)
```

## 目錄結構

```
SEANewsAlert/
│
├── app/                          # FastAPI 後端應用
│   ├── __init__.py
│   ├── main.py                   # 主應用程式
│   │   ├── FastAPI() 初始化
│   │   ├── CORS 設定
│   │   ├── Router 註冊
│   │   └── 靜態文件服務
│   │
│   ├── routers/                  # API 路由層
│   │   ├── __init__.py
│   │   └── tasks.py
│   │       ├── POST /api/tasks/news-report
│   │       └── GET  /api/tasks/{task_id}
│   │
│   └── services/                 # 業務邏輯層
│       ├── __init__.py
│       ├── progress.py           # 任務狀態管理
│       │   ├── TaskStatus (enum)
│       │   ├── TaskProgress (class)
│       │   └── task_manager (實例)
│       │
│       └── workflow.py           # 工作流程封裝
│           └── NewsReportWorkflow
│               ├── execute_task() (主流程)
│               └── _parse_prompt() (需求解析)
│
├── agents/                       # AI Agents (既有)
│   ├── __init__.py
│   ├── research_agent.py         # 搜尋代理
│   ├── analyst_agent.py          # 分析代理
│   ├── report_agent.py           # 報告生成
│   └── email_agent.py            # 郵件發送
│
├── public/                       # 靜態前端
│   └── index.html                # 測試頁面
│
├── reports/                      # 報告輸出目錄
│   ├── *.pdf                     # PDF 報告
│   └── *.xlsx                    # Excel 報告
│
├── config.py                     # 配置管理
├── .env                          # 環境變數
├── .env.example                  # 環境變數範例
│
├── requirements-api.txt          # API 依賴
├── pyproject.toml                # 專案配置
│
├── start-api.bat                 # Windows 啟動腳本
├── start-api.sh                  # Linux/Mac 啟動腳本
├── START-API.ps1                 # PowerShell 啟動腳本
│
├── test_setup.py                 # 環境驗證測試
├── test_api.py                   # API 功能測試
│
├── README-API.md                 # 完整 API 文檔
├── QUICKSTART-API.md             # 快速啟動指南
├── FASTAPI_DELIVERY_SUMMARY.md  # 交付總結
└── ARCHITECTURE.md               # 本架構圖 (此文件)
```

## 技術堆疊

```
┌─────────────────────────────────────────┐
│         應用層 (Application)            │
│  - FastAPI                              │
│  - Pydantic                             │
│  - BackgroundTasks                      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         服務層 (Services)               │
│  - NewsReportWorkflow                   │
│  - TaskProgress                         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Agent 層 (Agents)               │
│  - ResearchAgent (Agno + OpenAI)        │
│  - AnalystAgent (Agno + OpenAI)         │
│  - ReportGeneratorAgent (ReportLab)     │
│  - EmailAgent (SMTP)                    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         外部服務 (External)             │
│  - OpenAI API (GPT-4)                   │
│  - DuckDuckGo (搜尋)                    │
│  - SMTP Server (Gmail)                  │
└─────────────────────────────────────────┘
```

---

**文件版本**: 1.0  
**最後更新**: 2025-01-16
