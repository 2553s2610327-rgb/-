import streamlit as st
import time
import datetime

# 페이지 설정
st.set_page_config(
    page_title="자리배치 아카이브",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ 자리배치 아카이브 및 내 자리 체크")
st.write("과거에 생성된 자리배치를 확인하고, 내가 앉았던 자리를 체크해 보세요!")

# 아카이브 저장소 세션 초기화
if "custom_archive" not in st.session_state:
    st.session_state.custom_archive = []
if "my_seats" not in st.session_state:
    st.session_state.my_seats = {}

# ------------------------------------------------------------------
# [핵심] 원래 로딩중.py가 화면에 뿌리는 컴포넌트의 값을 역으로 추적하는 로직
# ------------------------------------------------------------------
# 로딩중.py에서 사용한 names_input, rows, cols가 세션에 남아있는지 확인
if "names_input" in st.session_state and st.session_state.names_input.strip():
    try:
        raw_names = [n.strip() for n in st.session_state.names_input.split(",") if n.strip()]
        r_val = int(st.session_state.get("rows", 3))
        c_val = int(st.session_state.get("cols", 3))
        total = r_val * c_val
        
        if len(raw_names) <= total and len(raw_names) > 0:
            # 원래 코드의 빈자리 채우기 로직 재현
            temp_names = list(raw_names)
            while len(temp_names) < total:
                temp_names.append("빈자리")
            
            # 2차원 배열 레이아웃 구조화
            current_layout = []
            idx = 0
            for r in range(r_val):
                row_cells = []
                for c in range(c_val):
                    row_cells.append(temp_names[idx])
                    idx += 1
                current_layout.append(row_cells)
            
            # 중복 저장 방지용 키 생성
            layout_signature = f"{r_val}_{c_val}_{','.join(temp_names)}"
            
            # 마지막으로 등록된 배치와 다르면 아카이브에 자동 등록
            if not st.session_state.custom_archive or st.session_state.custom_archive[0]["signature"] != layout_signature:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.custom_archive.insert(0, {
                    "id": time.time(),
                    "signature": layout_signature,
                    "time": now,
                    "rows": r_val,
                    "cols": c_val,
                    "layout": current_layout
                })
    except Exception:
        pass # 에러 발생 시 아카이브 수집만 건너뜀 (안정성 확보)

# ------------------------------------------------------------------
# 아카이브 화면 출력 영역
# ------------------------------------------------------------------
if not st.session_state.custom_archive:
    st.info("아직 저장된 자리배치가 없습니다. '로딩중' 페이지에서 자리를 먼저 생성한 뒤 아카이브 페이지를 열어주세요!")
else:
    # 아카이브 삭제 함수
    def delete_item(item_id):
        st.session_state.custom_archive = [item for item in st.session_state.custom_archive if item["id"] != item_id]
        if item_id in st.session_state.my_seats:
            del st.session_state.my_seats[item_id]
        st.rerun()

    # 저장된 배치 목록 루프
    for item in st.session_state.custom_archive:
        item_id = item["id"]
        
        st.markdown(f"### 📅 생성 시간: {item['time']}")
        
        col_main, col_btn = st.columns([9, 1])
        
        with col_btn:
            if st.button("🗑️ 삭제", key=f"del_{item_id}"):
                delete_item(item_id)
                
        with col_main:
            # 현재 배치에서 빈자리 제외한 이름 목록 추출
            unique_names = sorted(list(set([name for row in item["layout"] for name in row if name != "빈자리"])))
            
            if item_id not in st.session_state.my_seats:
                st.session_state.my_seats[item_id] = []
                
            selected = st.multiselect(
                "이 배치에서 내가 앉았던 자리를 선택하세요 (하이라이트 표시):",
                options=unique_names,
                default=st.session_state.my_seats[item_id],
                key=f"select_{item_id}"
            )
            st.session_state.my_seats[item_id] = selected
            
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
                    elif name in selected:
                        # 내가 앉은 자리는 주황색 하이라이트
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
