import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="자리배치 아카이브",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ 자리배치 아카이브 및 내 자리 체크")
st.write("과거에 생성된 자리배치를 확인하고, 내가 앉았던 자리를 체크해 보세요!")

# 세션 상태 초기화
if "archive" not in st.session_state:
    st.session_state.archive = []
if "my_seats" not in st.session_state:
    st.session_state.my_seats = {} # {layout_id: [체크된 이름들]}

# 삭제 로직 함수
def delete_archive(archive_id):
    st.session_state.archive = [item for item in st.session_state.archive if item["id"] != archive_id]
    if archive_id in st.session_state.my_seats:
        del st.session_state.my_seats[archive_id]
    st.rerun()

# 아카이브가 비어있을 때
if not st.session_state.archive:
    st.info("아직 생성된 자리배치가 없습니다. '로딩중' 페이지에서 자리를 먼저 생성해 주세요!")
else:
    # 아카이브 순회
    for idx, item in enumerate(st.session_state.archive):
        item_id = item["id"]
        
        # 외곽 카드 스타일 구분선
        st.markdown(f"### 📅 생성 시간: {item['time']}")
        
        col_main, col_btn = st.columns([9, 1])
        
        with col_btn:
            # 개별 고유 키를 제공하여 휴지통 버튼 생성
            if st.button("🗑️ 삭제", key=f"del_{item_id}"):
                delete_archive(item_id)
        
        with col_main:
            # 해당 배치에서 고유한 이름 추출 (빈자리 제외)
            unique_names = sorted(list(set([name for row in item["layout"] for name in row if name != "빈자리"])))
            
            # 내 자리 체크 멀티셀렉트
            if item_id not in st.session_state.my_seats:
                st.session_state.my_seats[item_id] = []
                
            selected_names = st.multiselect(
                "이 배치에서 내가 앉았던 자리를 선택하세요 (하이라이트 표시):",
                options=unique_names,
                default=st.session_state.my_seats[item_id],
                key=f"select_{item_id}"
            )
            st.session_state.my_seats[item_id] = selected_names
            
            # 자리 배치 시각화
            st.write("**[자리 배치도]**")
            for r in range(item["rows"]):
                cols_ui = st.columns(item["cols"])
                for c in range(item["cols"]):
                    name = item["layout"][r][c]
                    
                    if name == "빈자리":
                        cols_ui[c].markdown(
                            "<div style='text-align:center; padding:10px; border-radius:5px; background-color:#eeeeee; color:#999999; font-size:14px;'>빈자리</div>",
                            unsafe_allow_html=True
                        )
                    elif name in selected_names:
                        # 내가 앉았던 자리 체크 시 주황색 하이라이트
                        cols_ui[c].markdown(
                            f"<div style='text-align:center; padding:10px; border-radius:5px; background-color:#ffe8cc; border:2px solid #ff922b; font-weight:bold; color:#d9480f;'>⭐ {name}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        cols_ui[c].markdown(
                            f"<div style='text-align:center; padding:10px; border-radius:5px; background-color:#e3faf2; border:1px solid #94d82d; font-size:14px;'>{name}</div>",
                            unsafe_allow_html=True
                        )
        st.markdown("---")
