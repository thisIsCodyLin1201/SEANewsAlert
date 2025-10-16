git # 🚀 如何啟動系統

## 方法 1: 使用啟動腳本（最簡單）✨

### Windows PowerShell

```powershell
.\START.ps1
```

或

```powershell
.\start.bat
```

### Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

---

## 方法 2: 手動啟動

### Windows

```powershell
# 方式 A: 直接執行（推薦）
.\.venv\Scripts\python.exe -m streamlit run app.py

# 方式 B: 先啟動虛擬環境
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

### Linux / macOS

```bash
# 方式 A: 直接執行
./.venv/bin/python -m streamlit run app.py

# 方式 B: 先啟動虛擬環境
source .venv/bin/activate
python -m streamlit run app.py
```

---

## 方法 3: 使用 Python 主程式

### Web 介面

```powershell
python main.py web
```

### 命令列模式

```powershell
python main.py cli -q "搜尋主題" -e "your@email.com"
```

---

## 訪問系統

啟動後，在瀏覽器中訪問：

- **http://localhost:8501**
- **http://127.0.0.1:8501**

---

## 停止服務

按 `Ctrl + C` 即可停止服務

---

## 常見問題

### Q: 提示 "streamlit: command not found"？

**A:** 使用完整路徑或先啟動虛擬環境：

```powershell
# Windows
.\.venv\Scripts\python.exe -m streamlit run app.py

# Linux/macOS
./.venv/bin/python -m streamlit run app.py
```

### Q: 無法連接到 localhost:8501？

**A:** 嘗試使用 IP 地址：

```
http://127.0.0.1:8501
```

或檢查防火牆設定。

### Q: 需要重新安裝依賴？

**A:** 執行：

```powershell
.\.venv\Scripts\Activate.ps1
uv pip install -e .
```

---

## 完整啟動流程（首次使用）

```powershell
# 1. 建立虛擬環境
uv venv

# 2. 啟動虛擬環境
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/macOS

# 3. 安裝依賴
uv pip install -e .

# 4. 驗證系統
python main.py validate

# 5. 啟動應用
python -m streamlit run app.py
```

---

## 快速命令參考

| 操作 | 命令 |
|------|------|
| 啟動 Web 介面 | `.\START.ps1` 或 `.\.venv\Scripts\python.exe -m streamlit run app.py` |
| 驗證系統 | `python main.py validate` |
| CLI 模式 | `python main.py cli -q "查詢" -e "email"` |
| 執行測試 | `pytest tests/ -v` |
| 停止服務 | `Ctrl + C` |

---

## PDF 字體確認

系統已自動註冊 Windows 中文字體（微軟正黑體）。

生成的 PDF 會顯示：
✅ **已註冊中文字體: C:\Windows\Fonts\msjh.ttc**

測試 PDF 檔案位於：`reports/test_full_chinese.pdf`

---

**提示**: 建議使用 `.\START.ps1` 啟動腳本，最簡單快速！
