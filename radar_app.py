import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import altair as alt
from pytrends.request import TrendReq
import time

# ----------------------------
# CONFIGURATION
# ----------------------------
st.set_page_config(page_title="Skill Demand Radar", layout="wide")
st.title("📡 Skill Demand Radar (Live from Google Trends)")
st.markdown("Trends shown below are based on real-time Google search interest in the UAE region.")

# ----------------------------
# CATEGORY & SKILL MAPPING
# ----------------------------
skill_categories = {
    "Technical Skills": ["Python", "Java", "Data Analysis", "Cybersecurity"],
    "Soft Skills": ["Communication", "Leadership", "Teamwork", "Problem Solving"],
    "Business & Management": ["Project Management", "Strategic Planning", "Marketing"],
    "Creative Skills": ["Graphic Design", "Video Editing", "UX Design"],
    "Marketing Skills": ["SEO", "Digital Marketing", "Branding"],
    "Data Science": ["Machine Learning", "Data Visualization", "SQL"],
    "Customer Service": ["Customer Support", "Empathy", "CRM"],
    "Sales": ["Negotiation", "Lead Generation", "CRM Software"],
    # You can add more categories and skills here
}

# ----------------------------
# SELECT CATEGORY
# ----------------------------
selected_category = st.selectbox("Choose a Skill Category", list(skill_categories.keys()))
skills = skill_categories[selected_category]

# ----------------------------
# GET GOOGLE TRENDS DATA
# ----------------------------
pytrends = TrendReq(hl="en-US", tz=4)

try:
    pytrends.build_payload(skills, geo='AE', timeframe='now 7-d')
    trends_data = pytrends.interest_over_time()

    if trends_data.empty:
        st.error("No trend data returned.")
    else:
        # Prepare trend scores
        latest_trends = trends_data.iloc[-1][skills].sort_values(ascending=False)
        trend_df = pd.DataFrame({
            "Skill": latest_trends.index,
            "Score": latest_trends.values
        })

        # ----------------------------
        # CHART TYPE SELECTOR
        # ----------------------------
        chart_type = st.radio("Select Visualization Type", ["Radar", "Bar", "Pie"], horizontal=True)

        # ----------------------------
        # DISPLAY: GRID
        # ----------------------------
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("🔍 Top Skills by Demand")
            st.dataframe(trend_df, use_container_width=True)

        with col2:
            if chart_type == "Bar":
                st.subheader("📊 Bar Chart")
                bar_chart = alt.Chart(trend_df).mark_bar().encode(
                    x=alt.X("Skill", sort="-y"),
                    y="Score",
                    color="Skill"
                ).properties(height=400)
                st.altair_chart(bar_chart, use_container_width=True)

            elif chart_type == "Pie":
                st.subheader("🟠 Pie Chart")
                pie_chart = alt.Chart(trend_df).mark_arc().encode(
                    theta="Score",
                    color="Skill"
                ).properties(height=400)
                st.altair_chart(pie_chart, use_container_width=True)

            elif chart_type == "Radar":
                st.subheader("📡 Radar Chart")
                fig = go.Figure(data=go.Scatterpolar(
                    r=trend_df["Score"],
                    theta=trend_df["Skill"],
                    fill='toself',
                    marker=dict(color="royalblue")
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=False,
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show raw trend data"):
            st.write(trends_data)

except Exception as e:
    st.error("Failed to fetch real-time Google Trends data.")
    st.error(f"Error: {e}")
