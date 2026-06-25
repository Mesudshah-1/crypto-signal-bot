import os
import requests

TOKEN = os.environ["8703847181:AAGrOqw8hWrQqmIIpe7JYYqZrz81QMGzbe0"]
CHAT_ID = os.environ["-1003953455562"]

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"]

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": f"📊 BTC: {btc}"
    }
)
