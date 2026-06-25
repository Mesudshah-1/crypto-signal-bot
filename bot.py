print("BOT STARTED")

import requests

TOKEN = "8703847181:AAG7ZoIJ4XHpqniqm2wp16ZUCHJL7tIzctg"
CHAT_ID = "-1003953455562"

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"]

print("BTC:", btc)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": f"BTC PRICE: {btc}"
})

print("MESSAGE SENT")
