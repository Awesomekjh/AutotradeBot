# strategy_zscore.py
import pandas as pd

def calculate_zscore(series1, series2, window=60):
    spread = pd.Series(series1) - pd.Series(series2)
    mean = spread.rolling(window=window).mean()
    std = spread.rolling(window=window).std()
    zscore = (spread - mean) / std
    return zscore

def zscore_signal(zscore_series, threshold=2.0):
    if len(zscore_series) < 1:
        return None
    latest = zscore_series.iloc[-1]
    if latest > threshold:
        return "SHORT"
    elif latest < -threshold:
        return "LONG"
    return None
