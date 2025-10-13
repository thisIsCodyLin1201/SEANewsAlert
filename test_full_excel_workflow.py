"""
完整測試：從 Markdown 報告生成 Excel，驗證中文標題
"""
from agents.analyst_agent import AnalystAgent
from agents.report_agent import ReportGeneratorAgent
from pathlib import Path

# 模擬的搜尋結果（包含中文翻譯的 Markdown 報告）
mock_search_results = {
    "status": "success",
    "query": "新加坡金融科技發展",
    "content": """
# 東南亞金融新聞報告

## 📋 報告摘要
本報告涵蓋新加坡金融科技領域的最新發展動態。

## 📰 新聞詳情

### 1. 新加坡金融科技投資創歷史新高
- **來源**：[The Straits Times](https://www.straitstimes.com/business/fintech-2025)
- **日期**：2025-10-13
- **摘要**：新加坡在2025年第三季度的金融科技投資達到創紀錄的50億美元...

### 2. 馬來西亞推出數位銀行執照
- **來源**：[The Star](https://www.thestar.com.my/business/digital-banks)
- **日期**：2025-10-12
- **摘要**：馬來西亞央行宣布將發放五張數位銀行執照...

### 3. 泰國央行測試數位泰銖
- **來源**：[Bangkok Post](https://www.bangkokpost.com/business/cbdc-trial)
- **日期**：2025年10月11日
- **摘要**：泰國央行啟動了數位泰銖的第二階段試點計劃...

## 💡 市場洞察
- 東南亞金融科技投資持續增長
- 數位貨幣成為各國央行關注焦點
"""
}

def test_full_workflow():
    """測試完整工作流程：Markdown -> 結構化數據 -> Excel"""
    print("=" * 70)
    print("完整工作流程測試：驗證 Excel 中的中文標題")
    print("=" * 70)
    
    try:
        # 步驟 1: 初始化 Agents
        print("\n📝 步驟 1: 初始化 Agents...")
        analyst = AnalystAgent()
        report_agent = ReportGeneratorAgent()
        
        # 步驟 2: 使用 AnalystAgent 提取結構化數據
        print("\n📊 步驟 2: 從 Markdown 報告中提取結構化新聞數據...")
        markdown_content = mock_search_results['content']
        query = mock_search_results['query']
        
        # 使用 _extract_structured_data 方法
        structured_news = analyst._extract_structured_data(
            markdown_report=markdown_content,
            raw_content=mock_search_results['content'],
            query=query
        )
        
        print(f"   ✓ 提取到 {len(structured_news)} 則新聞")
        
        # 步驟 3: 驗證標題是否為中文
        print("\n📰 步驟 3: 驗證新聞標題...")
        chinese_count = 0
        for idx, news in enumerate(structured_news, 1):
            title = news.get('新聞標題（中文）', '')
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in title)
            
            print(f"   新聞 {idx}:")
            print(f"      標題: {title}")
            print(f"      中文: {'✓' if has_chinese else '✗'}")
            print(f"      日期: {news.get('發布日期', 'N/A')}")
            
            if has_chinese:
                chinese_count += 1
        
        # 步驟 4: 生成 Excel 文件
        print(f"\n📊 步驟 4: 生成 Excel 文件...")
        excel_path = report_agent.generate_excel(
            news_data=structured_news,
            filename='完整測試_中文標題驗證.xlsx'
        )
        
        # 步驟 5: 驗證結果
        print("\n" + "=" * 70)
        print("測試結果摘要：")
        print("=" * 70)
        print(f"  📊 Excel 文件: {excel_path.name}")
        print(f"  📏 文件大小: {excel_path.stat().st_size / 1024:.2f} KB")
        print(f"  📰 新聞數量: {len(structured_news)}")
        print(f"  ✅ 中文標題: {chinese_count}/{len(structured_news)}")
        print(f"  📅 含日期資訊: {sum(1 for n in structured_news if n.get('發布日期'))}/{len(structured_news)}")
        
        # 驗證欄位
        print("\n  📋 Excel 欄位檢查:")
        if structured_news:
            sample = structured_news[0]
            expected_fields = ['新聞標題（中文）', '來源國家', '來源網站連結', '發布日期']
            for field in expected_fields:
                has_field = field in sample
                print(f"      {field}: {'✓' if has_field else '✗'}")
            
            # 檢查不應該存在的欄位
            removed_fields = ['關鍵字', '來源']
            for field in removed_fields:
                if field not in sample:
                    print(f"      {field} (已移除): ✓")
        
        print("\n" + "=" * 70)
        
        # 判斷測試是否成功
        success = (
            chinese_count == len(structured_news) and
            len(structured_news) > 0 and
            excel_path.exists()
        )
        
        if success:
            print("🎉 測試完全通過！Excel 中的標題已正確翻譯為中文")
            print(f"📁 請查看: {excel_path}")
        else:
            print("⚠️  測試未完全通過，請檢查上述結果")
        
        print("=" * 70)
        
        return success
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_workflow()
    exit(0 if success else 1)
