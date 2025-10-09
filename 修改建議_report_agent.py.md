# Report Agent 修改建議

## 🎯 修改目標

將 `agents/report_agent.py` 從**簡單字符串匹配**改為**正確的 Markdown 解析**

## 📋 需要安裝的依賴

```bash
pip install beautifulsoup4
```

（markdown 和 reportlab 已經安裝）

## 🔧 具體修改步驟

### 步驟 1：添加導入語句

**位置**: 文件頂部 (Line 1-19)

**當前**:
```python
import markdown
from reportlab.lib.pagesizes import A4
# ... 其他導入
from html.parser import HTMLParser
```

**添加**:
```python
from bs4 import BeautifulSoup
from bs4 import NavigableString
```

**完整導入區應該是**:
```python
"""
Report Generator Agent
負責將 Markdown 報告轉換為 PDF
"""
from pathlib import Path
from datetime import datetime
from typing import Optional
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup
from bs4 import NavigableString
from config import Config
import re
```

---

### 步驟 2：重寫 `_parse_markdown_to_story` 方法

**位置**: Line 170-221

**當前代碼**（需要完全替換）:
```python
def _parse_markdown_to_story(self, markdown_content: str):
    """將 Markdown 內容轉換為 ReportLab Story"""
    story = []
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.2*inch))
            continue
        
        # H1 標題
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, self.styles['CustomTitle']))
            story.append(Spacer(1, 0.3*inch))
        # ... 更多 if-elif
```

**新代碼**（完全替換）:
```python
def _parse_markdown_to_story(self, markdown_content: str):
    """將 Markdown 內容轉換為 ReportLab Story（改進版）"""
    # Step 1: 使用 markdown 庫將 Markdown 轉換為 HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    
    # Step 2: 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Step 3: 將 HTML 元素轉換為 ReportLab 元素
    story = []
    
    for element in soup.children:
        # 跳過純文本節點（如果在根層級）
        if isinstance(element, NavigableString):
            continue
        
        # 處理標題
        if element.name == 'h1':
            text = self._extract_text(element)
            story.append(Paragraph(text, self.styles['CustomTitle']))
            story.append(Spacer(1, 0.3*inch))
        
        elif element.name == 'h2':
            text = self._extract_text(element)
            story.append(Paragraph(text, self.styles['CustomHeading2']))
            story.append(Spacer(1, 0.2*inch))
        
        elif element.name == 'h3':
            text = self._extract_text(element)
            story.append(Paragraph(text, self.styles['CustomHeading3']))
            story.append(Spacer(1, 0.1*inch))
        
        # 處理段落
        elif element.name == 'p':
            text = self._process_inline_elements(element)
            if text.strip():
                story.append(Paragraph(text, self.styles['CustomBody']))
                story.append(Spacer(1, 0.1*inch))
        
        # 處理無序列表
        elif element.name == 'ul':
            for li in element.find_all('li', recursive=False):
                text = self._process_inline_elements(li)
                bullet_text = '• ' + text
                story.append(Paragraph(bullet_text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
        
        # 處理有序列表
        elif element.name == 'ol':
            for idx, li in enumerate(element.find_all('li', recursive=False), 1):
                text = self._process_inline_elements(li)
                numbered_text = f'{idx}. {text}'
                story.append(Paragraph(numbered_text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
        
        # 處理水平線
        elif element.name == 'hr':
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph('_' * 80, self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # 處理引用塊
        elif element.name == 'blockquote':
            text = self._process_inline_elements(element)
            # 可以創建特殊的引用樣式
            story.append(Paragraph(f'"{text}"', self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
    
    return story
```

---

### 步驟 3：添加輔助方法

**位置**: 在 `_parse_markdown_to_story` 方法之後

**添加以下兩個新方法**:

