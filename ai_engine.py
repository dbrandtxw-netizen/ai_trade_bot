import ta

class AIDecisionEngine:
    def evaluate(self, df, target_usd, balance):
        close = df['close']
        high = df['high']
        low = df['low']

        ema9 = ta.trend.ema_indicator(close, 9)
        ema21 = ta.trend.ema_indicator(close, 21)
        rsi = ta.momentum.rsi(close, 14)
        atr = ta.volatility.average_true_range(high, low, close, 14)

        price = close.iloc[-1]

        # Hindari choppy
        if abs(ema9.iloc[-1] - ema21.iloc[-1]) / price < 0.0004:
            return None

        side = None
        if ema9.iloc[-1] > ema21.iloc[-1] and 50 < rsi.iloc[-1] < 65:
            side = "LONG"
        elif ema9.iloc[-1] < ema21.iloc[-1] and 35 < rsi.iloc[-1] < 50:
            side = "SHORT"
        else:
            return None

        leverage = 20
        margin = min(balance * 0.2, 10)  # AMAN utk saldo kecil
        notional = margin * leverage
        move_pct = target_usd / notional

        # Volatility cukup?
        if atr.iloc[-1] / price < move_pct * 1.2:
            return None

        return {
            "side": side,
            "entry": price,
            "tp_pct": move_pct,
            "sl_pct": move_pct / 2,
            "leverage": leverage,
            "margin": margin
        }
