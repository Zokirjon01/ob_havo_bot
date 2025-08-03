# Telegram'ga webhook URL yuboruvchi fayl - Telegram API orqali webhook manzilini o‘rnatad
import requests

TOKEN = "8452355657:AAFinwieyCMPaZ17sdK0tzYqmjw2jYxp-Jw"
NGROK_URL = "https://c1f125430503.ngrok-free.app"
API_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"

webhook_url = f"{NGROK_URL}/webhook/{TOKEN}"
response = requests.get(API_URL, params={"url": webhook_url})
print(response.json())