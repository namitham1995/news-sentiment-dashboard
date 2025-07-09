import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page Config

st.set_page_config(
    page_title="News analytics sentiment score dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Connect to RDS

engine = create_engine("postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres")
df = pd.read_sql("SELECT * FROM news_analytics ORDER BY timestamp DESC", engine)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sidebar - Explanation

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



# Highlight Sentiment

def highlight_row(row):
    sentiment = row['sentiment_score']
    if sentiment > 0.2:
        return ['background-color: green; color: white'] * len(row)
    elif sentiment < -0.2:
        return ['background-color: red; color: white'] * len(row)
    else:
        return ['background-color: gray; color: white'] * len(row)

# Main Content 

if view_option == "View News":
    st.markdown("## 📰 News analytics sentiment score dashboard")

    # 📅 Filter by Date
    date_filter = st.date_input("📅 Select date to filter:")
    if date_filter:
        filtered_df = df[df['timestamp'].dt.date == date_filter]
    else:
        filtered_df = df

    # 🧾 Display Table
    if not filtered_df.empty:
        styled_df = filtered_df.style.apply(highlight_row, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.warning("No news articles found for the selected date.")

    # 📈 Sentiment Summary
    st.markdown("### 📈 Sentiment Summary")
    if 'sentiment_score' in filtered_df.columns:
        st.metric("Average Sentiment Score", round(filtered_df['sentiment_score'].mean(), 2))
    else:
        st.write("No sentiment score data available.")

    # 📊 Plotly Sentiment Trend
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

    # ⏱️ Most Recent Entry
    st.markdown("### 🕒 Most Recent Entry Timestamp")
    st.code(df['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S"))

elif view_option == "Analytics":
    st.markdown("## 📊 Sentiment Analytics Dashboard")

    # 🟢 Sentiment Classification
    def classify_sentiment(score):
        if score > 0.2:
            return 'Positive'
        elif score < -0.2:
            return 'Negative'
        else:
            return 'Neutral'

    df['sentiment_label'] = df['sentiment_score'].apply(classify_sentiment)

    # 📊 Sentiment Distribution Bar Chart
    st.markdown("### 🔍 Sentiment Distribution")
    sentiment_counts = df['sentiment_label'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment',
                     color_discrete_map={'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'})
    st.plotly_chart(fig_bar, use_container_width=True)

    # 📅 Daily Sentiment Trend
    st.markdown("### 📈 Daily Average Sentiment Trend")
    daily_avg = df.groupby(df['timestamp'].dt.date)['sentiment_score'].mean().reset_index()
    daily_avg.columns = ['Date', 'Average Sentiment']
    fig_line = px.line(daily_avg, x='Date', y='Average Sentiment', markers=True, title="Avg Sentiment per Day")
    fig_line.update_layout(template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)
    # ☁️ Word Cloud from Descriptions
    st.markdown("### ☁️ Word Cloud of News Descriptions")
    text = " ".join(df['description'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=250, height=60, background_color='white').generate(text)

    fig_wc, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_wc)
