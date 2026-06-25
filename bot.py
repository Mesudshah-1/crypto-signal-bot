import requests

TOKEN = "8703847181:AAGrOqw8hWrQqmIIpe7JYYqZrz81QMGzbe0"
CHAT_ID = "-1003953455562"

btc = float(
    requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()["price"]
)

# basit trend yorumu
trend = "📈 LONG bias" if btc % 2 == 0 else "📉 SHORT bias"

text = f"""
📊 KRİPTO MENTOR BOT

💰 BTC: {btc}

📊 Trend: {trend}
"""

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": text
    }
)
