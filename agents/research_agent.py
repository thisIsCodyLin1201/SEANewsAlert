"""
Research Agent
負責使用 OpenAI Responses API 進行深度網路搜尋
"""
from openai import OpenAI
from config import Config
import json
from typing import Dict, Any
from datetime import datetime


class ResearchAgent:
    """研究代理 - 執行深度網路搜尋"""
    
    # 指定的18個可信新聞來源網站
    TRUSTED_NEWS_SOURCES = [
        {"name": "VietJo", "domain": "viet-jo.com", "region": "Vietnam"},
        {"name": "Cafef", "domain": "cafef.vn", "region": "Vietnam"},
        {"name": "VNExpress", "domain": "vnexpress.net", "region": "Vietnam"},
        {"name": "Vietnam Finance", "domain": "vietnamfinance.vn", "region": "Vietnam"},
        {"name": "Vietnam Investment Review", "domain": "vir.com.vn", "region": "Vietnam"},
        {"name": "Vietnambiz", "domain": "vietnambiz.vn", "region": "Vietnam"},
        {"name": "Tap Chi Tai chinh", "domain": "tapchikinhtetaichinh.vn", "region": "Vietnam"},
        {"name": "Bangkok Post", "domain": "bangkokpost.com", "region": "Thailand"},
        {"name": "Techsauce", "domain": "techsauce.co", "region": "Thailand"},
        {"name": "Fintech Singapore", "domain": "fintechnews.sg", "region": "Singapore"},
        {"name": "Fintech Philippines", "domain": "fintechnews.ph", "region": "Philippines"},
        {"name": "Khmer Times", "domain": "khmertimeskh.com", "region": "Cambodia"},
        {"name": "柬中時報", "domain": "cc-times.com", "region": "Cambodia"},
        {"name": "The Phnom Penh Post", "domain": "phnompenhpost.com", "region": "Cambodia"},
        {"name": "Deal Street Asia", "domain": "dealstreetasia.com", "region": "Southeast Asia"},
        {"name": "Tech in Asia", "domain": "techinasia.com", "region": "Southeast Asia"},
        {"name": "Nikkei Asia", "domain": "asia.nikkei.com", "region": "Southeast Asia"},
        {"name": "Heaptalk", "domain": "heaptalk.com", "region": "Southeast Asia"},
    ]
    
    def __init__(self):
        """初始化 Research Agent"""
        # 初始化 OpenAI 客戶端
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def search(self, query: str, time_instruction: str = "最近 7 天內", num_instruction: str = "5-10篇", language: str = "English") -> Dict[str, Any]:
        """
        執行搜尋
        
        Args:
            query: 用戶的搜尋查詢
            time_instruction: 時間範圍指令 (例如: "最近一個月內")
            num_instruction: 新聞數量指令 (例如: "約15篇")
            language: 新聞來源語言 (例如: "English", "Chinese", "Vietnamese", "Thai", "Malay", "Indonesian")
            
        Returns:
            Dict: 包含搜尋結果和來源的字典
        """
        print(f"🔍 Research Agent 開始搜尋: {query} ({time_instruction}, {num_instruction}, 語言: {language})")
        
        # 建立語言相關的搜尋關鍵字
        language_keywords = {
            "English": "in English",
            "Chinese": "中文 OR 華語 OR Chinese",
            "Vietnamese": "tiếng Việt OR Vietnamese",
            "Thai": "ภาษาไทย OR Thai",
            "Malay": "Bahasa Melayu OR Malay",
            "Indonesian": "Bahasa Indonesia OR Indonesian"
        }
        
        language_hint = language_keywords.get(language, "in English")
        
        # 生成可信來源列表
        sources_list = "\n".join([
            f"  - {src['name']} (site:{src['domain']}) - {src['region']}" 
            for src in self.TRUSTED_NEWS_SOURCES
        ])
        
        # 生成 site: 搜尋字串組合（用於建議搜尋範例）
        site_examples = [
            f"site:{src['domain']}" 
            for src in self.TRUSTED_NEWS_SOURCES[:5]  # 只取前5個作為範例
        ]
        site_search_example = " OR ".join(site_examples)
        
        # 生成域名列表用於驗證
        allowed_domains = [src['domain'] for src in self.TRUSTED_NEWS_SOURCES]
        allowed_domains_str = ", ".join(allowed_domains)
        
        # 強化搜尋提示詞，要求以 JSON 格式返回結果
        enhanced_query = f"""
        請扮演一位頂尖的金融研究員，深入搜尋關於「{query}」的東南亞金融新聞。

        **核心任務指令:**
        1.  **搜尋範圍**: 嚴格鎖定東南亞國家（新加坡、馬來西亞、泰國、印尼、越南、菲律賓、柬埔寨）。
        2.  **時間要求**: 嚴格篩選在 **{time_instruction}** 內發布的新聞。
        3.  **數量要求**: 你的目標是找到並提供 **{num_instruction}** 的高品質新聞。你必須盡力達成這個數量目標。
        4.  **語言要求**: 請優先搜尋 **{language}** 語言的新聞來源。在搜尋時加上關鍵字：{language_hint}

        5.  **來源建議**: 優先從以下可信新聞網站搜尋新聞：

{sources_list}

        6.  **搜尋技巧 - 強制多樣性策略（非常重要）**:

            ⚠️ **必須遵守**: 為了確保新聞來源的多樣性，你**必須**對多個不同網站進行**獨立搜尋**。

            **推薦策略 - 分區域獨立搜尋**:

            a) 🇻🇳 **越南區域** (至少搜尋 2-3 個網站):
               - 越南的金融科技、銀行、投資相關新聞

            b) 🇹🇭 **泰國區域** (至少搜尋 1-2 個網站):
               - 泰國的金融科技、銀行、投資相關新聞

            c) 🇸🇬 **新加坡/區域媒體** (至少搜尋 2-3 個網站):
               - 新加坡和東南亞區域的金融科技、銀行、投資相關新聞

            d) 🇵🇭 **菲律賓區域**:
               - 菲律賓的金融科技、銀行、投資相關新聞

            e) 🇰🇭 **柬埔寨區域**:
               - 柬埔寨的金融科技、銀行、投資相關新聞

        7.  **多樣性建議**:
            - 💡 **建議做法**: 盡量使用 3-4 個或以上不同的新聞來源
            - 🔄 **執行方式**: 對不同區域進行搜尋，嘗試從多個網站收集新聞
            - 📊 **平衡策略**: 優先選擇最相關和高質量的新聞，同時適度考慮來源多樣性
            - 使用不同的關鍵字變化（中英文、同義詞等）

        8.  **域名建議**:
            - 優先使用以下網站：{allowed_domains_str}
            - 但不限於這些網站，也可以使用其他可信的東南亞金融新聞來源

        9.  **資訊完整性**: 每條新聞都必須包含清晰的「標題」、「摘要」、「來源網站」、「完整網址」和「發布日期」。

        **輸出格式要求（非常重要）:**
        你**必須嚴格**遵循下面的 JSON 格式返回結果。請在你的回應中包含一個 JSON 代碼塊（用 ```json 包裹）。

        ```json
        {{
            "search_query": "{query}",
            "search_date": "{datetime.now().strftime('%Y-%m-%d')}",
            "results": [
                {{
                    "title": "新聞標題（英文或原文）",
                    "summary": "這是新聞的詳細摘要內容，應該包含新聞的主要資訊、數據和關鍵事件...",
                    "source": "新聞來源名稱",
                    "url": "https://example.com/news-article-1",
                    "date": "YYYY-MM-DD"
                }},
                {{
                    "title": "新聞標題（英文或原文）",
                    "summary": "這是新聞的詳細摘要內容，應該包含新聞的主要資訊、數據和關鍵事件...",
                    "source": "新聞來源名稱",
                    "url": "https://example.com/news-article-2",
                    "date": "YYYY-MM-DD"
                }}
            ]
        }}
        ```

        **請務必:**
        1. 使用 ```json 和 ``` 包裹你的 JSON 回應
        2. 確保 JSON 格式正確（有效的 JSON 語法）
        3. 每條新聞都必須包含所有必要欄位（title, summary, source, url, date）
        4. summary 應該詳細且資訊豐富（至少 100-200 字）
        5. 日期格式必須為 YYYY-MM-DD
        """
        
        try:
            # 使用 OpenAI Responses API 執行網路搜尋
            response = self.client.responses.create(
                model=self.model,
                input=enhanced_query,
                tools=[
                    {
                        "type": "web_search"
                    }
                ]
            )

            # 提取回應內容和來源
            content = ""
            sources = []

            for output_item in response.output:
                if output_item.type == "web_search_call":
                    print(f"🔍 網路搜尋狀態: {output_item.status}")

                elif output_item.type == "message":
                    # 提取文本內容
                    for content_item in output_item.content:
                        if content_item.type == "output_text":
                            content += content_item.text

                            # 處理引用/來源資訊
                            if hasattr(content_item, 'annotations') and content_item.annotations:
                                for annotation in content_item.annotations:
                                    if annotation.type == "url_citation":
                                        sources.append({
                                            "title": annotation.title,
                                            "url": annotation.url,
                                            "index": annotation.index if hasattr(annotation, 'index') else None
                                        })

            print("✅ Research Agent 搜尋完成")
            print(f"📰 找到 {len(sources)} 個來源")

            return {
                "status": "success",
                "query": query,
                "content": content,
                "sources": sources,
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
        """測試 OpenAI API 連接是否正常"""
        try:
            test_response = self.client.responses.create(
                model=self.model,
                input="測試連接",
                tools=[{"type": "web_search"}]
            )
            print("✅ OpenAI API 連接成功")
            return True
        except Exception as e:
            print(f"❌ 連接測試失敗: {str(e)}")
            return False


if __name__ == "__main__":
    # 測試 Research Agent
    agent = ResearchAgent()
    result = agent.search("新加坡股市最新動態")
    print(json.dumps(result, ensure_ascii=False, indent=2))