```python
def _extract_text(self, element):
    """從 HTML 元素中提取純文本"""
    return element.get_text().strip()

def _process_inline_elements(self, element):
    """
    處理段落內的內聯元素（粗體、斜體、連結）
    將它們轉換為 ReportLab 的 HTML 標籤格式
    """
    result = ""
    
    for child in element.descendants:
        if isinstance(child, NavigableString):
            # 純文本節點
            if child.parent == element or child.parent.name in ['li', 'p', 'blockquote']:
                result += str(child)
        
        elif child.name == 'strong' or child.name == 'b':
            # 粗體
            text = child.get_text()
            result += f'<b>{text}</b>'
        
        elif child.name == 'em' or child.name == 'i':
            # 斜體
            text = child.get_text()
            result += f'<i>{text}</i>'
        
        elif child.name == 'a':
            # 連結
            text = child.get_text()
            href = child.get('href', '')
            # 格式: 文字 (URL)
            result += f'{text} (<font color="blue"><u>{href}</u></font>)'
        
        elif child.name == 'code':
            # 代碼（內聯）
            text = child.get_text()
            result += f'<font face="Courier">{text}</font>'
    
    # 清理多餘的空白
    result = ' '.join(result.split())
    return result
```

---

### 步驟 4：刪除不再需要的方法（可選）

**可以保留以下方法作為備用**，但它們不再被使用:
- `_clean_markdown` (Line 223)
- `_clean_markdown_links` (Line 238)

或者，你可以註釋掉這些方法並添加說明:
```python
# def _clean_markdown(self, text: str) -> str:
#     """已棄用 - 使用 markdown 庫和 BeautifulSoup 替代"""
#     pass

# def _clean_markdown_links(self, text: str) -> str:
#     """已棄用 - 使用 markdown 庫和 BeautifulSoup 替代"""
#     pass
```

---

### 步驟 5：刪除不再使用的類（可選）

**位置**: Line 21-31

**當前代碼**:
```python
class HTMLToTextParser(HTMLParser):
    """簡單的 HTML 轉文字解析器"""
    def __init__(self):
        super().__init__()
        self.text = []
        
    def handle_data(self, data):
        self.text.append(data)
        
    def get_text(self):
        return ''.join(self.text)
```

這個類不再需要，因為 BeautifulSoup 提供了更好的功能。可以刪除或註釋掉。

---

## 📝 完整的修改後文件結構

```python
# 導入區
from bs4 import BeautifulSoup
from bs4 import NavigableString
# ... 其他導入

# 類定義
class ReportGeneratorAgent:
    def __init__(self):
        # ... 不變
    
    def setup_styles(self):
        # ... 不變
    
    def generate_pdf(self, markdown_content, filename=None):
        # ... 不變
    
    def _parse_markdown_to_story(self, markdown_content: str):
        # ✅ 新的實現（使用 markdown + BeautifulSoup）
        ...
    
    def _extract_text(self, element):
        # ✅ 新方法
        ...
    
    def _process_inline_elements(self, element):
        # ✅ 新方法
        ...
    
    # 舊方法（可以刪除或保留）
    # def _clean_markdown(self, text: str):
    # def _clean_markdown_links(self, text: str):
```

---

## 🧪 測試方法

### 測試 1：使用現有的測試代碼

**位置**: 文件底部 (Line 247-269)

```bash
python agents/report_agent.py
```

應該生成 `test_report.pdf`，檢查：
- ✅ 標題格式
- ✅ 粗體 (`**文字**` 應該顯示為粗體)
- ✅ 連結 (`[文字](URL)` 應該顯示連結)
- ✅ 列表格式

### 測試 2：創建更完整的測試

在 `__main__` 區塊添加更多測試:

```python
if __name__ == "__main__":
    agent = ReportGeneratorAgent()
    
    test_markdown = """
# 測試報告

## 格式測試

### 粗體和斜體
這是 **粗體文字** 和 *斜體文字* 的測試。

### 連結測試
訪問 [Google](https://www.google.com) 獲取更多資訊。

### 列表測試

#### 無序列表
- 項目 1
- 項目 2
- 項目 3

#### 有序列表
1. 第一項
2. 第二項
3. 第三項

### 混合格式
這是一個包含 **粗體**、*斜體* 和 [連結](https://example.com) 的段落。

---

報告結束。
"""
    
    pdf_path = agent.generate_pdf(test_markdown, "test_format.pdf")
    print(f"測試 PDF 已生成: {pdf_path}")
```

---

## ⚠️ 注意事項

### 1. 中文字體處理

