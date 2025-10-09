"""
主程式入口
提供 CLI 和 Web 兩種執行方式
"""
import sys
import argparse
from workflow import SEANewsWorkflow
from config import Config
import json


def run_cli(args):
    """CLI 模式執行"""
    print("=" * 60)
    print(f"  {Config.APP_NAME} v{Config.APP_VERSION}")
    print("=" * 60)
    print()
    
    # 初始化工作流程
    workflow = SEANewsWorkflow()
    
    # 執行工作流程
    result = workflow.execute(
        search_query=args.query,
        recipient_emails=args.email
    )
    
    # 顯示結果
    print()
    print("=" * 60)
    print("執行結果:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 返回狀態碼
    return 0 if result.get("status") == "success" else 1


def run_web():
    """Web 模式執行（啟動 Streamlit）"""
    import subprocess
    subprocess.run(["streamlit", "run", "app.py"])


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description=f"{Config.APP_NAME} - 東南亞金融新聞自動化搜尋與報告系統"
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="執行模式")
    
    # CLI 模式
    cli_parser = subparsers.add_parser("cli", help="命令列模式")
    cli_parser.add_argument(
        "-q", "--query",
        required=True,
        help="搜尋查詢（例如：新加坡股市動態）"
    )
    cli_parser.add_argument(
        "-e", "--email",
        required=True,
        help="收件人郵箱（多個郵箱用逗號分隔）"
    )
    
    # Web 模式
    web_parser = subparsers.add_parser("web", help="Web 介面模式")
    
    # 驗證模式
    validate_parser = subparsers.add_parser("validate", help="驗證系統配置")
    
    # 解析參數
    args = parser.parse_args()
    
    # 根據模式執行
    if args.mode == "cli":
        sys.exit(run_cli(args))
    elif args.mode == "web":
        run_web()
    elif args.mode == "validate":
        print("🔍 驗證系統配置...")
        try:
            Config.validate()
            print("✅ 配置驗證通過")
            
            workflow = SEANewsWorkflow()
            validation_results = workflow.validate_agents()
            
            if all(validation_results.values()):
                print("✅ 所有 Agents 運作正常")
                sys.exit(0)
            else:
                print("⚠️  部分 Agents 驗證失敗")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 驗證失敗: {str(e)}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
