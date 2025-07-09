import requests
API_KEY='eaf871ec167143d0919be19c93294442'
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={'eaf871ec167143d0919be19c93294442'}"
response = requests.get(url)

# Print the first article title
print(response.json()["articles"][0]["title"])
