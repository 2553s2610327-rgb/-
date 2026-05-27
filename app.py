import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

# 제목
st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

except Exception:
    st.error("API 키를 불러오지 못했습니다. secrets 설정을 확인해주세요.")
    st.stop()

# 모델 설정
MODEL_NAME = "gemini-2.5-flash-lite"

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"모델 초기화 오류: {e}")
    st.stop()

# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 따뜻하고 공감 능력이 뛰어난 연애상담 전문가야.

규칙:
- 사용자의 감정을 먼저 공감해줘.
- 지나치게 딱딱하지 않게 자연스럽게 대화해.
- 현실적인 조언을 제공해.
- 공격적이거나 위험한 조언은 하지 마.
- 답변은 너무 길지 않게 적당한 길이로 해줘.
"""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 대화 기록 구성
                conversation = SYSTEM_PROMPT + "\n\n"

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    conversation += f"{role}: {msg['content']}\n"

                # Gemini 호출
                response = model.generate_content(conversation)

                bot_reply = response.text

                # 응답 출력
                st.markdown(bot_reply)

                # 기록 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_reply
                })

            except Exception as e:
                error_message = f"오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# 사이드바
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 사용 모델")
    st.code(MODEL_NAME)
