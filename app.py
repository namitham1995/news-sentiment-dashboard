import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:root@localhost:5432/new_db")

# Insert test data into the table
test_data = {
    "author": "BBC",
    "title": "Test news",
    "sentiment": 0.7,
    "timestamp": "2025-06-06 14:30:00"
}

# Insert as DataFrame
pd.DataFrame([test_data]).to_sql("news_analytics", engine, if_exists="append", index=False)
# Read data from table
df = pd.read_sql("SELECT * FROM news_analytics", engine)

# Display title and data
st.title("News Sentiment Dashboard")
st.dataframe(df)
