import requests

print("BOT STARTED")

TOKEN = "8703847181:AAGrOqw8hWrQqmIIpe7JYYqZrz81QMGzbe0"
CHAT_ID = "-1003953455562"

print("STEP 1 OK")

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")

print("BINANCE STATUS:", btc.status_code)
print("BINANCE TEXT:", btc.text)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

r = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": "FINAL TEST"
})

print("TELEGRAM STATUS:", r.status_code)
print("TELEGRAM RESPONSE:", r.text)
