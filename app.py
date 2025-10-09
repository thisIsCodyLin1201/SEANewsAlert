"""
Streamlit Web 應用程式
簡潔的前端介面，用於輸入搜尋查詢和收件人郵箱
"""
import streamlit as st
from workflow import SEANewsWorkflow
from config import Config
import json
from datetime import datetime


# 頁面配置
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🌏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定義 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1a5490;
        padding: 20px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1a5490;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2c5aa0;
    }
    .success-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 Session State
if 'workflow' not in st.session_state:
    st.session_state.workflow = None
if 'execution_result' not in st.session_state:
    st.session_state.execution_result = None
if 'progress_messages' not in st.session_state:
    st.session_state.progress_messages = []


def initialize_workflow():
    """初始化工作流程"""
    if st.session_state.workflow is None:
        with st.spinner("正在初始化系統..."):
            try:
                st.session_state.workflow = SEANewsWorkflow()
                return True
            except Exception as e:
                st.error(f"系統初始化失敗: {str(e)}")
                return False
    return True


def progress_callback(step: str, message: str):
    """進度回調函數"""
    st.session_state.progress_messages.append({
        "step": step,
        "message": message,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


# ============ 主介面 ============

# 標題
st.markdown('<h1 class="main-header">🌏 東南亞金融新聞搜尋系統</h1>', unsafe_allow_html=True)

# 系統資訊
with st.expander("ℹ️ 系統資訊", expanded=False):
    st.info(f"""
    **系統版本**: {Config.APP_VERSION}
    
    **功能說明**:
    1. 使用 ChatGPT 進行深度網路搜尋
    2. 自動整理並結構化新聞資訊
    3. 生成專業的 PDF 報告
    4. 自動發送至指定郵箱
    
    **支援區域**: 新加坡、馬來西亞、泰國、印尼、越南、菲律賓
    
    **建議搜尋主題**:
    - 新加坡股市動態
    - 東南亞金融科技趨勢
    - 馬來西亞經濟政策
    - 泰國旅遊產業復甦
    - 印尼數位經濟發展
    """)

# 初始化系統
if not initialize_workflow():
    st.stop()

# 表單區域
with st.form("search_form"):
    st.subheader("📝 請輸入搜尋資訊")
    
    # 搜尋查詢輸入
    search_query = st.text_area(
        "您的需求 (Prompt)",
        placeholder="請詳細描述您的新聞需求，例如：\n- 最近一個月內，關於新加坡 AI 領域的投資趨勢新聞",
        height=120,
        help="您可以輸入完整的句子，包含時間範圍、主題、國家、數量等資訊，系統會自動為您解析。",
        max_chars=500
    )
    
    # 收件人郵箱輸入
    recipient_emails = st.text_input(
        "收件人郵箱",
        placeholder="example@email.com 或 email1@test.com, email2@test.com",
        help="可以輸入多個郵箱，用逗號分隔"
    )
    
    # 提交按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.form_submit_button("🚀 開始搜尋並寄送報告")

# 處理表單提交
if submit_button:
    # 驗證輸入
    if not search_query.strip():
        st.error("❌ 請輸入搜尋主題")
    elif not recipient_emails.strip():
        st.error("❌ 請輸入收件人郵箱")
    else:
        # 清空之前的進度訊息
        st.session_state.progress_messages = []
        
        # 顯示進度容器
        progress_container = st.container()
        
        with progress_container:
            st.markdown('<div class="info-box">⏳ 工作流程執行中，請稍候...</div>', unsafe_allow_html=True)
            
            # 進度顯示區
            progress_placeholder = st.empty()
            
            # 執行工作流程
            result = st.session_state.workflow.execute(
                search_query=search_query.strip(),
                recipient_emails=recipient_emails.strip(),
                callback_func=progress_callback
            )
            
            # 顯示進度訊息
            for msg in st.session_state.progress_messages:
                progress_placeholder.markdown(
                    f"**[{msg['timestamp']}]** {msg['message']}"
                )
            
            st.session_state.execution_result = result
        
        # 顯示結果
        st.markdown("---")
        
        if result.get("status") == "success":
            st.markdown(
                f'<div class="success-box">'
                f'<h3>🎉 執行成功！</h3>'
                f'<p>報告已成功生成並發送至: <strong>{recipient_emails}</strong></p>'
                f'<p>PDF 路徑: {result.get("pdf_path", "N/A")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # 顯示詳細步驟
            with st.expander("📋 查看執行詳情"):
                st.json(result)
            
            # 成功後顯示慶祝動畫
            st.balloons()
            
        else:
            st.markdown(
                f'<div class="error-box">'
                f'<h3>❌ 執行失敗</h3>'
                f'<p>錯誤訊息: {result.get("error", "未知錯誤")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # 顯示錯誤詳情
            with st.expander("🔍 查看錯誤詳情"):
                st.json(result)

# 顯示歷史執行結果
if st.session_state.execution_result:
    st.markdown("---")
    st.subheader("📊 最近執行結果")
    
    result = st.session_state.execution_result
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "執行狀態",
            "✅ 成功" if result.get("status") == "success" else "❌ 失敗"
        )
    
    with col2:
        if "start_time" in result and "end_time" in result:
            start = datetime.fromisoformat(result["start_time"])
            end = datetime.fromisoformat(result["end_time"])
            duration = (end - start).total_seconds()
            st.metric("執行時長", f"{duration:.1f} 秒")
    
    with col3:
        steps_completed = len([s for s in result.get("steps", {}).values() if s.get("status") == "completed"])
        st.metric("完成步驟", f"{steps_completed}/4")

# 頁尾
st.markdown("---")
st.markdown(
    f'<div style="text-align: center; color: #666; font-size: 12px;">'
    f'© 2025 {Config.APP_NAME} v{Config.APP_VERSION} | Powered by Agno & OpenAI'
    f'</div>',
    unsafe_allow_html=True
)
