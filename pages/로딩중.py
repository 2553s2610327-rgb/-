import streamlit as st
import random
import time

st.set_page_config(page_title="자리배치 생성기", page_icon="🪑", layout="centered")

st.title("🪑 자리배치 랜덤 생성기")
st.write("학생 이름을 입력하고 랜덤으로 자리배치를 생성하세요!")

# -------------------------
# 입력 영역
# -------------------------
names_input = st.text_area(
    "학생 이름 입력 (쉼표로 구분)",
    placeholder="예: 철수, 영희, 민수, 지민"
)

col1, col2 = st.columns(2)
with col1:
    rows = st.number_input("행 수", min_value=1, max_value=10, value=3)
with col2:
    cols = st.number_input("열 수", min_value=1, max_value=10, value=3)

seed_option = st.checkbox("랜덤 고정 (같은 결과 유지)")
seed_value = st.number_input("시드 값", value=42) if seed_option else None

start = st.button("🎲 자리 배치 시작")

# -------------------------
# 함수
# -------------------------
def generate_seats(names, rows, cols, seed=None):
    if seed is not None:
        random.seed(seed)

    total = rows * cols

    while len(names) < total:
        names.append("빈자리")

    random.shuffle(names)
    return names

# -------------------------
# 실행
# -------------------------
if start:
    try:
        if not names_input.strip():
            st.warning("이름을 입력해주세요.")
            st.stop()

        names = [n.strip() for n in names_input.split(",") if n.strip()]

        if len(names) == 0:
            st.warning("유효한 이름이 없습니다.")
            st.stop()

        if len(names) > rows * cols:
            st.error("자리 수보다 학생 수가 많습니다!")
            st.stop()

        seats = generate_seats(names.copy(), rows, cols, seed_value)

        # -------------------------
        # 긴장 연출
        # -------------------------
        st.markdown("## 🥁 자리 배치 중...")

        # 브금
        st.markdown(
            """
            <iframe width="0" height="0"
            src="https://www.youtube.com/embed/2Z4m4lnjxkY?autoplay=1&loop=1&playlist=2Z4m4lnjxkY"
            frameborder="0" allow="autoplay"></iframe>
            """,
            unsafe_allow_html=True
        )

        placeholder = st.empty()

        # 북 애니메이션
        for _ in range(4):
            placeholder.markdown("### 🥁 🥁 🥁 🥁 🥁")
            time.sleep(0.4)

        # 카운트다운
        for i in range(3, 0, -1):
            placeholder.markdown(f"# ⏳ {i}...")
            time.sleep(1)

        placeholder.empty()

        st.success("🎉 자리 배치 완료!")

        # -------------------------
        # 결과 출력 (카드 스타일)
        # -------------------------
        idx = 0
        for r in range(rows):
            cols_ui = st.columns(cols)
            for c in range(cols):
                name = seats[idx]
                idx += 1

                if name == "빈자리":
                    cols_ui[c].markdown(
                        f"<div style='text-align:center; padding:15px; border-radius:10px; background-color:#f0f0f0;'>🪑 빈자리</div>",
                        unsafe_allow_html=True
                    )
                else:
                    cols_ui[c].markdown(
                        f"<div style='text-align:center; padding:15px; border-radius:10px; background-color:#d1e7dd; font-weight:bold;'>{name}</div>",
                        unsafe_allow_html=True
                    )

        # 재배치 버튼
        if st.button("🔄 다시 섞기"):
            st.rerun()

    except Exception as e:
        st.error(f"오류 발생: {e}")1
