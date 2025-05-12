from pytrends.request import TrendReq
import pandas as pd
import streamlit as st
import time

pytrends = TrendReq(hl='en-US', tz=360)

def get_trend_data(keywords):
    try:
        pytrends.build_payload(keywords, cat=0, timeframe='today 3-m', geo='', gprop='')
        data = pytrends.interest_over_time()
        return data.drop(columns=['isPartial'])
    except Exception as e:
        return None

st.title("📈 Skill Demand Radar (Trend View)")

skills_input = st.text_input("Enter skills to learn (comma-separated)", "Python, Excel")
skills = [s.strip() for s in skills_input.split(',') if s.strip()]

if st.button("Get Trends"):
    if skills:
        trend_data = get_trend_data(skills[:5])  # Limit to 5
        if trend_data is not None and not trend_data.empty:
            st.line_chart(trend_data)
        else:
            st.error("No trend data found or rate limited.")
    else:
        st.warning("Please enter at least one skill.")
