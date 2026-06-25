print("STEP 1 OK")

import requests

print("STEP 2 OK")

TOKEN = "8703847181:AAG7ZoIJ4XHpqniqm2wp16ZUCHJL7tIzctg"
CHAT_ID = "-1003953455562"

print("STEP 3 OK")

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()

print("BINANCE RESPONSE:", btc)

price = btc["price"]

print("PRICE:", price)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": f"TEST BTC: {price}"
})

print("TELEGRAM RESPONSE:", r.text)
