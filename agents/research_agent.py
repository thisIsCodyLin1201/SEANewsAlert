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
        
        # 建立語言與國家映射
        language_config = {
            "English": {"keywords": "in English", "countries": ["Singapore", "Malaysia", "Thailand", "Vietnam", "Philippines"]},
            "Chinese": {"keywords": "中文 華語 Chinese", "countries": ["Singapore", "Malaysia"]},
            "Vietnamese": {"keywords": "tiếng Việt Vietnamese", "countries": ["Vietnam"]},
            "Thai": {"keywords": "ภาษาไทย Thai", "countries": ["Thailand"]},
            "Malay": {"keywords": "Bahasa Melayu Malay", "countries": ["Malaysia"]},
            "Indonesian": {"keywords": "Bahasa Indonesia Indonesian", "countries": ["Indonesia"]}
        }
        
        lang_info = language_config.get(language, language_config["English"])
        language_keywords = lang_info["keywords"]
        target_countries = ", ".join(lang_info["countries"])
        
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
        
        # 精簡優化的搜尋提示詞
        enhanced_query = f"""
你是東南亞金融研究專家。搜尋主題：「{query}」

【核心要求】
- 地區：{target_countries}（東南亞國家）
- 時間：{time_instruction}
- 數量：{num_instruction}
- 來源：{allowed_domains_str}

【語言與查詢策略】
- 目標語言：{language}
- 步驟1：先用 {language} 生成 5-8 組多樣化關鍵詞（含同義詞、在地用詞、縮寫）
- 步驟2：用這些關鍵詞執行多輪搜尋，關鍵字提示：{language_keywords}
- 步驟3：優先回傳 {language} 頁面；不足時補充英文來源並標註語言

【搜尋策略】
1. 對不同域名進行搜尋，確保來源多樣性（至少 3 個不同網站）
2. 使用多組關鍵詞變化（同義詞、中英文混搭）
3. 每則新聞需包含：標題、摘要（100-300字）、來源、URL、日期（YYYY-MM-DD）

【輸出格式】
回傳 JSON（用 ```json 包裹）：
```json
{{
  "search_query": "{query}",
  "search_date": "{datetime.now().strftime('%Y-%m-%d')}",
  "results": [
    {{
      "title": "新聞標題（原文）",
      "summary": "100-300字摘要，包含主要資訊與數據",
      "source": "來源名稱",
      "url": "https://...",
      "date": "YYYY-MM-DD",
      "language": "{language}"
    }}
  ]
}}
```

注意：確保 JSON 語法正確、所有欄位完整、日期在指定範圍內。
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
