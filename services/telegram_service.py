import requests
import os

TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN"
)


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
