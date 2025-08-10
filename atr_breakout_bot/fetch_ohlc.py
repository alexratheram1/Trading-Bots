
import requests
from datetime import datetime, UTC
def get_daily_ohlc(coin_id: str, days: int = 365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    out = []
    for ts_ms, o, h, l, c in data:
        date = datetime.fromtimestamp(ts_ms/1000, UTC).strftime("%Y-%m-%d")
        out.append({"date": date, "open": float(o), "high": float(h),
                    "low": float(l), "close": float(c)})
    return out

if __name__ == "__main__":
    rows = get_daily_ohlc("ethereum", days=180)
    print(rows[:3])