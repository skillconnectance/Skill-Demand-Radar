import streamlit as st
import pandas as pd

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/linkedin_skills.csv')
    df['skills'] = df['skills'].fillna('').str.lower()
    return df

df = load_data()

# Title
st.title("🧠 Skill Demand Radar (Real World)")

# Input Skills
user_input = st.text_input("Enter desired skills (comma-separated):", "Python, Excel")
input_skills = [skill.strip().lower() for skill in user_input.split(',') if skill.strip()]

# Match and Count
matched_rows = df[df['skills'].apply(lambda x: any(skill in x for skill in input_skills))]

# Skill Frequencies
skill_counts = {}
for skills in matched_rows['skills']:
    for skill in skills.split(','):
        skill = skill.strip()
        if skill:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

# Display
st.subheader("🔍 Skill Demand (based on job listings)")
st.write(f"Total job listings matched: {len(matched_rows)}")

if skill_counts:
    sorted_skills = dict(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True))
    st.bar_chart(pd.Series(sorted_skills))
else:
    st.warning("No matches found. Try with more common skill names.")
