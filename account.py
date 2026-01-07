from binance.client import Client
from telegram_bot import send_msg

class AccountChecker:
    def __init__(self, key, secret):
        self.client = Client(key, secret)

    def get_balance(self):
        acc = self.client.futures_account_balance()
        for a in acc:
            if a['asset'] == 'USDT':
                return float(a['balance'])
        return 0.0

    def get_position(self, symbol):
        positions = self.client.futures_position_information()

        for p in positions:
            if p['symbol'] == symbol:
                amt = float(p['positionAmt'])
                pnl = float(p['unRealizedProfit'])

                if amt == 0 and abs(pnl) > 0.01:
                    send_msg(
                        f"📌 *POSITION CLOSED*\n"
                        f"Pair: `{symbol}`\n"
                        f"PNL: `{pnl:.2f} USDT`"
                    )
                return amt, pnl

        return 0.0, 0.0
