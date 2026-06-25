import os
import requests

print("BOT STARTED")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("GENERAL_CHANNEL_ID")

print("TOKEN OK:", bool(TOKEN))
print("CHAT ID:", CHAT_ID)

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
print("BINANCE OK:", btc)

message = f"BTC: {btc['price']}"

r = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("TELEGRAM RESPONSE:", r.text)
