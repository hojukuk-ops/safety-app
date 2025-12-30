import streamlit as st

# [주의] st.set_page_config는 app.py에서 설정하므로 생략

# ==========================================
# 헤더
# ==========================================
st.title("⚖️ 안전보건관련 법령")
st.info("안전보건 관계 법령 및 안산도시공사 사규 원문을 확인하세요.")

st.markdown("---")

# ==========================================
# 법령 및 사규 버튼 배치 (2x2 그리드)
# ==========================================

# 첫 번째 줄 (산안법, 중처법)
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🏗️ 산업안전보건법")
    st.link_button(
        "법령 보기 (Click)", 
        "https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%82%B0%EC%97%85%EC%95%88%EC%A0%84%EB%B3%B4%EA%B1%B4%EB%B2%95", 
        use_container_width=True
    )

with col2:
    st.markdown("##### ⚖️ 중대재해처벌법")
    st.link_button(
        "법령 보기 (Click)", 
        "https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%A4%91%EB%8C%80%EC%9E%AC%ED%95%B4%EC%B2%98%EB%B2%8C%EB%B2%95", 
        use_container_width=True
    )

st.write("") # 줄 간격 띄우기 (여백)

# 두 번째 줄 (재난법, 공사 사규)
col3, col4 = st.columns(2)

with col3:
    st.markdown("##### 🚨 재난안전법")
    st.link_button(
        "법령 보기 (Click)", 
        "https://www.law.go.kr/LSW/lsSc.do?menuId=1&query=%EC%9E%AC%EB%82%9C%20%EB%B0%8F%20%EC%95%88%EC%A0%84%EA%B4%80%EB%A6%AC%20%EA%B8%B0%EB%B3%B8%EB%B2%95", 
        use_container_width=True
    )

with col4:
    st.markdown("##### 🏢 안산도시공사 사규")
    st.link_button(
        "공사 규정 전체보기 (Click)", 
        "https://www.law.go.kr/schlPubRulSc.do?menuId=13&subMenuId=467&tabMenuId=509&query=%EC%95%88%EC%82%B0%EB%8F%84%EC%8B%9C%EA%B3%B5%EC%82%AC", 
        use_container_width=True
    )

# ==========================================
# 하단 안내
# ==========================================
st.markdown("---")
st.caption("※ 각 버튼을 누르면 법제처 국가법령정보센터로 연결됩니다.")