# st.form은 "제출" 버튼을 포함하여 요소들을 함께 묶는 양식을 생성합니다.

# 일반적으로 사용자가 위젯과 상호작용할 때마다 Streamlit 앱이 다시 실행됩니다.

# 양식은 다른 요소 및 위젯들을 시각적으로 그룹화하는 컨테이너이며, 제출 버튼을 포함합니다. 여기서 사용자는 제출 버튼을 누를 때까지 원하는 만큼 여러 위젯과 여러 번 상호작용할 수 있으며, 이는 앱의 재실행을 일으키지 않습니다. 마지막으로, 양식의 제출 버튼이 눌리면 양식 내의 모든 위젯 값들이 한 번에 Streamlit에 전송됩니다.

# 양식 객체에 요소를 추가하려면 with 표기법(선호됨)을 사용하거나, 변수에 할당한 후 Streamlit 메소드를 적용함으로써 양식에 메소드를 직접 호출하는 객체 표기법을 사용할 수 있습니다. 예제 앱에서 확인해 보세요.

# 양식에는 몇 가지 제약 사항이 있습니다.

# 모든 양식은 st.form_submit_button을 포함해야 합니다.
# st.button과 st.download_button은 양식에 추가할 수 없습니다.
# 양식은 앱의 어디에나(사이드바, 칼럼 등) 나타날 수 있지만, 다른 양식 내에 포함될 수는 없습니다.


import streamlit as st

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')

st.title('st.form')

st.subheader('커피 머신')

with st.form(key="coffee_form"):

    # 입력 위젯
    coffee_bean_val = st.selectbox('커피콩', ['아라비카', '로부스타'])
    coffee_roast_val = st.selectbox('커피 로스팅', ['라이트', '미디엄', '다크'])
    brewing_val = st.selectbox('추출 방법', ['에어로프레스', '드립', '프렌치 프레스', '모카 포트', '사이폰'])
    serving_type_val = st.selectbox('서빙 형식', ['핫', '아이스', '프라페'])
    milk_val = st.select_slider('우유 정도', ['없음', '낮음', '중간', '높음'])
    owncup_val = st.checkbox('자신의 컵 가져오기')

    submitted = st.form_submit_button("제출")


if submitted:
    # submit 하면 수행할 코드
    st.markdown(f'''
        ☕ 주문하신 내용:
        - 커피콩: `{coffee_bean_val}`
        - 커피 로스팅: `{coffee_roast_val}`
        - 추출 방법: `{brewing_val}`
        - 서빙 형식: `{serving_type_val}`
        - 우유: `{milk_val}`
        - 자신의 컵 가져오기: `{owncup_val}`
        ''')
else:
    st.write('☝️ 주문하세요!')    