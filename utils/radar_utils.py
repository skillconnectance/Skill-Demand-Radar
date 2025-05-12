import pandas as pd

def load_skill_data(skills_path, occupation_path):
    skills_df = pd.read_excel(skills_path)
    occupations_df = pd.read_excel(occupation_path)
    return skills_df, occupations_df

def get_top_skills_by_importance(skills_df, threshold=3.5):
    # Filter for Importance scores (Scale ID = 'IM')
    top_skills = skills_df[skills_df["Scale ID"] == "IM"]
    
    # Filter based on threshold
    top_skills = top_skills[top_skills["Data Value"] >= threshold]
    
    return top_skills

def get_skill_counts(top_skills):
    return top_skills["Element Name"].value_counts().reset_index().rename(
        columns={"index": "Skill", "Element Name": "Count"}
    )