當前的中文字體註冊應該繼續工作，但如果遇到問題，可以改進:

```python
def setup_styles(self):
    """設置 PDF 樣式"""
    self.styles = getSampleStyleSheet()
    
    # 改進的字體註冊
    try:
        from reportlab.pdfbase.ttfonts import TTFont
        font_registered = False
        
        # 支援更多字體
        font_paths = [
            ('C:\\Windows\\Fonts\\msjh.ttc', 'Microsoft JhengHei'),  # 微軟正黑體
            ('C:\\Windows\\Fonts\\msyh.ttc', 'Microsoft YaHei'),     # 微軟雅黑
            ('C:\\Windows\\Fonts\\kaiu.ttf', 'DFKai-SB'),            # 標楷體
        ]
        
        for font_path, font_name in font_paths:
            if Path(font_path).exists():
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    self.chinese_font = 'ChineseFont'
                    font_registered = True
                    print(f"✅ 已註冊中文字體: {font_name} ({font_path})")
                    break
                except Exception as e:
                    print(f"⚠️ 字體註冊失敗 {font_name}: {e}")
                    continue
        
        if not font_registered:
            print("⚠️ 未找到中文字體，使用預設字體（中文可能顯示不正確）")
            self.chinese_font = 'Helvetica'
    
    except Exception as e:
        print(f"⚠️ 字體處理錯誤: {e}")
        self.chinese_font = 'Helvetica'
    
    # 其餘樣式設置保持不變
    ...
```

### 2. 處理特殊字符

ReportLab 的 Paragraph 需要 XML 安全的文字:

```python
def _process_inline_elements(self, element):
    """處理內聯元素"""
    result = ""
    
    for child in element.descendants:
        if isinstance(child, NavigableString):
            text = str(child)
            # 轉義特殊字符
            text = text.replace('&', '&amp;')
            text = text.replace('<', '&lt;')
            text = text.replace('>', '&gt;')
            result += text
        # ... 其他處理
    
    return result
```

### 3. 嵌套列表

如果需要支援嵌套列表，需要遞歸處理:

```python
elif element.name == 'ul':
    self._process_list(element, story, bullet='•')

def _process_list(self, list_element, story, bullet='•', indent=0):
    """遞歸處理列表（支援嵌套）"""
    for li in list_element.find_all('li', recursive=False):
        # 處理列表項文本
        text = self._process_inline_elements(li)
        bullet_text = '  ' * indent + bullet + ' ' + text
        story.append(Paragraph(bullet_text, self.styles['CustomBody']))
        
        # 處理嵌套列表
        nested_ul = li.find('ul', recursive=False)
        if nested_ul:
            self._process_list(nested_ul, story, bullet='◦', indent=indent+1)
```

---

## 📊 修改前後對比

### 修改前
```
Markdown 文字
    ↓ (簡單字符串匹配)
    split('\n')
    if line.startswith('# '):
    ↓
ReportLab 元素 (基本格式)
```

### 修改後
```
Markdown 文字
    ↓ (markdown 庫)
HTML
    ↓ (BeautifulSoup)
解析的 HTML 樹
    ↓ (遍歷和轉換)
ReportLab 元素 (完整格式)
```

---

## ✅ 檢查清單

修改完成後，確認以下項目:

- [ ] BeautifulSoup 已導入
- [ ] `_parse_markdown_to_story` 使用 markdown 庫
- [ ] 添加了 `_extract_text` 方法
- [ ] 添加了 `_process_inline_elements` 方法
- [ ] 測試代碼可以運行
- [ ] 生成的 PDF 包含正確的格式:
  - [ ] 標題 (H1, H2, H3)
  - [ ] 粗體
  - [ ] 斜體
  - [ ] 連結
  - [ ] 列表
  - [ ] 中文顯示正常

---

## 🔗 相關文檔

- `MARKDOWN_PDF_分析報告.md` - 完整問題分析
- `架構分析圖.txt` - 視覺化架構圖
- `快速參考指南.md` - JSON vs Markdown 使用指南

---

**修改建議生成時間**: 2025-10-03  
**目標文件**: `agents/report_agent.py`  
**預計修改時間**: 30-60 分鐘
