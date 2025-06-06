import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'new_db'

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Fetch latest 10 entries from news_analytics table
query = "SELECT * FROM news_analytics ORDER BY timestamp DESC LIMIT 10"
df = pd.read_sql(query, engine)

st.title("Live News Sentiment Dashboard")
st.dataframe(df)
