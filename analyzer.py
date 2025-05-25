# analyzer.py
import pandas as pd
from collections import Counter

def analyze():
    df = pd.read_csv("jobs.csv")
    
    top_titles = df['Title'].value_counts().head(5)
    top_locations = df['Location'].value_counts().head(5)
    
    return {
        "top_titles": top_titles,
        "top_locations": top_locations,
        "total_jobs": len(df)
    }
