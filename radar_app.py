import streamlit as st
import pandas as pd

@st.cache_data
def load_data_from_gdrive(file_id):
    url = f"https://drive.google.com/uc?id={1XicvrF83jmLw45emfjiRy1eBs7wxScIH}"
    return pd.read_csv(url, low_memory=False)

# Replace this with your actual file ID
file_id = "1XicvrF83jmLw45emfjiRy1eBs7wxScIH"

st.title("Load CSV from Google Drive")

try:
    df = load_data_from_gdrive(1XicvrF83jmLw45emfjiRy1eBs7wxScIH)
    st.success("Data loaded successfully!")
    st.dataframe(df.head(20))  # Show top 20 rows
except Exception as e:
    st.error(f"Failed to load data: {e}")
