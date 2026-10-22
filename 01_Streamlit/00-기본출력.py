import streamlit as st
import numpy as np
import pandas as pd

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # 필요한 환경변수


# 서버 실행
# > streamlit run ******.py
#    ※ 초반에 email 물어보면 걍 엔터 치세요.

# 서버 종료
# 터미널창에서 user break (CTRL + C) 연타
# user break 되지 않으면 terminal 종료(kill) 하세요

# 기본적인 widget(ui)
st.title('기본 출력')

st.title("스마일 :sunglasses:")
st.header("헤더를 입력할수 있다 :sparkles:")
st.subheader("이것은 subheader 임당")

st.text("일반적인 텍스트")

st.caption('캡션도 넣을수 있다.')

sample_code = '''
def function():
    print('hello, world')
'''
st.code(sample_code, language='python')

st.markdown('**마크다운 문법**을 지원 합니다')

st.markdown("텍스트의 색상을 :green[초록색]으로, 그리고 **:blue[파란색]** 볼드체로 설정할 수 있습니다.")
st.markdown(r":green[$\sqrt{x^2+y^2}$]  latex 문법 수식 표현 ")


st.latex(r'\sqrt{x^2+y^2}')

st.markdown('---')

st.title("Dataframe, Metric")

# DataFrame 생성
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
})

# DataFrame
# interactive 한 UI 도 제공
# use_container_width 기능은 데이터프레임을 컨테이너 크기에 확장할 때 사용합니다. (True/False)
st.dataframe(df, use_container_width=True)
st.dataframe(df, use_container_width=False)

st.table(df)

st.metric(label="온도", value="10°C", delta="1.2°C")
st.metric(label="삼성전자", value="61,000원", delta="-1,200원")

st.markdown('---')

st.title('write()')

st.write('hello')
st.write(10, 20, 30)
st.write([1, 2, 3 , 4])
st.write({'x': 100, 'y': 200})

import re

st.write(re.Pattern)

# Streamlit 에선 이와같이 값만 작성해도
# write() 한것과 동일하게 출력됨.
10000

a = [1, 2, 3, 4]
d = {'x': 1, 'y': -1}

a
d

import matplotlib.pyplot as plt
import seaborn as sns

# 한글폰트 설정
from matplotlib import font_manager, rc
import platform
try : 
    if platform.system() == 'Windows':
    # 윈도우인 경우
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    else:    
    # Mac 인 경우
        rc('font', family='AppleGothic')
except : 
    pass
plt.rcParams['axes.unicode_minus'] = False   

st.title('Chart 그리기')

data = pd.DataFrame({
    '이름': ['영식', '철수', '영희'],
    '나이': [22, 31, 25],
    '몸무게': [75.5, 80.2, 55.1]
})

st.dataframe(data, use_container_width=True)

fig, ax = plt.subplots()
ax.bar(data['이름'], data['나이'])
st.pyplot(fig)


barplot = sns.barplot(x='이름', y='나이', hue='이름', data=data,
            ax=ax, palette='Set2', legend=False)

fig = barplot.get_figure()
st.pyplot(fig)

# matplotlib 의 gallery 에 많은 예제들 
# https://matplotlib.org/stable/gallery/index.html

species = (
    "Adelie\n $\\mu=$3700.66g",
    "Chinstrap\n $\\mu=$3733.09g",
    "Gentoo\n $\\mu=5076.02g$",
)
weight_counts = {
    "Below": np.array([70, 31, 58]),
    "Above": np.array([82, 37, 66]),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Number of penguins with above average body mass")
ax.legend(loc="upper right")

st.pyplot(fig)