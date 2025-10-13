"""
測試語言指定功能
"""
import sys
import os

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow import SEANewsWorkflow
from config import Config


def validate_config():
    """驗證配置"""
    if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your-openai-api-key":
        print("❌ 請先設定 OPENAI_API_KEY")
        return False
    print("✅ 配置驗證成功")
    return True


def test_language_parsing():
    """測試語言解析功能"""
    if not validate_config():
        return
    
    print("=" * 70)
    print("測試語言指定功能")
    print("=" * 70)
    
    workflow = SEANewsWorkflow()
    
    test_cases = [
        {
            "input": "我想找最近一個月內，關於新加坡AI領域的20篇中文投資趨勢新聞",
            "expected_language": "Chinese"
        },
        {
            "input": "找10篇關於泰國央行的英文新聞",
            "expected_language": "English"
        },
        {
            "input": "越南電商市場分析（越南文）",
            "expected_language": "Vietnamese"
        },
        {
            "input": "馬來西亞房地產趨勢",  # 沒有指定語言，應該預設為英文
            "expected_language": "English"
        },
        {
            "input": "印尼金融科技新聞 印尼語",
            "expected_language": "Indonesian"
        }
    ]
    
    print("\n開始測試...\n")
    
    success_count = 0
    for i, case in enumerate(test_cases, 1):
        print(f"測試案例 {i}: {case['input']}")
        print("-" * 70)
        
        result = workflow._parse_prompt(case['input'])
        
        actual_language = result.get('language', 'Unknown')
        expected_language = case['expected_language']
        
        if actual_language == expected_language:
            print(f"✅ 語言解析正確: {actual_language}")
            success_count += 1
        else:
            print(f"⚠️ 語言解析不符: 期望={expected_language}, 實際={actual_language}")
        
        print(f"   關鍵字: {result.get('keywords')}")
        print(f"   時間範圍: {result.get('time_instruction')}")
        print(f"   數量: {result.get('num_instruction')}")
        print()
    
    print("=" * 70)
    print(f"測試完成: {success_count}/{len(test_cases)} 個案例成功")
    print("=" * 70)


if __name__ == "__main__":
    test_language_parsing()
