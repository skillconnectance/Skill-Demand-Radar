import streamlit as st
import pandas as pd
from utils.radar_utils import load_skill_data, get_top_skills_by_importance, get_skill_counts

st.set_page_config(page_title="Skill Demand Radar", layout="wide")

st.title("📊 Skill Demand Radar (Static Analysis)")
st.write("Shows most important skills across occupations based on O*NET data.")

# Load data
skills_path = "data/Skills.xlsx"
occupation_path = "data/Occupation Data.xlsx"

try:
    skills_df, occupation_df = load_skill_data(skills_path, occupation_path)

    # Filter high-importance skills
    top_skills = get_top_skills_by_importance(skills_df)
    skill_counts = get_skill_counts(top_skills)

    st.subheader("🔥 Top In-Demand Skills (by importance score ≥ 3.5)")
    st.dataframe(skill_counts.head(20))

    st.bar_chart(skill_counts.head(10).set_index("Skill"))

except FileNotFoundError:
    st.error("Make sure 'Skills.xlsx' and 'Occupation Data.xlsx' are inside the 'data' folder.")

