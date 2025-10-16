"""
測試 Excel 新增「摘要」和「重點分析」欄位功能
"""
import sys
import os

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.analyst_agent import AnalystAgent
from agents.report_agent import ReportGeneratorAgent
from pathlib import Path


def test_summary_and_analysis_extraction():
    """測試從 Markdown 中提取摘要和重點分析"""
    
    print("=" * 70)
    print("測試 Excel 新欄位：摘要、重點分析")
    print("=" * 70)
    print()
    
    # 創建測試用的 Markdown 報告
    test_markdown = """
# 東南亞金融新聞報告

## 📋 報告摘要
本報告涵蓋東南亞主要國家的金融市場動態。

## 📰 新聞詳情

### 1. 新加坡股市創新高 科技股領漲
- **來源**：[彭博社](https://www.bloomberg.com/news/article1)
- **日期**：2025-10-15
- **摘要**：新加坡海峽時報指數今日收盤上漲1.8%，創下歷史新高。科技股領漲，其中半導體相關公司表現尤為突出，投資者對區域經濟前景保持樂觀態度。
- **重點分析**：1) 科技股帶動大盤上漲 2) 外資持續流入 3) 經濟數據優於預期 4) 區域市場情緒轉好

### 2. 馬來西亞央行維持基準利率不變
- **來源**：[路透社](https://www.reuters.com/news/article2)
- **日期**：2025-10-14
- **摘要**：馬來西亞國家銀行在最新的貨幣政策會議上決定維持隔夜政策利率在3.00%不變，符合市場預期。央行表示將持續監控通脹和經濟成長狀況。
- **重點分析**：1) 貨幣政策維持穩定 2) 通脹壓力可控 3) 經濟成長動能良好 4) 林吉特匯率穩定

### 3. 泰國旅遊業復甦強勁 帶動經濟成長
- **來源**：[曼谷郵報](https://www.bangkokpost.com/news/article3)
- **日期**：2025-10-13
- **摘要**：泰國旅遊局公布最新數據顯示，今年前9個月外國遊客人數已超過2500萬人次，較去年同期成長35%。旅遊業強勁復甦成為經濟成長的主要動力。
- **重點分析**：1) 中國遊客回流明顯 2) 酒店業營收創新高 3) 零售消費增加 4) 就業市場改善

## 💡 市場洞察
1. 東南亞股市整體表現優於全球平均
2. 區域經濟復甦態勢明確
3. 外資持續看好東南亞市場前景
"""
    
    print("步驟 1: 測試 Analyst Agent 提取功能")
    print("-" * 70)
    
    analyst = AnalystAgent()
    structured_news = analyst._extract_from_markdown(test_markdown, "東南亞金融市場")
    
    print(f"✅ 成功提取 {len(structured_news)} 則新聞\n")
    
    # 驗證提取結果
    for i, news in enumerate(structured_news, 1):
        print(f"新聞 {i}:")
        print(f"  標題: {news.get('新聞標題（中文）', 'N/A')}")
        print(f"  國家: {news.get('來源國家', 'N/A')}")
        print(f"  日期: {news.get('發布日期', 'N/A')}")
        print(f"  連結: {news.get('來源網站連結', 'N/A')}")
        
        summary = news.get('摘要', '')
        analysis = news.get('重點分析', '')
        
        if summary:
            print(f"  摘要: {summary[:50]}..." if len(summary) > 50 else f"  摘要: {summary}")
            print(f"       ✅ 摘要欄位存在")
        else:
            print(f"       ❌ 摘要欄位缺失")
        
        if analysis:
            print(f"  重點分析: {analysis[:50]}..." if len(analysis) > 50 else f"  重點分析: {analysis}")
            print(f"           ✅ 重點分析欄位存在")
        else:
            print(f"           ❌ 重點分析欄位缺失")
        
        print()
    
    print("=" * 70)
    print("步驟 2: 測試 Excel 生成功能")
    print("-" * 70)
    
    report_generator = ReportGeneratorAgent()
    excel_path = report_generator.generate_excel(structured_news, "測試報告_含摘要分析.xlsx")
    
    print(f"\n✅ Excel 文件已生成: {excel_path}")
    print(f"   文件大小: {excel_path.stat().st_size / 1024:.2f} KB")
    
    # 驗證 Excel 內容
    print("\n步驟 3: 驗證 Excel 文件內容")
    print("-" * 70)
    
    import pandas as pd
    df = pd.read_excel(excel_path)
    
    print(f"✅ Excel 欄位: {list(df.columns)}")
    print(f"✅ 資料筆數: {len(df)}")
    print()
    
    # 檢查必要欄位是否存在
    required_columns = ['新聞標題（中文）', '來源國家', '來源網站連結', '發布日期', '摘要', '重點分析']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ 缺少欄位: {missing_columns}")
    else:
        print("✅ 所有必要欄位都存在")
    
    # 檢查摘要和重點分析是否有內容
    summary_filled = df['摘要'].notna().sum()
    analysis_filled = df['重點分析'].notna().sum()
    
    print(f"\n資料完整度:")
    print(f"  摘要欄位有內容: {summary_filled}/{len(df)} ({summary_filled/len(df)*100:.1f}%)")
    print(f"  重點分析有內容: {analysis_filled}/{len(df)} ({analysis_filled/len(df)*100:.1f}%)")
    
    if summary_filled == len(df) and analysis_filled == len(df):
        print("\n✅ 測試完全成功！所有新聞都包含摘要和重點分析")
    elif summary_filled > 0 and analysis_filled > 0:
        print("\n⚠️ 測試部分成功，部分新聞包含摘要和重點分析")
    else:
        print("\n❌ 測試失敗，摘要或重點分析未能正確提取")
    
    print("\n" + "=" * 70)
    print("測試完成")
    print("=" * 70)


if __name__ == "__main__":
    test_summary_and_analysis_extraction()
