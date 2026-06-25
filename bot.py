import requests

TOKEN = "8703847181:AAG7ZoIJ4XHpqniqm2wp16ZUCHJL7tIzctg"
CHAT_ID = "-1003953455562"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

r = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": "DIAGNOSTIC TEST MESSAGE"
})

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)
