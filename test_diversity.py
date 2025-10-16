"""
測試新聞來源多樣性
"""
from agents.research_agent import ResearchAgent
from urllib.parse import urlparse
import json

def extract_domain(url):
    """從 URL 中提取域名"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # 移除 www.
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None

def test_diversity():
    """測試新聞來源的多樣性"""
    print("=" * 70)
    print("🧪 測試新聞來源多樣性")
    print("=" * 70)
    
    # 初始化 Research Agent
    agent = ResearchAgent()
    
    # 測試查詢（模擬用戶輸入）
    test_cases = [
        {
            "query": "泰國數位支付",
            "time": "最近 30 天內",
            "count": "5-8篇",
            "language": "English"
        },
        {
            "query": "越南金融科技",
            "time": "最近 30 天內",
            "count": "5-8篇",
            "language": "English"
        },
        {
            "query": "東南亞加密貨幣監管",
            "time": "最近 30 天內",
            "count": "5-8篇",
            "language": "English"
        }
    ]
    
    allowed_domains = [src['domain'] for src in agent.TRUSTED_NEWS_SOURCES]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"📋 測試案例 {i}: {test_case['query']}")
        print(f"   時間範圍: {test_case['time']}")
        print(f"   數量要求: {test_case['count']}")
        print(f"   語言: {test_case['language']}")
        print("=" * 70)
        
        # 執行搜尋
        result = agent.search(
            query=test_case['query'],
            time_instruction=test_case['time'],
            num_instruction=test_case['count'],
            language=test_case['language']
        )
        
        print(f"\n✅ Research Agent 搜尋完成\n")
        
        # 解析結果
        try:
            if isinstance(result, dict) and 'content' in result:
                content = result['content']
            else:
                content = str(result)
            
            # 嘗試提取 JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                data = json.loads(json_match.group())
            else:
                print("⚠️  無法解析 JSON 結果")
                print(f"原始結果: {content[:500]}")
                continue
            
            articles = data.get('articles', [])
            
            print(f"📊 找到 {len(articles)} 篇新聞\n")
            
            # 統計來源分布
            source_count = {}
            valid_count = 0
            invalid_count = 0
            
            for idx, article in enumerate(articles, 1):
                title = article.get('title', 'No title')[:60]
                url = article.get('url', '')
                source = article.get('source', 'Unknown')
                
                domain = extract_domain(url)
                is_valid = domain in allowed_domains
                
                if is_valid:
                    valid_count += 1
                    source_count[domain] = source_count.get(domain, 0) + 1
                    status = "✅"
                else:
                    invalid_count += 1
                    status = "❌"
                
                print(f"{idx}. {status} {title}...")
                print(f"   來源: {source}")
                print(f"   域名: {domain}")
                print()
            
            # 顯示統計
            print("=" * 70)
            print("📈 來源多樣性分析")
            print("=" * 70)
            print(f"✅ 符合指定來源: {valid_count} 篇 ({valid_count/len(articles)*100:.1f}%)")
            print(f"❌ 非指定來源: {invalid_count} 篇 ({invalid_count/len(articles)*100:.1f}%)")
            
            if source_count:
                print(f"\n📊 來源分布:")
                sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
                for domain, count in sorted_sources:
                    percentage = count / len(articles) * 100
                    bar = "█" * int(percentage / 5)
                    print(f"   {domain:30s}: {count:2d} 篇 ({percentage:5.1f}%) {bar}")
                
                # 計算多樣性指標
                unique_sources = len(source_count)
                diversity_score = unique_sources / len(agent.TRUSTED_NEWS_SOURCES) * 100
                print(f"\n🎯 多樣性指標:")
                print(f"   使用了 {unique_sources} 個不同來源 (共18個可用來源)")
                print(f"   多樣性得分: {diversity_score:.1f}%")
                
                if diversity_score < 30:
                    print(f"   ⚠️  來源多樣性較低，建議改善")
                elif diversity_score < 50:
                    print(f"   ℹ️  來源多樣性中等")
                else:
                    print(f"   ✅ 來源多樣性良好")
            
        except Exception as e:
            print(f"❌ 解析結果時發生錯誤: {e}")
            print(f"原始結果: {str(result)[:500]}")

if __name__ == "__main__":
    test_diversity()
