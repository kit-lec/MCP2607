import streamlit as st
import FinanceDataReader as fdr
import datetime

print('✅실행됨')

st.title('종목 차트 검색')

with st.sidebar:
    start_date = st.date_input(
        "조회 시작일을 선택해 주세요",
        datetime.datetime(2026, 10, 1),
    )

    end_date = st.date_input(
        "조회 종료일을 선택해 주세요",
        datetime.datetime(2026, 10, 26),
    )

    code = st.text_input(
        '종목코드',
        value='005930',  # 삼성전자
        placeholder='종목코드를 입력해 주세요'
    )

if code and start_date and end_date:
    df = fdr.DataReader(code, start_date, end_date)
    data = df.sort_index(ascending=True)['Close']

    tab1, tab2 = st.tabs(['차트', '데이터'])

    with tab1:
        st.line_chart(data)

    with tab2:
        st.dataframe(df.sort_index(ascending=False))


    with st.expander('컬럼 설명'):
        st.markdown("""
        - Open: 시가
        - High: 고가
        - Low: 저가
        - Close: 종가
        - Adj Close: 수정 종가
        - Volumn: 거래량
        """)
