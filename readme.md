# NEWS SENTIMENT ANALYSIS DASHBOAR

This is a full-stack, production-ready dashboard that automatically fetches news headlines, analyzes sentiment using NLP, and displays real-time insights through an interactive Streamlit web interface — all containerized and deployed on AWS.

## 🎯 Project Features

- Fetches live news using NewsAPI   
- Analyzes sentiment (positive / neutral / negative)  
- Stores processed data in AWS RDS (PostgreSQL)    
- Visualizes insights via Streamlit dashboard (ECS-hosted)      
- Uses Docker + ECS + Lambda + EventBridge for automation    
 

## 🧱 Architecture Overview

NewsAPI → Lambda → ECS Task → sentiment.py → PostgreSQL (RDS)
                            ↘ Dockerized → S3 (optional)
Dashboard: ECS (Streamlit) ← ALB ← app.py ← PostgreSQL

 ![alt text](images/image-3.png)

## 🧠 Technologies Used

• Frontend: Streamlit, Plotly  
• Backend: Python, TextBlob  
• Database: PostgreSQL (RDS)  
• Cloud Infra: Docker, ECS Fargate, Lambda, EventBridge, CloudWatch, IAM, S3, VPC  

## 🛠️ Step-by-Step Implementation Guide  

### 1. Local Prototype
    Tools Installation:
    • Python 3.9+
    • Docker Desktop (with WSL2 on Windows)
    • Required Python packages:
    pip install pandas textblob streamlit sqlalchemy psycopg2-binary requests   plotly

### 2. Files Created & Purpose
   
####  `news_fetcher.py`

This script fetches top news headlines from NewsAPI, analyzes sentiment using TextBlob, uploads raw data to S3, and stores the processed results into a PostgreSQL (RDS) table for dashboard visualization.
It automates the full data pipeline for news sentiment analysis and storage..  

```python
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
engine = create_engine("postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres")
response = requests.get(url)
if response.status_code == 200:
    news_json = response.json()
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
    df = pd.DataFrame(data)
    df.to_sql("news_analytics", engine, if_exists="append", index=False)
    print(" News saved to PostgreSQL!")
    print(df.head())
else:
    print("❌ Failed to fetch news:", response.status_code, response.text)
  ```

#### `app.py`

This Streamlit app connects to an AWS RDS PostgreSQL database to display news sentiment data in interactive views.  
It allows users to filter news by date, view sentiment trends, and explore analytics like sentiment distribution and word clouds.  

