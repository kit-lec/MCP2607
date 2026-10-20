import streamlit as st
import os
import time

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력

st.title('hello streamlit')
st.text(time.strftime('%Y-%m-%d %H:%M:%S'))

# 실행
# streamlit run 파일명