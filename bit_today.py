#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pyupbit
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="KRW-BTC 10년 트래커", layout="wide")

st.title("🇰🇷 대한민국 비트코인(BTC/KRW) 실시간 시세 & 10년 데이터")

# 1. 실시간 시세 스크래핑 (업비트 API 활용)
def get_current_data():
    price = pyupbit.get_current_price("KRW-BTC")
    return price

current_price = get_current_data()
st.metric(label="현재 비트코인 가격 (Upbit)", value=f"{current_price:,.0f} KRW")

# 2. 10년치 역사적 데이터 불러오기
# 업비트 API는 최대 200개 캔들만 지원하므로, 10년치(일봉)를 가져오려면 반복 호출이 필요합니다.
@st.cache_data(ttl=3600)  # 1시간 동안 데이터 캐싱
def get_historical_10yr():
    df_list = []
    curr_date = datetime.now()

    # 약 10년(3650일) 데이터를 200개씩 끊어서 가져옴
    for _ in range(19): # 200 * 19 = 3800일 데이터
        df = pyupbit.get_ohlcv("KRW-BTC", interval="day", to=curr_date, count=200)
        if df is None or df.empty:
            break
        df_list.append(df)
        curr_date = df.index[0] # 가장 과거 데이터의 날짜로 업데이트

    full_df = pd.concat(df_list).sort_index()
    return full_df

with st.spinner('10년치 데이터를 불러오는 중...'):
    hist_df = get_historical_10yr()

# 3. 그래프 출력 (Plotly 활용)
fig = go.Figure()
fig.add_trace(go.Scatter(x=hist_df.index, y=hist_df['close'], mode='lines', name='종가 (KRW)'))

fig.update_layout(
    title="비트코인 10년 가격 추이 (일봉)",
    xaxis_title="날짜",
    yaxis_title="가격 (KRW)",
    hovermode="x unified",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_view_container=True)

# 데이터 요약 정보
col1, col2, col3 = st.columns(3)
col1.write(f"**데이터 시작일:** {hist_df.index[0].date()}")
col2.write(f"**역대 최고가:** {hist_df['high'].max():,.0f} KRW")
col3.write(f"**총 데이터 개수:** {len(hist_df)} 일")


# In[ ]:




