from binance.client import Client
import config

client = Client(
    config.BINANCE_API_KEY,
    config.BINANCE_API_SECRET
)

def futures_balance():
    data = client.futures_account_balance()
    for a in data:
        if a['asset'] == 'USDT':
            return float(a['availableBalance'])
    return 0

def all_usdt_pairs():
    info = client.futures_exchange_info()
    return [
        s['symbol'] for s in info['symbols']
        if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING'
    ]
