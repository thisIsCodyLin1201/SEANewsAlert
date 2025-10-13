"""
測試語言識別功能
"""
from workflow import SEANewsWorkflow
from config import Config

def test_language_detection():
    """測試不同語言需求的解析"""
    
    print("=" * 70)
    print("測試語言識別功能")
    print("=" * 70)
    
    # 驗證配置
    if not Config.validate():
        print("❌ 配置驗證失敗")
        return
    
    print("✅ 配置驗證成功")
    
    # 初始化工作流程
    workflow = SEANewsWorkflow()
    
    # 測試案例
    test_cases = [
        {
            "input": "我想找中文新聞關於新加坡金融科技的發展",
            "expected_language": "chinese"
        },
        {
            "input": "找英文新聞關於泰國央行的政策",
            "expected_language": "english"
        },
        {
            "input": "搜尋當地語言的越南股市新聞",
            "expected_language": "local"
        },
        {
            "input": "不限語言，找印尼經濟的新聞",
            "expected_language": "any"
        },
        {
            "input": "新加坡AI投資趨勢",
            "expected_language": "english"  # 預設值
        }
    ]
    
    print("\n開始測試...\n")
    
    success_count = 0
    for i, test_case in enumerate(test_cases, 1):
        print(f"測試案例 {i}: {test_case['input']}")
        print("-" * 70)
        
        # 解析需求
        parsed = workflow._parse_prompt(test_case['input'])
        
        # 檢查結果
        detected_language = parsed.get('language', 'english')
        expected_language = test_case['expected_language']
        
        language_names = {
            "english": "英文",
            "chinese": "中文", 
            "local": "當地語言",
            "any": "不限"
        }
        
        if detected_language == expected_language:
            print(f"✅ 語言識別正確: {language_names.get(detected_language, detected_language)}")
            success_count += 1
        else:
            print(f"❌ 語言識別錯誤:")
            print(f"   預期: {language_names.get(expected_language, expected_language)}")
            print(f"   實際: {language_names.get(detected_language, detected_language)}")
        
        print(f"   完整解析結果:")
        print(f"   - 關鍵字: {parsed.get('keywords', 'N/A')}")
        print(f"   - 時間範圍: {parsed.get('time_instruction', 'N/A')}")
        print(f"   - 數量: {parsed.get('num_instruction', 'N/A')}")
        print(f"   - 語言: {language_names.get(parsed.get('language', 'english'), 'N/A')}")
        print()
    
    print("=" * 70)
    print(f"測試完成: {success_count}/{len(test_cases)} 個案例成功")
    print("=" * 70)

if __name__ == "__main__":
    test_language_detection()
