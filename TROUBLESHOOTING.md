# ⚠️ PowerShell 啟動問題解決方案

## 問題描述

執行 `.\START-API.ps1` 時出現錯誤：
```
uvicorn: The term 'uvicorn' is not recognized as a name of a cmdlet...
```

## 原因分析

這個問題有幾個可能的原因：

1. **虛擬環境路徑問題** - PowerShell 的虛擬環境啟動可能失敗
2. **PATH 環境變數** - uvicorn 不在系統 PATH 中
3. **執行策略限制** - PowerShell 執行策略可能阻止腳本運行

## ✅ 解決方案（推薦順序）

### 方案 1：使用簡化版啟動腳本（最簡單）

我已經創建了一個更可靠的啟動腳本：

```bash
start-api-simple.bat
```

這個腳本會：
- 使用系統的 Python（不依賴虛擬環境）
- 自動檢查並安裝缺少的套件
- 直接啟動服務

**使用方式**：
```powershell
.\start-api-simple.bat
```

---

### 方案 2：直接使用 Python 命令（推薦）

不使用啟動腳本，直接運行：

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

這是最可靠的方式，因為：
- 直接使用 `python -m` 調用模組
- 不依賴虛擬環境啟動
- 不需要 uvicorn 在 PATH 中

---

### 方案 3：修復 PowerShell 執行策略

如果你想繼續使用 PowerShell 腳本，可能需要調整執行策略：

```powershell
# 檢查當前執行策略
Get-ExecutionPolicy

# 如果是 Restricted，需要改為 RemoteSigned
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然後再次執行
.\START-API.ps1
```

---

### 方案 4：在 CMD 中使用 BAT 腳本

如果 PowerShell 有問題，可以使用 CMD：

```cmd
start-api-simple.bat
```

---

## ✅ 當前狀態

**好消息！** 🎉 我已經幫你成功啟動了服務！

服務目前正在運行：
- 地址: http://127.0.0.1:8000
- API 文檔: http://127.0.0.1:8000/docs
- 測試前端: http://127.0.0.1:8000/static/index.html

你可以直接訪問這些網址來使用系統。

---

## 📝 推薦的啟動方式

### Windows 用戶

#### 選項 A：使用 BAT 腳本（最簡單）
```cmd
start-api-simple.bat
```

#### 選項 B：直接使用 Python（最可靠）
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 選項 C：創建桌面快捷方式

1. 右鍵桌面 → 新增 → 捷徑
2. 輸入位置：
   ```
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. 工作目錄設為：`C:\Cathay\SEANewsAlert`
4. 命名為「啟動新聞搜尋 API」

---

## 🔧 驗證服務是否運行

### 方法 1：訪問網頁
打開瀏覽器訪問：http://127.0.0.1:8000

### 方法 2：使用 curl
```powershell
curl http://127.0.0.1:8000/health
```

### 方法 3：查看進程
```powershell
# PowerShell
Get-Process python

# CMD
tasklist | findstr python
```

---

## 🛑 如何停止服務

### 如果服務在前台運行
按 `Ctrl + C`

### 如果服務在背景運行
```powershell
# 找到 Python 進程
Get-Process python | Where-Object {$_.MainWindowTitle -like "*uvicorn*"} | Stop-Process

# 或者直接停止所有 Python 進程（小心使用）
Get-Process python | Stop-Process
```

---

## 📋 完整的啟動檢查清單

1. ✅ 確認在專案目錄：`C:\Cathay\SEANewsAlert`
2. ✅ 確認 Python 已安裝：`python --version`
3. ✅ 確認套件已安裝：`python -m pip show fastapi uvicorn`
4. ✅ 確認 `.env` 文件已設定
5. ✅ 使用推薦的啟動方式：`python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
6. ✅ 訪問測試：http://127.0.0.1:8000

---

## 💡 額外提示

### 開發模式（自動重載）
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 生產模式（無自動重載）
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 指定不同端口
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

### 顯示詳細日誌
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --log-level debug
```

---

## 🎯 總結

**最簡單的啟動方式**：

```powershell
# 方式 1：使用 BAT 腳本
.\start-api-simple.bat

# 方式 2：直接命令（推薦）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**驗證服務**：
訪問 http://127.0.0.1:8000/docs

**停止服務**：
按 `Ctrl + C`

---

**目前狀態：✅ 服務已啟動並運行中！**

可以直接開始使用了！🚀
