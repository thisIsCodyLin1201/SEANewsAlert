"""
測試需求解析功能
"""
from workflow import SEANewsWorkflow

def test_prompt_parsing():
    """測試 prompt 解析功能"""
    print("=" * 70)
    print("測試需求解析功能")
    print("=" * 70)
    
    workflow = SEANewsWorkflow()
    
    test_cases = [
        {
            "input": "我想找最近一個月內，關於新加坡AI領域的20篇投資趨勢新聞",
            "expected": {
                "keywords": "新加坡AI領域的投資趨勢",
                "time_instruction": "最近一個月內",
                "num_instruction": "約20篇"
            }
        },
        {
            "input": "新加坡金融科技",
            "expected": {
                "keywords": "新加坡金融科技",
                "time_instruction": "最近7天內",
                "num_instruction": "5-10篇"
            }
        },
        {
            "input": "找10篇關於泰國央行的新聞",
            "expected": {
                "keywords": "泰國央行",
                "time_instruction": "最近7天內",
                "num_instruction": "10篇"
            }
        }
    ]
    
    print("\n開始測試...\n")
    
    success_count = 0
    for idx, test_case in enumerate(test_cases, 1):
        print(f"測試案例 {idx}: {test_case['input']}")
        print("-" * 70)
        
        try:
            result = workflow._parse_prompt(test_case['input'])
            
            print(f"✅ 解析成功:")
            print(f"   關鍵字: {result['keywords']}")
            print(f"   時間範圍: {result['time_instruction']}")
            print(f"   數量: {result['num_instruction']}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ 解析失敗: {str(e)}")
        
        print()
    
    print("=" * 70)
    print(f"測試完成: {success_count}/{len(test_cases)} 個案例成功")
    print("=" * 70)
    
    return success_count == len(test_cases)

if __name__ == "__main__":
    success = test_prompt_parsing()
    exit(0 if success else 1)
