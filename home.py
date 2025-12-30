import streamlit as st

# [주의] st.set_page_config는 app.py에 있으므로 생략

# ==========================================
# 1. 스타일 설정 (그룹핑 강화)
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
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        transition: transform 0.2s;  
        
        /* 👇 버튼 아래 여백을 줄여서 설명글과 가깝게 붙임 */
        margin-bottom: 0px !important; 
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
    
    /* 2. 설명 글씨(손가락 부분) 스타일 */
    .feature-desc {
        color: #333333 !important;  
        font-weight: 600;           
        font-size: 0.95rem;         
        margin-top: 8px !important;    /* 버튼이랑 살짝만 띄움 */
        margin-bottom: 0px !important; /* 아래쪽은 구분선이 처리함 */
        padding-left: 10px;            /* 살짝 들여쓰기 */
        line-height: 1.4;
    }

    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    /* 구분선(hr) 스타일 연하게 */
    hr {
        margin-top: 15px !important;
        margin-bottom: 15px !important;
        border-color: #eee;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 메인 헤더
# ==========================================
st.title("🏗️ 안산도시공사 AI 안전보건 플랫폼")
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
# 3. 메뉴 바로가기 (구분선으로 확실히 분리)
# ==========================================

# [1번] 도급 안전 도우미
st.page_link("pages/1_📑_도급·용역_안전_도우미.py", label="📑 도급·용역 AI 안전 도우미", use_container_width=True)
st.markdown('<p class="feature-desc">└ 👉 계약 시 필요한 안전 서류와 절차 자동 안내</p>', unsafe_allow_html=True)
st.markdown("---") # 구분선

# [2번] AI 위험성평가
st.page_link("pages/2_📸_AI_세이프티_렌즈.py", label="📸 AI 세이프티 렌즈 (위험성 평가)", use_container_width=True)
st.markdown('<p class="feature-desc">└ 👉 현장 사진 촬영 후 즉시 위험요인/대책 분석</p>', unsafe_allow_html=True)
st.markdown("---") # 구분선

# [3번] AI 근로감독관 (챗봇)
st.page_link("pages/3_👮_AI_근로감독관.py", label="👮 AI 근로감독관 (챗봇)", use_container_width=True)
st.markdown('<p class="feature-desc">└ 👉 산업안전보건법, 중대재해처벌법 등 법적 준수사항 실시간 채팅 상담</p>', unsafe_allow_html=True)
st.markdown("---") # 구분선

# [4번] 안전보건관련 법령
st.page_link("pages/4_⚖️_안전보건관련_법령.py", label="⚖️ 안전보건관련 법령 및 사규", use_container_width=True)
st.markdown('<p class="feature-desc">└ 👉 산안법, 중처법, 재난법, 공사 사규 원문 조회</p>', unsafe_allow_html=True)


# ==========================================
# 4. 푸터
# ==========================================
st.write("")
st.caption("ⓒ Ansan Urban Corporation Safety Team | 시스템 문의: 안전관리팀 주임 진형국(내선 4872)")