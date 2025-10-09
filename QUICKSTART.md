# 🚀 快速入門指南

歡迎使用東南亞金融新聞智能搜尋與報告系統！本指南將幫助您在 5 分鐘內啟動系統。

## ✅ 前置檢查清單

在開始之前，請確認以下項目：

- [ ] Python 3.11 或更高版本已安裝
- [ ] 已取得 OpenAI API Key
- [ ] 已設定 Gmail 應用程式密碼（用於發送郵件）
- [ ] 已安裝 UV 套件管理工具（可選，腳本會自動安裝）

## 📦 安裝步驟

### Windows 用戶

1. **開啟 PowerShell 並導航到專案目錄**
```powershell
cd C:\Cathay\NewSeaNews
```

2. **執行自動設置腳本**
```powershell
.\scripts\setup.ps1
```

如果遇到執行策略問題，先執行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **或手動安裝**
```powershell
# 安裝 UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 建立虛擬環境
uv venv

# 啟動虛擬環境
.\.venv\Scripts\Activate.ps1

# 安裝依賴
uv pip install -e .
```

### macOS / Linux 用戶

```bash
# 執行設置腳本
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## 🔑 配置 API Keys

`.env` 文件已包含配置模板，請確認以下資訊：

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
```

### 如何取得 Gmail 應用程式密碼

1. 前往 [Google 帳戶設定](https://myaccount.google.com/)
2. 選擇「安全性」
3. 啟用「兩步驟驗證」
4. 搜尋「應用程式密碼」
5. 選擇「郵件」和「其他裝置」
6. 生成密碼並複製到 `.env` 文件

## ✅ 驗證系統

```powershell
python main.py validate
```

您應該看到：
```
✅ 配置驗證成功
🚀 初始化東南亞金融新聞搜尋系統...
✅ 所有 Agents 初始化完成
🔍 驗證 Agents...
✅ 所有 Agents 驗證通過
```

## 🎯 第一次使用

### 方式 1: Web 介面（推薦新手）

1. **啟動 Web 應用**
```powershell
streamlit run app.py
```

2. **瀏覽器會自動開啟** `http://localhost:8501`

3. **輸入搜尋資訊**
   - 搜尋主題：`新加坡金融科技發展趨勢`
   - 收件人郵箱：`your-email@example.com`

4. **點擊「開始搜尋並寄送報告」**

5. **等待執行**（約 1-2 分鐘）
   - 🔍 搜尋新聞
   - 📊 分析資訊
   - 📄 生成 PDF
   - 📧 發送郵件

6. **檢查郵箱**，您會收到 PDF 報告！

### 方式 2: 命令列介面（適合進階用戶）

```powershell
python main.py cli `
  -q "馬來西亞經濟政策最新動態" `
  -e "recipient@example.com"
```

## 📝 使用建議

### 推薦搜尋主題範例

1. **國家經濟**
   - 新加坡 2025 年經濟展望
   - 泰國旅遊產業復甦狀況
   - 印尼數位經濟發展

2. **金融市場**
   - 東南亞股市本週表現
   - 馬來西亞林吉特匯率走勢
   - 菲律賓央行利率決策

3. **產業動態**
   - 越南製造業投資趨勢
   - 新加坡金融科技創新
   - 東南亞電商市場分析

### 搜尋技巧

✅ **好的搜尋**：
- "新加坡金融科技最新發展"
- "泰國旅遊業 2025 年趨勢"
- "東南亞跨境支付創新"

❌ **避免過於籠統**：
- "新聞"
- "經濟"
- "金融"

## 🎨 界面說明

### Web 介面功能

1. **搜尋輸入框**
   - 支援繁體中文輸入
   - 最多 500 字
   - 支援多行輸入

2. **郵箱輸入框**
   - 支援單個或多個郵箱
   - 多個郵箱用逗號分隔
   - 自動格式驗證

3. **進度顯示**
   - 即時顯示各步驟狀態
   - 預估執行時間
   - 錯誤提示

4. **結果查看**
   - 執行摘要
   - PDF 路徑
   - 執行時長統計

## 🔧 常見問題

### Q1: 系統啟動失敗？

**A:** 檢查 Python 版本和依賴安裝
```powershell
python --version  # 應該 >= 3.11
uv pip list       # 查看已安裝套件
```

### Q2: OpenAI API 錯誤？

**A:** 確認 API Key 正確且有額度
- 檢查 `.env` 文件中的 `OPENAI_API_KEY`
- 前往 [OpenAI 平台](https://platform.openai.com/) 查看額度
- 確認 API 端點可訪問

### Q3: 郵件發送失敗？

**A:** Gmail 安全設定問題
- 確認已啟用兩步驟驗證
- 使用應用程式密碼，不是帳號密碼
- 檢查 SMTP 端口（587）未被防火牆阻擋

### Q4: PDF 生成失敗？

**A:** 檢查 WeasyPrint 依賴
```powershell
uv pip install weasyprint --upgrade
```

### Q5: 搜尋結果不理想？

**A:** 優化搜尋查詢
- 使用更具體的關鍵字
- 指定國家或地區
- 添加時間範圍（如"最近一週"）

## 📊 系統監控

### 查看生成的報告

所有 PDF 報告儲存在：
```
C:\Cathay\NewSeaNews\reports\
```

### 查看日誌

執行時會在終端顯示即時日誌：
```
🔍 Research Agent 開始搜尋...
✅ Research Agent 搜尋完成
📊 Analyst Agent 開始分析...
✅ Analyst Agent 分析完成
...
```

## 🎓 進階使用

### 自定義配置

編輯 `config.py` 調整系統設定：
- 更改 OpenAI 模型
- 調整報告樣式
- 修改郵件模板

### 開發新功能

參考 `PRD.md` 和 `README.md` 了解系統架構。

### 測試

```powershell
# 執行測試
pytest tests/ -v

# 執行特定測試
pytest tests/test_agents.py -v
```

## 🆘 需要幫助？

1. **查看完整文檔**
   - `README.md` - 專案概覽
   - `PRD.md` - 產品需求文件
   - `DEPLOYMENT.md` - 部署指南

2. **檢查錯誤日誌**
   - 終端輸出
   - 錯誤訊息

3. **驗證系統**
```powershell
python main.py validate
```

## 🎉 開始使用！

現在您已經準備好了！執行以下命令開始：

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

祝您使用愉快！🚀

---

**提示**: 第一次執行可能需要較長時間（下載模型），請耐心等待。
**建議**: 先用簡單的測試查詢熟悉系統，再進行實際使用。
