from binance.client import Client

class Executor:
    def __init__(self, key, secret):
        self.client = Client(key, secret)

    def place_trade(self, symbol, d):
        qty = round((d['margin'] * d['leverage']) / d['entry'], 2)

        self.client.futures_change_leverage(
            symbol=symbol,
            leverage=d['leverage']
        )

        side = Client.SIDE_BUY if d['side'] == "LONG" else Client.SIDE_SELL
        close_side = Client.SIDE_SELL if d['side'] == "LONG" else Client.SIDE_BUY

        # ENTRY
        self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=qty
        )

        # TP & SL
        tp_price = d['entry'] * (1 + d['tp_pct'] if d['side']=="LONG" else 1 - d['tp_pct'])
        sl_price = d['entry'] * (1 - d['sl_pct'] if d['side']=="LONG" else 1 + d['sl_pct'])

        self.client.futures_create_order(
            symbol=symbol,
            side=close_side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=round(tp_price, 3),
            closePosition=True
        )

        self.client.futures_create_order(
            symbol=symbol,
            side=close_side,
            type="STOP_MARKET",
            stopPrice=round(sl_price, 3),
            closePosition=True
        )
