import streamlit as st

# [주의] st.set_page_config는 app.py에 있으므로 생략

# ==========================================
# 1. 스타일 설정 (모바일 최적화 & 글씨 진하게)
# ==========================================
st.markdown("""
<style>
    /* 1. 버튼(Page Link) 디자인 */
    a[data-testid="stPageLink-NavLink"] {
        border: 2px solid #007bff;
        background-color: #f0f8ff;
        border-radius: 12px;
        padding: 18px !important;
        text-align: center !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        transition: transform 0.2s;  
        margin-bottom: 5px; /* 버튼과 설명 사이 간격 */
    }

    a[data-testid="stPageLink-NavLink"]:hover {
        transform: scale(1.02);
        background-color: #e0f0ff;
    }
    
    a[data-testid="stPageLink-NavLink"] p {
        font-size: 1.2rem !important; 
        font-weight: 800 !important;  
        color: #0056b3 !important;    
    }
    
    /* 2. [수정됨] 설명 글씨(손가락 부분) 스타일 - 아주 진하게! */
    .feature-desc {
        color: #111111 !important;  /* 거의 완전 검은색 */
        font-weight: 600;           /* 글씨 굵게 */
        font-size: 1rem;            /* 글씨 크기 약간 키움 */
        margin-top: 0px;
        margin-bottom: 25px;        /* 다음 버튼과의 간격 */
        line-height: 1.4;
    }

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
    📢 **[시스템 안내]**
    
    1. **도급 안전 도우미:** 계약 단계별 필수 서류와 절차를 안내합니다.
    2. **AI 위험성평가:** 현장 사진을 분석하여 위험요인을 찾아냅니다.
    3. **AI 근로감독관:** 궁금한 법령과 기준을 채팅으로 물어보세요.
    4. **안전보건 법령:** 관계 법령 및 공사 사규 원문을 확인하세요.
    """)

st.write("") 

# ==========================================
# 3. 메뉴 바로가기 (글씨 진하게 적용)
# ==========================================

# [1번] 도급 안전 도우미
st.page_link("pages/1_📑_도급·용역_안전_도우미.py", label="📑 도급·용역 안전 도우미", use_container_width=True)
# 👇 여기가 수정되었습니다 (HTML로 직접 진하게 출력)
st.markdown('<p class="feature-desc">👉 계약 시 필요한 안전 서류와 절차를 안내받고 보고서를 만듭니다.</p>', unsafe_allow_html=True)


# [2번] AI 위험성평가
st.page_link("pages/2_📸_AI_세이프티_렌즈.py", label="📸 AI 위험성평가 (세이프티 렌즈)", use_container_width=True)
st.markdown('<p class="feature-desc">👉 현장 사진을 찍으면 위험요인을 분석하고 대책을 알려줍니다.</p>', unsafe_allow_html=True)


# [3번] AI 근로감독관 (챗봇)
st.page_link("pages/3_👮_AI_근로감독관.py", label="👮 AI 근로감독관 (법령 상담)", use_container_width=True)
st.markdown('<p class="feature-desc">👉 궁금한 법령, 과태료 기준을 AI에게 채팅으로 물어보세요.</p>', unsafe_allow_html=True)


# [4번] 안전보건관련 법령
st.page_link("pages/4_⚖️_안전보건관련_법령.py", label="⚖️ 안전보건관련 법령 및 사규", use_container_width=True)
st.markdown('<p class="feature-desc">👉 산업안전보건법, 중대재해처벌법 및 공사 규정 원문을 확인합니다.</p>', unsafe_allow_html=True)


# ==========================================
# 4. 푸터
# ==========================================
st.markdown("---")
st.caption("ⓒ Ansan Urban Corporation Safety Team | 시스템 문의: 안전관리팀 주임 진형국(내선 4872)")