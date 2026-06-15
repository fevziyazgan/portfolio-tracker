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


def get_updates(
    offset=None
):

    url = (
        f"https://api.telegram.org/"
        f"bot{TOKEN}/getUpdates"
    )

    params = {}

    if offset is not None:

        params[
            "offset"
        ] = offset

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    try:

        return response.json()

    except Exception:

        return {
            "ok": False,
            "result": []
        }


def load_offset():

    try:

        with open(
            "data/telegram_offset.txt",
            "r"
        ) as f:

            return int(
                f.read().strip()
            )

    except Exception:

        return None


def save_offset(
    offset
):

    with open(
        "data/telegram_offset.txt",
        "w"
    ) as f:

        f.write(
            str(offset)
        )


def get_new_messages():

    offset = load_offset()

    updates = get_updates(
        offset
    )

    if not updates.get(
        "ok"
    ):
        return []

    messages = []

    for update in updates[
        "result"
    ]:

        save_offset(
            update[
                "update_id"
            ] + 1
        )

        message = update.get(
            "message"
        )

        if not message:
            continue

        text = message.get(
            "text",
            ""
        )

        chat_id = (
            message["chat"]["id"]
        )

        messages.append(
            {
                "chat_id":
                chat_id,

                "text":
                text
            }
        )

    return messages
