# Flask server (webhook listener) - Flask ilova – Telegram dan kelgan so‘rovlarni eshitadi
from flask import Flask, request
import requests
from ob_havo_pro import DISTRICTS, get_weather_text, make_district_keyboard, save_user

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
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        username = message["from"].get("username")
        first_name = message["from"].get("first_name")

        save_user(chat_id, username, first_name)

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


if __name__ == '__main__':
    from ob_havo_pro import init_db
    init_db()
    app.run(port=5000)
