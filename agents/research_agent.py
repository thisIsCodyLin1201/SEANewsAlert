"""
Research Agent
負責使用 ChatGPT 進行深度網路搜尋
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from config import Config
import json
from typing import Dict, Any


class ResearchAgent:
    """研究代理 - 執行深度網路搜尋"""
    
    def __init__(self):
        """初始化 Research Agent"""
        # 確保使用一致的 OpenAI 端點
        self.agent = Agent(
            name="東南亞金融新聞研究員",
            model=OpenAIChat(
                id=Config.OPENAI_MODEL,
                api_key=Config.OPENAI_API_KEY,
                max_tokens=2048,
            ),
            tools=[DuckDuckGoTools()],
            description="專門搜尋和分析東南亞金融市場新聞的研究員",
            instructions=[
                "你是一位專業的金融新聞研究員，專注於東南亞市場",
                "使用搜尋工具查找最新、最相關的金融新聞",
                "搜尋時優先關注：新加坡、馬來西亞、泰國、印尼、越南、菲律賓等國家",
                "關注主題包括：股市、匯率、經濟政策、投資趨勢、企業動態",
                "收集至少 5-10 條高質量新聞資訊",
                "記錄每條新聞的來源網址",
                "以 JSON 格式整理結果"
            ],
            markdown=True,
        )
    
    def search(self, query: str, time_instruction: str = "最近 7 天內", num_instruction: str = "5-10篇") -> Dict[str, Any]:
        """
        執行搜尋
        
        Args:
            query: 用戶的搜尋查詢
            time_instruction: 時間範圍指令 (例如: "最近一個月內")
            num_instruction: 新聞數量指令 (例如: "約15篇")
            
        Returns:
            Dict: 包含搜尋結果和來源的字典
        """
        print(f"🔍 Research Agent 開始搜尋: {query} ({time_instruction}, {num_instruction})")
        
        # 強化搜尋提示詞，聚焦東南亞金融
        enhanced_query = f"""
        請扮演一位頂尖的金融研究員，深入搜尋關於「{query}」的東南亞金融新聞。

        **核心任務指令:**
        1.  **搜尋範圍**: 嚴格鎖定東南亞國家（新加坡、馬來西亞、泰國、印尼、越南、菲律賓）。
        2.  **時間要求**: 嚴格篩選在 **{time_instruction}** 內發布的新聞。
        3.  **數量要求**: 你的目標是找到並提供 **{num_instruction}** 的高品質新聞。你必須盡力達成這個數量目標。
        4.  **重試策略**: 如果初步搜尋結果數量不足，**請不要隨意更改核心關鍵字**。你應該嘗試從**更多元、更廣泛的來源網站**（例如：其他國家的主流媒體、專業金融分析網站、行業部落格）進行搜尋，以擴大資訊覆蓋面。
        5.  **資訊完整性**: 每條新聞都必須包含清晰的「標題」、「摘要」、「來源網站」、「完整網址」和「發布日期」。

        **輸出格式要求:**
        你必須嚴格遵循下面的 JSON 格式返回結果。`results` 陣列必須包含所有找到的新聞。

        ```json
        {{
            "search_query": "{query}",
            "search_date": "YYYY-MM-DD",
            "results": [
                {{
                    "title": "新聞標題範例 1",
                    "summary": "這是第一則新聞的摘要內容...",
                    "source": "新聞來源 A",
                    "url": "https://example.com/news-article-1",
                    "date": "YYYY-MM-DD"
                }},
                {{
                    "title": "新聞標題範例 2",
                    "summary": "這是第二則新聞的摘要內容...",
                    "source": "新聞來源 B",
                    "url": "https://example.com/news-article-2",
                    "date": "YYYY-MM-DD"
                }}
            ]
        }}
        ```
        """
        
        try:
            # 使用 Agent 執行搜尋
            response = self.agent.run(enhanced_query)
            
            # 提取回應內容
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            print("✅ Research Agent 搜尋完成")
            
            return {
                "status": "success",
                "query": query,
                "content": content,
                "raw_response": response
            }
            
        except Exception as e:
            print(f"❌ Research Agent 搜尋失敗: {str(e)}")
            return {
                "status": "error",
                "query": query,
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """測試 Agent 連接是否正常"""
        try:
            test_response = self.agent.run("測試連接")
            return True
        except Exception as e:
            print(f"❌ 連接測試失敗: {str(e)}")
            return False


if __name__ == "__main__":
    # 測試 Research Agent
    agent = ResearchAgent()
    result = agent.search("新加坡股市最新動態")
    print(json.dumps(result, ensure_ascii=False, indent=2))
