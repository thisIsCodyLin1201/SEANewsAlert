"""
測試從 Markdown 提取日期功能
"""
from agents.analyst_agent import AnalystAgent

# 創建模擬的搜尋結果和 Markdown 報告
mock_search_results = {
    "status": "success",
    "query": "新加坡金融科技",
    "content": """這是模擬的搜尋內容"""
}

# 創建包含日期資訊的 Markdown 報告
test_markdown = """
# 東南亞金融新聞報告

## 📋 報告摘要
本報告涵蓋東南亞主要國家的金融科技發展動態。

## 🔍 搜尋主題
新加坡金融科技

## 📅 報告日期
2025年10月13日

## 📰 新聞詳情

### 1. 新加坡金融科技創新達到新高峰
- **來源**：[Singapore Times](https://www.example.com/news1)
- **日期**：2025-10-13
- **摘要**：新加坡金融科技公司在數位支付領域取得重大突破...

### 2. 馬來西亞央行發布數位貨幣白皮書
- **來源**：[Malaysia Financial News](https://www.example.com/news2)
- **日期**：2025年10月12日
- **摘要**：馬來西亞央行今日發布數位貨幣研究白皮書...

### 3. 泰國推動區塊鏈技術應用
- **來源**：[Bangkok Post](https://www.example.com/news3)
- **日期**：2025/10/11
- **摘要**：泰國政府宣布將在金融領域大力推動區塊鏈技術...

## 💡 市場洞察
- 東南亞金融科技市場持續升溫
- 各國政府積極推動數位化轉型

---
**報告生成時間**：2025-10-13 14:30:00
**系統**：東南亞金融新聞智能搜尋與報告系統
"""

def test_date_extraction():
    """測試日期提取和中文標題功能"""
    print("=" * 60)
    print("開始測試日期提取和中文標題功能")
    print("=" * 60)
    
    try:
        # 初始化 AnalystAgent
        analyst = AnalystAgent()
        
        # 使用私有方法提取結構化數據
        structured_news = analyst._extract_from_markdown(test_markdown, "新加坡金融科技")
        
        print(f"\n📋 提取到 {len(structured_news)} 則新聞\n")
        
        # 驗證標題是否為中文
        chinese_titles = []
        for idx, news in enumerate(structured_news, 1):
            title = news.get('新聞標題（中文）', 'N/A')
            print(f"新聞 {idx}:")
            print(f"  標題: {title}")
            print(f"  國家: {news.get('來源國家', 'N/A')}")
            print(f"  日期: {news.get('發布日期', 'N/A')}")
            print(f"  連結: {news.get('來源網站連結', 'N/A')}")
            
            # 檢查標題是否包含中文字元
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in title)
            if has_chinese:
                chinese_titles.append(title)
            print(f"  ✓ 標題為中文: {'是' if has_chinese else '否'}")
            print()
        
        # 驗證日期是否正確提取
        dates_extracted = [news.get('發布日期', '') for news in structured_news]
        dates_with_content = [d for d in dates_extracted if d]
        
        print("=" * 60)
        print("測試結果：")
        print(f"  📰 新聞數量: {len(structured_news)}")
        print(f"  ✅ 日期提取成功: {len(dates_with_content)}/{len(structured_news)}")
        print(f"  ✅ 中文標題數量: {len(chinese_titles)}/{len(structured_news)}")
        
        all_success = (
            len(dates_with_content) == len(structured_news) and
            len(chinese_titles) == len(structured_news)
        )
        
        if all_success:
            print("\n🎉 所有測試通過！")
        else:
            print("\n⚠️  部分測試未通過")
        print("=" * 60)
        
        return all_success
        
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_date_extraction()
    exit(0 if success else 1)
