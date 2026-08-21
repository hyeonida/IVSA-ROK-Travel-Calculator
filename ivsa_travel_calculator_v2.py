import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="IVSA 임원진 교통비 환급 계산기",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 스타일 커스텀
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0F52BA;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0A3D91;
        color: white;
    }
    .result-box {
        background-color: #F0F4F8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0F52BA;
        margin-top: 1.5rem;
    }
    .rule-box {
        background-color: #FFF9E6;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #FFAA00;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 IVSA 임원진 교통비 환급 계산기")
st.write("IVSA 임원진 환급 규정에 맞춰 본인의 최종 환급액을 미리 계산해 볼 수 있는 계산기입니다.")
st.write("해당 계산기를 이용하여 구글폼에 **환급 신청 금액을 작성해주세요.")

# 안내 문구 (접이식)
with st.expander("📌 IVSA 교통비 환급 핵심 규정 보기"):
    st.markdown("""
    * **기본 원칙:** 실제 이용 교통수단(KTX, 비행기 등)과 관계없이 **도시 간 우등 고속버스 요금**을 기준으로 지급합니다.
    * **소요 시간 가산금 (편도당):**
        * 편도 소요 시간 **2시간 30분 이상**: 편도 요금 +10,000원 추가
        * 편도 소요 시간 **3시간 30분 이상**: 편도 요금 +15,000원 추가
        * **제주대생 항공편 이용 시**: 소요 시간 관계없이 편도 요금 +15,000원 추가
    * **5만원 초과 상한선 규정:** 
        * 환급 기준액(x)이 50,000원을 초과할 경우, 초과 금액의 50%만 인정됩니다. 
        * **공식:** (x - 50,000) / 2 + 50,000 ₩
    * **실제 지출액 상한선:** 계산된 환급액이 아무리 높더라도, **실제로 지출한 금액(영수증 총합)을 초과할 수 없습니다.**
    """)

# 입력 폼 시작
st.write("---")

with st.form("calculator_form"):
    st.subheader("이동 1")
    fare1 = st.number_input("우등 고속버스 기준 요금 1 (원)", min_value=0, value=13300, step=100)
    duration_choice1 = st.selectbox(
        "가는 편 소요 시간 / 제주대 항공 여부 선택",
        options=[
            "2시간 30분 미만 (추가금 없음)",
            "2시간 30분 이상 ~ 3시간 30분 미만 (편도 +10,000원 가산)",
            "3시간 30분 이상 (편도 +15,000원 가산)",
            "제주대학교 학생 - 항공편 이용 (편도 +15,000원 가산)"
        ],
        index=0
    )

    st.write("")
    st.subheader("이동 2")
    fare2 = st.number_input("우등 고속버스 기준 요금 2 (원)", min_value=0, value=13300, step=100)
    duration_choice2 = st.selectbox(
        "오는 편 소요 시간 / 제주대 항공 여부 선택",
        options=[
            "2시간 30분 미만 (추가금 없음)",
            "2시간 30분 이상 ~ 3시간 30분 미만 (편도 +10,000원 가산)",
            "3시간 30분 이상 (편도 +15,000원 가산)",
            "제주대학교 학생 - 항공편 이용 (편도 +15,000원 가산)"
        ],
        index=0
    )

    st.write("")
    st.subheader("🧾 증빙 및 실지출액")
    actual_spent = st.number_input("실제 교통비로 지출한 총 금액 (모든 영수증의 합계, 원)", min_value=0, value=30000, step=100)

    # 제출 버튼
    submitted = st.form_submit_button("💰 환급 금액 계산하기")

if submitted:
    # 1. 가는 편 가산금 판정
    add1 = 0
    if "3시간 30분 이상" in duration_choice1 or "제주대학교" in duration_choice1:
        add1 = 15000
    elif "2시간 30분 이상" in duration_choice1:
        add1 = 10000
    total1 = fare1 + add1

    # 2. 오는 편 가산금 판정
    add2 = 0
    if "3시간 30분 이상" in duration_choice2 or "제주대학교" in duration_choice2:
        add2 = 15000
    elif "2시간 30분 이상" in duration_choice2:
        add2 = 10000
    total2 = fare2 + add2

    # 3. 총 기준액(X) 산출
    total_x = total1 + total2

    # 4. 50,000원 초과 규정 적용
    is_capped = False
    if total_x > 50000:
        calculated_amount = (total_x - 50000) / 2 + 50000
        is_capped = True
    else:
        calculated_amount = total_x

    # 5. 실제 지불액 상한선 적용
    final_refund = min(calculated_amount, actual_spent)
    is_actual_spent_limit = calculated_amount > actual_spent

    # 결과 화면 출력
    st.markdown("### 📊 계산 결과")
    
    # 최종 결과 카드
    st.markdown(f"""
        <div class="result-box">
            <h4 style="margin:0; color:#0F52BA;">최종 환급 결정액</h4>
            <p style="font-size: 2rem; font-weight: bold; margin: 5px 0 0 0; color:#0A3D91;">
                {int(final_refund):,} 원
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 상세 계산 내역 설명
    st.markdown("#### 🔍 세부 산출 과정")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **🛫 가는 편 기준액:**  
        * 기본 요금: {fare1:,}원  
        * 추가 가산금: {add1:,}원  
        * **소계: {total1:,}원**
        """)
    with col2:
        st.markdown(f"""
        **🛬 오는 편 기준액:**  
        * 기본 요금: {fare2:,}원  
        * 추가 가산금: {add2:,}원  
        * **소계: {total2:,}원**
        """)

    st.markdown(f"**시외/고속버스 이용기준 상 환급 가능 금액 :** {total_x:,}원")
    
    if is_capped:
        st.markdown(f"⚠️ **5만원 초과 감액 적용:** 기준액이 50,000원을 초과하여 공식 `(x - 50,000) / 2 + 50,000`이 적용되었습니다. → **{int(calculated_amount):,}원**")
    else:
        st.markdown(f"✅ **5만원 이하 정상 적용:** 기준액이 50,000원 이하이므로 전액 인정됩니다. → **{int(calculated_amount):,}원**")

    if is_actual_spent_limit:
        st.markdown(f"⚠️ **영수증 지출 한도 제한:** 계산된 환급액이 실제 지출한 금액({actual_spent:,}원)보다 크므로, 규정에 따라 **실제 영수증 지출 금액까지만 환급**됩니다.")
    else:
        st.markdown("✅ **영수증 한도 검증 완료:** 계산된 환급액이 실제 영수증 범위 내에 있으므로 전액 환급이 가능합니다.")

    st.info("💡 계산된 환급 금액은 규정 기준을 엄격하게 적용한 금액이며, 최종 지급을 위해서는 제출하신 버스 기준 요금 캡처 및 영수증 증빙이 일치해야 합니다.")
