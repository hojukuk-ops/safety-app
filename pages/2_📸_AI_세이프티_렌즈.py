import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI 세이프티 렌즈 (위험성 평가)", page_icon="📸")

# API 키 설정
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("🚨 API 키 오류: secrets.toml을 확인하세요.")
    st.stop()

st.title("📸 AI 세이프티 렌즈 (위험성 평가)")
st.info("현장 사진을 찍거나 업로드하면, AI를 활용하여 산업안전보건법 기반으로 위험성평가를 실시합니다.")

# 입력 방식 선택
input_method = st.radio("입력 방식", ["📷 실시간 촬영", "🖼️ 갤러리 업로드"], horizontal=True)

img_data = None
if input_method == "📷 실시간 촬영":
    img_data = st.camera_input("현장 촬영")
else:
    img_data = st.file_uploader("사진 파일 선택", type=['jpg', 'png', 'jpeg'])

if img_data:
    image = Image.open(img_data)
    st.image(image, caption="분석 대상", use_container_width=True)
    
    user_req = st.text_input("중점 확인 요청사항 (선택)", placeholder="예: 추락 위험 중심으로 봐줘")
    
    if st.button("🚀 AI 분석 시작", type="primary", use_container_width=True):
        with st.spinner("🚧 베테랑 AI가 법적 기준을 검토 중입니다..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash-preview')
                prompt = f"""
                당신은 산업안전보건법 및 중대재해처벌법 전문가입니다.
                사진을 분석하여 다음 내용을 마크다운으로 작성하세요:
                1. 🚨 핵심 위험요인 (5가지 이상)
                2. ⚖️ 위반 예상 법규 (구체적 조항 명시)
                3. ✅ 즉시 조치 및 관리적 대책
                (사용자 요청: {user_req})
                """
                response = model.generate_content([prompt, image])
                
                st.success("분석 완료!")
                st.markdown("### 📋 전문가 분석 보고서")
                with st.container(border=True):
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"분석 실패: {e}")