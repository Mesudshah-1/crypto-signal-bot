import requests
import feedparser

TOKEN = "8703847181:AAG7ZoIJ4XHpqniqm2wp16ZUCHJL7tIzctg"
CHAT_ID = "-1003953455562"

def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })

# BTC fiyat
btc = requests.get(
    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
).json()["price"]

# haber
rss = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")

news = ""
if rss.entries:
    n = rss.entries[0]
    news = f"📰 <b>{n.title}</b>\n{n.link}"

msg = f"""
📊 <b>Kripto Mentoru</b>

💰 BTC: <b>{btc}</b>

{news}
"""

send(msg)
