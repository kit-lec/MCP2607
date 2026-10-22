import streamlit as st
import time
st.title('st.progress')

with st.expander('이 앱에 대하여'):
    st.write('계산의 진행상태를 표시합니다')

my_bar = st.progress(0)

for i in range(100):
    time.sleep(0.05)
    my_bar.progress(i + 1)

st.balloons()