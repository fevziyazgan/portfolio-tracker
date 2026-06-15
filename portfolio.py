from services.telegram_service import (
    get_new_messages,
    send_message
)

from services.telegram_command_service import (
    process_command
)

from services.portfolio_service import (
    run_portfolios
)


def process_telegram_commands():

    messages = (
        get_new_messages()
    )

    for message in messages:

        chat_id = message[
            "chat_id"
        ]

        text = message[
            "text"
        ]

        if not text.startswith(
            "/"
        ):
            continue

        response = (
            process_command(
                chat_id,
                text
            )
        )

        if response:

            send_message(
                chat_id,
                response
            )


if __name__ == "__main__":

    process_telegram_commands()

    run_portfolios()
