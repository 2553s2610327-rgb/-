import streamlit as st

st.set_page_config(
    page_title="Bloody Seat Review",
    page_icon="🩸",
    layout="wide"
)

# ----------------------------
# 세션 상태 초기화
# ----------------------------

if "reviews" not in st.session_state:
    st.session_state.reviews = []

if "complaints" not in st.session_state:
    st.session_state.complaints = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# ----------------------------
# CSS
# ----------------------------

st.markdown("""
<style>

.stApp{
    background-color:#050505;
    color:white;
}

.main-title{
    text-align:center;
    color:#ff0000;
    font-size:50px;
    font-weight:bold;
    text-shadow:0 0 20px red;
    animation: blink 1.5s infinite;
}

@keyframes blink{
    50%{
        opacity:0.5;
    }
}

.sub-title{
    text-align:center;
    color:#ff4444;
    font-size:22px;
}

.block{
    background:#120000;
    padding:20px;
    border-radius:15px;
    border:2px solid #990000;
    margin-bottom:20px;
}

.stat-box{
    background:#220000;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:2px solid red;
}

h1,h2,h3{
    color:#ff4444;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 헤더
# ----------------------------

st.markdown(
    """
    <div class='main-title'>
    🩸 BLOODY SEAT REVIEW 🩸
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
    오늘도 누군가는 최악의 자리에 배치된다...
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# 통계
# ----------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.reviews)}</h2>
        리뷰
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.complaints)}</h2>
        불만
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.suggestions)}</h2>
        개선 제안
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ----------------------------
# 리뷰
# ----------------------------

st.header("😈 자리바꾸기 리뷰")

with st.form("review_form"):

    nickname = st.text_input("닉네임")

    rating = st.selectbox(
        "만족도",
        [
            "😈 매우 불만",
            "😡 불만",
            "😐 보통",
            "🙂 만족",
            "😇 매우 만족"
        ]
    )

    review = st.text_area("리뷰 작성")

    submit_review = st.form_submit_button("리뷰 등록")

    if submit_review:
        try:
            if review.strip():

                st.session_state.reviews.append({
                    "name": nickname if nickname else "익명",
                    "rating": rating,
                    "review": review
                })

                st.success("리뷰 등록 완료!")

            else:
                st.warning("리뷰를 입력해주세요.")

        except Exception as e:
            st.error(f"오류 발생: {e}")

# ----------------------------
# 리뷰 출력
# ----------------------------

for item in reversed(st.session_state.reviews):

    st.markdown(
        f"""
        <div class='block'>
        <b>{item['name']}</b><br><br>
        {item['rating']}<br><br>
        {item['review']}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ----------------------------
# 불평불만
# ----------------------------

st.header("💀 불평불만 접수소")

complaint = st.text_area(
    "자리바꾸기에 대한 분노를 적어보세요",
    key="complaint"
)

if st.button("불만 등록"):

    try:

        if complaint.strip():

            st.session_state.complaints.append(
                complaint
            )

            st.success("불만 접수 완료!")

        else:
            st.warning("내용을 입력해주세요.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

for text in reversed(st.session_state.complaints):

    st.error(text)

st.divider()

# ----------------------------
# 개선점
# ----------------------------

st.header("🩸 개선점 제안")

suggestion = st.text_area(
    "개선 아이디어 작성",
    key="suggestion"
)

if st.button("제안 등록"):

    try:

        if suggestion.strip():

            st.session_state.suggestions.append(
                suggestion
            )

            st.success("제안 등록 완료!")

        else:
            st.warning("내용을 입력해주세요.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

for item in reversed(st.session_state.suggestions):

    st.info(item)

st.divider()

st.markdown(
    """
    ### ☠️ 관리자 메모

    - 친구 우선 배치 기능 필요
    - 반복 자리 방지 기능 필요
    - 랜덤 제외 기능 필요
    - 공정성 검증 기능 필요
    """
)
