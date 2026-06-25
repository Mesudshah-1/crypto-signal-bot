print("STARTED BOT")

import requests

print("IMPORT OK")

btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")

print("STATUS:", btc.status_code)
print("DATA:", btc.text)
