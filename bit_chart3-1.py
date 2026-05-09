#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 스트림릿 페이지 설정
st.set_page_config(page_title="비트코인 10년 시세 트래커", layout="wide")

# 1. 데이터 가져오기 (캐싱 처리하여 속도 향상)
@st.cache_data(ttl=3600) # 1시간마다 데이터 갱신
def get_bitcoin_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)
    ticker = "BTC-USD"
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# 데이터 로딩
with st.spinner('비트코인 데이터를 불러오는 중...'):
    data = get_bitcoin_data()

# 2. 웹앱 구성
st.title("₿ 비트코인 10년 시세 트래커")
st.markdown("---")

if data.empty:
    st.error("데이터를 불러오는데 실패했습니다.")
else:
    # 오늘 가격 (가장 최근 종가)
    current_price = data['Close'].iloc[-1].item()
    last_date = data.index[-1].strftime('%Y-%m-%d')

    # 상단 메트릭(요약) 표시
    st.metric(label=f"{last_date} 기준 비트코인 종가", value=f"${current_price:,.2f}")

    # 3. Matplotlib 그래프 생성 및 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Close Price', color='orange', linewidth=1.5)
    ax.set_title("Bitcoin 10-Year Price Chart", fontsize=16)
    ax.set_ylabel("Price (USD)")
    ax.set_xlabel("Date")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    # 스트림릿에 matplotlib figure 표시
    st.pyplot(fig)

    # 데이터프레임 원본 보기
    with st.expander("원본 데이터 보기"):
        st.dataframe(data.tail(3600)) # 최근 100개

st.markdown("---")
st.caption("Source: Yahoo Finance")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




