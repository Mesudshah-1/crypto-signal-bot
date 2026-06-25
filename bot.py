import os
import requests
import pandas as pd
import feedparser

# Token güvenliğiniz için GitHub Secrets'tan alınır
TELEGRAM_TOKEN = os.getenv("8703847181:AAGrOqw8hWrQqmIIpe7JYYqZrz81QMGzbe0")
# Chat ID'niz doğrudan koda entegre edilmiştir
TELEGRAM_CHAT_ID = "-1003953455562"

def send_telegram_message(message):
    """Telegram kanalına/grubuna mesaj gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram mesajı başarıyla gönderildi.")
        else:
            print(f"Telegram hatası: {response.text}")
    except Exception as e:
        print(f"Mesaj gönderilirken hata oluştu: {e}")

def get_btc_analysis():
    """Binance API kullanarak BTC verilerini çeker ve teknik analiz yapar."""
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "4h", 
        "limit": 300      
    }
    
    try:
        response = requests.get(url, params=params).json()
        df = pd.DataFrame(response, columns=[
            'Open_time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close_time', 'Quote_asset_volume', 'Number_of_trades',
            'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'
        ])
        
        df['Close'] = df['Close'].astype(float)
        
        # --- İndikatör Hesaplamaları ---
        # EMA 50 ve 200
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        # MACD (12, 26, 9)
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['Close']
        
        # EMA Durumu
        if last_row['EMA_50'] > last_row['EMA_200']:
            ema_status = "Boğa (EMA 50, EMA 200'ün üzerinde) 🟢"
            if prev_row['EMA_50'] <= prev_row['EMA_200']:
                ema_status += " \n⚠️ **GOLDEN CROSS GERÇEKLEŞTİ!**"
        else:
            ema_status = "Ayı (EMA 50, EMA 200'ün altında) 🔴"
            if prev_row['EMA_50'] >= prev_row['EMA_200']:
                ema_status += " \n⚠️ **DEATH CROSS GERÇEKLEŞTİ!**"
                
        # MACD Durumu
        if last_row['MACD'] > last_row['Signal']:
            macd_status = "Pozitif (MACD Sinyali Yukarı Kesti) 🟢"
            if prev_row['MACD'] <= prev_row['Signal']:
                macd_status += " \n⚠️ **MACD AL VERDİ!**"
        else:
            macd_status = "Negatif (MACD Sinyali Aşağı Kesti) 🔴"
            if prev_row['MACD'] >= prev_row['Signal']:
                macd_status += " \n⚠️ **MACD SAT VERDİ!**"
                
        analysis_msg = (
            f"📊 **Günlük BTC/USDT Analiz Raporu**\n\n"
            f"💰 **Güncel Fiyat:** ${current_price:,.2f}\n\n"
            f"📈 **EMA 50/200 Trendi:** {ema_status}\n"
            f"📉 **MACD Durumu:** {macd_status}\n"
        )
        return analysis_msg
        
    except Exception as e:
        print(f"Binance veri hatası: {e}")
        return "❌ Binance verileri alınırken bir hata oluştu."

def get_coindesk_news():
    """CoinDesk RSS Feed üzerinden en son haberi çeker."""
    feed_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            latest_story = feed.entries[0]
            title = latest_story.title
            link = latest_story.link
            news_msg = f"📰 **CoinDesk Son Dakika Haberi:**\n\n[{title}]({link})"
            return news_msg
        return "📰 Güncel haber bulunamadı."
    except Exception as e:
        print(f"Haber çekme hatası: {e}")
        return "❌ Haberler çekilirken bir hata oluştu."

if __name__ == "__main__":
    btc_report = get_btc_analysis()
    crypto_news = get_coindesk_news()
    
    final_message = f"{btc_report}\n---------------------------\n\n{crypto_news}"
    send_telegram_message(final_message)
