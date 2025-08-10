import os
import json
import requests
from datetime import datetime, timedelta, UTC

start_date = datetime(2025, 8, 1, tzinfo=UTC)
end_date = datetime.now(UTC)

API_KEY = "0530b3cedaec40d2bdd6b0706e343603"  # ← Replace with your real API key
data_dir = "data"
query = "bitcoin OR ethereum OR blockchain"

def get_news_for_day(api_key, date_str):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": date_str,
        "to": date_str,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey": api_key,
        "pageSize": 100
    }
    response = requests.get(url, params=params)
    return response.json()

# Date range
start_date = datetime(2025, 8, 1, tzinfo=UTC)
end_date = datetime.now(UTC)

# Loop through each day
current = start_date
while current <= end_date:
    date_str = current.strftime('%Y-%m-%d')
    filename = f"{data_dir}/headlines_{date_str}.json"

    if os.path.exists(filename):
        print(f"🟡 Skipping {date_str} (already exists)")
    else:
        print(f"📅 Fetching news for {date_str}...")
        data = get_news_for_day(API_KEY, date_str)
        if "articles" in data:
            headlines = [article["title"] for article in data["articles"]]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(headlines, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(headlines)} headlines to {filename}")
        else:
            print(f"⚠️ No articles found or API error on {date_str}")

    current += timedelta(days=1)