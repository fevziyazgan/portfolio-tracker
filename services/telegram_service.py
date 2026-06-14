import os
import requests


TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN"
)


def send_message(
    chat_id,
    text
):

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=30
    )

    return response.status_code


def send_photo(
    chat_id,
    image_path,
    caption=""
):

    url = (
        f"https://api.telegram.org/"
        f"bot{TOKEN}/sendPhoto"
    )

    with open(
        image_path,
        "rb"
    ) as photo:

        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "caption": caption
            },
            files={
                "photo": photo
            },
            timeout=60
        )

    return response.status_code
