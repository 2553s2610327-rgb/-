import streamlit as st
import random
import pandas as pd

# 1. 페이지 기본 설정 및 디자인 커스텀 (CSS Injection)
st.set_page_config(
    page_title="Secret Seat Matrix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세련되고 섹시한 다크 모드 & 네온 스타일 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 스타일 */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%);
        color: #e0e0e6;
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff007f, #7928ca);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }
    
    /* 좌석 박스 스타일 */
    .seat-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: #ffffff;
    }
    .seat-container:hover {
        transform: translateY(-5px);
        border-color: #ff007f;
        box-shadow: 0 10px 25px rgba(255, 0, 127, 0.2);
    }
    
    /* 교탁/칠판 스타일 */
    .board {
        background: linear-gradient(90deg, #1e1b4b, #311042);
        border: 2px solid #7928ca;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        letter-spacing: 5px;
        color: #a855f7;
        margin: 20px auto 40px auto;
        max-width: 400px;
        box-shadow: 0 0 15px rgba(121, 40, 202, 0.4);
    }
    
    /* 대나무숲 카드 스타일 */
    .bamboo-card {
        background: rgba(255, 255, 255, 0.02);
        border-left: 5px solid #ff007f;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px 12px 12px 4px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Session State 초기화 (데이터 유지용)
if 'seat_layout' not in st.session_state:
    st.session_state.seat_layout = None
if 'bamboo_forest' not in st.session_state:
    st.session_state.bamboo_forest = [
        {"emoji": "🤬", "text": "문 앞자리 걸렸음.. 나갈 때마다 문지기 확정 타임라인 지린다", "time": "방금 전"},
        {"emoji": "😭", "text": "최악의 빌런이랑 짝꿍됨 살려줘라 진짜", "time": "5분 전"}
    ]

# --- 사이드바 설정 영역 ---
st.sidebar.markdown("## ⚙️ Seat Settings")
st.sidebar.markdown("자리를 배치할 기준을 입력하세요.")

# 입력 방식 선택
num_people = st.sidebar.number_input("총 인원 수", min_value=1, max_value=100, value=16)
rows = st.sidebar.number_input("행 (Rows)", min_value=1, max_value=20, value=4)
cols = st.sidebar.number_input("열 (Columns)", min_value=1, max_value=20, value=4)

# 인원 수와 행x열 매칭 검증
if rows * cols < num_people:
    st.sidebar.warning(f"⚠️ 좌석 수({rows * cols}개)가 설정한 인원({num_people}명)보다 적습니다. 행 또는 열을 늘려주세요.")

default_names = ", ".join([f"참가자{i}" for i in range(1, num_people + 1)])
names_input = st.sidebar.text_area("이름 명단 (쉼표로 구분)", value=default_names, height=150)

# 배치하기 버튼
shuffle_button = st.sidebar.button("🔮 운명의 주사위 굴리기", use_container_width=True)


# --- 메인 화면 영역 ---
st.markdown('<p class="main-title">🔮 SECRET SEAT MATRIX</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">완벽한 배치, 그리고 은밀한 불평불만의 공간</p>', unsafe_allow_html=True)

# 탭 구성 (가독성 높은 모던 스타일)
tab1, tab2 = st.tabs(["✨ 배치 결과 보기", "🤫 대나무숲 (불평불만)"])

# 로직 처리: 셔플 버튼 클릭 시
if shuffle_button:
    # 예외 처리: 이름 파싱
    name_list = [name.strip() for name in names_input.split(",") if name.strip()]
    
    if len(name_list) < num_people:
        # 입력된 이름이 부족하면 자동으로 채움
        diff = num_people - len(name_list)
        for i in range(diff):
            name_list.append(f"추가인원{i+1}")
    elif len(name_list) > num_people:
        name_list = name_list[:num_people]
        
    # 랜덤 셔플
    random.shuffle(name_list)
    
    # 2차원 배열 좌석 배치 생성 (빈 자리는 빈 문자열)
    layout = []
    idx = 0
    for r in range(rows):
        row_seats = []
        for c in range(cols):
            if idx < len(name_list):
                row_seats.append(name_list[idx])
            else:
                row_seats.append("")
            idx += 1
        layout.append(row_seats)
        
    st.session_state.seat_layout = layout
    st.toast("🔮 자리가 공정하게 재배치되었습니다!", icon="✨")


# --- Tab 1: 배치 결과 화면 ---
with tab1:
    if st.session_state.seat_layout is not None:
        st.markdown('<div class="board">🖥️ FRONT / SCREEN</div>', unsafe_allow_html=True)
        
        # Grid 레이아웃 출력
        for r_idx, row in enumerate(st.session_state.seat_layout):
            columns = st.columns(cols)
            for c_idx, seat_name in enumerate(row):
                with columns[c_idx]:
                    if seat_name:
                        st.markdown(f'<div class="seat-container">{seat_name}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="seat-container" style="opacity: 0.2; border-style: dashed;">Empty</div>', unsafe_allow_html=True)
            st.write("") # 행간 간격 격차 확보
            
        st.success("💡 좌석 위로 마우스를 올리면 네온 하이라이트 효과를 볼 수 있습니다.")
    else:
        st.info("👈 왼쪽 사이드바에서 설정을 확인한 후 '🔮 운명의 주사위 굴리기' 버튼을 눌러주세요!")


# --- Tab 2: 불평불만 대나무숲 ---
with tab2:
    st.markdown("### 🤫 익명 불평불만 대나무숲")
    st.write("자리가 맘에 안 드시나요? 뒷자리라 안 보이시나요? 이름 없이 시원하게 털어놓으세요.")
    
    # 글 쓰기 구역
    with st.form(key="bamboo_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            emoji_choice = st.selectbox("기분", ["🤬", "😭", "😮‍💨", "🖕", "🚨", "👻"])
        with col2:
            complaint_text = st.text_input("서러운 한마디를 적어보세요...", placeholder="예: 아 내 앞자리 머리 진짜 크다 망했다")
            
        submit_complaint = st.form_submit_submit_button("익명 투고하기", use_container_width=True)
        
        if submit_complaint:
            if complaint_text.strip():
                # 최신글이 맨 위로 오도록 insert
                st.session_state.bamboo_forest.insert(0, {
                    "emoji": emoji_choice,
                    "text": complaint_text.strip(),
                    "time": "방금 전"
                })
                st.toast("🔥 대나무숲에 대나무를 심었습니다.", icon="🤫")
                st.rerun()
            else:
                st.warning("내용을 입력하셔야 대나무숲에 메아리가 울립니다!")
                
    st.markdown("---")
    
    # 글 목록 출력
    if st.session_state.bamboo_forest:
        for post in st.session_state.bamboo_forest:
            st.markdown(f"""
                <div class="bamboo-card">
                    <span style="font-size: 1.5rem; margin-right: 10px;">{post['emoji']}</span>
                    <strong style="color: #fff; font-size: 1.1rem;">{post['text']}</strong>
                    <div style="font-size: 0.8rem; color: #718096; margin-top: 5px; text-align: right;">{post['time']} · 익명객</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("아직 불평이 없습니다. 완벽한 자리배치였나 보군요...?")
