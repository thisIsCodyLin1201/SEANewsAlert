"""
測試 DuckDuckGo site: 語法的新聞來源限制功能
驗證 AI 能否正確使用 site: 語法搜尋指定來源
"""
import sys
from agents.research_agent import ResearchAgent
from urllib.parse import urlparse
import re


def extract_domain(url):
    """從 URL 提取域名"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # 移除 www. 前綴
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None


def test_site_syntax_search():
    """測試使用 site: 語法的搜尋功能"""
    print("="*70)
    print("測試 DuckDuckGo site: 語法 - 新聞來源限制")
    print("="*70)
    
    # 初始化 Research Agent
    agent = ResearchAgent()
    
    # 獲取允許的域名列表
    allowed_domains = [src['domain'].lower() for src in agent.TRUSTED_NEWS_SOURCES]
    print(f"\n📋 允許的18個新聞來源域名:")
    for i, domain in enumerate(allowed_domains, 1):
        src = agent.TRUSTED_NEWS_SOURCES[i-1]
        print(f"   {i}. {src['name']} ({domain}) - {src['region']}")
    
    # 測試查詢
    test_query = "泰國數位支付"
    print(f"\n🔍 測試查詢: {test_query}")
    print(f"   時間範圍: 最近 30 天內")
    print(f"   數量要求: 5-8篇")
    print(f"   語言偏好: English")
    print("\n⏳ 正在搜尋（AI 會使用 site: 語法限制來源）...\n")
    
    # 執行搜尋
    result = agent.search(
        query=test_query,
        time_instruction="最近 30 天內",
        num_instruction="5-8篇",
        language="English"
    )
    
    if result['status'] != 'success':
        print(f"❌ 搜尋失敗: {result.get('error', 'Unknown error')}")
        return
    
    # 分析結果
    content = result['content']
    print("\n" + "="*70)
    print("📊 搜尋結果分析")
    print("="*70)
    
    # 嘗試提取 JSON 結果
    try:
        # 尋找 JSON 區塊
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            import json
            data = json.loads(json_match.group(1))
            results = data.get('results', [])
            
            if len(results) == 0:
                print("\n⚠️ 未找到任何新聞")
                print("\n這可能表示：")
                print("1. 指定網站確實沒有相關新聞")
                print("2. DuckDuckGo 對這些網站的索引覆蓋度有限")
                print("3. site: 語法限制過於嚴格")
                print("\n建議：嘗試更廣泛的搜尋關鍵字或擴大時間範圍")
                return
            
            print(f"\n✅ 找到 {len(results)} 篇新聞")
            
            # 驗證每條新聞的來源
            valid_count = 0
            invalid_count = 0
            invalid_sources = []
            
            for i, news in enumerate(results, 1):
                url = news.get('url', '')
                title = news.get('title', 'N/A')
                source = news.get('source', 'N/A')
                
                domain = extract_domain(url)
                is_valid = domain in allowed_domains
                
                status = "✅" if is_valid else "❌"
                print(f"\n{i}. {status} {title[:60]}...")
                print(f"   來源: {source}")
                print(f"   URL: {url}")
                print(f"   域名: {domain}")
                
                if is_valid:
                    valid_count += 1
                else:
                    invalid_count += 1
                    invalid_sources.append((domain, url))
            
            # 統計結果
            print("\n" + "="*70)
            print("📈 驗證統計")
            print("="*70)
            print(f"✅ 符合指定來源: {valid_count} 篇 ({valid_count/len(results)*100:.1f}%)")
            print(f"❌ 非指定來源: {invalid_count} 篇 ({invalid_count/len(results)*100:.1f}%)")
            
            if invalid_count > 0:
                print(f"\n⚠️ 發現 {invalid_count} 個非指定來源:")
                for domain, url in invalid_sources:
                    print(f"   - {domain}: {url}")
                print("\n💡 建議: 需要在 prompt 中更強調 site: 語法的使用")
            else:
                print(f"\n🎉 完美！所有新聞都來自指定的18個可信網站")
                print("✅ site: 語法限制策略成功！")
            
            # 來源分布統計
            source_distribution = {}
            for news in results:
                domain = extract_domain(news.get('url', ''))
                if domain in allowed_domains:
                    source_distribution[domain] = source_distribution.get(domain, 0) + 1
            
            if source_distribution:
                print(f"\n📊 來源分布:")
                for domain, count in sorted(source_distribution.items(), key=lambda x: x[1], reverse=True):
                    # 找到對應的網站名稱
                    site_name = next((src['name'] for src in agent.TRUSTED_NEWS_SOURCES if src['domain'].lower() == domain), domain)
                    print(f"   {site_name} ({domain}): {count} 篇")
            
        else:
            print("⚠️ 無法從回應中提取 JSON 格式的結果")
            print("\n完整回應:")
            print(content[:1000] + "..." if len(content) > 1000 else content)
    
    except Exception as e:
        print(f"❌ 解析結果時出錯: {str(e)}")
        print("\n完整回應:")
        print(content[:1000] + "..." if len(content) > 1000 else content)


if __name__ == "__main__":
    test_site_syntax_search()
