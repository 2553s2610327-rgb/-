import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="자리 배치도 아카이브", page_icon="🗄️", layout="wide")

# 1. 초기 세션 상태(st.session_state) 및 샘플 데이터 설정
if "archive_data" not in st.session_state:
    # 초보자분들이 바로 확인할 수 있도록 샘플 데이터를 미리 넣어둡니다.
    st.session_state.archive_data = [
        {
            "id": 1,
            "title": "제1회 정기 세미나 자리 배치",
            "date": "2026-05-10",
            "rows": 3,
            "cols": 4,
            "layout": [
                ["민우", "서연", "지민", "준호"],
                ["하은", "도윤", "유진", "시우"],
                ["지우", "현우", "수아", "동현"]
            ],
            "my_seat": (1, 2)  # (row, col) 형태로 내가 앉은 자리 저장 (유진)
        },
        {
            "id": 2,
            "title": "6월 조별 프로젝트 부서 배치",
            "date": "2026-06-01",
            "rows": 2,
            "cols": 3,
            "layout": [
                ["팀장", "A조", "B조"],
                ["C조", "D조", "비어있음"]
            ],
            "my_seat": None  # 아직 체크 안 함
        }
    ]

# 2. 앱 헤더 및 설명
st.title("🗄️ 자리 배치도 아카이브")
st.markdown("""
과거에 생성된 자리 배치도를 확인하고 관리하는 페이지입니다.
* **내가 앉았던 자리 표시:** 각 배치도에서 본인이 앉았던 자리를 클릭해 체크하세요!
* **배치도 삭제:** 더 이상 필요 없는 배치도는 **휴지통(🗑️)** 버튼을 눌러 아카이브에서 제거할 수 있습니다.
""")

st.write("---")

# 3. 아카이브 목록 렌더링
if not st.session_state.archive_data:
    st.info("아카이브에 저장된 자리 배치도가 없습니다. 새로운 자리를 배치하고 저장해주세요!")
else:
    # 가독성을 위해 역순(최신순)으로 배치도 정렬
    for idx, item in enumerate(reversed(st.session_state.archive_data)):
        # 실제 세션 상태의 오리지널 인덱스 계산
        original_idx = len(st.session_state.archive_data) - 1 - idx
        
        # 카드 스타일의 레이아웃 구성 (제목 영역과 휴지통 버튼 분할)
        col_title, col_delete = st.columns([0.9, 0.1])
        
        with col_title:
            st.subheader(f"📍 {item['title']}")
            st.caption(f"생성일: {item['date']} | 크기: {item['rows']}x{item['cols']}")
        
        with col_delete:
            # 안전한 예외 처리가 포함된 삭제 버튼
            st.write("") # 정렬용 공백
            if st.button("🗑️", key=f"del_{item['id']}", help="이 배치도를 아카이브에서 삭제합니다."):
                try:
                    st.session_state.archive_data.pop(original_idx)
                    st.success("배치도가 삭제되었습니다.")
                    st.rerun() # 화면 즉시 갱신
                except Exception as e:
                    st.error(f"삭제 중 오류가 발생했습니다: {e}")

        # 자리 배치도 시각화 (그리드 구현)
        st.write("**[자리 배치 현황]** (클릭하여 내가 앉았던 자리를 지정/변경할 수 있습니다)")
        
        # 행(Row)별로 루프
        for r in range(item['rows']):
            cols_list = st.columns(item['cols']) # 열(Col) 개수만큼 스트림릿 컬럼 생성
            
            for c in range(item['cols']):
                with cols_list[c]:
                    try:
                        seat_name = item['layout'][r][c]
                    except IndexError:
                        seat_name = "비어있음"
                    
                    # 현재 자리가 내가 앉았던 자리인지 확인
                    is_my_seat = (item['my_seat'] == (r, c))
                    
                    # 버튼 스타일 차별화 (내가 앉은 자리는 직관적인 다른 형태/색상 유도)
                    # Streamlit 기본 버튼은 색상 커스텀이 제한적이므로 type으로 차별화
                    btn_type = "primary" if is_my_seat else "secondary"
                    btn_label = f"⭐ {seat_name} (나)" if is_my_seat else seat_name
                    
                    # 좌석 버튼 클릭 시 상태 변경
                    if st.button(btn_label, key=f"seat_{item['id']}_{r}_{c}", type=btn_type, use_container_width=True):
                        if is_my_seat:
                            # 이미 내 자리면 취소
                            st.session_state.archive_data[original_idx]['my_seat'] = None
                        else:
                            # 새로운 자리로 등록
                            st.session_state.archive_data[original_idx]['my_seat'] = (r, c)
                        st.rerun()
                        
        st.write("---") # 배치도 간 구분선

# 4. 개발자/테스트용 데이터 리셋 기능 (하단 구석 배치)
with st.sidebar:
    st.markdown("### ⚙️ 관리자 도구")
    if st.button("🔄 샘플 데이터로 리셋", use_container_width=True):
        if "archive_data" in st.session_state:
            del st.session_state.archive_data
        st.rerun()
