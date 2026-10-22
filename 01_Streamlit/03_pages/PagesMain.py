# page Home 작성

import streamlit as st

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')

# '여러 페이지'를 가진 애플리케이션도 만들어 보자.
#   home (메인) 페이지 만들기
#   각 앱을 위한 별개의 page들이 필요.

# 주의! pages/ 경로
# your_working_directory/   <-- streamlit 이 실행한 파일(py) 경로기준!
# ├── pages/
# │   ├── a_page.py
# │   └── another_page.py
# └── your_homepage.py
# 

# 공식]
#  Multipage apps
#    https://docs.streamlit.io/develop/concepts/multipage-apps
#  Automatic page labels and URLs
#    https://docs.streamlit.io/develop/concepts/multipage-apps/overview#automatic-page-labels-and-urls

st.set_page_config(  # <- streamlit 의 첫번재 실행문장이어야 한다
    page_title="Page",
    page_icon="😎",
)


st.title("Pages")


