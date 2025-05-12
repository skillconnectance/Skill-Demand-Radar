import pandas as pd

import pandas as pd

def load_skill_data():
    df = pd.read_csv("data/all_data_skill_and_nonskills.csv")
    df.rename(columns={"Text": "skill_name", "Label": "is_skill"}, inplace=True)
    df = df[df["is_skill"] == 1]  # keep only skill-labeled rows
    return df

def match_user_skills(user_skills, skill_df):
    user_skills = [skill.lower().strip() for skill in user_skills]
    matched = skill_df[skill_df['skill_name'].str.lower().isin(user_skills)]
    return matched
