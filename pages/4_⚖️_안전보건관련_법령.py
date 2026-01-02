import streamlit as st

# [주의] st.set_page_config는 app.py에서 설정하므로 생략

# ==========================================
# 1. 스타일 설정 (밑줄 강제 제거 및 디자인 수정)
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
        
        /* 🚨 밑줄 강제 제거 (!important) */
        text-decoration: none !important; 
        
        color: #0056b3 !important;   /* 글자색 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;         /* 버튼 간 간격 */
    }
    
    /* 마우스 올렸을 때 효과 */
    .link-card:hover {
        background-color: #dbeaff;   /* 배경만 약간 진하게 */
        border-color: #0056b3;       /* 테두리 진하게 */
        
        /* 🚨 마우스 올려도 밑줄 안 생기게 유지 */
        text-decoration: none !important;
        
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
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 헤더
# ==========================================
st.title("⚖️ 안전보건관련 법령")
st.info("아래 카드를 클릭하면 법제처 국가법령정보센터에서 **최신 법령 원문** 및 **사내 규정** 조회가 가능합니다.")
st.write("") 

# ==========================================
# 3. 법령 카드 배치 (2열 x 3행 = 총 6개)
# ==========================================

# [첫 번째 줄] 핵심 안전 법령 (산안법, 중처법)
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

# [두 번째 줄] 시설 및 건설 법령 (시특법, 건진법) - ✨ 신규 추가됨!
col3, col4 = st.columns(2) 

with col3:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%8B%9C%EC%84%A4%EB%AC%BC%EC%9D%98%20%EC%95%88%EC%A0%84%20%EB%B0%8F%20%EC%9C%A0%EC%A7%80%EA%B4%80%EB%A6%AC%EC%97%90%20%EA%B4%80%ED%95%9C%20%ED%8A%B9%EB%B3%84%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">🏢 시설물안전법 (시특법)</span>
        <span class="card-desc">1·2·3종 시설물의 안전진단 및<br>유지관리 의무 규정</span>
    </a>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EA%B1%B4%EC%84%A4%EA%B8%B0%EC%88%A0%20%EC%A7%84%ED%9D%A5%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">🚜 건설기술 진흥법 (건진법)</span>
        <span class="card-desc">건설공사 안전관리계획서 수립 및<br>품질관리 기준</span>
    </a>
    """, unsafe_allow_html=True)

# [세 번째 줄] 재난 법령 및 사규
col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <a href="https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%9E%AC%EB%82%9C%20%EB%B0%8F%20%EC%95%88%EC%A0%84%EA%B4%80%EB%A6%AC%20%EA%B8%B0%EB%B3%B8%EB%B2%95" target="_blank" class="link-card">
        <span class="card-title">🚨 재난안전기본법</span>
        <span class="card-desc">국가 및 지자체의 재난관리<br>책임과 절차 규정</span>
    </a>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <a href="https://www.law.go.kr/schlPubRulSc.do?menuId=13&subMenuId=467&tabMenuId=509&query=%EC%95%88%EC%82%B0%EB%8F%84%EC%8B%9C%EA%B3%B5%EC%82%AC" target="_blank" class="link-card">
        <span class="card-title">📒 안산도시공사 사규</span>
        <span class="card-desc">공사 안전보건관리규정 등<br>내부 지침 전체보기</span>
    </a>
    """, unsafe_allow_html=True)

# ==========================================
# 4. 하단 안내
# ==========================================
st.write("")
st.markdown("---")
st.caption("※ 위 카드를 클릭하면 법제처 국가법령정보센터로 새 창이 열립니다.")