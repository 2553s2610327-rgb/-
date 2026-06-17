import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="스마트 자리배치 생성기",
    layout="wide"
)

# --------------------------
# 초기 데이터
# --------------------------

if "students" not in st.session_state:
    st.session_state.students = [
        "김민준","이서준","박도윤","최예준",
        "정하준","강지호","윤시우","한유진",
        "송서연","임지민","조수아","장하은"
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "current_seat" not in st.session_state:
    st.session_state.current_seat = None

# --------------------------
# 점수 계산
# --------------------------

def seat_score(new_pos, histories):

    score = 0

    for old in histories:

        for student in new_pos:

            if student not in old:
                continue

            nr, nc = new_pos[student]
            orr, occ = old[student]

            distance = abs(nr-orr) + abs(nc-occ)

            score += distance * 5

            if (nr, nc) == (orr, occ):
                score -= 100

    return score

# --------------------------
# 배치 생성
# --------------------------

def generate_best_seat(students, rows, cols, histories):

    seats = [(r, c) for r in range(rows) for c in range(cols)]

    if len(students) > len(seats):
        raise ValueError("학생 수가 좌석 수보다 많습니다.")

    best_score = -999999
    best_map = None

    for _ in range(300):

        shuffled = students[:]
        random.shuffle(shuffled)

        pos = {}

        for i, student in enumerate(shuffled):
            pos[student] = seats[i]

        score = seat_score(pos, histories)

        if score > best_score:
            best_score = score
            best_map = pos

    return best_map

# --------------------------
# 좌석표 출력
# --------------------------

def draw_classroom(seat_map, rows, cols):

    grid = [["" for _ in range(cols)] for _ in range(rows)]

    for student, (r, c) in seat_map.items():
        grid[r][c] = student

    st.markdown(
        """
        <div style="
        background:#ffd54f;
        text-align:center;
        padding:15px;
        border-radius:10px;
        font-size:24px;
        font-weight:bold;">
        교 탁
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    for r in range(rows):

        cols_ui = st.columns(cols)

        for c in range(cols):

            name = grid[r][c]

            with cols_ui[c]:

                st.markdown(
                    f"""
                    <div style="
                    border:2px solid #444;
                    border-radius:10px;
                    padding:18px;
                    text-align:center;
                    background:#f5f5f5;
                    min-height:80px;
                    font-weight:bold;
                    ">
                    🪑<br>
                    {name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# --------------------------
# 사이드바
# --------------------------

st.sidebar.header("설정")

student_text = st.sidebar.text_area(
    "학생 이름 (한 줄에 한 명)",
    "\n".join(st.session_state.students)
)

rows = st.sidebar.number_input(
    "행 수",
    min_value=1,
    max_value=10,
    value=3
)

cols = st.sidebar.number_input(
    "열 수",
    min_value=1,
    max_value=10,
    value=4
)

students = [
    s.strip()
    for s in student_text.split("\n")
    if s.strip()
]

st.session_state.students = students

# --------------------------
# 자리 생성 버튼
# --------------------------

if st.sidebar.button("새 자리배치 생성"):

    try:

        result = generate_best_seat(
            students,
            rows,
            cols,
            st.session_state.history
        )

        st.session_state.current_seat = result

        st.session_state.history.append(result)

    except Exception as e:
        st.error(str(e))

# --------------------------
# 메인 화면
# --------------------------

st.title("🏫 스마트 자리배치 생성기")

st.caption("이전 자리와 최대한 겹치지 않게 자동 배치")

if st.session_state.current_seat is None:

    try:

        first = generate_best_seat(
            students,
            rows,
            cols,
            st.session_state.history
        )

        st.session_state.current_seat = first

    except:
        pass

if st.session_state.current_seat:

    draw_classroom(
        st.session_state.current_seat,
        rows,
        cols
    )

    st.divider()

    seat_df = []

    for student, pos in sorted(
        st.session_state.current_seat.items()
    ):
        seat_df.append(
            [student, f"{pos[0]+1}행 {pos[1]+1}열"]
        )

    st.subheader("학생별 위치")

    st.dataframe(
        pd.DataFrame(
            seat_df,
            columns=["학생", "위치"]
        ),
        use_container_width=True
    )

else:
    st.info("학생 수를 입력한 뒤 자리배치를 생성하세요.")
