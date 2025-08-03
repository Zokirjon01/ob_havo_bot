# Flask server (webhook listener) - Flask ilova – Telegram dan kelgan so‘rovlarni eshitadi
from flask import Flask, request
import requests
from ob_havo_pro import DISTRICTS, get_weather_text, make_district_keyboard, add_user_to_db, init_db

init_db()

app = Flask(__name__)
TOKEN = "8452355657:AAFinwieyCMPaZ17sdK0tzYqmjw2jYxp-Jw"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", data=payload)

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat = update["message"]["chat"]
        chat_id = chat["id"]
        text = update["message"].get("text", "")
        first = chat.get("first_name")
        last = chat.get("last_name")
        username = chat.get("username")

        add_user_to_db(chat_id, first, last, username)

        if text == "/start":
            send_message(chat_id, "📍 Farg'ona tumani tanlang:", make_district_keyboard())
        else:
            send_message(chat_id, "Yuborilgan matn tanilmadi. /start buyrug'ini yuboring.")

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        district = query["data"]
        lat, lon = DISTRICTS[district]
        weather = get_weather_text(lat, lon)
        send_message(chat_id, f"📍 <b>{district}</b> ob-havosi:\n\n{weather}")

    return {"ok": True}

@app.route("/")
def home():
    return "✅ Ob-havo boti ishlayapti!"

# HTML ko'rinishda foydalanuvchilar ro'yxati
@app.route("/users")
def show_users():
    users = get_all_users()
    html = "<h2>👥 Bot foydalanuvchilari:</h2><ul>"
    for uid, fname, lname, uname in users:
        html += f"<li><b>{fname or ''} {lname or ''}</b> @{uname or ''} - ID: {uid}</li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(port=5000)
