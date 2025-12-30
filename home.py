import streamlit as st

# [주의] st.set_page_config는 app.py에 있으므로 생략

# ==========================================
# 1. 스타일 설정 (모바일 최적화 디자인)
# ==========================================
st.markdown("""
<style>
    /* 설명 텍스트 스타일 */
    div[data-testid="stVerticalBlock"] p {
        white-space: normal !important;
        word-break: keep-all;
        color: #444; 
    }

    /* 버튼(Page Link) 디자인 - 카드처럼 꾸미기 */
    a[data-testid="stPageLink-NavLink"] {
        border: 2px solid #007bff;   /* 파란 테두리 */
        background-color: #f0f8ff;   /* 연한 파란 배경 */
        border-radius: 12px;         /* 둥글게 */
        padding: 18px !important;    /* 터치하기 좋게 여백 늘림 */
        text-align: center !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        transition: transform 0.2s;  
        margin-bottom: 5px; /* 버튼 아래 간격 */
    }

    /* 눌렀을 때 효과 */
    a[data-testid="stPageLink-NavLink"]:hover {
        transform: scale(1.02);
        background-color: #e0f0ff;
    }
    
    /* 버튼 글씨 크기 키움 (모바일 가독성) */
    a[data-testid="stPageLink-NavLink"] p {
        font-size: 1.3rem !important; 
        font-weight: 800 !important;  
        color: #0056b3 !important;    
        margin: 0 !important;
    }
    
    /* 제목 옆 쇠사슬 아이콘 숨기기 */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 메인 헤더
# ==========================================
st.title("🏗️ 안산도시공사 안전보건 플랫폼")
st.markdown("### 환영합니다! 원하시는 업무를 선택해주세요. 👋")
st.markdown("---")

# 공지사항
with st.container(border=True):
    st.info("""
    📢 **[주요 공지사항]**
            
            1. 도급·용역 계약 시 '도급·용역 안전 도우미' 기능을 적극 활용 바랍니다.

            2. 현장 순회 점검 시 'AI 위험성평가' 기능을 활용하여 기록을 남겨주세요.

            3. 법적 기준이 헷갈릴 땐 'AI 근로감독관'에게 채팅으로 물어보세요.
    """)

st.write("") # 간격 띄우기

# ==========================================
# 3. 메뉴 바로가기 (세로 배치 - 모바일 최적화)
# ==========================================
# 👇 st.columns(3)를 제거하고, 그냥 순서대로 쭉 나열합니다.

# [1번] 도급 안전 도우미
with st.container(border=True):
    st.page_link(
        "pages/1_📑_도급·용역_안전_도우미.py", 
        label="📑 도급·용역 AI 안전 도우미", 
        use_container_width=True
    )
    st.write("") 
    st.write("👉 도급·용역 계약 시 필요한 안전 서류와 절차를 안내받고 보고서를 만듭니다.")

st.write("") # 버튼 사이 간격

# [2번] AI 위험성평가
with st.container(border=True):
    st.page_link(
        "pages/2_📸_AI_세이프티_렌즈.py", 
        label="📸 AI 세이프티 렌즈 (위험성 평가)", 
        use_container_width=True
    )
    st.write("")
    st.write("👉 현장 사진을 찍으면 AI가 위험요인을 분석하고 대책을 알려줍니다.")

st.write("") # 버튼 사이 간격

# [3번] AI 근로감독관
with st.container(border=True):
    st.page_link(
        "pages/3_👮_AI_근로감독관.py", 
        label="👮 AI 근로감독관 (챗봇)", 
        use_container_width=True
    )
    st.write("")
    st.write("👉 산업안전보건법, 중대재해처벌법, 재난안전법과 관련하여 궁금한 점을  AI 감독관에게 채팅으로 물어보세요.")

# ==========================================
# 4. 푸터
# ==========================================
st.markdown("---")
st.caption("ⓒ Ansan Urban Corporation Safety Team | 시스템 문의: 안전관리팀 주임 진형국(내선 4872)")