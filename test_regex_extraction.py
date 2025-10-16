"""
測試摘要和重點分析的正則表達式提取
"""
import re

# 模擬 Markdown 報告的不同格式
test_cases = [
    {
        "name": "標準格式（換行+新項目）",
        "content": """- **來源**：[Bloomberg](https://example.com)
- **日期**：2025-10-15
- **摘要**：新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。
- **重點分析**：1) 科技股帶動 2) 外資流入
"""
    },
    {
        "name": "格式2（摘要後無破折號）",
        "content": """- **來源**：[Bloomberg](https://example.com)
- **日期**：2025-10-15
- **摘要**：新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。
**重點分析**：1) 科技股帶動 2) 外資流入
"""
    },
    {
        "name": "格式3（冒號變體）",
        "content": """- **來源**: [Bloomberg](https://example.com)
- **日期**: 2025-10-15
- **摘要**: 新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。
- **重點分析**: 1) 科技股帶動 2) 外資流入
"""
    },
    {
        "name": "格式4（無破折號前綴）",
        "content": """**來源**：[Bloomberg](https://example.com)
**日期**：2025-10-15
**摘要**：新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。
**重點分析**：1) 科技股帶動 2) 外資流入
"""
    },
    {
        "name": "格式5（多行摘要）",
        "content": """- **來源**：[Bloomberg](https://example.com)
- **日期**：2025-10-15
- **摘要**：新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。
  科技股領漲，其中半導體相關公司表現尤為突出，投資者對區域經濟前景保持樂觀態度。
- **重點分析**：1) 科技股帶動大盤上漲 2) 外資持續流入 3) 經濟數據優於預期
"""
    },
    {
        "name": "格式6（AI 可能的實際輸出）",
        "content": """- **來源**：[The Straits Times](https://www.straitstimes.com/business/fintech-2025)
- **日期**：2025-10-15
- **摘要**：新加坡金融管理局宣布，將在2026年推出新的數位支付框架，以支持金融科技創新並加強消費者保護。此舉被視為新加坡進一步鞏固其作為全球金融科技中心地位的重要步驟。該框架將涵蓋數位錢包、即時支付系統和跨境支付等領域，並要求所有金融科技公司遵守更嚴格的安全和隱私標準。
- **重點分析**：
  1) 新加坡持續強化金融科技監管框架
  2) 數位支付成為政策重點
  3) 跨境支付創新受到鼓勵
  4) 消費者保護措施升級

"""
    }
]

# 測試不同的正則表達式
patterns = [
    {
        "name": "原始模式",
        "pattern": r'\*\*摘要\*\*[：:]\s*(.*?)(?=\n\s*[-\*]|\Z)'
    },
    {
        "name": "改進模式1（匹配到下一個粗體或結束）",
        "pattern": r'\*\*摘要\*\*[：:]\s*(.*?)(?=\n\*\*|\Z)'
    },
    {
        "name": "改進模式2（匹配到換行符後的破折號）",
        "pattern": r'\*\*摘要\*\*[：:]\s*(.*?)(?=\n-\s*\*\*|\n\*\*|\Z)'
    },
    {
        "name": "改進模式3（非貪婪匹配到下一個粗體標記）",
        "pattern": r'\*\*摘要\*\*[：:]\s*((?:(?!\*\*).)*)'
    },
    {
        "name": "改進模式4（包含多行）",
        "pattern": r'\*\*摘要\*\*[：:]\s*([^\n]*(?:\n(?!\s*[-\*]\s*\*\*)[^\n]*)*)'
    }
]

print("=" * 80)
print("正則表達式測試：摘要提取")
print("=" * 80)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n測試案例 {i}: {test_case['name']}")
    print("-" * 80)
    
    for pattern_info in patterns:
        match = re.search(pattern_info['pattern'], test_case['content'], re.DOTALL)
        
        if match:
            summary = match.group(1).strip()
            # 限制顯示長度
            display_summary = summary[:60] + "..." if len(summary) > 60 else summary
            print(f"✅ {pattern_info['name']:30s}: {display_summary}")
        else:
            print(f"❌ {pattern_info['name']:30s}: 無法匹配")

# 測試重點分析
print("\n" + "=" * 80)
print("正則表達式測試：重點分析提取")
print("=" * 80)

analysis_patterns = [
    {
        "name": "原始模式",
        "pattern": r'\*\*重點分析\*\*[：:]\s*(.*?)(?=\n\s*[-\*]|\Z)'
    },
    {
        "name": "改進模式（匹配到下一個標題或結束）",
        "pattern": r'\*\*重點分析\*\*[：:]\s*((?:(?!###).)*)'
    },
    {
        "name": "改進模式（包含換行和條列）",
        "pattern": r'\*\*重點分析\*\*[：:]\s*([^\n]*(?:\n(?!\s*###|\s*##)[^\n]*)*)'
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n測試案例 {i}: {test_case['name']}")
    print("-" * 80)
    
    for pattern_info in analysis_patterns:
        match = re.search(pattern_info['pattern'], test_case['content'], re.DOTALL)
        
        if match:
            analysis = match.group(1).strip()
            display_analysis = analysis[:60] + "..." if len(analysis) > 60 else analysis
            print(f"✅ {pattern_info['name']:40s}: {display_analysis}")
        else:
            print(f"❌ {pattern_info['name']:40s}: 無法匹配")

print("\n" + "=" * 80)
print("推薦使用的正則表達式模式")
print("=" * 80)
print("""
# 摘要提取（推薦）：
summary_pattern = r'\\*\\*摘要\\*\\*[：:]\\s*([^\\n]*(?:\\n(?!\\s*[-\\*]\\s*\\*\\*)[^\\n]*)*)'

# 重點分析提取（推薦）：
analysis_pattern = r'\\*\\*重點分析\\*\\*[：:]\\s*([^\\n]*(?:\\n(?!\\s*###|\\s*##)[^\\n]*)*)'

說明：
- 匹配「**摘要**：」或「**摘要**:」
- 捕獲第一行內容
- 繼續捕獲後續行，直到遇到新的項目（- **xxx**）或新的標題（###）
- 使用非貪婪匹配，避免過度捕獲
""")
