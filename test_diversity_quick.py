"""
快速測試新聞來源多樣性
"""
from agents.research_agent import ResearchAgent
from urllib.parse import urlparse
import json
import re

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None

print('=' * 70)
print('測試新聞來源多樣性')
print('=' * 70)

agent = ResearchAgent()
result = agent.search(
    query='越南金融科技',
    time_instruction='最近 30 天內',
    num_instruction='8-10篇',
    language='English'
)

print('\n搜尋完成\n')

content = result.get('content', str(result)) if isinstance(result, dict) else str(result)
json_match = re.search(r'\{[\s\S]*\}', content)

if json_match:
    data = json.loads(json_match.group())
    articles = data.get('articles', [])
    
    print(f'找到 {len(articles)} 篇新聞\n')
    
    source_count = {}
    allowed_domains = [src['domain'] for src in agent.TRUSTED_NEWS_SOURCES]
    
    for idx, article in enumerate(articles, 1):
        title = article.get('title', 'No title')[:50]
        url = article.get('url', '')
        domain = extract_domain(url)
        
        if domain in allowed_domains:
            source_count[domain] = source_count.get(domain, 0) + 1
            print(f'{idx}. OK {title}...')
            print(f'   Domain: {domain}')
        else:
            print(f'{idx}. ERROR {title}...')
            print(f'   Domain: {domain}')
    
    print('\n' + '=' * 70)
    print('來源多樣性分析')
    print('=' * 70)
    
    if source_count:
        sorted_sources = sorted(source_count.items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_sources:
            percentage = count / len(articles) * 100
            bar = '#' * int(percentage / 5)
            print(f'{domain:30s}: {count:2d} 篇 ({percentage:5.1f}%) {bar}')
        
        unique_sources = len(source_count)
        diversity_score = unique_sources / 18 * 100
        max_percentage = max(source_count.values()) / len(articles) * 100
        
        print(f'\n多樣性指標:')
        print(f'   使用來源數: {unique_sources}/18 ({diversity_score:.1f}%)')
        print(f'   最大占比: {max_percentage:.1f}%')
        
        if max_percentage <= 40 and unique_sources >= 4:
            print(f'   OK 多樣性良好！')
        elif max_percentage <= 60:
            print(f'   WARNING 多樣性中等，可進一步改善')
        else:
            print(f'   ERROR 多樣性不足，需要改進')
else:
    print('ERROR 無法解析 JSON 結果')
