import pandas as pd

def load_skill_data(filepath="data/all_data_skill_and_non_skill.csv"):
    df = pd.read_csv(filepath)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def match_user_skills(user_skills, skill_df):
    user_skills = [skill.lower().strip() for skill in user_skills]
    matched = skill_df[skill_df['skill_name'].str.lower().isin(user_skills)]
    return matched
