import asyncio, time
import pandas as pd
from binance.client import Client
from ai_engine import AIDecisionEngine
from executor import Executor
from account import AccountChecker
from telegram_bot import run_bot, send_msg
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from state import STATE
import threading

client = Client()
ai = AIDecisionEngine()
execu = Executor(BINANCE_API_KEY, BINANCE_API_SECRET)
acct = AccountChecker(BINANCE_API_KEY, BINANCE_API_SECRET)

last_heartbeat = 0

async def loop():
    global last_heartbeat
    while True:
        # Heartbeat tiap 5 menit
        now = time.time()
        if now - last_heartbeat > 300:
            send_msg(
                f"🫀 *BOT AKTIF*\n"
                f"Pair: `{STATE.pair}`\n"
                f"TP: `${STATE.target_profit}`\n"
                f"Status: scanning market"
            )
            last_heartbeat = now

        if not STATE.trading_enabled:
            await asyncio.sleep(5)
            continue

        pos, _ = acct.get_position(STATE.pair)
        if pos != 0:
            await asyncio.sleep(5)
            continue

        kl = client.futures_klines(symbol=STATE.pair, interval="1m", limit=100)
        df = pd.DataFrame(kl, columns=['t','o','h','l','c','v','_','_','_','_','_','_'])
        df[['o','h','l','c','v']] = df[['o','h','l','c','v']].astype(float)
        df.rename(columns={'o':'open','h':'high','l':'low','c':'close','v':'volume'}, inplace=True)

        bal = acct.get_balance()
        decision = ai.evaluate(df, STATE.target_profit, bal)

        if decision:
            send_msg(
                f"🚀 *ENTRY*\n"
                f"Pair: `{STATE.pair}`\n"
                f"Side: *{decision['side']}*\n"
                f"Entry: `{decision['entry']:.4f}`\n"
                f"TP: `${STATE.target_profit}`"
            )
            execu.place_trade(STATE.pair, decision)

        await asyncio.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    asyncio.run(loop())
