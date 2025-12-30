import streamlit as st

# [주의] st.set_page_config는 app.py에서 설정하므로 생략

# ==========================================
# 1. 스타일 설정 (애니메이션 제거, 깔끔한 반응)
# ==========================================
st.markdown("""
<style>
    /* 카드형 버튼 스타일 정의 */
    .link-card {
        display: block;
        border: 2px solid #007bff;   /* 파란 테두리 */
        background-color: #f0f8ff;   /* 연한 파란 배경 */
        border-radius: 12px;         /* 둥글게 */
        padding: 20px;               /* 내부 여백 */
        text-align: center;
        text-decoration: none;       /* 밑줄 제거 */
        color: #0056b3 !important;   /* 글자색 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;         /* 버튼 간 간격 */
        
        /* 🚨 수정됨: transition(서서히 변함) 제거 -> 즉시 반응 */
    }
    
    /* 마우스 올렸을 때 효과 */
    .link-card:hover {
        /* 🚨 수정됨: transform(확대) 제거 -> 크기 고정 */
        background-color: #dbeaff;   /* 배경만 약간 진하게 */
        border-color: #0056b3;       /* 테두리 진하게 */
        text-decoration: none;
        color: #003d82 !important;   /* 글자 진하게 */
    }

    /* 제목 텍스트 스타일 */
    .card-title {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 8px;
        display: block;
    }

    /* 설명 텍스트 스타일 */
    .card-desc {
        font-size: 0.95rem;
        color: #333;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 헤더
# ==========================================
st.title("⚖️ 안전보건관련 법령")
st.info("아래 카드를 클릭하면 **최신 법령 원문(3단 비교)** 및 **사내 규정** 페이지로 이동합니다.")
st.write("") # 간격

# ==========================================
# 3. 법령 카드 배치 (2열로 배치)
# ==========================================

# [첫 번째 줄]
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%82%B0%EC%97%85%EC%95%88%EC%A0%84%EB%B3%B4%EA%B1%B4%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">🏗️ 산업안전보건법</span>
        <span class="card-desc">사업장 안전 및 보건 기준의<br>기본이 되는 법률</span>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%A4%91%EB%8C%80%EC%9E%AC%ED%95%B4%EC%B2%98%EB%B2%8C%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">⚖️ 중대재해처벌법</span>
        <span class="card-desc">경영책임자의 안전 확보 의무를<br>규정한 법률</span>
    </a>
    """, unsafe_allow_html=True)

# [두 번째 줄]
col3, col4 = st.columns(2) 

with col3:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%9E%AC%EB%82%9C%20%EB%B0%8F%20%EC%95%88%EC%A0%84%EA%B4%80%EB%A6%AC%20%EA%B8%B0%EB%B3%B8%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">🚨 재난안전기본법</span>
        <span class="card-desc">국가 및 지자체의 재난관리<br>책임과 절차 규정</span>
    </a>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <a href="https://www.law.go.kr/schlPubRulSc.do?menuId=13&subMenuId=467&tabMenuId=509&query=%EC%95%88%EC%82%B0%EB%8F%84%EC%8B%9C%EA%B3%B5%EC%82%AC" target="_blank" class="link-card">
        <span class="card-title">🏢 안산도시공사 사규</span>
        <span class="card-desc">공사 안전보건관리규정 등<br>내부 지침 전체보기</span>
    </a>
    """, unsafe_allow_html=True)

# ==========================================
# 4. 하단 안내
# ==========================================
st.write("")
st.markdown("---")
st.caption("※ 위 카드를 클릭하면 법제처 국가법령정보센터로 새 창이 열립니다.")