import os
import requests
import feedparser

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GENERAL = os.environ["-1003953455562"]
VIP = os.environ["-1003950012200"]

# ---------------- TELEGRAM ----------------
def send(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    })

# ---------------- BTC PRICE ----------------
price = requests.get(
    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
).json()

btc_price = float(price["price"])

# ---------------- NEWS ----------------
rss = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")

news = ""
if rss.entries:
    n = rss.entries[0]
    news = f"📰 <b>{n.title}</b>\n{n.link}"

# ---------------- MESSAGE ----------------
msg = f"""
📊 <b>Kripto Mentoru Günlük Analiz</b>

💰 BTC: <b>{btc_price}</b>

📌 Trend: EMA + MACD sistemi yakında aktif olacak

{news}

#Bitcoin #Crypto
"""

# ---------------- SEND TO GENERAL ----------------
send(GENERAL, msg)
