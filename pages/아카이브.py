import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="자리배치 아카이브",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ 자리배치 아카이브 박스")
st.write("그동안 배치된 자리를 확인하고, 내가 앉았던 자리를 체크하여 기록해 두세요!")

# 2. 글로벌 전역 세션 상태 확인 및 강제 연동
if "seat_archive" not in st.session_state:
    st.session_state["seat_archive"] = []
if "checked_seats" not in st.session_state:
    st.session_state["checked_seats"] = {}

# 3. 데이터가 비어있을 때의 처리
if not st.session_state["seat_archive"]:
    st.info("아직 저장된 자리 배치도가 없습니다. '로딩중' 페이지에서 자리를 먼저 생성해 주세요!")
    st.stop()

# 4. 아카이브 순회 출력
# 대포적인 렌더링 꼬임 방지를 위해 복사본 리스트를 기준으로 루프를 돕니다.
current_items = list(st.session_state["seat_archive"])

for item in current_items:
    item_id = item["id"]
    
    st.markdown(f"### 📅 배치 생성 시간: {item['time']}")
    
    # 구조 레이아웃 분리 (정렬 유지)
    col_main, col_btn = st.columns([9, 1])
    
    with col_btn:
        # 휴지통 기능 (삭제 처리 후 세션 즉시 동기화)
        if st.button("🗑️ 삭제", key=f"del_{item_id}"):
            # 삭제 로직 실행
            st.session_state["seat_archive"] = [i for i in st.session_state["seat_archive"] if i["id"] != item_id]
            if item_id in st.session_state["checked_seats"]:
                del st.session_state["checked_seats"][item_id]
            
            # 중요: 변경 사항을 시스템에 즉시 반영하기 위해 리런(Rerun) 호출
            st.rerun()
            
    with col_main:
        # 해당 배치도에서 빈자리를 제외한 실명 명단 추출
        all_names = sorted(list(set([name for row in item["layout"] for name in row if name != "빈자리"])))
        
        # 내가 앉았던 자리를 저장할 공간 빌드
        if item_id not in st.session_state["checked_seats"]:
            st.session_state["checked_seats"][item_id] = []
            
        # 선택박스 변경 시 세션에 즉시 반영되도록 트리거 설정
        my_selected = st.multiselect(
            "이 배치도에서 내가 앉았던 자리를 선택하세요 (주황색으로 강조됩니다):",
            options=all_names,
            default=st.session_state["checked_seats"][item_id],
            key=f"chk_{item_id}"
        )
        st.session_state["checked_seats"][item_id] = my_selected
        
        # 5. 자리배치도 시각화 그리드 출력
        st.write("**[배치도 구조]**")
        for r in range(item["rows"]):
            cols_ui = st.columns(item["cols"])
            for c in range(item["cols"]):
                name = item["layout"][r][c]
                
                if name == "빈자리":
                    cols_ui[c].markdown(
                        "<div style='text-align:center; padding:12px; border-radius:8px; background-color:#eeeeee; color:#aaaaaa; border:1px solid #dddddd;'>빈자리</div>",
                        unsafe_allow_html=True
                    )
                elif name in my_selected:
                    # 내가 체크한 자리는 주황색 하이라이트와 별 표기
                    cols_ui[c].markdown(
                        f"<div style='text-align:center; padding:12px; border-radius:8px; background-color:#ffe8cc; border:2px solid #ff922b; font-weight:bold; color:#d9480f;'>⭐ {name}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    # 일반 배치 자리 (연한 녹색 바탕)
                    cols_ui[c].markdown(
                        f"<div style='text-align:center; padding:12px; border-radius:8px; background-color:#e3faf2; border:1px solid #choice; color:#2b8a3e;'>{name}</div>",
                        unsafe_allow_html=True
                    )
    st.markdown("---")
