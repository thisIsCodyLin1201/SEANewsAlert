# 語言指定功能 - 快速參考

## 🎯 核心概念

系統現在可以**智能識別**用戶需求中的語言指定，如果沒有指定，則**預設使用英文新聞**。

## ✅ 支援的語言

| 語言 | 識別關鍵字範例 | 搜尋優化 |
|------|--------------|---------|
| English (預設) | 英文、英語、English | in English |
| Chinese | 中文、華語、中文版 | 中文 OR 華語 OR Chinese |
| Vietnamese | 越南文、越南語 | tiếng Việt OR Vietnamese |
| Thai | 泰文、泰語 | ภาษาไทย OR Thai |
| Malay | 馬來文、馬來語 | Bahasa Melayu OR Malay |
| Indonesian | 印尼文、印尼語 | Bahasa Indonesia OR Indonesian |

## 📝 使用範例

### ✨ 指定語言的範例

```
✅ "我想找最近一個月內，關於新加坡AI領域的20篇中文投資趨勢新聞"
   → 語言: Chinese

✅ "找10篇關於泰國央行的英文新聞"
   → 語言: English

✅ "越南電商市場分析（越南文）"
   → 語言: Vietnamese

✅ "印尼金融科技新聞 印尼語"
   → 語言: Indonesian
```

### 🔄 未指定語言（自動預設英文）

```
⚪ "馬來西亞房地產趨勢"
   → 語言: English (預設)

⚪ "新加坡金融科技"
   → 語言: English (預設)

⚪ "找10篇關於泰國央行的新聞"
   → 語言: English (預設)
```

## 🧪 測試驗證

執行測試腳本:
```bash
.venv/Scripts/python.exe test_language_detection.py
```

**測試結果**: ✅ 5/5 全部通過

## 🔧 技術細節

### 解析流程
1. 用戶輸入需求 → 
2. AI 解析提取語言指定 → 
3. 生成對應的搜尋關鍵字 → 
4. 優先搜尋指定語言的新聞

### 容錯機制
- 如果 AI 解析失敗 → 自動回退到預設值 (English)
- 如果語言不在支援列表 → 使用 "in English"

### 相關檔案
- `workflow.py` - Prompt 解析邏輯
- `research_agent.py` - 搜尋執行邏輯
- `test_language_detection.py` - 語言功能測試

## 💡 最佳實踐

1. **明確指定**: 如果需要特定語言，請在需求中明確說明
2. **預設英文**: 不確定時，系統會使用英文，這是最安全的選擇
3. **自然表達**: 可以用中文、括號、或直接說明的方式指定語言

## 📊 實際運作範例

```
輸入: "找最近一週的新加坡金融科技中文新聞"

解析結果:
{
    "keywords": "新加坡金融科技",
    "time_instruction": "最近一週",
    "num_instruction": "5-10篇",
    "language": "Chinese"  ← 成功識別
}

搜尋優化:
→ 加入關鍵字: "中文 OR 華語 OR Chinese"
→ 優先搜尋中文新聞來源
```

---

**功能狀態**: ✅ 已實現並測試完成  
**預設行為**: 英文 (English)  
**AI 解析**: OpenAI GPT 智能識別
