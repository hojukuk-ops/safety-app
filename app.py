import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import BytesIO
from datetime import datetime
import json

# ==========================================
# 🔑 API 키 설정 (따옴표 안에 키를 넣으세요)
# ==========================================
API_KEY = "AIzaSyC1azwSUAeE0xAwJ4s6NKNmFsuUOF0SC8Y" 

# ==========================================
# 1. 화면 구성 (UI)
# ==========================================
st.set_page_config(page_title="공사 안전점검 AI", page_icon="🏗️")

st.title("🏗️ 도급·용역 안전보건 절차 확인 AI")
st.markdown("---")
st.info("작업 내용과 기간을 입력하면, AI가 위험성을 분석하고 필요한 안전 서류를 엑셀로 만들어줍니다.")

# 입력 폼 (화면 좌우 분할)
col1, col2 = st.columns(2)

with col1:
    job_name = st.text_input("공사/작업명", placeholder="예: 본관 옥상 우레탄 방수공사")
    amount = st.number_input("공사 금액 (원)", min_value=0, step=100000, format="%d")

with col2:
    duration = st.number_input("공사 기간 (일)", min_value=1, value=1)
    
st.markdown("### ✅ 작업 조건 체크")
check_outside = st.checkbox("사업장 밖(외) 작업입니다.")
check_high_risk = st.checkbox("고위험 작업이 포함되어 있나요? (화재, 폭발, 질식, 고소작업 등)")
col_sub1, col_sub2 = st.columns(2)
with col_sub1:
    check_over_30 = st.checkbox("공사 기간 30일 초과")
with col_sub2:
    check_over_60_year = st.checkbox("연간 총 공사기간 60일 초과")