```python
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.set_page_config(
    page_title="News analytics sentiment score dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
engine = create_engine("postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres")
df = pd.read_sql("SELECT * FROM news_analytics ORDER BY timestamp DESC", engine)
df['timestamp'] = pd.to_datetime(df['timestamp'])
with st.sidebar:
    view_option = st.radio("🔎 Select View", ["View News", "Analytics"], index=0)

    if view_option == "Analytics":
        st.markdown("### Explanation")
        st.write("""
        Sentiment score indicates a **positive sentiment** when the score is positive and conversely, when the score is negative, the sentiment is also **negative**.

        _Consider that scores above 0.2 or under -0.2 are a small part and can therefore be seen as very positive or very negative._
        """)
        st.markdown(f"**Last update date :** `{df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')}`")
        st.write("Adjust starting date or ending date to refresh data")
def highlight_row(row):
    sentiment = row['sentiment_score']
    if sentiment > 0.2:
        return ['background-color: green; color: white'] * len(row)
    elif sentiment < -0.2:
        return ['background-color: red; color: white'] * len(row)
    else:
        return ['background-color: gray; color: white'] * len(row)
if view_option == "View News":
    st.markdown("## 📰 News analytics sentiment score dashboard")
    date_filter = st.date_input("📅 Select date to filter:")
    if date_filter:
        filtered_df = df[df['timestamp'].dt.date == date_filter]
    else:
        filtered_df = df
    if not filtered_df.empty:
        styled_df = filtered_df.style.apply(highlight_row, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.warning("No news articles found for the selected date.")
    st.markdown("### 📈 Sentiment Summary")
    if 'sentiment_score' in filtered_df.columns:
        st.metric("Average Sentiment Score", round(filtered_df['sentiment_score'].mean(), 2))
    else:
        st.write("No sentiment score data available.")
    if not filtered_df.empty:
        st.markdown("### 📊 Sentiment Trend Over Time")
        fig = px.line(
            filtered_df.sort_values("timestamp"),
            x="timestamp",
            y="sentiment_score",
            title="Sentiment Score Over Time",
            labels={"timestamp": "Timestamp", "sentiment_score": "Sentiment Score"},
            markers=True
        )
        fig.update_layout(
            xaxis_title="Timestamp",
            yaxis_title="Sentiment Score",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("### 🕒 Most Recent Entry Timestamp")
    st.code(df['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S"))

elif view_option == "Analytics":
    st.markdown("## 📊 Sentiment Analytics Dashboard")
    def classify_sentiment(score):
        if score > 0.2:
            return 'Positive'
        elif score < -0.2:
            return 'Negative'
        else:
            return 'Neutral'

    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)
    st.markdown("### 🔍 Sentiment Distribution")
    sentiment_counts = df['sentiment_label'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment',
                     color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'})
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("### 📈 Daily Average Sentiment Trend")
    daily_avg = df.groupby(df['timestamp'].dt.date)['sentiment_score'].mean().reset_index()
    daily_avg.columns = ['Date', 'Average Sentiment']
    fig_line = px.line(daily_avg, x='Date', y='Average Sentiment', markers=True, title="Avg Sentiment per Day")
    fig_line.update_layout(template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("### ☁️ Word Cloud of News Descriptions")
    text = " ".join(df['description'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=250, height=60,  background_color='white').generate(text)
    fig_wc, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_wc)
```


#### `Dockerfile .`  

Containerizes news fetcher.  

```python
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
```

#### `fetcher.Dockerfile`  
```python
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "news_fetcher.py"]
```

#### `backup.sql`

 Used for backing up your RDS PostgreSQL schema.  

#### `sentiment.py`

This line computes the sentiment polarity score of the text using TextBlob, indicating how positive or negative it is.    
```python
from textblob import TextBlob
text="The new AI tool is Amazing!"
print(TextBlob(text).sentiment.polarity)
```

#### `test_rds_connecton.py`

This code tests the connection to an AWS RDS PostgreSQL database and prints the database version to confirm successful connectivity.    
```python
from sqlalchemy import create_engine,text
aws_engine = create_engine(
    "postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres"
)
with aws_engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
```

### 3. Docker & Local Database Setup

Run local PostgreSQL:

docker run --name news-db -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres

Create table:

CREATE TABLE news_analytics (
    Id SERIAL PRIMARY KEY,
    author VARCHAR(50),
    description VARCHAR(700),
    sentiment_score DOUBLE PRECISION,
    timestamp VARCHAR(20)
);

Build and test the dashboard:
docker build -f Dockerfile.dashboard -t news-dashboard .
docker run -p 8501:8501 news-dashboard
Access in browser: http://localhost:8501

## 🚀 AWS Deployment

   ECR
•	aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <ecr-uri>
•	docker build -f fetcher.dockerfile -t news-fetcher .
•	docker tag news-fetcher:latest <ecr-uri>/news-fetcher:latest
•	docker push <ecr-uri>/news-fetcher:latest
![alt text](image-4.png)
 
   RDS
•	Create PostgreSQL RDS instance
•	Open port 5432 in security group
•	Create table: news_analytics
![alt text](image-5.png)
 
 #### S3

•	Create an S3 bucket (e.g., news-raw-data)
•	news_fetcher.py uploads raw API responses as .json
•	Used for logging or backup
![alt text](image-6.png)
![alt text](image-7.png)
 
#### Lambda & EventBridge  

•	Use Lambda to trigger ECS Task for fetcher script
•	EventBridge triggers Lambda every 5 minutes
![alt text](image-8.png)
 
#### ECS

•	One Task for dashboard (always running)
•	Another Task triggered by Lambda (news_fetcher.py)
•	ALB routes traffic to dashboard
![alt text](image-10.png)

#### CloudWatch  

•	Automatically captures logs from:
o	Lambda functions
o	ECS fetcher and dashboard containers
o	EventBridge triggers
•	Used for debugging errors and monitoring task health
![alt text](image-9.png)
Log Group	Purpose
/aws/lambda/newsSentimentFetcher	Logs from  Lambda function that triggers ECS
/ecs/news-task	Logs from ECS Task running news_fetcher.py
	

## 📊 Dashboard Features 

• Filter news by date   
• Color-coded sentiment table    
• Line chart: Sentiment over time  
• Word cloud of common words  
• Bar chart: Sentiment category distribution  

📁 Project Structure
intern1/
├── app.py
├── news_fetcher.py
├── sentiment.py
├── Dockerfile.dashboard
├── fetcher.dockerfile
├── requirements.txt
├── backup.sql
└── README.docx
📸 Screenshots
▶️ Sentiment Distribution
 ![alt text](image-11.png)
☁️ Word Cloud and Sentiment Line Chart
 ![alt text](image-2.png)
🗞️ News Sentiment Table View
 ![alt text](image-1.png)
📈 Trend & Timestamp Summary
![alt text](image.png)


## ✅ Next Improvements  

• Add more visual analytics (trends, keywords)  
• Auto backup data to S3  
• Export as CSV  
• Use CloudFormation / Terraform for infrastructure setup  

## 🏁 Conclusion   

This project demonstrates:  
• Automated News Collection    
• Real-Time Sentiment Analysis  
• Interactive Analytics  
• Cloud-native & Scalable Deployment  

