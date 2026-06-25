import os
import requests
import pandas as pd
import feedparser
import html

# Token ve Chat ID tanımlamaları
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "-1003953455562"

def send_telegram_message(message):
    """Telegram kanalına/grubuna HTML formatında mesaj gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",  # Markdown yerine HTML yaptık, hata riskini sıfırladık
        "disable_web_page_preview": False
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
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data, columns=[
            'Open_time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close_time', 'Quote_asset_volume', 'Number_of_trades',
            'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'
        ])
        
        df['Close'] = df['Close'].astype(float)
        
        # --- İndikatör Hesaplamaları ---
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
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
                ema_status += " \n⚠️ <b>GOLDEN CROSS GERÇEKLEŞTİ!</b>"
        else:
            ema_status = "Ayı (EMA 50, EMA 200'ün altında) 🔴"
            if prev_row['EMA_50'] >= prev_row['EMA_200']:
                ema_status += " \n⚠️ <b>DEATH CROSS GERÇEKLEŞTİ!</b>"
                
        # MACD Durumu
        if last_row['MACD'] > last_row['Signal']:
            macd_status = "Pozitif (MACD Sinyali Yukarı Kesti) 🟢"
            if prev_row['MACD'] <= prev_row['Signal']:
                macd_status += " \n⚠️ <b>MACD AL VERDİ!</b>"
        else:
            macd_status = "Negatif (MACD Sinyali Aşağı Kesti) 🔴"
            if prev_row['MACD'] >= prev_row['Signal']:
                macd_status += " \n⚠️ <b>MACD SAT VERDİ!</b>"
                
        analysis_msg = (
            f"📊 <b>Günlük BTC/USDT Analiz Raporu</b>\n\n"
            f"💰 <b>Güncel Fiyat:</b> ${current_price:,.2f}\n\n"
            f"📈 <b>EMA 50/200 Trendi:</b> {ema_status}\n"
            f"📉 <b>MACD Durumu:</b> {macd_status}\n"
        )
        return analysis_msg
        
    except Exception as e:
        return f"❌ Binance verileri alınırken hata oluştu: {str(e)}"

def get_coindesk_news():
    """CoinDesk RSS Feed üzerinden en son haberi çeker ve HTML uyumlu yapar."""
    feed_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    try:
        feed = feedparser.parse(feed_url)
        if hasattr(feed, 'entries') and len(feed.entries) > 0:
            latest_story = feed.entries[0]
            # Karakter hatalarını önlemek için temizleme yapıyoruz
            title = html.escape(latest_story.title)
            link = latest_story.link
            return f"📰 <b>CoinDesk Son Dakika Haberi:</b>\n\n<a href='{link}'>{title}</a>"
        return "📰 Güncel CoinDesk haberi şu an alınamadı."
    except Exception as e:
        return f"⚠️ Haber havuzuna bağlanırken ufak bir kesinti oldu."

if __name__ == "__main__":
    btc_report = get_btc_analysis()
    crypto_news = get_coindesk_news()
    
    final_message = f"{btc_report}\n---------------------------\n\n{crypto_news}"
    send_telegram_message(final_message)