# ==========================================
# 2. 로직 처리 함수 (AI 통신)
# ==========================================
def get_ai_analysis(job_name):
    """제미나이에게 분석 요청"""
    try:
        genai.configure(api_key=API_KEY)
        # 사장님이 요청하신 Flash 모델 사용
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        당신은 산업안전보건법 전문가입니다. 
        작업명: "{job_name}"
        
        다음 3가지를 분석하여 JSON으로만 답하세요. (마크다운 없이 순수 JSON만)
        1. industry: "건설업" 인지 "기타업종" 인지 판단 (도장, 방수, 시설공사, 인테리어, 보수공사는 건설업. 청소, 경비, SW개발, 단순용역, 유지보수는 기타업종)
        2. is_low_risk: 사무직, SW개발, 단순 강의, 전화상담, 단순물품납품 등 신체적 위험이 거의 없는지 (true/false)
        3. risks: 이 작업에서 발생할 수 있는 잠재적 위험요인 5가지를 구체적인 문장(한국어)으로 리스트업.

        [응답 예시]
        {{
            "industry": "건설업",
            "is_low_risk": false,
            "risks": ["고소 작업 중 추락", "유기용제 중독"]
        }}
        """
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI 분석 중 오류가 발생했습니다. API 키를 확인해주세요.\n에러 내용: {e}")
        return None

# ==========================================
# 3. 엑셀 생성 함수 (xlsxwriter 사용)
# ==========================================
def create_excel(data):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # 데이터프레임 껍데기 생성
    df = pd.DataFrame(columns=["구분", "내용"])
    df.to_excel(writer, index=False, sheet_name='결과보고서')
    
    workbook = writer.book
    worksheet = writer.sheets['결과보고서']
    
    # 엑셀 스타일 정의
    header_format = workbook.add_format({'bold': True, 'bg_color': '#EFEFEF', 'border': 1, 'align': 'left'})
    cell_format = workbook.add_format({'text_wrap': True, 'border': 1, 'valign': 'top'})
    title_format = workbook.add_format({'bold': True, 'font_size': 16})
    
    # 제목 및 기본정보
    worksheet.write('A1', "📋 도급·용역 안전보건 절차 이행 확인서", title_format)
    worksheet.write('A2', f"작성일: {datetime.now().strftime('%Y-%m-%d')}")
    
    row = 3
    # [1] 공사 개요
    worksheet.merge_range(row, 0, row, 1, "[1] 공사 개요", header_format)
    row += 1
    worksheet.write(row, 0, "공사명", cell_format)
    worksheet.write(row, 1, data['job_name'], cell_format)
    row += 1
    worksheet.write(row, 0, "기간/금액", cell_format)
    worksheet.write(row, 1, f"{data['duration']}일 / {data['amount']:,}원", cell_format)
    row += 1
    worksheet.write(row, 0, "분석결과", cell_format)
    worksheet.write(row, 1, f"{data['industry']} / {data['risk_level']}", cell_format)
    row += 1
    worksheet.write(row, 0, "검토결과", cell_format)
    worksheet.write(row, 1, data['conclusion'], cell_format)
    row += 2

    # 섹션 출력 헬퍼 함수
    def write_section(title, items):
        nonlocal row
        if items:
            worksheet.merge_range(row, 0, row, 1, title, header_format)
            row += 1
            for idx, item in enumerate(items, 1):
                worksheet.write(row, 0, str(idx), cell_format)
                worksheet.write(row, 1, item, cell_format)
                row += 1
            row += 1

    write_section("[2] 착수 전 검토 서류", data['doc_review'])
    write_section("[3] 작업 전/중 현장 관리 서류", data['doc_action'])
    write_section("[4] 기간 중 협의체 및 점검", data['doc_period'])
    write_section("[5] 식별된 핵심 위험요인", data['risks'])
    
    # 열 너비 조정
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 70)
    
    writer.close()
    return output.getvalue()

# ==========================================
# 4. 메인 실행 버튼 및 로직
# ==========================================
if st.button("🚀 AI 분석 및 결과 생성", type="primary"):
    if not job_name:
        st.warning("공사명을 입력해주세요.")
    else:
        with st.spinner("AI가 공사 내용을 분석하고 법적 기준을 검토 중입니다..."):
            ai_result = get_ai_analysis(job_name)
            
            if ai_result:
                # 변수 추출
                industry = ai_result.get('industry', '기타업종')
                risks = ai_result.get('risks', [])
                is_low_risk_ai = ai_result.get('is_low_risk', False)
                
                # 강제 추가 위험요인
                risks.append("그 외 근골격계 질환, 넘어짐, 베임 등 중대재해 발생 가능성")

                doc_review = []
                doc_action = []
                doc_period = []
                conclusion = ""

                # ---------------------------------------------------------
                # [핵심 로직] 사장님 코드의 Logic 변환
                # ---------------------------------------------------------
                
                # 합동점검 대상 판단 (건설업 60일, 기타 90일)
                needs_joint_inspection = False
                if industry == "건설업" and duration >= 60:
                    needs_joint_inspection = True
                elif industry != "건설업" and duration >= 90:
                    needs_joint_inspection = True

                # CASE 1: 완전 면제 (사업장 밖 or 단순저위험)
                if check_outside:
                    conclusion = "사업장 밖(외) 작업으로, [안전서약서] 준비"
                    doc_review.append("안전서약서 (사업장 밖 작업)")
                    risk_level_str = "사업장 밖"
                
                elif is_low_risk_ai:
                    conclusion = "단순 저위험 용역으로, [안전서약서] 준비"
                    doc_review.append("안전서약서 (단순/저위험)")
                    risk_level_str = "단순/저위험"

                # CASE 2: 준저위험 (위험요인 없음 - 여기서는 AI가 위험요인이 없다고 판단한 경우로 가정)
                # (Streamlit에서는 체크박스 단계가 없으므로 고위험 작업이 아니고 Risks가 비어있으면 이쪽으로 분류)
                elif not check_high_risk and not risks:
                     conclusion = "위험요인이 식별되지 않아 [안전서약서]로 갈음하되, 기본 안전관리는 수행"
                     doc_review.append("안전서약서 (식별된 위험요인 없음)")
                     doc_review.append("적격수급업체평가표")
                     doc_action.append("위험성평가 (간소화)")
                     doc_action.append("안전보건교육 (일지, 사진, 서명)")
                     
                     if industry == "건설업":
                         doc_action.append("작업장 순회점검 (2일에 1회 이상)")
                     else:
                         doc_action.append("작업장 순회점검 (1주일에 1회 이상)")
                     
                     doc_action.append("작업허가서")
                     risk_level_str = "일반/준저위험"
                     
                     if needs_joint_inspection:
                        freq = "2개월에 1회" if industry == "건설업" else "3개월(분기)에 1회"
                        doc_period.append(f"합동안전보건점검 (사장님/대표 참여, {freq})")
                     
                     if check_over_30 or check_over_60_year:
                        doc_period.append("안전보건협의체 회의 (매월 1회)")
                     if duration >= 90:
                        doc_period.append("안전근로협의체 (분기별 의견서)")

                # CASE 3: 표준 (일반/고위험) - 대부분 이쪽으로 옴
                else:
                    conclusion = "산업안전보건법에 따른 안전보건 절차 이행 필요"
                    risk_level_str = "일반/고위험"
                    
                    doc_review.append("안전보건관리계획서")
                    doc_review.append("적격수급업체평가표")
                    if check_high_risk or risks:
                        doc_review.append("작업계획서 (위험요인/공종 해당)")
                    
                    doc_action.append("위험성평가 (위험성평가표)")
                    doc_action.append("안전보건교육 (일지, 사진, 서명)")
                    
                    # 순회점검 로직
                    if industry == "건설업":
                         doc_action.append("작업장 순회점검 (2일에 1회 이상)")
                    else:
                         doc_action.append("작업장 순회점검 (1주일에 1회 이상)")
                    
                    doc_action.append("작업허가서")

                    # 합동점검 로직
                    if needs_joint_inspection:
                        freq = "2개월에 1회" if industry == "건설업" else "3개월(분기)에 1회"
                        doc_period.append(f"합동안전보건점검 (사장님/대표 참여, {freq})")
                    
                    # 협의체 로직
                    if check_over_30 or check_over_60_year:
                        doc_period.append("안전보건협의체 회의 (매월 1회)")
                    if duration >= 90:
                        doc_period.append("안전근로협의체 (분기별 의견서)")

                # ---------------------------------------------------------
                # 결과 출력 및 엑셀 다운로드
                # ---------------------------------------------------------
                st.success("분석 완료!")
                st.subheader(f"📊 결과: {industry} / {risk_level_str}")
                st.write(f"**결론:** {conclusion}")
                
                with st.expander("⚠️ 식별된 위험요인 보기"):
                    for r in risks:
                        st.write(f"- {r}")

                # 데이터 패키징
                final_data = {
                    "job_name": job_name,
                    "duration": duration,
                    "amount": amount,
                    "industry": industry,
                    "risk_level": risk_level_str,
                    "conclusion": conclusion,
                    "doc_review": doc_review,
                    "doc_action": doc_action,
                    "doc_period": doc_period,
                    "risks": risks
                }

                # 엑셀 다운로드 버튼
                excel_data = create_excel(final_data)
                st.download_button(
                    label="📥 결과 보고서 엑셀 다운로드",
                    data=excel_data,
                    file_name=f"안전점검_{job_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )