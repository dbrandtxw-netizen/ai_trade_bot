import pandas as pd
import ta

def analyze(df):
    df['ema9'] = ta.trend.ema_indicator(df['close'], 9)
    df['ema21'] = ta.trend.ema_indicator(df['close'], 21)
    df['rsi'] = ta.momentum.rsi(df['close'], 14)

    last = df.iloc[-1]

    if last.ema9 > last.ema21 and last.rsi < 70:
        return "LONG"
    if last.ema9 < last.ema21 and last.rsi > 30:
        return "SHORT"
    return None
