import streamlit as st
import pandas as pd

# Load your data (assume O*NET or your preprocessed skill trends)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data/skill_trends.xlsx")  # Or CSV if needed
    except:
        st.error("Failed to load skill data file.")
        return None
    return df

# Input: Desired skills from user (simulate for now)
desired_skills = st.text_input("Enter desired skills to learn (comma separated):", "Python, Communication")

# Clean and split
skill_list = [skill.strip().lower() for skill in desired_skills.split(",") if skill.strip()]

# Load data
df = load_data()
if df is not None:
    # Normalize skill column
    df["Skill_Lower"] = df["Skill"].str.lower()

    # Filter
    filtered_df = df[df["Skill_Lower"].isin(skill_list)]

    if filtered_df.empty:
        st.warning("No matching data found for the skills you entered.")
    else:
        st.success(f"Found {len(filtered_df)} relevant skill records.")
        st.dataframe(filtered_df[["Skill", "Industry", "TrendScore"]])

        # Optional bar chart
        st.bar_chart(filtered_df.set_index("Skill")["TrendScore"])
