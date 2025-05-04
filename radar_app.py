import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from pytrends.request import TrendReq

# Page config
st.set_page_config(page_title="Skill Demand Radar (Live)", layout="wide")

# Title
st.title("📡 Skill Demand Radar (Live from Google Trends)")
st.markdown("Trends shown below are based on real-time Google search interest in the UAE region.")

# Step 1: Define skills and fetch trends
skills = ['Data Science', 'AI', 'Cybersecurity', 'Cloud Computing', 'Blockchain', 'Digital Marketing', 'UI UX Design']

try:
    pytrends = TrendReq(hl='en-US', tz=300)
    pytrends.build_payload(skills, cat=0, timeframe='now 7-d', geo='AE')  # AE = UAE

    trends = pytrends.interest_over_time()
    if not trends.empty:
        trends = trends.drop(columns='isPartial')
        skill_scores = trends.iloc[-1]  # Get most recent data point
    else:
        st.warning("⚠️ No trend data received. Displaying default scores.")
        skill_scores = pd.Series([60, 70, 65, 80, 50, 75, 55], index=skills)

except Exception as e:
    st.error("Failed to fetch real-time Google Trends data.")
    st.code(str(e))
    skill_scores = pd.Series([60, 70, 65, 80, 50, 75, 55], index=skills)

# Step 2: Radar chart
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=skill_scores.values.tolist() + [skill_scores.values[0]],  # close the loop
    theta=skill_scores.index.tolist() + [skill_scores.index[0]],
    fill='toself',
    name='Skill Demand'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100])
    ),
    showlegend=False,
    title="Real-Time Skill Demand in UAE (Last 7 Days)"
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show raw data
with st.expander("🔍 Show raw trend data"):
    st.dataframe(skill_scores.sort_values(ascending=False))
Update radar_app with new features    
