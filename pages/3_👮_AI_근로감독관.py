import streamlit as st
import google.generativeai as genai

# [주의] st.set_page_config는 app.py에서 설정하므로 생략

# API 키 설정
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("🚨 API 키 오류: secrets.toml을 확인하세요.")
    st.stop()

# ==========================================
# 헤더: AI 근로감독관 페르소나 설정
# ==========================================
st.title("👮 안산도시공사 AI 근로감독관 (챗봇)")
st.info("산업안전보건법, 중대재해처벌법 등 복잡한 법령, **AI 근로감독관**에게 바로 물어보세요!")

# ==========================================
# 채팅 인터페이스 (탭 없이 바로 시작)
# ==========================================

# 1. 초기 인사말 (화면에 항상 떠 있음)
with st.chat_message("assistant"):
    st.write("반갑습니다. 안산도시공사 **AI 근로감독관**입니다. 👮‍♂️\n\n작업 현장의 안전 기준이나 법적 과태료 사항 등 궁금한 점을 물어보세요.")

# 2. 사용자 입력 받기
user_question = st.chat_input("질문 예: 2m 이상 고소작업 시 안전난간 설치 기준은?")

if user_question:
    # 3. 사용자의 질문 표시
    with st.chat_message("user"):
        st.write(user_question)

    # 4. AI 답변 생성 및 표시
    with st.chat_message("assistant"):
        with st.spinner("법령 및 지침을 검토 중입니다..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash-preview')
                prompt = f"""
                당신은 냉철하고 정확한 '대한민국 고용노동부 근로감독관'이자 '산업안전 전문가'입니다.
                사용자의 질문에 대해 법적 근거(산업안전보건법, 중대재해처벌법, 재난안전법, 이와 관련된 시행령과 규칙 등)를 명확히 들어 답변하세요.
                
                [답변 원칙]
                1. 근거 없는 답변은 하지 않는다.
                2. 법 조항(제몇조 제몇항)을 구체적으로 명시한다.
                3. 현장에서 실천해야 할 '핵심 조치사항'을 요약해준다.
                4. 말투는 정중하되, 전문가답게 단호하고 명확하게 한다.

                사용자 질문: {user_question}
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"상담 중 오류가 발생했습니다: {e}")