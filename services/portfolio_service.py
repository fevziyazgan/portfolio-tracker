import json
from datetime import datetime
from services.yahoo_service import (
    get_price,
    get_gram_gold
)
from services.tefas_service import (
    get_fund_price
)
from services.crypto_service import (
    get_crypto_price
)
from services.telegram_service import (
    send_photo
)
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
            cost = fund.get(
                "cost",
                0
            )
            cost_value = (
                cost
                * fund["quantity"]
            )
            profit = (
                value
                - cost_value
            )
            funds.append(
                {
                    "code":
                    fund["code"],
                    "quantity":
                    fund["quantity"],
                    "price":
                    price,
                    "cost":
                    cost,
                    "value":
                    round(
                        value,
                        2
                    ),
                    "cost_value":
                    round(
                        cost_value,
                        2
                    ),
                    "profit":
                    round(
                        profit,
                        2
                    )
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
            cost = crypto.get(
                "cost",
                0
            )
            value_tl = (
                value
                * usdtry
            )
            profit = (
                (
                    price
                    - cost
                )
                *
                crypto["quantity"]
            )
            cryptos.append(
                {
                    "symbol":
                    crypto["symbol"],
                    "quantity":
                    crypto["quantity"],
                    "price":
                    price,
                    "cost":
                    cost,
                    "value":
                    round(
                        value,
                        2
                    ),
                    "value_tl":
                    round(
                        value_tl,
                        2
                    ),
                    "profit":
                    round(
                        profit,
                        2
                    )
                }
            )
        except Exception:
            continue
    crypto_total_tl = (
        crypto_total_usd
        * usdtry
    )
    gold_data = user.get(
        "gold",
        {}
    )
    gold_grams = gold_data.get(
        "grams",
        0
    )
    gold_price = (
        get_gram_gold()
        or 0
    )
    gold_total_tl = (
        gold_grams
        * gold_price
    )
    gold_cost = (
        gold_data.get(
            "cost",
            0
        )
    )
    gold_cost_total = (
        gold_cost
        * gold_grams
    )
    total_cost = 0
    for fund in funds:
        total_cost += fund[
            "cost_value"
        ]
    for crypto in cryptos:
        total_cost += (
            crypto["cost"]
            * crypto["quantity"]
            * usdtry
        )
    total_cost += (
        gold_cost_total
    )
    total_value_tl = (
        fund_total_tl
        + crypto_total_tl
        + gold_total_tl
    )
    profit_tl = (
        total_value_tl
        - total_cost
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
            ),
            "total_cost_tl":
            round(
                total_cost,
                0
            ),
            "profit_tl":
            round(
                profit_tl,
                0
            )
        },
        "funds":
        funds,
        "cryptos":
        cryptos,
        "gold": {
            "grams":
            gold_grams,
            "price":
            gold_price,
            "value":
            round(
                gold_total_tl,
                2
            ),
            "cost":
            gold_cost,
            "cost_value":
            round(
                gold_cost_total,
                2
            )
        },
        "market": {
            "usdtry":
            usdtry,
            "bist100":
            bist100,
            "us10y":
            us10y,
            "gram_gold":
            gold_price
        }
    }
from services.db_service import (
    init_db,
    save_daily_snapshot
)
def run_portfolios():

    init_db()

    users = load_users()

    for user in users:

        try:

            report_data = (
                build_report_data(
                    user
                )
            )

            save_daily_snapshot(
                report_data
            )

            image_file = (
                create_report_image(
                    report_data
                )
            )

            send_photo(
                user["telegram"]["chat_id"],
                image_file
            )

        except Exception as e:

            print(
                f"ERROR: {e}"
            )
