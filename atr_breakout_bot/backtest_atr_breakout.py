from atr_breakout_bot.fetch_ohlc import get_daily_ohlc
from atr_breakout_bot.indicators import atr, donchian
import os
import csv

def backtest(days=365, donch_window=20, atr_period=14, risk_per_trade=0.01, k_atr=2.0, fee_bps=5):
    rows = get_daily_ohlc("bitcoin", days=days)
    dates  = [r["date"] for r in rows]
    opens  = [r["open"] for r in rows]
    highs  = [r["high"] for r in rows]
    lows   = [r["low"] for r in rows]
    closes = [r["close"] for r in rows]

    # Indicators
    atr_vals = atr(highs, lows, closes, period=atr_period)
    up, lo   = donchian(highs, lows, window=donch_window)

    # Diagnostic
    valid = sum(
        1 for i in range(len(closes))
        if up[i] is not None and lo[i] is not None and atr_vals[i] is not None
    )
    print(f"Usable bars with indicators: {valid} / {len(closes)}")

    equity = 1.0
    pos = 0.0
    entry_price = None
    stop_price  = None
    fee = fee_bps / 10000.0

    daily_pnl = [0.0]
    equity_curve = [equity]
    trades = 0

    for i in range(1, len(closes)):
        # price-change PnL on existing position
        ret = (closes[i] - closes[i-1]) / closes[i-1]
        pnl_today = pos * ret

        # ATR stop logic
        if stop_price is not None:
            if pos > 0 and lows[i] < stop_price:
                slip_ret = (stop_price - closes[i-1]) / closes[i-1]
                pnl_today = pos * slip_ret
                pos = 0.0
                entry_price = None
                stop_price = None
                pnl_today -= 2 * fee
                trades += 1
            elif pos < 0 and highs[i] > stop_price:
                slip_ret = (closes[i-1] - stop_price) / closes[i-1]
                pnl_today = (-pos) * slip_ret
                pos = 0.0
                entry_price = None
                stop_price = None
                pnl_today -= 2 * fee
                trades += 1

        # require yesterday's bands and today's ATR
        if up[i-1] is None or lo[i-1] is None or atr_vals[i] is None:
            equity += pnl_today
            daily_pnl.append(pnl_today)
            equity_curve.append(equity)
            continue

        up_prev = up[i-1]
        lo_prev = lo[i-1]

        # Intraday breakout of yesterday’s band (classic Donchian)
        entry_long  = highs[i] > up_prev
        entry_short = lows[i]  < lo_prev

        if pos == 0.0 and (entry_long or entry_short):
            atr_usd = atr_vals[i]
            if atr_usd and atr_usd > 0:
                dollar_risk = equity * risk_per_trade
                size = dollar_risk / (atr_usd * k_atr)
                if entry_long:
                    pos = +size
                    entry_price = closes[i]
                    stop_price  = entry_price - k_atr * atr_usd
                else:
                    pos = -size
                    entry_price = closes[i]
                    stop_price  = entry_price + k_atr * atr_usd
                pnl_today -= 2 * fee
                trades += 1

        elif pos > 0 and entry_short:
            pnl_today -= 2 * fee
            dollar_risk = equity * risk_per_trade
            size = dollar_risk / (atr_vals[i] * k_atr) if atr_vals[i] else 0
            pos = -size
            entry_price = closes[i]
            stop_price  = entry_price + k_atr * atr_vals[i]
            trades += 1

        elif pos < 0 and entry_long:
            pnl_today -= 2 * fee
            dollar_risk = equity * risk_per_trade
            size = dollar_risk / (atr_vals[i] * k_atr) if atr_vals[i] else 0
            pos = +size
            entry_price = closes[i]
            stop_price  = entry_price - k_atr * atr_vals[i]
            trades += 1

        equity += pnl_today
        daily_pnl.append(pnl_today)
        equity_curve.append(equity)

    return {
        "dates": dates,
        "equity": equity_curve,
        "daily_pnl": daily_pnl,
        "trades": trades
    }

def save_results_csv(result, out_path="outputs/atr_breakout_results.csv"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    dates   = result["dates"]
    equity  = result["equity"]
    pnl     = result["daily_pnl"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "equity", "daily_pnl"])
        for d, e, p in zip(dates, equity, pnl):
            w.writerow([d, f"{e:.8f}", f"{p:.8f}"])
    print(f"Saved CSV to {out_path}")

def plot_equity(result, out_path="outputs/atr_breakout_equity.png"):
    import matplotlib.pyplot as plt

    dates  = result["dates"]
    equity = result["equity"]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, equity)
    plt.title("ATR Donchian Breakout – Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity (notional = 1.0 start)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved equity plot to {out_path}")

if __name__ == "__main__":
    res = backtest(days=365, donch_window=12, atr_period=9, risk_per_trade=0.01, k_atr=1.5, fee_bps=5)
    print("Trades:", res["trades"])
    print("Final equity:", round(res["equity"][-1], 4))

    save_results_csv(res, out_path="outputs/atr_breakout_results.csv")
    plot_equity(res, out_path="outputs/atr_breakout_equity.png")