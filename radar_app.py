import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq
import json
import time

st.set_page_config(page_title="Skill Demand Radar", layout="wide")

st.title("📡 Skill Demand Radar (Live from Google Trends)")
st.write("Trends shown below are based on real-time Google search interest in the UAE region.")

# Load skill categories
with open("skill_categories.json") as f:
    skill_data = json.load(f)

categories = list(skill_data.keys())
selected_category = st.selectbox("Choose Skill Category", categories)

skills = skill_data[selected_category]

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)
region = 'AE'  # United Arab Emirates

# Fetch interest data
results = {}
st.info("Fetching data from Google Trends...")

for skill in skills:
    try:
        pytrends.build_payload([skill], cat=0, timeframe='now 7-d', geo=region, gprop='')
        df = pytrends.interest_over_time()
        if not df.empty:
            score = df[skill].mean()
            results[skill] = round(score, 2)
        time.sleep(1)
    except Exception as e:
        st.error(f"Failed for {skill}: {e}")

if results:
    df = pd.DataFrame.from_dict(results, orient='index', columns=['Trend Score']).reset_index()
    df.rename(columns={'index': 'Skill'}, inplace=True)
    top_n = st.slider("Select Top N Skills", 3, len(df), 5)
    df = df.sort_values("Trend Score", ascending=False).head(top_n)

    # Radar chart
    fig = px.line_polar(df, r='Trend Score', theta='Skill', line_close=True,
                        title=f"Top {top_n} Trending Skills in {selected_category}",
                        color_discrete_sequence=['#00BFFF'])
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected category.")

# Raw data
with st.expander("🔍 Show raw trend data"):
    st.dataframe(df)
