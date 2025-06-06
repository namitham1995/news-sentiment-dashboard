
from textblob import TextBlob
import pandas as pd
import requests
from sqlalchemy import create_engine

API_KEY = 'eaf871ec167143d0919be19c93294442'
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

response = requests.get(url)
articles = response.json()["articles"]
data = []
for article in articles:
    sentiment = TextBlob(article["title"]).sentiment.polarity
    data.append({
        "author": article["author"],
        "title": article["title"],
        "sentiment": sentiment
        })
df = pd.DataFrame(data)
print(df.head())

engine = create_engine("postgresql://postgres:root@localhost:5432/new_db")
df.to_sql('news_analytics', engine, if_exists='append', index=False)
print('Data saved to SQL successfully.')
