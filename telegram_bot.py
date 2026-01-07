from telegram.ext import CommandHandler, Updater
from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from state import STATE

_bot = Bot(token=TELEGRAM_TOKEN)

def send_msg(text):
    try:
        _bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode="Markdown"
        )
    except Exception as e:
        print("Telegram error:", e)

def start(update, ctx):
    update.message.reply_text("🤖 AI Futures Bot Active")

def on(update, ctx):
    STATE.trading_enabled = True
    update.message.reply_text("✅ Trading ON")

def off(update, ctx):
    STATE.trading_enabled = False
    update.message.reply_text("⛔ Trading OFF")

def setpair(update, ctx):
    STATE.pair = ctx.args[0].upper()
    update.message.reply_text(f"🔁 Pair set to {STATE.pair}")

def settp(update, ctx):
    STATE.target_profit = float(ctx.args[0])
    update.message.reply_text(f"🎯 TP set ${STATE.target_profit}")

def run_bot():
    up = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = up.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("off", off))
    dp.add_handler(CommandHandler("pair", setpair))
    dp.add_handler(CommandHandler("tp", settp))
    up.start_polling()
