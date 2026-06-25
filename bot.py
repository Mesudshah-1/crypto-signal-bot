import requests
import feedparser

# 🔐 SENİN BİLGİLERİN DİREKT GİRİLDİ
TOKEN = "8703847181:AAG7ZoIJ4XHpqniqm2wp16ZUCHJL7tIzctg"
GENERAL_CHANNEL = "-1003953455562"
VIP_CHANNEL = "-1003950012200"

def send(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    })

# 🔥 BTC FİYAT
btc = requests.get(
    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
).json()["price"]

# 📰 HABER
rss = feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/")

news = ""
if rss.entries:
    n = rss.entries[0]
    news = f"📰 <b>{n.title}</b>\n{n.link}"

# 📊 MESAJ
message = f"""
📊 <b>Kripto Mentoru</b>

💰 BTC: <b>{btc}</b>

{news}

#BTC #Crypto
"""

# 📤 GENEL KANALA GÖNDER
send(GENERAL_CHANNEL, message)
