# PDF 格式修復說明

## 問題描述
PDF 中出現未渲染的 Markdown 符號，例如：
```
• **來源**:Pattaya Mail
• **日期**:2025年09月28日
• **摘要**:泰國旅遊業即將進入期待已久的旺季...
```

在 PDF 中顯示為原始 Markdown 格式，而不是渲染後的粗體效果。

## 根本原因
在 `agents/report_agent.py` 的 `_parse_markdown_to_story` 方法中：
- 處理列表項時（第 201-205 行），只調用了 `_clean_markdown_links()` 清理連結
- **沒有調用** `_clean_markdown()` 清理粗體和斜體標記
- 導致 `**text**` 和 `*text*` 等 Markdown 格式符號直接顯示在 PDF 中

## 修復方案

### 修改 1: 列表項處理
**文件**: `agents/report_agent.py` (第 200-205 行)

**修改前**:
```python
# 列表項
elif line.startswith('- ') or line.startswith('* '):
    text = '• ' + line[2:].strip()
    # 清理 Markdown 連結格式
    text = self._clean_markdown_links(text)
    story.append(Paragraph(text, self.styles['CustomBody']))
```

**修改後**:
```python
# 列表項
elif line.startswith('- ') or line.startswith('* '):
    text = '• ' + line[2:].strip()
    # 清理 Markdown 格式（包含粗體、斜體和連結）
    text = self._clean_markdown(text)
    story.append(Paragraph(text, self.styles['CustomBody']))
```

### 修改 2: 優化 Markdown 清理正則表達式
**文件**: `agents/report_agent.py` (第 223-236 行)

**修改前**:
```python
def _clean_markdown(self, text: str) -> str:
    """清理 Markdown 格式標記"""
    # 移除粗體標記
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
    
    # 移除斜體標記
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
    
    # 清理連結
    text = self._clean_markdown_links(text)
    
    return text
```

**修改後**:
```python
def _clean_markdown(self, text: str) -> str:
    """清理 Markdown 格式標記"""
    # 先處理粗體標記（兩個星號或底線）
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
    
    # 再處理斜體標記（單個星號或底線，但不能是已經處理過的粗體）
    # 使用負向先行斷言避免匹配 <b> 標籤內的內容
    text = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'(?<!_)_(?!_)([^_]+?)(?<!_)_(?!_)', r'<i>\1</i>', text)
    
    # 清理連結
    text = self._clean_markdown_links(text)
    
    return text
```

## 修復效果

### 修復前
```
• **來源**:Pattaya Mail
• **日期**:2025年09月28日
• **摘要**:泰國旅遊業即將進入期待已久的旺季...
• **重點分析**:安全與刺激措施對提升遊客數量和重建信心至關重要。
```

### 修復後
```
• 來源:Pattaya Mail (粗體效果)
• 日期:2025年09月28日 (粗體效果)
• 摘要:泰國旅遊業即將進入期待已久的旺季... (粗體效果)
• 重點分析:安全與刺激措施對提升遊客數量和重建信心至關重要。(粗體效果)
```

## 測試驗證

已創建測試文件驗證修復效果：
- `reports/test_markdown_rendering.pdf` - 基本 Markdown 格式測試
- `reports/test_full_markdown_formatting.pdf` - 完整格式測試（粗體、斜體、連結）

測試內容包括：
1. ✅ 粗體格式 (`**text**`)
2. ✅ 斜體格式 (`*text*`)
3. ✅ 連結格式 (`[文字](URL)`)
4. ✅ 混合格式使用
5. ✅ 實際新聞報告案例

## 兼容性
- ✅ 不影響現有功能
- ✅ 向後兼容
- ✅ 所有 Markdown 格式都能正確轉換

## 如何驗證修復
1. 重新啟動應用程式（已自動完成）
2. 生成一份新的報告
3. 檢查 PDF 中的格式是否正確顯示（粗體、斜體、連結）

---

**修復時間**: 2025-10-03
**修復文件**: `agents/report_agent.py`
**測試狀態**: ✅ 通過
