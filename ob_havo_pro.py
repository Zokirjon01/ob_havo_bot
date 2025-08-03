# Botning logikasi: tumanlar, ob-havo, foydalanuvchi saqlash - Asosiy bot mantiqlari: tugmalar, ob-havo olish, db ishlash
import requests
import json
import sqlite3

# API kalitingizni shu yerga yozing
OPENWEATHER_KEY = "a31f28e0afcf5884405f129fc329f04a"

DISTRICTS = {
    "Farg'ona shahri": (40.3896, 71.7824),
    "Qo'shtepa": (40.5526, 71.5623),
    "Quva": (40.5222, 72.0741),
    "Buvayda": (40.4472, 71.7188),
    "Dang'ara": (40.7303, 71.9467),
    "Oltiariq": (40.3786, 71.5300),
    "O'zbekiston": (40.6405, 72.0400),
    "Bag'dod": (40.4561, 71.6894),
    "Beshariq": (40.4300, 71.9208),
    "Furqat": (40.5500, 71.7833),
    "Marg'ilon": (40.4710, 71.7246),
    "Rishton": (40.3576, 71.2843),
    "Toshloq": (40.5566, 71.7896),
    "Uchko'prik": (40.6598, 71.5214),
    "Yozyovon": (40.6853, 71.5530)
}

def get_weather_text(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric&lang=uz"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ Ob-havo ma'lumotini olishda xatolik yuz berdi."

    data = response.json()
    weather = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels = data['main']['feels_like']
    humidity = data['main']['humidity']

    return f"🌤 Ob-havo: {weather}\n🌡 Harorat: {temp}°C (His qilinadi: {feels}°C)\n💧 Namlik: {humidity}%"

def make_district_keyboard():
    keyboard = {
        "inline_keyboard": [
            [{"text": name, "callback_data": name}] for name in DISTRICTS.keys()
        ]
    }
    return json.dumps(keyboard)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_user(chat_id, username, first_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (chat_id, username, first_name) VALUES (?, ?, ?)
    """, (chat_id, username, first_name))
    conn.commit()
    conn.close()
