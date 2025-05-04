import streamlit as st
import time
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px
import random

# Function to fetch trends with retry logic
def fetch_trends(skills, retries=5):
    pytrends = TrendReq(hl="en-US", tz=4)
    
    for attempt in range(retries):
        try:
            pytrends.build_payload(skills, geo='AE', timeframe='now 7-d')
            time.sleep(5 + random.uniform(1, 3))  # Sleep to avoid hitting rate limit
            
            # Fetch trend data
            trends_data = pytrends.interest_over_time()

            if trends_data.empty:
                st.error("No trend data returned.")
            else:
                return trends_data
        except Exception as e:
            if attempt == retries - 1:
                st.error(f"Failed after {retries} attempts. Error: {e}")
                return None
            else:
                st.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(10 * (2 ** attempt))  # Exponential backoff

# List of skills (already provided by you)
skills = [
    "Python", "Java", "Cloud Computing", "Cybersecurity", "Data Analysis", 
    "SEO", "Digital Marketing", "Machine Learning", "AI", "Project Management",
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management",
    "Emotional Intelligence", "Adaptability", "Negotiation", "CRM Software", "Sales Strategy",
    "Graphic Design", "UX/UI Design", "SEO", "SEM", "Content Marketing", "Branding"
]

# Fetch the trends data
trends_data = fetch_trends(skills)

# Display the trend data as a chart
if trends_data is not None:
    st.subheader('Google Trends Data')
    st.write(trends_data)

    # Plot the trends as a line chart
    st.write("Trends Over Time")
    st.line_chart(trends_data)

    # Optionally, you can show the trends as a bar chart
    st.write("Bar Chart for Trends")
    trends_data_mean = trends_data.mean()
    bar_chart = trends_data_mean.sort_values(ascending=False).head(10)
    st.bar_chart(bar_chart)

    # Plot as a pie chart
    st.write("Pie Chart for Top Skills")
    pie_chart = px.pie(names=bar_chart.index, values=bar_chart.values, title="Top Skills")
    st.plotly_chart(pie_chart)
