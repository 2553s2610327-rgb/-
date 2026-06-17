import streamlit as st
import pandas as pd
import json
import random
from pathlib import Path

st.set_page_config(
    page_title="Seat Shuffle",
    page_icon="🪑",
    layout="wide"
)

DATA_FILE = "seat_history.json"


def load_history():
    try:
        if Path(DATA_FILE).exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception:
        return []


def save_history(history):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"저장 오류: {e}")


def generate_new_seating(students, history):
    seats = list(range(len(students)))

    previous_positions = {}

    for record in history:
        for student, seat in record.items():
            previous_positions.setdefault(student, set()).add(seat)

    best_assignment = None
    best_score = -1

    for _ in range(500):
        shuffled = seats.copy()
        random.shuffle(shuffled)

        assignment = dict(zip(students, shuffled))

        score = 0

        for student, seat in assignment.items():
            if seat not in previous_positions.get(student, set()):
                score += 1

        if score > best_score:
            best_score = score
            best_assignment = assignment

    return best_assignment


st.title("🪑 Seat Shuffle")
st.subheader("이전 자리와 최대한 겹치지 않는 새로운 자리 배치")

history = load_history()

col1, col2 = st.columns(2)

with col1:
    st.metric("저장된 배치 기록", len(history))

with col2:
    if history:
        latest = history[-1]
        st.metric("최근 배치 학생 수", len(latest))
    else:
        st.metric("최근 배치 학생 수", 0)

st.markdown("---")

st.markdown("""
### 📌 서비스 소개

Seat Shuffle은 이전 자리 기록을 분석하여
학생들이 과거와 최대한 다른 자리에 앉을 수 있도록
새로운 자리 배치를 생성합니다.

공정하고 다양한 자리 경험을 제공하는 것이 목표입니다.
""")

st.markdown("---")

st.header("학생 명단 입력")

student_text = st.text_area(
    "학생 이름을 한 줄에 한 명씩 입력하세요",
    height=250,
    placeholder="""
김민수
이서연
박준호
최지우
...
"""
)

if st.button("🎲 새로운 자리 생성"):
    try:
        students = [
            name.strip()
            for name in student_text.split("\n")
            if name.strip()
        ]

        if len(students) < 2:
            st.warning("학생을 2명 이상 입력하세요.")
        else:
            new_assignment = generate_new_seating(
                students,
                history
            )

            history.append(new_assignment)
            save_history(history)

            result_df = pd.DataFrame(
                {
                    "학생": list(new_assignment.keys()),
                    "자리번호": list(new_assignment.values())
                }
            ).sort_values("자리번호")

            st.success("새 자리 배치 생성 완료!")

            st.dataframe(
                result_df,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"오류 발생: {e}")

st.markdown("---")

st.header("📚 최근 배치 기록")

if history:
    recent = history[-1]

    recent_df = pd.DataFrame(
        {
            "학생": list(recent.keys()),
            "자리번호": list(recent.values())
        }
    ).sort_values("자리번호")

    st.dataframe(
        recent_df,
        use_container_width=True
    )

else:
    st.info("아직 저장된 자리 배치가 없습니다.")

st.markdown("---")

st.caption("Seat Shuffle | 이전 자리와 겹치지 않는 공정한 자리 배치")
