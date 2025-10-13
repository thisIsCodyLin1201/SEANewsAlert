# 語言指定功能說明

## 功能概述

系統現在支援在搜尋新聞時**指定新聞來源的語言**。如果用戶沒有明確指定語言，系統將預設搜尋**英文新聞**。

## 支援的語言

- **English** (英文) - 預設語言
- **Chinese** (中文/華語)
- **Vietnamese** (越南文)
- **Thai** (泰文)
- **Malay** (馬來文)
- **Indonesian** (印尼文)

## 使用方式

### 方式 1: 直接在需求中說明語言
```
我想找最近一個月內，關於新加坡AI領域的20篇中文投資趨勢新聞
```
→ 系統會解析出: `language='Chinese'`

### 方式 2: 在需求結尾註明語言
```
找10篇關於泰國央行的英文新聞
```
→ 系統會解析出: `language='English'`

### 方式 3: 使用括號說明
```
越南電商市場分析（越南文）
```
→ 系統會解析出: `language='Vietnamese'`

### 方式 4: 直接說明語言名稱
```
印尼金融科技新聞 印尼語
```
→ 系統會解析出: `language='Indonesian'`

### 方式 5: 沒有指定語言（預設）
```
馬來西亞房地產趨勢
```
→ 系統會使用預設值: `language='English'`

## 技術實現

### 1. Prompt 解析階段 (`workflow.py`)

`_parse_prompt()` 方法會從用戶需求中提取四個關鍵資訊：

```python
{
    "keywords": "核心搜尋主題",
    "time_instruction": "時間範圍",
    "num_instruction": "新聞數量",
    "language": "新聞語言"  # 新增欄位
}
```

### 2. 搜尋階段 (`research_agent.py`)

`ResearchAgent.search()` 方法接收語言參數並：

1. 根據指定語言建立對應的搜尋關鍵字：
   - English → "in English"
   - Chinese → "中文 OR 華語 OR Chinese"
   - Vietnamese → "tiếng Việt OR Vietnamese"
   - Thai → "ภาษาไทย OR Thai"
   - Malay → "Bahasa Melayu OR Malay"
   - Indonesian → "Bahasa Indonesia OR Indonesian"

2. 將語言關鍵字加入搜尋提示中，優先搜尋指定語言的新聞來源

## 測試結果

執行 `test_language_detection.py` 的測試結果：

| 測試案例 | 輸入 | 解析語言 | 結果 |
|---------|------|---------|------|
| 1 | 關於新加坡AI領域的20篇**中文**投資趨勢新聞 | Chinese | ✅ |
| 2 | 找10篇關於泰國央行的**英文**新聞 | English | ✅ |
| 3 | 越南電商市場分析（**越南文**） | Vietnamese | ✅ |
| 4 | 馬來西亞房地產趨勢（無語言指定） | English | ✅ |
| 5 | 印尼金融科技新聞 **印尼語** | Indonesian | ✅ |

**測試成功率: 5/5 (100%)**

## 預設行為

**重要**: 當用戶沒有明確指定新聞語言時，系統將**預設搜尋英文新聞**。

這是因為：
1. 英文是國際金融新聞的主流語言
2. 英文新聞來源較為豐富且容易取得
3. 符合大多數商業用戶的需求

## 程式碼變更摘要

### `workflow.py`
- 修改 `_parse_prompt()` 的 prompt，增加語言提取指令
- 解析結果中增加 `language` 欄位（預設 "English"）
- 在搜尋時傳遞 `language` 參數給 `ResearchAgent`

### `research_agent.py`
- `search()` 方法簽名增加 `language` 參數
- 建立語言關鍵字映射表
- 在搜尋提示中加入語言要求和對應關鍵字

## 使用範例

### 範例 1: 搜尋中文新聞
```
用戶輸入: "我想找最近一週內，關於新加坡金融科技的中文新聞"

系統解析:
- keywords: "新加坡金融科技"
- time_instruction: "最近一週內"
- num_instruction: "5-10篇"
- language: "Chinese"

搜尋時會優先尋找: 中文 OR 華語 OR Chinese 的新聞來源
```

### 範例 2: 搜尋泰文新聞
```
用戶輸入: "泰國股市最新消息 泰文"

系統解析:
- keywords: "泰國股市"
- time_instruction: "最近7天內" (預設)
- num_instruction: "5-10篇" (預設)
- language: "Thai"

搜尋時會優先尋找: ภาษาไทย OR Thai 的新聞來源
```

### 範例 3: 沒有指定語言（預設英文）
```
用戶輸入: "越南經濟成長報告"

系統解析:
- keywords: "越南經濟成長報告"
- time_instruction: "最近7天內" (預設)
- num_instruction: "5-10篇" (預設)
- language: "English" (預設)

搜尋時會優先尋找: in English 的新聞來源
```

## 注意事項

1. **智能解析**: 系統會使用 AI (OpenAI GPT) 智能解析用戶需求中的語言指定
2. **容錯機制**: 如果解析失敗，會回退到預設值 (English)
3. **搜尋優化**: 語言關鍵字會被加入搜尋提示中，幫助搜尋引擎找到對應語言的內容
4. **多語言支援**: 搜尋關鍵字使用 "OR" 邏輯，增加找到相關內容的機率

## 後續建議

1. 可以考慮在 UI 中加入語言選擇下拉選單
2. 可以根據用戶歷史偏好記憶預設語言
3. 可以支援多語言混合搜尋（例如: "中文或英文"）
4. 可以在報告中標示每則新聞的實際語言

---

**更新日期**: 2025-01-13  
**測試狀態**: ✅ 已驗證  
**相關檔案**: `workflow.py`, `research_agent.py`, `test_language_detection.py`
