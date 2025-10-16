"""
簡單的 API 啟動測試
用於驗證後端是否可以正常啟動
"""
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("=" * 60)
    print("測試 1: 檢查配置...")
    print("=" * 60)
    
    from config import Config
    print(f"✅ 配置載入成功")
    print(f"   - OpenAI API Key: {'已設定' if Config.OPENAI_API_KEY else '未設定'}")
    print(f"   - Email: {'已設定' if Config.EMAIL_ADDRESS else '未設定'}")
    print()
    
    print("=" * 60)
    print("測試 2: 檢查 Agents...")
    print("=" * 60)
    
    from agents import ResearchAgent, AnalystAgent, ReportGeneratorAgent, EmailAgent
    print("✅ 所有 Agent 模組載入成功")
    print()
    
    print("=" * 60)
    print("測試 3: 檢查 FastAPI 應用...")
    print("=" * 60)
    
    from app.main import app
    print("✅ FastAPI 應用載入成功")
    print(f"   - 標題: {app.title}")
    print(f"   - 版本: {app.version}")
    print()
    
    print("=" * 60)
    print("測試 4: 檢查服務層...")
    print("=" * 60)
    
    from app.services.progress import task_manager
    from app.services.workflow import workflow
    print("✅ 服務層模組載入成功")
    print()
    
    print("=" * 60)
    print("✅ 所有測試通過！")
    print("=" * 60)
    print()
    print("🚀 可以啟動服務了：")
    print("   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    print()
    
except Exception as e:
    print(f"❌ 測試失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
