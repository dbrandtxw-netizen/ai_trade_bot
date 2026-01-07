from binance_client import client
import config

def set_leverage(symbol, lev):
    client.futures_change_leverage(symbol=symbol, leverage=lev)

def open_trade(symbol, side, qty):
    return client.futures_create_order(
        symbol=symbol,
        side="BUY" if side=="LONG" else "SELL",
        type="MARKET",
        quantity=qty
    )
