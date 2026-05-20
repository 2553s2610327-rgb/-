import streamlit as st
import pandas as pd

st.set_page_config(page_title="식단 관리", page_icon="🍱")

st.title("🍱 식단 관리 앱")

# 세션 상태 초기화
if "foods" not in st.session_state:
    st.session_state.foods = []

# 입력 폼
with st.form("food_form"):
    food_name = st.text_input("음식 이름")
    calories = st.number_input("칼로리", min_value=0, step=1)

    submitted = st.form_submit_button("추가")

    if submitted:
        if food_name.strip() != "":
            st.session_state.foods.append({
                "음식": food_name,
                "칼로리": calories
            })
            st.success("추가 완료!")
        else:
            st.warning("음식 이름을 입력하세요.")

# 데이터 표시
if st.session_state.foods:
    df = pd.DataFrame(st.session_state.foods)

    st.subheader("오늘의 식단")
    st.dataframe(df, use_container_width=True)

    total_calories = df["칼로리"].sum()

    st.metric("총 칼로리", f"{total_calories} kcal")

    # 전체 삭제
    if st.button("전체 삭제"):
        st.session_state.foods = []
        st.rerun()
else:
    st.info("아직 추가된 식단이 없습니다.")
