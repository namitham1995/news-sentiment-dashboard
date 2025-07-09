import requests
from textblob import TextBlob
import pandas as pd
from sqlalchemy import create_engine
import boto3
from datetime import datetime
import json

API_KEY = "eaf871ec167143d0919be19c93294442"  
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
bucket_name = "newsapi-raw-data"
#  Connect to PostgreSQL
# engine = create_engine("postgresql://postgres:root@localhost:5432/postgres")
# rds connection
engine = create_engine("postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres")

#   Fetch news
response = requests.get(url)

if response.status_code == 200:
    news_json = response.json()
    # ✅ Upload raw JSON to S3
    s3 = boto3.client("s3")
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    s3_key = f"news_raw_{timestamp}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=json.dumps(news_json),
        ContentType="application/json"
    )
    print(f"✅ Raw data uploaded to S3 bucket '{bucket_name}' as '{s3_key}'")

    articles = response.json().get("articles", [])
    data = []

    for article in articles:
        title = article.get("title", "")
        author = article.get("author", "Unknown")
        sentiment = TextBlob(title).sentiment.polarity

        data.append({
            "author": author,
            "description": title,
            "sentiment_score": sentiment,
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to PostgreSQL
    df.to_sql("news_analytics", engine, if_exists="append", index=False)

    print(" News saved to PostgreSQL!")
    print(df.head())

else:
    print("❌ Failed to fetch news:", response.status_code, response.text)
