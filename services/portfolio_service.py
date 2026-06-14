import json
from datetime import datetime
from services.yahoo_service import get_price
from services.tefas_service import get_fund_price
from services.crypto_service import get_crypto_price
from services.telegram_service import send_photo
from services.report_image_service import (
    create_report_image
)
CONFIG_FILE = "config/users.json"
def load_users():
    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)
    return data["users"]
def build_report_data(
    user
):
    usdtry = (
        get_price(
            "USDTRY=X"
        ) or 0
    )
    bist100 = (
        get_price(
            "XU100.IS"
        ) or 0
    )
    us10y = (
        get_price(
            "^TNX"
        ) or 0
    )
    funds = []
    fund_total_tl = 0
    for fund in user.get(
        "funds",
        []
    ):
        try:
            data = get_fund_price(
                fund["code"]
            )
            if not data:
                continue
            price = data["price"]
            value = (
                price
                * fund["quantity"]
            )
            fund_total_tl += value
            funds.append(
                {
                    "code":
                    fund["code"],
                    "quantity":
                    fund["quantity"],
                    "price":
                    price,
                    "value":
                    round(value, 2)
                }
            )
        except Exception:
            continue
    cryptos = []
    crypto_total_usd = 0
    for crypto in user.get(
        "crypto",
        []
    ):
        try:
            price = (
                get_crypto_price(
                    crypto["symbol"]
                )
            )
            if not price:
                continue
            value = (
                price
                * crypto["quantity"]
            )
            crypto_total_usd += value
            cryptos.append(
                {
                    "symbol":
                    crypto["symbol"],
                    "quantity":
                    crypto["quantity"],
                    "price":
                    price,
                    "value":
                    round(value, 2)
                }
            )
        except Exception:
            continue
    crypto_total_tl = (
        crypto_total_usd
        * usdtry
    )
    gold_total_tl = 0
    total_value_tl = (
        fund_total_tl
        + crypto_total_tl
        + gold_total_tl
    )
    return {
        "date":
        datetime.now().strftime(
            "%d.%m.%Y"
        ),
        "summary": {
            "total_value_tl":
            round(
                total_value_tl,
                0
            ),
            "fund_total_tl":
            round(
                fund_total_tl,
                0
            ),
            "crypto_total_tl":
            round(
                crypto_total_tl,
                0
            ),
            "gold_total_tl":
            round(
                gold_total_tl,
                0
            )
        },
        "funds":
        funds,
        "cryptos":
        cryptos,
        "market": {
            "usdtry":
            usdtry,
            "bist100":
            bist100,
            "us10y":
            us10y
        }
    }
def run_portfolios():
    users = load_users()
    for user in users:
        try:
            report_data = (
                build_report_data(
                    user
                )
            )
            image_file = (
                create_report_image(
                    report_data
                )
            )
            send_photo(
                user[
                    "telegram"
                ][
                    "chat_id"
                ],
                image_file
            )
        except Exception as e:
            print(
                f"ERROR: {e}"
            )
