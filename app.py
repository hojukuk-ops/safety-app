import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import BytesIO
from datetime import datetime
import json
import math 

# ==========================================
# 1. 화면 구성 (UI) - 설정은 맨 위에 와야 함
# ==========================================
st.set_page_config(page_title="안산도시공사 안전보건 AI", page_icon="🏗️")

# ==========================================
# 0. API 키 설정 (보안 강화)
# ==========================================
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 API 키를 찾을 수 없습니다.")
    st.stop()

# ==========================================
# 세션 상태 초기화
# ==========================================
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'ai_result' not in st.session_state:
    st.session_state.ai_result = None

# ==========================================
# 메인 화면
# ==========================================
st.title("🏗️ 안산도시공사 도급·용역 안전보건 절차 확인 AI")
st.markdown("---")
st.info("작업 내용 입력 → AI 잠재 위험·요인 발굴 → **위험요인 선택(및 직접추가)** → **[웹에서 결과 확인]** → **[엑셀 다운로드]**")

# 입력 폼
col1, col2 = st.columns(2)
with col1:
    job_name = st.text_input("공사/작업명", placeholder="예: 본관 옥상 우레탄 방수공사")
    amount = st.number_input("공사 금액 (원)", min_value=0, step=100000, format="%d")

with col2:
    duration = st.number_input("계약 기간 (일)", min_value=1, value=1)
    
st.markdown("### ✅ 작업 조건 체크")
check_outside = st.checkbox("사업장 밖(외) 작업인가요?")
# 문구 수정: 사용자가 헷갈리지 않게 설명을 보강
check_high_risk = st.checkbox("고위험 작업이 포함되어 있나요? (밀폐공간, 고소, 중장비, 화기, 굴착, 방사선 작업 등)")
col_sub1, col_sub2 = st.columns(2)
with col_sub1:
    check_over_30 = st.checkbox("연속된 작업으로 공사 기간 30일 초과")
with col_sub2:
    check_over_60_year = st.checkbox("간헐적 작업으로 연간 총 공사기간 60일 초과")

# ==========================================
# 2. 로직 처리 함수
# ==========================================
def get_ai_analysis(job_name):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-3-flash-preview') # 모델명 최신화 권장 (gemini-3-flash-preview 등 사용 가능 시 유지)
        
        prompt = f"""
        당신은 산업안전보건법 및 중대재해 처벌법 전문가이자 베테랑 현장 소장입니다. 
        작업명: "{job_name}"
        
        다음 3가지를 분석하여 JSON으로만 답하세요. (마크다운 없이 순수 JSON만)
        1. industry: "건설업" 또는 "기타업종"
        2. is_low_risk: 전화상담, 단순 사무보조, 소프트웨어 설치, 단순 강의, 행사 진행 등 신체적 위험이 거의 없는 단순 노무/사무 용역인지 (true/false)
        3. risks: 이 작업의 핵심 위험요인 10개 이상을 발굴하고, 각 위험요인별로 작업반장님이 근로자에게 지시할 구체적인 '안전대책(한 줄 멘트)'을 쌍으로 작성.
        
        *중요: 고소작업, 화기작업, 밀폐공간, 중장비 사용 등 작업계획서 작성이 필요한 위험요소가 있다면 반드시 포함시키세요.*

        [응답 예시]
        {{
            "industry": "건설업",
            "is_low_risk": false,
            "risks": [
                {{"risk": "고소 작업 중 추락 위험", "measure": "안전대 고리 체결 철저 및 안전모 턱끈 조임 확인"}},
                {{"risk": "유기용제 중독 위험", "measure": "밀폐공간 환기팬 가동 및 방독마스크 착용"}}
            ]
        }}
        """
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None

