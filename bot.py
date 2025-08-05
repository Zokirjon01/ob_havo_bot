# Flask server (webhook listener) - Flask ilova – Telegram dan kelgan so‘rovlarni eshitadi
from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from ob_havo_pro import DISTRICTS, get_weather_text, make_district_keyboard, save_user, init_db

load_dotenv()
app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        username = msg["from"].get("username", "")
        first_name = msg["from"].get("first_name", "")

        save_user(chat_id, username, first_name)

        if text == "/start":
            send_message(chat_id, "🌍 Farg‘ona viloyati tumanini tanlang:", make_district_keyboard())
        else:
            send_message(chat_id, "Iltimos, /start buyrug‘ini yuboring.")

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        district = query["data"]

        if district in DISTRICTS:
            lat, lon = DISTRICTS[district]
            weather = get_weather_text(lat, lon)
            send_message(chat_id, f"📍 <b>{district}</b>\n\n{weather}")
        else:
            send_message(chat_id, "❌ Noto‘g‘ri tuman tanlandi.")

    return {"ok": True}

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=payload)

@app.route("/")
def home():
    return "✅ Bot ishga tushdi!"

if __name__ == "__main__":
    from ob_havo_pro import init_db
    init_db()
    app.run(host="0.0.0.0", port=5000)
