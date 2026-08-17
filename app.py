import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


def send_message(chat_id, text):
    if not TOKEN:
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=15
    )

    return response.ok


@app.get("/")
def home():
    return "Vinscan Telegram Bot is running!", 200


@app.post("/webhook")
@app.post("/api")
def webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message")

    if not message:
        return jsonify({"ok": True}), 200

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id:
        return jsonify({"ok": True}), 200

    if text == "/start":
        reply = (
            "Welcome to Vinscan! 👋\n\n"
            "I am online and ready to help.\n\n"
            "Send me a message and I will respond."
        )

    elif text == "/help":
        reply = (
            "Vinscan Help\n\n"
            "Send me any message and I will respond."
        )

    elif text:
        reply = f"Vinscan received: {text}"

    else:
        reply = "Please send a text message."

    try:
        send_message(chat_id, reply)
    except Exception:
        pass

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
