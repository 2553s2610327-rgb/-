import streamlit as st
import random

st.title("자리배치 생성기")

names_input = st.text_input("이름 입력 (쉼표로 구분)")
rows = st.number_input("행", 1, 10, 3)
cols = st.number_input("열", 1, 10, 3)

if st.button("생성"):
    if not names_input:
        st.warning("이름 입력하세요")
    else:
        names = [n.strip() for n in names_input.split(",")]

        if len(names) > rows * cols:
            st.error("자리 부족")
        else:
            while len(names) < rows * cols:
                names.append("빈자리")

            random.shuffle(names)

            idx = 0
            for r in range(rows):
                cols_ui = st.columns(cols)
                for c in range(cols):
                    cols_ui[c].write(names[idx])
                    idx += 1
