import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(
        url,
        json={"chat_id": chat_id, "text": text},
        timeout=15
    )

@app.get("/")
def home():
    return "Vinscan Telegram Bot is running!", 200

@app.post("/webhook")
def webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message")

    if message:
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        text = message.get("text", "").strip()

        if chat_id:
            if text == "/start":
                reply = (
                    "Welcome to Vinscan! 👋\n\n"
                    "I am online and ready to help. "
                    "Send me a message."
                )
            elif text == "/help":
                reply = "Vinscan is online. Send me your question."
            elif text:
                reply = f"Vinscan received: {text}"
            else:
                reply = "Please send a text message."

            send_message(chat_id, reply)

    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
