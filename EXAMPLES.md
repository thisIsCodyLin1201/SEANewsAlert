# 📖 使用範例與常見場景

## 🎯 基本使用流程

### 1. 簡單查詢

**情境**: 想了解新加坡金融科技最新動態

**操作步驟**:
1. 訪問測試前端: http://127.0.0.1:8000/static/index.html
2. 輸入搜尋需求: `新加坡金融科技發展趨勢`
3. 輸入郵箱: `your.email@example.com`
4. 使用預設設定（語言: English，時間: 最近 7 天內，數量: 5-10篇）
5. 點擊「開始搜尋」
6. 等待 1-3 分鐘
7. 檢查郵箱，收到報告

**API 請求範例**:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/news-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "新加坡金融科技發展趨勢",
    "email": "your.email@example.com"
  }'
```

**預期輸出**:
```json
{
  "task_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": "Task started"
}
```

---

### 2. 多語言查詢

**情境**: 想要中文新聞來源

**前端操作**:
1. 訪問測試前端
2. 輸入搜尋需求: `越南股市最新動態`
3. 輸入郵箱
4. 在「進階選項」中選擇語言: `Chinese`
5. 提交

**API 請求範例**:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/news-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "越南股市最新動態",
    "email": "your.email@example.com",
    "language": "Chinese"
  }'
```

**支援的語言選項**:
- `English` (預設)
- `Chinese`
- `Vietnamese`
- `Thai`
- `Malay`
- `Indonesian`

---

### 3. 自訂時間範圍與數量

**情境**: 想要最近一個月的詳細報告（約 15 篇）

**API 請求範例**:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/news-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "泰國經濟政策變化",
    "email": "your.email@example.com",
    "language": "English",
    "time_range": "最近一個月內",
    "count_hint": "約15篇"
  }'
```

---

## 🔍 進階使用場景

### 場景 1: 多主題報告

**需求**: 同時關注多個國家的金融動態

**方法**: 在 Prompt 中列出多個主題

**Prompt 範例**:
```
請搜尋以下主題的最新新聞：
1. 新加坡金融科技發展
2. 越南股市表現
3. 泰國經濟政策
4. 印尼投資趨勢
```

**API 請求**:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/news-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "請搜尋以下主題的最新新聞：\n1. 新加坡金融科技發展\n2. 越南股市表現\n3. 泰國經濟政策\n4. 印尼投資趨勢",
    "email": "your.email@example.com",
    "count_hint": "每個主題2-3篇"
  }'
```

---

### 場景 2: 特定產業焦點

**需求**: 關注金融科技產業

**Prompt 範例**:
```
東南亞金融科技（Fintech）產業最新發展，
包括數位支付、區塊鏈、加密貨幣、數位銀行等領域
```

**API 請求**:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/news-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "東南亞金融科技（Fintech）產業最新發展，包括數位支付、區塊鏈、加密貨幣、數位銀行等領域",
    "email": "your.email@example.com",
    "time_range": "最近兩週內",
    "count_hint": "10-15篇"
  }'
```

---

### 場景 3: 輪詢任務狀態

**需求**: 在程式中追蹤任務進度

**Python 範例**:
```python
import requests
import time

# 1. 創建任務
response = requests.post(
    "http://127.0.0.1:8000/api/tasks/news-report",
    json={
        "user_prompt": "新加坡金融科技發展趨勢",
        "email": "your.email@example.com"
    }
)

task_id = response.json()["task_id"]
print(f"任務已創建: {task_id}")

# 2. 輪詢狀態
while True:
    status_response = requests.get(
        f"http://127.0.0.1:8000/api/tasks/{task_id}"
    )
    
    status_data = status_response.json()
    status = status_data["status"]
    progress = status_data["progress"]
    
    print(f"狀態: {status} | 進度: {progress}%")
    
    if status == "succeeded":
        print("任務完成！")
        print(f"PDF: {status_data['artifacts']['pdf_path']}")
        print(f"Excel: {status_data['artifacts']['xlsx_path']}")
        break
    elif status == "failed":
        print(f"任務失敗: {status_data['error']}")
        break
    
    time.sleep(2)  # 每 2 秒檢查一次
