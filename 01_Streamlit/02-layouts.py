import streamlit as st
import os
import time

import numpy as np

from dotenv import load_dotenv
load_dotenv()


print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')

st.title('layout')

# layout
#  streamlit 에서 제공하는 다양한 레이아웃 
#  공식: https://docs.streamlit.io/develop/api-reference/layout  (◀ 함 보자!)

# ────────────────────────────────────────────────────────

# 레이아웃 사용방식
# 방식1
cont = st.container(border=True)
cont.write('container 내부의 요소')
cont.text_input("이름 입력")

st.write('conatainer 바깥의 요소')
cont.slider('나이')

# 방식2  (추천) with 사용
with st.container(border=True):
    st.write('컨테이너 안 입니다')
    st.bar_chart(np.random.randn(50, 3))

# container vs. empty
# container() : 여러 요소들을 담는다
# empty() : 한개의 요소만 담는다.

with st.empty():
    st.write('뽀로로')
    st.write('하츄핑')


st.title('sidebar')

with st.sidebar:
    st.header('sidebar header')
    st.text_input('검색어')
    'Hello Everyone'

st.title('tabs')
tab_one, tab_two, tab_three = st.tabs(['뽀로로', '크롱', '포비'])

with tab_one:
    st.subheader('뽀통령')

with tab_two:
    st.subheader('크롱크롱')

with tab_three:
    st.subheader("삐뽀삐뽀")


st.title('columns')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='달러USD', value='1,228원', delta="-12.00원")
with col2:
    st.metric(label="일본JPY(100엔)", value="958.63 원", delta="-7.44 원")
with col3: 
    st.metric(label="유럽연합EUR", value="1,335.82 원", delta="11.44 원")
