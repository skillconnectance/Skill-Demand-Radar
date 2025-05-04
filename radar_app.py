import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq
import time

st.set_page_config(page_title="Skill Demand Radar", layout="centered")

st.title("📡 Skill Demand Radar (Live from Google Trends)")
st.caption("Trends shown below are based on real-time Google search interest in the UAE region.")

# Define skills of interest
skills = ["Data Science", "Digital Marketing", "AI", "Cloud Computing", "Cybersecurity", "UI UX", "Blockchain", "Project Management"]

# Initialize pytrends with retry + delay
pytrends = TrendReq(hl='en-US', tz=300, retries=3, backoff_factor=0.3)

# Try to fetch Google Trends data
try:
    time.sleep(3)  # prevent hammering the API
    pytrends.build_payload(skills, geo='AE')
    trends_df = pytrends.interest_over_time()

    if trends_df.empty:
        raise Exception("Empty data received from Google Trends.")

    trends_latest = trends_df.iloc[-1][skills].sort_values(ascending=False)
    st.success("✅ Fetched real-time data from Google Trends (UAE).")

except Exception as e:
    st.error(f"❌ Failed to fetch real-time Google Trends data.\n\nUsing fallback data instead.\n\nError: {str(e)}")
    trends_latest = pd.read_csv("fallback_trends.csv", index_col=0)["score"]

# ---
