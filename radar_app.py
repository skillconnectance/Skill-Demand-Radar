import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("skill_demand_mock_data.csv")

st.title("📊 Skill Demand Radar - GCC Region")

# Sidebar filters
region = st.sidebar.multiselect("Filter by Region", options=df["Region"].unique(), default=df["Region"].unique())
industry = st.sidebar.multiselect("Filter by Industry", options=df["Industry"].unique(), default=df["Industry"].unique())

# Filter data
filtered_df = df[(df["Region"].isin(region)) & (df["Industry"].isin(industry))]

# Show table
st.subheader("Filtered Skills")
st.dataframe(filtered_df)

# Bar chart
fig = px.bar(filtered_df, x="Skill", y="DemandScore", color="Industry", title="Skill Demand by Score")
st.plotly_chart(fig)

import plotly.graph_objects as go

# Data for Radar chart (example)
skills = ["Data Science", "AI", "Cloud Computing", "Digital Marketing", "Cybersecurity"]
scores = [85, 90, 80, 70, 75]  # Demand scores

# Create Radar chart
fig = go.Figure(data=go.Scatterpolar(
    r=scores,
    theta=skills,
    fill='toself',
    name='Demand Scores'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]  # Score range
        )
    ),
    showlegend=False
)

# Show radar chart
st.plotly_chart(fig)

top_n = st.slider("Top N Skills", 1, len(skills), 5)

# Sort skills by score and show the top N
top_skills = sorted(zip(skills, scores), key=lambda x: x[1], reverse=True)[:top_n]
top_skills_df = pd.DataFrame(top_skills, columns=["Skill", "DemandScore"])

# Display top N skills
st.write("Top Skills by Demand Score:")
st.dataframe(top_skills_df)