def create_excel(data):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # [시트 1] 결과보고서
    df = pd.DataFrame(columns=["구분", "내용"])
    df.to_excel(writer, index=False, sheet_name='결과보고서')
    
    wb = writer.book
    ws1 = writer.sheets['결과보고서']
    
    fmt_title = wb.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter'})
    fmt_date = wb.add_format({'align': 'right', 'italic': True})
    fmt_header = wb.add_format({'bold': True, 'bg_color': '#EFEFEF', 'border': 1, 'align': 'left'})
    fmt_cell = wb.add_format({'text_wrap': True, 'border': 1, 'valign': 'top'})
    
    ws1.merge_range('A1:B1', "📋 도급·용역 안전보건 절차 이행 확인서", fmt_title)
    ws1.merge_range('A2:B2', f"작성일: {datetime.now().strftime('%Y-%m-%d')}", fmt_date)
    
    row = 3
    ws1.merge_range(row, 0, row, 1, "[1] 공사 개요", fmt_header)
    row += 1
    ws1.write(row, 0, "공사명", fmt_cell)
    ws1.write(row, 1, data['job_name'], fmt_cell)
    row += 1
    ws1.write(row, 0, "기간/금액", fmt_cell)
    ws1.write(row, 1, f"{data['duration']}일 / {data['amount']:,}원", fmt_cell)
    row += 1
    ws1.write(row, 0, "분석결과", fmt_cell)
    ws1.write(row, 1, f"{data['industry']} / {data['risk_level']}", fmt_cell)
    row += 1
    ws1.write(row, 0, "검토결과", fmt_cell)
    ws1.write(row, 1, data['conclusion'], fmt_cell)
    row += 2

    def write_section(ws, r, title, items):
        if items:
            ws.merge_range(r, 0, r, 1, title, fmt_header)
            r += 1
            for idx, item in enumerate(items, 1):
                ws.write(r, 0, str(idx), fmt_cell)
                ws.write(r, 1, item, fmt_cell)
                r += 1
            r += 1
        return r

    row = write_section(ws1, row, "[2] 착수 전 검토 서류", data['doc_review'])
    row = write_section(ws1, row, "[3] 작업 전/중 현장 관리 서류", data['doc_action'])
    row = write_section(ws1, row, "[4] 계약 기간 중 협의체 및 점검", data['doc_period'])
    
    risk_names = [r['risk'] for r in data['risks']]
    if risk_names:
        row = write_section(ws1, row, "[5] 식별된 핵심 위험요인", risk_names)
    else:
        ws1.merge_range(row, 0, row, 1, "[5] 식별된 핵심 위험요인", fmt_header)
        row += 1
        ws1.merge_range(row, 0, row, 1, "해당 없음 (사업장 밖 작업 등)", fmt_cell)
    
    ws1.set_column('A:A', 5)
    ws1.set_column('B:B', 70)

    # [시트 2] 안전·보건 교육 일지
    df2 = pd.DataFrame()
    df2.to_excel(writer, index=False, sheet_name='교육일지')
    ws2 = writer.sheets['교육일지']
    ws2.set_paper(9) # A4
    ws2.fit_to_pages(1, 1) 
    ws2.set_portrait() 
    ws2.set_margins(left=0.5, right=0.5, top=0.5, bottom=0.5)

    f_center = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    f_left = wb.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    f_bold_center = wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#F2F2F2'})
    f_title = wb.add_format({'bold': True, 'font_size': 22, 'align': 'center', 'valign': 'vcenter', 'underline': True})
    f_cell_left_top = wb.add_format({'align': 'left', 'valign': 'top', 'border': 1, 'text_wrap': True})

    ws2.set_column('A:A', 15)
    ws2.set_column('B:I', 13) 
    manual_row_height = 35

    ws2.merge_range('A1:F3', "안 전 · 보 건  교 육  일 지", f_title)
    ws2.merge_range('G1:G3', "결\n\n재", f_center)
    ws2.write('H1', "담 당", f_bold_center)
    ws2.merge_range('H2:H3', "", f_center)
    ws2.write('I1', "부 장", f_bold_center)
    ws2.merge_range('I2:I3', "", f_center)

    ws2.set_row(3, manual_row_height)
    ws2.write('A4', "교육일시", f_bold_center)
    ws2.merge_range('B4:I4', "", f_left) 

    ws2.merge_range('A5:A6', "교육구분", f_bold_center)
    ws2.merge_range('B5:I6', "☑ 도급 용역 전 안전보건 교육", f_left)

    ws2.write('A7', "구  분", f_bold_center)
    ws2.merge_range('B7:C7', "계", f_bold_center)
    ws2.merge_range('D7:E7', "남", f_bold_center)
    ws2.merge_range('F7:G7', "여", f_bold_center)
    ws2.merge_range('H7:I7', "교육 미실시 사유", f_bold_center)

    rows = [("교육대상자 수", "A8"), ("교육실시자 수", "A9"), ("교육미실시자 수", "A10")]
    for label, cell in rows:
        r = int(cell[1:]) - 1
        ws2.write(r, 0, label, f_bold_center)
        ws2.merge_range(r, 1, r, 2, "", f_center)
        ws2.merge_range(r, 3, r, 4, "", f_center)
        ws2.merge_range(r, 5, r, 6, "", f_center)
        ws2.merge_range(r, 7, r, 8, "", f_center)

    ws2.write('A11', "교육제목", f_bold_center)
    ws2.merge_range('B11:I11', f"{data['job_name']} 작업 전 안전보건교육", f_left)
    ws2.write('A12', "교육자료", f_bold_center)
    ws2.merge_range('B12:I12', "□ 교안    □ PPT    ☑ 기타 (현장 TBM 자료)", f_left)

    ws2.merge_range('B13:E13', "위험 요인", f_bold_center)
    ws2.merge_range('F13:I13', "핵심 안전수칙", f_bold_center)
    
    risks = data['risks']
    risk_count = len(risks)
    if risk_count == 0: risk_count = 1 
    last_risk_row = 12 + risk_count 
    ws2.merge_range(12, 0, last_risk_row, 0, "교 육\n내 용", f_bold_center)

    base_height = 32 
    if not risks:
        ws2.merge_range(13, 1, 13, 8, "해당 없음 (사업장 밖 작업 또는 단순 노무/사무)", f_cell_left_top)
        ws2.set_row(13, base_height)
    else:
        for i, item in enumerate(risks):
            r = 13 + i 
            risk_text = f"{i+1}. {item['risk']}"
            measure_text = f"👉 {item['measure']}"
            
            max_len = max(len(risk_text), len(measure_text))
            lines = (max_len // 22) + 1 
            row_height = max(base_height, lines * 16) 
            ws2.set_row(r, row_height) 
            ws2.merge_range(r, 1, r, 4, risk_text, f_cell_left_top)
            ws2.merge_range(r, 5, r, 8, measure_text, f_cell_left_top)

    start_row = last_risk_row + 1
    ws2.set_row(start_row, manual_row_height)
    ws2.merge_range(start_row, 0, start_row+1, 0, "교육실시자\n및 장소", f_bold_center)
    ws2.write(start_row, 1, "성 명", f_bold_center)
    ws2.merge_range(start_row, 2, start_row, 3, "", f_center)
    ws2.write(start_row, 4, "직 명", f_bold_center)
    ws2.merge_range(start_row, 5, start_row, 6, "관리감독자", f_center)
    ws2.write(start_row, 7, "장 소", f_bold_center)
    ws2.write(start_row, 8, "", f_center)

    ws2.set_row(start_row+1, manual_row_height)
    ws2.write(start_row+1, 1, "특기사항", f_bold_center)
    ws2.merge_range(start_row+1, 2, start_row+1, 8, "", f_left)

    writer.close()
    return output.getvalue()

# ==========================================
# 3. [1단계] 분석 시작 버튼
# ==========================================
st.markdown("---")
if st.button("🚀 분석 및 결과 생성 시작", type="primary"):
    if not job_name:
        st.warning("공사명을 입력해주세요.")
    else:
        if check_outside:
            st.session_state.ai_result = {
                "industry": "사업장 밖(외)",
                "is_low_risk": True,
                "risks": [] 
            }
            st.session_state.analyzed = True
        else:
            with st.spinner("AI가 작업 내용을 분석하고 있습니다..."):
                result = get_ai_analysis(job_name)
                
                if result:
                    if result.get('is_low_risk', False) == True:
                        result['risks'] = [] 
                        st.session_state.ai_result = result
                        st.session_state.analyzed = True
                    else:
                        st.session_state.ai_result = result
                        st.session_state.analyzed = True
                        st.session_state.ai_result['risks'].append({
                            "risk": "그 외 근골격계 질환, 넘어짐, 베임 등 중대재해 발생 가능성",
                            "measure": "작업 전 스트레칭 실시 및 주변 정리정돈 철저"
                        })

# ==========================================
# 4. [2단계] 결과 확인 및 선택
# ==========================================
if st.session_state.analyzed and st.session_state.ai_result:
    
    result_data = st.session_state.ai_result
    is_low_risk = result_data.get('is_low_risk', False)
    
    if check_outside or is_low_risk:
        if check_outside:
            st.success("✅ '사업장 밖(외) 작업'으로 확인되었습니다.")
        else:
            st.success(f"✅ '{result_data.get('industry', '기타')}' (단순/저위험 용역)으로 확인되었습니다.")
            
        st.info("📌 안전보건관리계획서 대신, **[안전서약서]** 로 대체 가능합니다.")
        final_selected_risks = []
        
    else:
        st.success(f"분석 완료! 업종: {result_data['industry']}")
        
        st.markdown("---")
        st.subheader("🧐 1. 위험요인 확인 및 체크")
        st.markdown("**아래 목록에서 실제 진행할 작업/위험요소를 체크(V)해주세요.**")

        final_selected_risks = []
        with st.container(border=True):
            for i, item in enumerate(result_data['risks']):
                label = f"⚠️ {item['risk']} (대책: {item['measure']})"
                # 기본값을 True로 할지 False로 할지는 선택 (현재: False)
                if st.checkbox(label, value=False, key=f"risk_checkbox_{i}"):
                    final_selected_risks.append(item) 
        
        st.write(f"👉 현재 **{len(final_selected_risks)}개**의 항목이 선택되었습니다.")

        st.markdown("---")
        st.subheader("➕ 2. 위험요인 직접 추가")
        with st.expander("눌러서 직접 입력하기", expanded=False):
            col_input1, col_input2, col_btn = st.columns([2, 3, 1])
            user_risk = col_input1.text_input("위험요인", placeholder="예: 지게차 충돌", key="input_risk")
            user_measure = col_input2.text_input("안전대책", placeholder="예: 신호수 배치", key="input_measure")
            if col_btn.button("목록에 추가", use_container_width=True):
                if user_risk and user_measure:
                    new_item = {"risk": user_risk, "measure": user_measure}
                    st.session_state.ai_result['risks'].append(new_item)
                    st.success("추가되었습니다! 위 목록 맨 아래를 확인해보세요.")
                    st.rerun()
                else:
                    st.warning("위험요인과 대책을 모두 입력해주세요.")

    # =========================================================
    # 3단계: 웹 보고서 출력 (여기가 핵심 수정 부분)
    # =========================================================
    
    industry = result_data.get('industry', '기타')
    doc_review, doc_action, doc_period = [], [], []
    conclusion = ""
    
    needs_joint = False
    if industry == "건설업" and duration >= 60: needs_joint = True
    elif industry != "건설업" and duration >= 90: needs_joint = True

    # [핵심 로직] 작업계획서가 필요한 고위험 키워드 리스트
    special_risk_keywords = ["고소", "추락", "화기", "용접", "절단", "불티", "밀폐", "질식", "중장비", "지게차", "굴착", "크레인", "비계"]
    
    # AI가 찾아낸 위험요소(사용자가 선택한 것) 중에 키워드가 있는지 검사
    detected_high_risk_task = False
    detected_keywords = []

    for item in final_selected_risks:
        risk_text = item['risk']
        # 키워드가 포함되어 있으면 True
        for keyword in special_risk_keywords:
            if keyword in risk_text:
                detected_high_risk_task = True
                detected_keywords.append(keyword)
                break # 하나의 항목에서 키워드 하나만 찾으면 루프 탈출
    
    # 중복 키워드 제거
    detected_keywords = list(set(detected_keywords))

    if check_outside:
        conclusion = "사업장 밖(외) 작업 (안전서약서 대상)"
        doc_review.append("안전서약서 (사업장 밖)")
        risk_level_str = "사업장 밖"
        if duration >= 90:
             doc_period.append("안전근로협의체 (계약 90일 이상, 분기별 1회, 안전보건의견서 작성)")

    elif is_low_risk:
        conclusion = "단순/저위험 용역 (안전서약서 대상)"
        doc_review.append("안전서약서 (단순/저위험)")
        risk_level_str = "단순/저위험"
        if duration >= 90:
             doc_period.append("안전근로협의체 (계약 90일 이상, 분기별 1회, 안전보건의견서 작성)")
        
    elif not check_high_risk and not final_selected_risks and not detected_high_risk_task:
        # 고위험 체크도 안했고, 위험요인도 선택 안했고, 감지된 고위험 키워드도 없을 때
        conclusion = "위험요인 미식별 (안전서약서 갈음)"
        doc_review.append("안전서약서 (식별된 위험요인 없음)")
        doc_review.append("적격수급업체평가표")
        doc_action = ["위험성평가표", "안전보건교육 (일지, 사진, 서명록)", "작업허가서 (핸디전자결재 후 편철)"]
        if industry == "건설업": doc_action.append("작업장 순회점검 (2일 1회), 작업장 순회점검일지 핸디 전자결재 후 편철")
        else: doc_action.append("작업장 순회점검 (1주 1회), 작업장 순회점검일지 핸디 전자결재 후 편철")
        risk_level_str = "일반/준저위험"
        
        if needs_joint:
            f = "2개월" if industry=="건설업" else "3개월"
            doc_period.append(f"합동안전보건점검 (사장님 및 수급업체 대표 참여 필요, 위임 가능, 합동안전점검일지 작성) ({f})")
        if check_over_30 or check_over_60_year: doc_period.append("안전보건협의체 (사장님 및 수급업체 대표 참여한 합동회의 실시, 월 1회, 위임가능, 회의결과보고)")
        if duration>=90: doc_period.append("안전근로협의체 (계약 90일 이상, 분기별 1회, 안전보건의견서 작성)")
    else:
        # 일반 혹은 고위험
        conclusion = "산업안전보건법 절차 이행 필요"
        doc_review = ["안전보건관리계획서", "적격수급업체평가표"]
        
        # [조건 수정] 수동 체크(check_high_risk) OR 자동 감지(detected_high_risk_task) 둘 중 하나라도 참이면
        if check_high_risk or detected_high_risk_task:
            reason = ""
            if detected_high_risk_task:
                reason = f" (사유: {', '.join(detected_keywords)} 관련 위험 선택됨)"
            doc_review.append(f"작업계획서{reason}")
            risk_level_str = "일반/고위험 (작업계획서 대상)"
            
            # 사용자에게 알림 (UI 표시)
            if not check_high_risk and detected_high_risk_task:
                 st.warning(f"🚨 선택하신 위험요인에 **[{', '.join(detected_keywords)}]** 작업이 포함되어 있어 '작업계획서'가 자동으로 추가되었습니다.")
        else:
             risk_level_str = "일반/위험"

        doc_action = ["위험성평가표", "안전보건교육 (일지, 사진, 서명록)", "작업허가서(핸디전자결재 후 편철)"]
        if industry == "건설업": doc_action.append("순회점검 (2일 1회), 작업장 순회점검일지 핸디 전자결재 후 편철")
        else: doc_action.append("순회점검 (1주 1회),작업장 순회점검일지 핸디 전자결재 후 편철")
        
        if needs_joint:
            f = "2개월" if industry=="건설업" else "3개월"
            doc_period.append(f"합동안전보건점검 (사장님 및 수급업체 대표 참여 필요, 위임 가능, 합동안전점검일지 작성) ({f})")
        if check_over_30 or check_over_60_year: doc_period.append("안전보건협의체 (사장님 및 수급업체 대표 참여한 합동회의 실시, 월 1회, 위임가능, 회의결과보고)")
        if duration>=90: doc_period.append("안전근로협의체 (계약 90일 이상, 분기별 1회, 안전보건의견서 작성)")

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
        "risks": final_selected_risks
    }

    st.markdown("---")
    st.subheader("📊 3. 분석 결과 보고서 미리보기")
    st.info(f"**결론:** {conclusion}")
    
    col_rep1, col_rep2, col_rep3 = st.columns(3)
    
    with col_rep1:
        st.markdown("**[착수 전 서류]**")
        for x in doc_review: st.write(f"- {x}")
        
    with col_rep2:
        st.markdown("**[작업 중 관리]**")
        for x in doc_action: st.write(f"- {x}")
        
    with col_rep3:
        st.markdown("**[협의체/점검]**")
        for x in doc_period: st.write(f"- {x}")

    st.markdown("---")
    
    excel_file = create_excel(final_data)
    st.download_button(
        label="📥 최종: 엑셀 보고서 + 교육일지 다운로드",
        data=excel_file,
        file_name=f"안전점검_{job_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )