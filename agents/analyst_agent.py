"""
Analyst Agent
負責將搜尋結果結構化並整理成專業報告
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import Config
from typing import Dict, Any
from datetime import datetime


class AnalystAgent:
    """分析代理 - 將原始搜尋結果整理成結構化報告"""
    
    def __init__(self):
        """初始化 Analyst Agent"""
        self.agent = Agent(
            name="金融新聞分析師",
            model=OpenAIChat(
                id=Config.OPENAI_MODEL,
                api_key=Config.OPENAI_API_KEY,
                max_tokens=4096,  # 增加輸出 token 限制，允許更詳細的報告
            ),
            description="專業的金融新聞分析師，擅長整理和結構化資訊",
            instructions=[
                "你是一位專業的金融分析師，負責整理新聞資訊",
                "將搜尋結果整理成清晰、專業的繁體中文報告",
                "報告結構應包含：標題、摘要、詳細內容、資料來源",
                "使用 Markdown 格式輸出",
                "每條新聞都要附上來源超連結",
                "去除重複和冗餘資訊",
                "按照重要性和時間順序排列",
                "使用專業但易懂的語言",
                "提供詳細且深入的分析，不要過於簡短",
                "每條新聞的摘要應該詳細完整，至少 150-300 字",
                "市場洞察部分應該提供 5-8 點深入的分析"
            ],
            markdown=True,
        )
    
    def analyze(self, search_results: Dict[str, Any]) -> str:
        """
        分析並結構化搜尋結果
        
        Args:
            search_results: 來自 Research Agent 的搜尋結果
            
        Returns:
            str: Markdown 格式的報告
        """
        print("📊 Analyst Agent 開始分析...")
        
        # 提取搜尋內容
        content = search_results.get("content", "")
        query = search_results.get("query", "")
        
        # 構建分析提示
        analysis_prompt = f"""
        請將以下搜尋結果整理成一份專業的繁體中文金融報告。
        
        原始查詢：{query}
        搜尋結果：
        {content}
        
        報告格式要求：
        
        # 東南亞金融新聞報告
        
        ## 📋 報告摘要
        [用 2-3 句話總結本報告的核心內容]
        
        ## 🔍 搜尋主題
        {query}
        
        ## 📅 報告日期
        {datetime.now().strftime("%Y年%m月%d日")}
        
        ## 📰 新聞詳情
        
        ### 1. [新聞標題]
        - **來源**：[來源名稱]([網址])
        - **日期**：[發布日期]
        - **摘要**：[新聞摘要，100-200字]
        - **重點分析**：[關鍵資訊提取]
        
        ### 2. [新聞標題]
        ...
        
        ## 💡 市場洞察
        [基於以上新聞，提供 3-5 點關鍵洞察]
        
        ## 📎 資料來源
        - [來源1標題](網址)
        - [來源2標題](網址)
        ...
        
        ---
        **報告生成時間**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        **系統**：{Config.APP_NAME}
        
        注意事項：
        1. 所有內容必須使用繁體中文
        2. 超連結格式：[標題](網址)
        3. 去除重複資訊
        4. 保持專業且易讀
        5. 如果沒有找到相關新聞，請明確說明
        """
        
        try:
            # 使用 Agent 執行分析
            response = self.agent.run(analysis_prompt)
            
            # 提取 Markdown 內容
            if hasattr(response, 'content'):
                markdown_report = response.content
            else:
                markdown_report = str(response)
            
            print("✅ Analyst Agent 分析完成")
            return markdown_report
            
        except Exception as e:
            print(f"❌ Analyst Agent 分析失敗: {str(e)}")
            # 返回錯誤報告
            return f"""
# 報告生成失敗

## 錯誤資訊
{str(e)}

## 原始搜尋查詢
{query}

請檢查系統設定並重試。
"""


if __name__ == "__main__":
    # 測試 Analyst Agent
    agent = AnalystAgent()
    
    # 模擬搜尋結果
    mock_results = {
        "status": "success",
        "query": "新加坡股市動態",
        "content": "測試內容：新加坡海峽時報指數上漲..."
    }
    
    report = agent.analyze(mock_results)
    print(report)
