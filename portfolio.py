from services.telegram_service import (
    get_updates,
    send_message
)

from services.telegram_command_service import (
    process_command
)

from services.portfolio_service import (
    run_portfolios
)

if __name__ == "__main__":

    run_portfolios()
