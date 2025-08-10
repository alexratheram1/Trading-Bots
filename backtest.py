import os
import json
from datetime import datetime
from get_prices import get_btc_daily_prices
from sentiment_analysis import analyze_headlines

# Settings
threshold = 0.2
data_dir = "data"

# Step 1: Load real BTC prices
btc_prices = get_btc_daily_prices(days=10)
btc_price_dict = {date: price for date, price in btc_prices}

# Step 2: Load all headline files from the /data folder
headline_files = sorted(f for f in os.listdir(data_dir) if f.startswith("headlines_"))

positions = []
pnl = []

# Step 3: Backtest loop
for i in range(len(headline_files) - 1):  # skip last since we need next day price
    file_today = headline_files[i]
    file_next = headline_files[i + 1]

    date_today = file_today.split("_")[1].split(".")[0]
    date_next = file_next.split("_")[1].split(".")[0]

    # Load today's headlines
    with open(os.path.join(data_dir, file_today), "r", encoding="utf-8") as f:
        headlines = json.load(f)

    # Get prices
    price_today = btc_price_dict.get(date_today)
    price_next = btc_price_dict.get(date_next)

    if price_today is None or price_next is None:
        print(f"⚠️ Skipping {date_today} due to missing price data.")
        continue

    # Analyze sentiment
    sentiment_score = analyze_headlines(headlines)

    # Make decision
    if sentiment_score > threshold:
        decision = "LONG"
        profit = price_next - price_today
    elif sentiment_score < -threshold:
        decision = "SHORT"
        profit = price_today - price_next
    else:
        decision = "HOLD"
        profit = 0

    positions.append((date_today, decision, sentiment_score, profit))
    pnl.append(profit)

# Final day: no trade
final_day = headline_files[-1].split("_")[1].split(".")[0]
positions.append((final_day, "NO TRADE", 0, 0))

# Output results
print("\n📅 Backtest Results:")
for date, decision, score, profit in positions:
    print(f"{date} | {decision:<8} | Sentiment: {score:+.2f} | PnL: ${profit:.2f}")

print("\n💰 Total PnL:", round(sum(pnl), 2))