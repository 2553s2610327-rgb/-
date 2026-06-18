import streamlit as st

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="The Cursed Seat System",
    page_icon="🩸",
    layout="wide"
)

# --------------------------------------------------
# 세션 상태
# --------------------------------------------------

if "reviews" not in st.session_state:
    st.session_state.reviews = []

if "complaints" not in st.session_state:
    st.session_state.complaints = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top,
    #500000 0%,
    #1a0000 30%,
    #090000 70%,
    #000000 100%);
    color:white;
}

/* 스크롤바 */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-track{
    background:#150000;
}

::-webkit-scrollbar-thumb{
    background:#ff0000;
    border-radius:10px;
}

/* 메인 제목 */

.main-title{
    text-align:center;
    font-size:60px;
    font-weight:900;
    color:#ff0000;
    letter-spacing:3px;

    text-shadow:
    0 0 5px #ff0000,
    0 0 15px #ff0000,
    0 0 30px #ff0000,
    0 0 60px #aa0000;

    animation:flicker 1.5s infinite;
}

/* 부제목 */

.drip{
    text-align:center;
    color:#ff1111;
    font-size:22px;
    margin-bottom:30px;
    text-shadow:0 0 15px red;
}

@keyframes flicker{

    0%{opacity:1;}
    25%{opacity:0.8;}
    50%{opacity:0.4;}
    75%{opacity:0.9;}
    100%{opacity:1;}

}

/* 카드 */

.block{

    background:
    linear-gradient(
        180deg,
        #400000,
        #180000
    );

    border:2px solid #ff0000;

    border-radius:20px;

    padding:20px;

    margin-bottom:15px;

    box-shadow:
    0 0 15px red,
    inset 0 0 20px #600000;

}

/* 통계 */

.stat-box{

    background:
    linear-gradient(
        180deg,
        #5a0000,
        #1a0000
    );

    border:3px solid #ff0000;

    border-radius:20px;

    text-align:center;

    padding:20px;

    box-shadow:
    0 0 20px red,
    inset 0 0 15px #800000;
}

/* 버튼 */

.stButton > button{

    width:100%;

    background:#8b0000;

    color:white;

    border:2px solid red;

    border-radius:15px;

    font-weight:bold;

    box-shadow:0 0 15px red;
}

.stButton > button:hover{

    background:#ff0000;
}

/* 입력창 */

.stTextInput input,
.stTextArea textarea{

    background:#220000 !important;

    color:white !important;

    border:2px solid red !important;

}

/* 제목 */

h1,h2,h3{

    color:#ff3333 !important;

    text-shadow:0 0 10px red;

}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 헤더
# --------------------------------------------------

st.markdown("""
<div class='main-title'>
🩸 THE CURSED SEAT SYSTEM 🩸
</div>

<div class='drip'>
누군가는 오늘도 가장 끔찍한 자리를 배정받는다...
<br>
그리고 그 저주는 계속된다.
</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# 통계
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.reviews)}</h2>
        리뷰 수
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.complaints)}</h2>
        불만 수
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class='stat-box'>
        <h2>{len(st.session_state.suggestions)}</h2>
        개선 제안 수
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --------------------------------------------------
# 리뷰
# --------------------------------------------------

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

    review = st.text_area("리뷰 내용")

    submit_review = st.form_submit_button("리뷰 등록")

    if submit_review:

        try:

            if review.strip():

                st.session_state.reviews.append({
                    "name": nickname if nickname else "익명",
                    "rating": rating,
                    "review": review
                })

                st.success("리뷰가 등록되었습니다.")

            else:
                st.warning("리뷰를 입력해주세요.")

        except Exception as e:
            st.error(f"오류 발생: {e}")

# 리뷰 목록

for item in reversed(st.session_state.reviews):

    st.markdown(
        f"""
        <div class='block'>
        <b>{item['name']}</b>
        <br><br>
        {item['rating']}
        <br><br>
        {item['review']}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --------------------------------------------------
# 불만 접수
# --------------------------------------------------

st.header("💀 불평불만 접수소")

complaint = st.text_area(
    "분노를 적어보세요",
    key="complaint_box"
)

if st.button("불만 등록"):

    try:

        if complaint.strip():

            st.session_state.complaints.append(
                complaint
            )

            st.success("불만이 접수되었습니다.")

        else:
            st.warning("내용을 입력해주세요.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

for item in reversed(st.session_state.complaints):

    st.error(item)

st.divider()

# --------------------------------------------------
# 개선점
# --------------------------------------------------

st.header("🩸 개선점 제안")

suggestion = st.text_area(
    "개선 아이디어를 적어주세요",
    key="suggestion_box"
)

if st.button("제안 등록"):

    try:

        if suggestion.strip():

            st.session_state.suggestions.append(
                suggestion
            )

            st.success("제안이 등록되었습니다.")

        else:
            st.warning("내용을 입력해주세요.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

for item in reversed(st.session_state.suggestions):

    st.info(item)

st.divider()

# --------------------------------------------------
# 관리자 메모
# --------------------------------------------------

st.markdown("""
### ☠️ 관리자 메모

- 친구 우선 배치 기능
- 반복 자리 방지 기능
- 랜덤 제외 기능
- 공정성 검증 시스템
- 원하는 구역 선택 기능
""")
