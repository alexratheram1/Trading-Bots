from typing import List, Tuple, Optional

def true_range(prev_close: float, high: float, low: float) -> float:  # 2
    a = high - low
    b = abs(high - prev_close)
    c = abs(low - prev_close)
    return max(a, b, c)

def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[Optional[float]]:
    n = len(closes)
    out: List[Optional[float]] = [None]*n
    if n == 0: return out
    trs = [None]*n
    trs[0] = highs[0] - lows[0]
    for i in range(1, n):
        trs[i] = true_range(closes[i-1], highs[i], lows[i])
    if n >= period:
        seed = sum(trs[1:period+1]) / period
        out[period] = seed
        for i in range(period+1, n):
            out[i] = (out[i-1]*(period-1) + trs[i]) / period
    return out

def donchian(highs: List[float], lows: List[float], window: int = 20) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    n = len(highs)
    up = [None]*n
    lo = [None]*n
    for i in range(n):
        if i+1 < window:
            continue
        window_high = max(highs[i+1-window:i+1])
        window_low  = min(lows[i+1-window:i+1])
        up[i] = window_high
        lo[i] = window_low
    return up, lo