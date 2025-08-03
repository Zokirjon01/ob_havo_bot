# Telegram'ga webhook URL yuboruvchi fayl - Telegram API orqali webhook manzilini o‘rnatad
import requests
import os

TOKEN = os.getenv("8452355657:AAFinwieyCMPaZ17sdK0tzYqmjw2jYxp-Jw")
NGROK_URL = "https://7cfe8e8bc85c.ngrok-free.app"  # NGROK ni to‘liq HTTPS linki
WEBHOOK_URL = f"{NGROK_URL}/webhook/{TOKEN}"

response = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    params={"url": WEBHOOK_URL}
)

print(response.json())
