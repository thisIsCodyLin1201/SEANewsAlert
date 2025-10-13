"""
測試 Excel 生成功能
"""
from agents.report_agent import ReportGeneratorAgent
from pathlib import Path

# 創建測試數據 - 新格式（移除「關鍵字」和「來源」欄位）
test_news_data = [
    {
        '新聞標題（中文）': '新加坡金融科技創新達到新高峰',
        '來源國家': '新加坡',
        '來源網站連結': 'https://www.example.com/news1',
        '發布日期': '2025-10-13'
    },
    {
        '新聞標題（中文）': '馬來西亞央行宣布新利率政策',
        '來源國家': '馬來西亞',
        '來源網站連結': 'https://www.example.com/news2',
        '發布日期': '2025-10-12'
    },
    {
        '新聞標題（中文）': '泰國股市迎來外資大量流入',
        '來源國家': '泰國',
        '來源網站連結': 'https://www.example.com/news3',
        '發布日期': '2025-10-11'
    },
    {
        '新聞標題（中文）': '印尼推出數位貨幣試點計劃',
        '來源國家': '印尼',
        '來源網站連結': 'https://www.example.com/news4',
        '發布日期': '2025-10-10'
    },
    {
        '新聞標題（中文）': '越南經濟增長超出預期',
        '來源國家': '越南',
        '來源網站連結': 'https://www.example.com/news5',
        '發布日期': '2025-10-09'
    }
]

def test_excel_generation():
    """測試 Excel 生成功能"""
    print("=" * 60)
    print("開始測試 Excel 生成功能")
    print("=" * 60)
    
    try:
        # 初始化 ReportGeneratorAgent
        report_agent = ReportGeneratorAgent()
        
        # 生成 Excel 文件
        excel_path = report_agent.generate_excel(
            news_data=test_news_data,
            filename='測試報告_東南亞金融新聞.xlsx'
        )
        
        # 驗證文件是否存在
        if excel_path.exists():
            print(f"\n✅ Excel 文件生成成功！")
            print(f"📁 文件路徑: {excel_path}")
            print(f"📊 文件大小: {excel_path.stat().st_size / 1024:.2f} KB")
            print(f"📋 新聞數量: {len(test_news_data)} 則")
            
            print("\n" + "=" * 60)
            print("測試結果：成功 ✅")
            print("=" * 60)
            return True
        else:
            print("\n❌ Excel 文件未能生成")
            return False
            
    except Exception as e:
        print(f"\n❌ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_excel_generation()
