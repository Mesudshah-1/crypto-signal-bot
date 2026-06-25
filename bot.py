import requests

TOKEN = "8703847181:AAGrOqw8hWrQqmIIpe7JYYqZrz81QMGzbe0"
CHAT_ID = "-1003953455562"

btc = requests.get(
    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
).json()["price"]

text = f"📊 BTC: {btc}"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

r = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": text
})

print(r.text)