```

**JavaScript 範例**:
```javascript
// 1. 創建任務
const createTask = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/tasks/news-report', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_prompt: '新加坡金融科技發展趨勢',
      email: 'your.email@example.com'
    })
  });
  
  const data = await response.json();
  return data.task_id;
};

// 2. 輪詢狀態
const pollStatus = async (taskId) => {
  const interval = setInterval(async () => {
    const response = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}`);
    const data = await response.json();
    
    console.log(`狀態: ${data.status} | 進度: ${data.progress}%`);
    
    if (data.status === 'succeeded') {
      console.log('任務完成！');
      console.log(`PDF: ${data.artifacts.pdf_path}`);
      console.log(`Excel: ${data.artifacts.xlsx_path}`);
      clearInterval(interval);
    } else if (data.status === 'failed') {
      console.log(`任務失敗: ${data.error}`);
      clearInterval(interval);
    }
  }, 2000);
};

// 使用
(async () => {
  const taskId = await createTask();
  console.log(`任務已創建: ${taskId}`);
  await pollStatus(taskId);
})();
```

---

## 📊 報告範例

### PDF 報告結構

```
東南亞金融新聞報告
==================

📋 報告摘要
-----------
本報告涵蓋新加坡金融科技發展趨勢...

🔍 搜尋主題
-----------
新加坡金融科技發展趨勢

📅 報告日期
-----------
2025年01月16日

📰 新聞詳情
-----------

1. 新加坡推出新金融科技監管框架
   - 來源: Fintech Singapore (https://fintechnews.sg/...)
   - 日期: 2025-01-15
   - 摘要: 新加坡金融管理局（MAS）宣布...
   - 重點分析:
     1) 監管框架更新重點
     2) 對產業的影響
     3) 未來發展方向

2. DBS 銀行數位化轉型進展
   - 來源: Deal Street Asia (https://dealstreetasia.com/...)
   - 日期: 2025-01-14
   - 摘要: 星展銀行（DBS）發布...
   - 重點分析:
     1) 數位服務擴展
     2) 客戶體驗提升
     3) 技術投資策略

...（更多新聞）

💡 市場洞察
-----------
1. 新加坡持續強化金融科技監管...
2. 傳統銀行積極數位轉型...
3. 跨境支付成為新熱點...

📎 資料來源
-----------
- 新加坡推出新金融科技監管框架 (https://...)
- DBS 銀行數位化轉型進展 (https://...)
...

---
報告生成時間: 2025-01-16 10:30:00
系統: 東南亞金融新聞搜尋系統
```

### Excel 報告結構

| 新聞標題（中文） | 來源國家 | 來源網站連結 | 發布日期 | 摘要 | 重點分析 |
|-----------------|---------|-------------|----------|------|----------|
| 新加坡推出新金融科技監管框架 | Singapore | https://fintechnews.sg/... | 2025-01-15 | 新加坡金融管理局... | 1) 監管框架更新重點 2) 對產業的影響... |
| DBS 銀行數位化轉型進展 | Singapore | https://dealstreetasia.com/... | 2025-01-14 | 星展銀行發布... | 1) 數位服務擴展 2) 客戶體驗提升... |
| ... | ... | ... | ... | ... | ... |

---

## 🛠️ 整合範例

### 整合到現有 Python 應用

```python
import requests

class SEANewsClient:
    """東南亞新聞搜尋 API 客戶端"""
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
    
    def create_report(self, prompt, email, **kwargs):
        """創建新聞報告"""
        response = requests.post(
            f"{self.base_url}/api/tasks/news-report",
            json={
                "user_prompt": prompt,
                "email": email,
                **kwargs
            }
        )
        response.raise_for_status()
        return response.json()["task_id"]
    
    def get_status(self, task_id):
        """獲取任務狀態"""
        response = requests.get(
            f"{self.base_url}/api/tasks/{task_id}"
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, task_id, poll_interval=2, timeout=600):
        """等待任務完成"""
        import time
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("任務執行超時")
            
            status = self.get_status(task_id)
            
            if status["status"] == "succeeded":
                return status
            elif status["status"] == "failed":
                raise Exception(f"任務失敗: {status['error']}")
            
            time.sleep(poll_interval)

# 使用範例
client = SEANewsClient()

# 創建任務
task_id = client.create_report(
    prompt="新加坡金融科技發展趨勢",
    email="your.email@example.com",
    language="English"
)

print(f"任務已創建: {task_id}")

# 等待完成
result = client.wait_for_completion(task_id)

print(f"任務完成！")
print(f"PDF: {result['artifacts']['pdf_path']}")
print(f"Excel: {result['artifacts']['xlsx_path']}")
```

---

### 整合到 Node.js 應用

```javascript
const axios = require('axios');

class SEANewsClient {
  constructor(baseUrl = 'http://127.0.0.1:8000') {
    this.baseUrl = baseUrl;
  }

  async createReport(prompt, email, options = {}) {
    const response = await axios.post(`${this.baseUrl}/api/tasks/news-report`, {
      user_prompt: prompt,
      email: email,
      ...options
    });
    return response.data.task_id;
  }

  async getStatus(taskId) {
    const response = await axios.get(`${this.baseUrl}/api/tasks/${taskId}`);
    return response.data;
  }

  async waitForCompletion(taskId, pollInterval = 2000, timeout = 600000) {
    const startTime = Date.now();

    while (true) {
      if (Date.now() - startTime > timeout) {
        throw new Error('任務執行超時');
      }

      const status = await this.getStatus(taskId);

      if (status.status === 'succeeded') {
        return status;
      } else if (status.status === 'failed') {
        throw new Error(`任務失敗: ${status.error}`);
      }

      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  }
}

// 使用範例
(async () => {
  const client = new SEANewsClient();

  // 創建任務
  const taskId = await client.createReport(
    '新加坡金融科技發展趨勢',
    'your.email@example.com',
    { language: 'English' }
  );

  console.log(`任務已創建: ${taskId}`);

  // 等待完成
  const result = await client.waitForCompletion(taskId);

  console.log('任務完成！');
  console.log(`PDF: ${result.artifacts.pdf_path}`);
  console.log(`Excel: ${result.artifacts.xlsx_path}`);
})();
```

---

## 💡 最佳實踐

### 1. 錯誤處理

```python
import requests

def create_report_with_retry(prompt, email, max_retries=3):
    """創建報告（帶重試機制）"""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/tasks/news-report",
                json={"user_prompt": prompt, "email": email},
                timeout=10
            )
            response.raise_for_status()
            return response.json()["task_id"]
        except requests.exceptions.RequestException as e:
            print(f"嘗試 {attempt + 1}/{max_retries} 失敗: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指數退避
```

### 2. 批次處理

```python
def create_multiple_reports(queries, email):
    """批次創建多個報告"""
    task_ids = []
    
    for query in queries:
        task_id = client.create_report(query, email)
        task_ids.append(task_id)
        print(f"已創建任務: {task_id} ({query})")
    
    # 等待所有任務完成
    results = []
    for task_id in task_ids:
        result = client.wait_for_completion(task_id)
        results.append(result)
    
    return results

# 使用
queries = [
    "新加坡金融科技發展",
    "越南股市最新動態",
    "泰國經濟政策變化"
]

results = create_multiple_reports(queries, "your.email@example.com")
```

### 3. 日誌記錄

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitored_report_creation(prompt, email):
    """帶監控的報告創建"""
    logger.info(f"開始創建報告: {prompt}")
    
    task_id = client.create_report(prompt, email)
    logger.info(f"任務已創建: {task_id}")
    
    while True:
        status = client.get_status(task_id)
        logger.info(f"任務狀態: {status['status']} ({status['progress']}%)")
        
        if status["status"] in ["succeeded", "failed"]:
            break
        
        time.sleep(2)
    
    if status["status"] == "succeeded":
        logger.info(f"報告生成成功: {status['artifacts']}")
    else:
        logger.error(f"報告生成失敗: {status['error']}")
    
    return status
```

---

**文件版本**: 1.0  
**最後更新**: 2025-01-16
