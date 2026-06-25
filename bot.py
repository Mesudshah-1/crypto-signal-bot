import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["GENERAL_CHANNEL_ID"]

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"]

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": f"📊 BTC: {btc}"
    }
)
