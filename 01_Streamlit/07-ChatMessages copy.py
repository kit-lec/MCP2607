import streamlit as st
import time

st.set_page_config(
    page_title="ChatMessages",
    page_icon="🌍",
)

st.title("Chat Messages")

with st.chat_message(name="human"):
    st.write('hello')
    st.write('how are you?')

with st.chat_message(name="ai"):
    st.write('nice to meet you')


st.chat_input(placeholder="Send a message to AI")

with st.status("Embedding file...", expanded=True) as status:
    time.sleep(3)
    st.write("Getting the file")
    time.sleep(3)
    st.write("Embedding the file")
    time.sleep(3)
    st.write("Caching the file")
    status.update(label="💥Error", state="error")










