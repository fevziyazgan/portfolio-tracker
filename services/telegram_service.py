import os
import requests
TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN"
)
def send_message(
    chat_id,
    text
):
    if not TOKEN:
        print(
            "TOKEN BULUNAMADI"
        )
        return False
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=30
        )
        print(
            "TELEGRAM:",
            response.status_code
        )
        return (
            response.status_code == 200
        )
    except Exception as e:
        print(
            f"TELEGRAM ERROR: {e}"
        )
        return False
