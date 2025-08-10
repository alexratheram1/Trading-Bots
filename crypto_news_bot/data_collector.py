import requests
from datetime import datetime, UTC, timedelta

# STEP 1: Paste your NewsAPI key here
api_key = "0530b3cedaec40d2bdd6b0706e343603"

# STEP 2: Define a function to get today's crypto news
def get_crypto_news(api_key):
    # Get today's date in YYYY-MM-DD format
    from_date = (datetime.now(UTC) - timedelta(days=3)).strftime('%Y-%m-%d')
    
    # Build the URL to send to the API
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=bitcoin OR ethereum OR blockchain&from={from_date}&sortBy=publishedAt&language=en&apiKey={api_key}"
    )
    
    # Send the request to the NewsAPI server
    response = requests.get(url)
    
    # If it worked (status code 200), return the JSON
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get news:", response.status_code)
        return None

# STEP 3: Actually run it and print the headlines
import json
from datetime import datetime

if __name__ == "__main__":
    news_data = get_crypto_news(api_key)

    if news_data:
        today = datetime.now(UTC).strftime('%Y-%m-%d')
        headlines = [article['title'] for article in news_data['articles']]

        # Save to a daily file
        with open(f"data/headlines_{today}.json", "w", encoding="utf-8") as f:
            json.dump(headlines, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(headlines)} headlines to data/headlines_{today}.json")
    else:
        print("❌ No news data available.")
            