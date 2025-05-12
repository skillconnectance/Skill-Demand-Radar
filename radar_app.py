import streamlit as st
from utils.skill_utils import load_skill_data, match_user_skills

st.set_page_config(page_title="Skill Demand Radar", layout="centered")

st.title("📊 Skill Demand Radar")
st.write("Enter your desired skills to see their classification.")

# Step 1: Input
user_input = st.text_input("🔍 Enter skills to learn (comma-separated):", placeholder="e.g., Python, Communication, Excel")

# Step 2: Load dataset
skill_df = load_skill_data()

# Step 3: Show matching results
if user_input:
    user_skills = [skill.strip() for skill in user_input.split(",")]
    result_df = match_user_skills(user_skills, skill_df)

    if not result_df.empty:
        st.success(f"✅ Found {len(result_df)} matching skills.")
        st.dataframe(result_df)
    else:
        st.warning("❌ No matching skills found in dataset.")
