"""
API 測試腳本
用於測試 FastAPI 後端的功能
"""
import requests
import time
import json

API_BASE_URL = "http://127.0.0.1:8000"


def test_health_check():
    """測試健康檢查端點"""
    print("=" * 60)
    print("測試：健康檢查")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("✅ 健康檢查通過\n")
        return True
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}\n")
        return False


def test_create_task():
    """測試創建新聞報告任務"""
    print("=" * 60)
    print("測試：創建新聞報告任務")
    print("=" * 60)
    
    # 請修改為你的實際郵箱
    payload = {
        "user_prompt": "新加坡金融科技發展趨勢",
        "email": "test@example.com",  # 請修改為實際郵箱
        "language": "English",
        "time_range": "最近 7 天內",
        "count_hint": "5-10篇"
    }
    
    print(f"請求內容: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/tasks/news-report",
            json=payload
        )
        
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"響應: {json.dumps(data, indent=2, ensure_ascii=False)}")
            print("✅ 任務創建成功\n")
            return data["task_id"]
        else:
            print(f"❌ 任務創建失敗: {response.text}\n")
            return None
            
    except Exception as e:
        print(f"❌ 任務創建失敗: {e}\n")
        return None


def test_get_task_status(task_id):
    """測試查詢任務狀態"""
    print("=" * 60)
    print(f"測試：查詢任務狀態 (ID: {task_id})")
    print("=" * 60)
    
    max_polls = 100  # 最多輪詢 100 次（約 3 分鐘）
    poll_interval = 2  # 每 2 秒輪詢一次
    
    for i in range(max_polls):
        try:
            response = requests.get(f"{API_BASE_URL}/api/tasks/{task_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                status = data["status"]
                progress = data["progress"]
                step_message = data.get("step_message", "")
                
                print(f"[輪詢 {i+1}/{max_polls}] 狀態: {status} | 進度: {progress}% | {step_message}")
                
                if status == "succeeded":
                    print("\n✅ 任務成功完成！")
                    print(f"產出文件:")
                    if data["artifacts"]["pdf_path"]:
                        print(f"  - PDF: {data['artifacts']['pdf_path']}")
                    if data["artifacts"]["xlsx_path"]:
                        print(f"  - Excel: {data['artifacts']['xlsx_path']}")
                    print()
                    return True
                    
                elif status == "failed":
                    print(f"\n❌ 任務失敗: {data.get('error', '未知錯誤')}\n")
                    return False
                
                # 繼續輪詢
                time.sleep(poll_interval)
                
            else:
                print(f"❌ 查詢失敗: {response.status_code} - {response.text}\n")
                return False
                
        except Exception as e:
            print(f"❌ 查詢失敗: {e}\n")
            return False
    
    print(f"⚠️  達到最大輪詢次數，任務可能仍在執行中\n")
    return False


def main():
    """主測試流程"""
    print("\n" + "=" * 60)
    print("東南亞金融新聞搜尋系統 - API 測試")
    print("=" * 60 + "\n")
    
    # 1. 健康檢查
    if not test_health_check():
        print("⚠️  健康檢查失敗，請確認服務是否正在運行")
        print("   啟動命令: uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
        return
    
    # 2. 創建任務
    task_id = test_create_task()
    if not task_id:
        print("⚠️  任務創建失敗，請檢查請求內容和後端日誌")
        return
    
    # 3. 輪詢任務狀態
    test_get_task_status(task_id)
    
    print("=" * 60)
    print("測試完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
