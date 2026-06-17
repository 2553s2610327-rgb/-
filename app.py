import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="자리배치 최적화",
    page_icon="🪑",
    layout="wide"
)

st.title("🪑 이전 자리와 겹치지 않는 자리배치")
st.caption("과거 자리 이력을 분석하여 최대한 다른 자리에 배치합니다.")

# ----------------------------
# 기본 학생 목록
# ----------------------------
DEFAULT_STUDENTS = [
    "김민수",
    "이서준",
    "박지호",
    "최도윤",
    "정하준",
    "강예린",
    "윤서연",
    "한지민",
    "송유진",
    "조수아",
    "오현우",
    "백지훈",
    "신민재",
    "문서윤",
    "장유나",
    "임채원",
    "김도현",
    "이하린",
    "박서준",
    "최유진"
]

# ----------------------------
# 사이드바
# ----------------------------
st.sidebar.header("설정")

uploaded_file = st.sidebar.file_uploader(
    "과거 자리 CSV 업로드",
    type=["csv"]
)

student_count = st.sidebar.number_input(
    "학생 수",
    min_value=4,
    max_value=40,
    value=20
)

cols = st.sidebar.number_input(
    "열(가로)",
    min_value=2,
    max_value=10,
    value=5
)

rows = st.sidebar.number_input(
    "행(세로)",
    min_value=2,
    max_value=10,
    value=4
)

if rows * cols < student_count:
    st.error("좌석 수가 학생 수보다 적습니다.")
    st.stop()

students = DEFAULT_STUDENTS[:student_count]

# ----------------------------
# 과거 데이터 읽기
# ----------------------------
history = {}

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        required_cols = {"학생", "자리"}

        if required_cols.issubset(df.columns):

            for _, row in df.iterrows():
                student = str(row["학생"])
                seat = int(row["자리"])

                history.setdefault(student, set()).add(seat)

            st.success("과거 데이터 로드 완료")

        else:
            st.warning(
                "CSV에는 '학생', '자리' 컬럼이 필요합니다."
            )

    except Exception as e:
        st.warning(f"파일 읽기 오류: {e}")

# ----------------------------
# 좌석 생성
# ----------------------------
seats = list(range(1, rows * cols + 1))

# ----------------------------
# 최적화 배치
# ----------------------------
best_assignment = {}
best_score = -1

for _ in range(500):
    shuffled = seats.copy()
    random.shuffle(shuffled)

    assignment = {}

    score = 0

    for student, seat in zip(students, shuffled):

        assignment[student] = seat

        if student in history:

            if seat not in history[student]:
                score += 10
            else:
                score -= 20

        else:
            score += 5

    if score > best_score:
        best_score = score
        best_assignment = assignment.copy()

# ----------------------------
# 결과 테이블 생성
# ----------------------------
seat_map = [["" for _ in range(cols)] for _ in range(rows)]

for student, seat in best_assignment.items():

    r = (seat - 1) // cols
    c = (seat - 1) % cols

    seat_map[r][c] = student

display_df = pd.DataFrame(
    seat_map,
    index=[f"{i+1}행" for i in range(rows)],
    columns=[f"{i+1}열" for i in range(cols)]
)

# ----------------------------
# 메인 화면
# ----------------------------
st.subheader("🎯 최종 자리배치")

st.dataframe(
    display_df,
    use_container_width=True
)

st.subheader("학생별 배정 결과")

result_df = pd.DataFrame(
    {
        "학생": list(best_assignment.keys()),
        "배정 자리": list(best_assignment.values())
    }
).sort_values("배정 자리")

st.dataframe(
    result_df,
    use_container_width=True
)

st.metric(
    "최적화 점수",
    best_score
)

st.download_button(
    "배치 결과 CSV 다운로드",
    result_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="seat_assignment.csv",
    mime="text/csv"
)
