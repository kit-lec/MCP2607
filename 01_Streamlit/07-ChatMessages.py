import streamlit as st
import time

st.set_page_config(
    page_title="ChatMessages",
    page_icon="🌍",
)

st.title("Chat Messages")

# session_state 는 여러번 재실행해도 data 가 보존될수 있도록 해준다.
#   보존되는 데이터는 key-value 형태로 session에 저장됨

# session_state 의 'messages' 라는 key 에 담아볼거다.
# 명심! 언제든지 refresh 될때 재실행 된다는 사실 있지 말자
 # ↓ session_state 가 messages 라는 key 값이 없는 경우에만 빈 list 로 초기화
#    이미 가지고 있었다면 (즉, 이미 값이 있었다면) 아무것도 하지 않는다.
if "messages" not in st.session_state:
    st.session_state['messages'] = []

message = st.chat_input(placeholder="Send a message to AI")

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.write(message)
    if save:
        st.session_state['messages'].append({"message": message, "role": role})

# 챗봇 화면 그리기
for msg in st.session_state['messages']:
    send_message(msg['message'], msg['role'], save=False)

if message:
    send_message(message, 'human')
    time.sleep(2)
    send_message(f"You said: {message}", "ai")











