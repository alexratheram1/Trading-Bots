import requests
from datetime import datetime

def get_btc_daily_prices(days=30):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = []
    for timestamp, price in data["prices"]:
        # Convert ms timestamp to readable date
        date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        prices.append((date, price))

    return prices

if __name__ == "__main__":
    btc_prices = get_btc_daily_prices()
    for date, price in btc_prices:
        print(f"{date} | ${round(price, 2)}")