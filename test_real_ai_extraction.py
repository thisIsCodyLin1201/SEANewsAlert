"""
實際測試：調用真實 AI 生成報告，驗證摘要和重點分析提取
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import ResearchAgent, AnalystAgent, ReportGeneratorAgent
from config import Config
import pandas as pd


def validate_config():
    """驗證配置"""
    if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your-openai-api-key":
        print("❌ 請先設定 OPENAI_API_KEY")
        return False
    print("✅ 配置驗證成功")
    return True


def test_real_ai_workflow():
    """使用真實 AI 測試完整工作流程"""
    if not validate_config():
        return
    
    print("=" * 80)
    print("真實 AI 測試：生成報告並驗證摘要和重點分析提取")
    print("=" * 80)
    print()
    
    # 步驟 1: 搜尋（使用較少的文章以節省 tokens）
    print("📍 步驟 1: 執行搜尋")
    print("-" * 80)
    research_agent = ResearchAgent()
    search_results = research_agent.search(
        query="新加坡金融科技",
        time_instruction="最近7天內",
        num_instruction="2篇",  # 只要2篇以節省時間
        language="English"
    )
    
    if search_results.get("status") == "error":
        print(f"❌ 搜尋失敗: {search_results.get('error')}")
        return
    
    print(f"✅ 搜尋完成 (內容長度: {len(search_results.get('content', ''))} 字元)")
    print()
    
    # 步驟 2: 分析生成報告
    print("📍 步驟 2: AI 分析並生成 Markdown 報告")
    print("-" * 80)
    analyst_agent = AnalystAgent()
    markdown_report, structured_news = analyst_agent.analyze(search_results)
    
    print(f"✅ 報告生成完成 (Markdown 長度: {len(markdown_report)} 字元)")
    print(f"✅ 提取到 {len(structured_news)} 則新聞")
    print()
    
    # 步驟 3: 顯示 Markdown 報告片段
    print("📍 步驟 3: 檢查 Markdown 報告格式")
    print("-" * 80)
    
    # 檢查是否包含必要的格式標記
    has_title_marker = "###" in markdown_report
    has_source_marker = "**來源**" in markdown_report or "**來源**:" in markdown_report
    has_date_marker = "**日期**" in markdown_report or "**日期**:" in markdown_report
    has_summary_marker = "**摘要**" in markdown_report or "**摘要**:" in markdown_report
    has_analysis_marker = "**重點分析**" in markdown_report or "**重點分析**:" in markdown_report
    
    print(f"包含標題標記 (###): {'✅' if has_title_marker else '❌'}")
    print(f"包含來源標記: {'✅' if has_source_marker else '❌'}")
    print(f"包含日期標記: {'✅' if has_date_marker else '❌'}")
    print(f"包含摘要標記: {'✅' if has_summary_marker else '❌'}")
    print(f"包含重點分析標記: {'✅' if has_analysis_marker else '❌'}")
    print()
    
    # 顯示第一則新聞的完整內容
    print("📄 第一則新聞的 Markdown 原始內容:")
    print("=" * 80)
    import re
    news_sections = re.findall(r'(###\s+\d+\..*?)(?=###|\Z)', markdown_report, re.DOTALL)
    if news_sections:
        first_news = news_sections[0]
        print(first_news[:1500])  # 顯示前1500字元
        if len(first_news) > 1500:
            print("\n... (內容被截斷)")
    print("=" * 80)
    print()
    
    # 步驟 4: 檢查提取的結構化數據
    print("📍 步驟 4: 檢查提取的結構化數據")
    print("-" * 80)
    
    summary_count = 0
    analysis_count = 0
    
    for i, news in enumerate(structured_news, 1):
        print(f"\n新聞 {i}:")
        print(f"  📰 標題: {news.get('新聞標題（中文）', 'N/A')[:60]}...")
        print(f"  🌏 國家: {news.get('來源國家', 'N/A')}")
        print(f"  📅 日期: {news.get('發布日期', 'N/A')}")
        print(f"  🔗 連結: {news.get('來源網站連結', 'N/A')[:60]}...")
        
        summary = news.get('摘要', '')
        analysis = news.get('重點分析', '')
        
        if summary and summary.strip():
            summary_count += 1
            print(f"  📝 摘要: {summary[:100]}..." if len(summary) > 100 else f"  📝 摘要: {summary}")
            print(f"      ✅ 摘要有內容 ({len(summary)} 字元)")
        else:
            print(f"      ❌ 摘要為空")
        
        if analysis and analysis.strip():
            analysis_count += 1
            print(f"  🎯 重點分析: {analysis[:100]}..." if len(analysis) > 100 else f"  🎯 重點分析: {analysis}")
            print(f"      ✅ 重點分析有內容 ({len(analysis)} 字元)")
        else:
            print(f"      ❌ 重點分析為空")
    
    print()
    print(f"📊 統計: 摘要 {summary_count}/{len(structured_news)}, 重點分析 {analysis_count}/{len(structured_news)}")
    print()
    
    # 步驟 5: 生成 Excel
    print("📍 步驟 5: 生成 Excel 並驗證")
    print("-" * 80)
    
    report_agent = ReportGeneratorAgent()
    excel_path = report_agent.generate_excel(structured_news, "真實測試_含摘要分析.xlsx")
    
    print(f"✅ Excel 已生成: {excel_path}")
    print(f"   檔案大小: {excel_path.stat().st_size / 1024:.2f} KB")
    print()
    
    # 步驟 6: 讀取並驗證 Excel
    print("📍 步驟 6: 讀取 Excel 驗證內容")
    print("-" * 80)
    
    df = pd.read_excel(excel_path)
    
    print(f"Excel 欄位: {list(df.columns)}")
    print(f"資料筆數: {len(df)}")
    print()
    
    if '摘要' in df.columns and '重點分析' in df.columns:
        excel_summary_count = df['摘要'].notna().sum()
        excel_analysis_count = df['重點分析'].notna().sum()
        
        print(f"Excel 中有內容的摘要: {excel_summary_count}/{len(df)}")
        print(f"Excel 中有內容的重點分析: {excel_analysis_count}/{len(df)}")
        print()
        
        # 顯示 Excel 中的資料
        print("Excel 資料預覽:")
        print("=" * 80)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 60)
        print(df.to_string(index=False))
        print("=" * 80)
    else:
        print("❌ Excel 缺少摘要或重點分析欄位！")
    
    print()
    
    # 最終結論
    print("=" * 80)
    print("🎯 測試結論")
    print("=" * 80)
    
    if summary_count == len(structured_news) and analysis_count == len(structured_news):
        print("✅ 完全成功！所有新聞都成功提取摘要和重點分析")
    elif summary_count > 0 or analysis_count > 0:
        print(f"⚠️ 部分成功：{summary_count}/{len(structured_news)} 摘要, {analysis_count}/{len(structured_news)} 重點分析")
        print("\n可能的原因：")
        print("1. AI 沒有嚴格按照指定格式生成內容")
        print("2. 部分新聞缺少摘要或重點分析欄位")
        print("3. 正則表達式需要進一步調整")
    else:
        print("❌ 失敗：所有摘要和重點分析都是空值")
        print("\n需要檢查：")
        print("1. Markdown 報告的實際格式")
        print("2. 正則表達式是否能匹配實際格式")
        print("3. AI 指令是否明確")
    
    print()
    print(f"📁 詳細資料請查看: {excel_path}")
    print("=" * 80)


if __name__ == "__main__":
    test_real_ai_workflow()
