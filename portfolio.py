import json
import csv
import os
from datetime import datetime
from services.yahoo_service import get_price
from services.telegram_service import send_message
from services.tefas_service import test_funds
CONFIG_FILE = "config/users.json"
HISTORY_DIR = "history"
def load_users():
    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)
    return data["users"]
def ensure_history_file(
    user_id
):
    os.makedirs(
        HISTORY_DIR,
        exist_ok=True
    )
    filename = (
        f"{HISTORY_DIR}/{user_id}.csv"
    )
    if not os.path.exists(
        filename
    ):
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow([
                "date",
                "total_value",
                "portfolio_return_pct",
                "usdtry",
                "gold",
                "bist100",
                "cds",
                "us10y"
            ])
    return filename
def append_history_row(
    filename,
    usdtry,
    bist100,
    us10y
):
    today = (
        datetime.now()
        .strftime("%Y-%m-%d")
    )
    with open(
        filename,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow([
            today,
            0,
            0,
            usdtry,
            0,
            bist100,
            0,
            us10y
        ])
def main():
    usdtry = get_price(
        "USDTRY=X"
    )
    bist100 = get_price(
        "XU100.IS"
    )
    us10y = get_price(
        "^TNX"
    )
    print(
        "USDTRY:",
        usdtry
    )
    print(
        "BIST100:",
        bist100
    )
    print(
        "US10Y:",
        us10y
    )
    print(
        "TEFAS TEST:"
    )
    print(
        test_funds()
    )
    users = load_users()
    for user in users:
        filename = (
            ensure_history_file(
                user["id"]
            )
        )
        append_history_row(
            filename,
            usdtry,
            bist100,
            us10y
        )
        send_message(
            user["telegram"]["chat_id"],
            (
                "🚀 Portfolio Tracker\n\n"
                f"Kullanıcı: {user['name']}\n"
                f"USDTRY: {usdtry}\n"
                f"BIST100: {bist100}\n"
                f"US10Y: {us10y}"
            )
        )
        print(
            f"OK -> "
            f"{user['name']} "
            f"({user['id']})"
        )
if __name__ == "__main__":
    main()
