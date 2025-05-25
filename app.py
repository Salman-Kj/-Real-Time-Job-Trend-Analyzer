import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('jobs.csv')

st.title("Real-Time Job Trend Analyzer")

# Sidebar filter input
keyword = st.sidebar.text_input("Enter job title keyword (e.g., Python, Analyst):", "")

# Filter based on keyword
if keyword.strip() == "":
    filtered_df = df.copy()
else:
    filtered_df = df[df['Title'].str.contains(keyword, case=False, na=False)]

# Show messages in sidebar
if keyword.strip() != "" and filtered_df.empty:
    st.sidebar.error(f"No jobs found with keyword: '{keyword}'")
elif keyword.strip() != "":
    st.sidebar.success(f"Showing results for '{keyword}'")

# If no jobs after filtering, show polite message on main page and skip charts and table
if filtered_df.empty:
    st.warning("😔 Sorry, no job listings match your search. Please try another keyword.")
else:
    # Charts & data when jobs found

    # Top 5 Job Titles
    top_titles = filtered_df['Title'].value_counts().head(5)
    st.subheader("Top 5 Most In-Demand Job Titles")
    st.bar_chart(top_titles)

    # Skills frequency chart
    if 'Skills' in filtered_df.columns:
        skills_series = filtered_df['Skills'].dropna().str.split(',').explode().str.strip()
        skills_count = skills_series.value_counts().head(10)
        st.subheader("Top 10 Most Frequent Skills Required")
        fig_skills = px.bar(
            x=skills_count.index,
            y=skills_count.values,
            labels={'x': 'Skills', 'y': 'Frequency'}
        )
        st.plotly_chart(fig_skills, use_container_width=True)
    else:
        st.info("Skills data not available.")

    # Job Posting Trends
    if 'Date Posted' in filtered_df.columns:
        filtered_df['Date Posted'] = pd.to_datetime(filtered_df['Date Posted'], errors='coerce')
        trend_df = filtered_df['Date Posted'].dt.date.value_counts().sort_index()
        st.subheader("Job Posting Trends Over Time")
        fig_trend = px.line(
            x=trend_df.index,
            y=trend_df.values,
            labels={'x': 'Date', 'y': 'Jobs Posted'}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Date Posted data not available.")

    # Show job listings with Title, Company, Location, Date Posted columns
    st.subheader("Filtered Job Listings")
    # Select columns, check if available
    columns_to_show = ['Title', 'Company', 'Location', 'Date Posted']
    existing_cols = [col for col in columns_to_show if col in filtered_df.columns]
    st.dataframe(filtered_df[existing_cols].reset_index(drop=True))
