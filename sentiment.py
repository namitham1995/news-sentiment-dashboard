from textblob import TextBlob
text="The new AI tool is Amazing!"
print(TextBlob(text).sentiment.polarity)