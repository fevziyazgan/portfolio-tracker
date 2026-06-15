import requests

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


def send_message(
    chat_id,
    text
):

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )


def get_updates(
    offset=None
):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/getUpdates"
    )

    params = {}

    if offset:
        params["offset"] = offset

    r = requests.get(
        url,
        params=params,
        timeout=30
    )

    return r.json()
