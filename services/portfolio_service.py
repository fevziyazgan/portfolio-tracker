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
from services.db_service import (
    init_db,
    save_daily_snapshot
)

from services.analytics_service import (
    get_daily_change,
    get_monthly_change,
    get_best_asset,
    get_worst_asset,
    get_asset_daily_change,
    get_asset_monthly_change
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
                "code": fund["code"],
                "quantity": fund["quantity"],
                "price": price,
                "cost": cost,
                "value": round(value, 2),
                "cost_value": round(cost_value, 2),
                "profit": round(profit, 2),
        
                "daily_pct": get_asset_daily_change(
                    fund["code"]
                ),
        
                "monthly_pct": get_asset_monthly_change(
                    fund["code"]
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
                "symbol": crypto["symbol"],
                "quantity": crypto["quantity"],
                "price": price,
                "cost": cost,
        
                "value": round(
                    value,
                    2
                ),
        
                "value_tl": round(
                    value_tl,
                    2
                ),
        
                "profit": round(
                    profit,
                    2
                ),
        
                "daily_pct": get_asset_daily_change(
                    crypto["symbol"]
                ),
        
                "monthly_pct": get_asset_monthly_change(
                    crypto["symbol"]
                )
            }
        )
        except Exception:
            continue
    crypto_total_tl = (
        crypto_total_usd
        * usdtry
    )
    for crypto in cryptos:

        crypto["portfolio_pct"] = round(
            (
                crypto["value_tl"]
                / crypto_total_tl
            ) * 100,
            2
        ) if crypto_total_tl else 0

    
    gold_info = user.get(
        "gold",
        {}
    )
    gold_grams = gold_info.get(
        "grams",
        0
    )
    gold_cost = gold_info.get(
        "cost",
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
    gold_cost_total = (
        gold_grams
        * gold_cost
    )
    gold_profit = (
        gold_total_tl
        - gold_cost_total
    )

    gold_daily_pct = (
        get_asset_daily_change(
            "GOLD"
        )
    )
    
    gold_monthly_pct = (
        get_asset_monthly_change(
            "GOLD"
        )
    )

    cash = user.get(
        "cash_interest",
        {}
    )
    
    cash_amount = cash.get(
        "amount",
        0
    )
    
    cash_rate = cash.get(
        "rate",
        0
    )
    
    cash_period = cash.get(
        "rate_period",
        "yearly"
    )
    
    cash_tax = cash.get(
        "tax_rate",
        15
    )
    
    if cash_period == "daily":
    
        daily_interest = (
            cash_amount
            * cash_rate
            / 100
        )
    
    elif cash_period == "monthly":
    
        daily_interest = (
            cash_amount
            * cash_rate
            / 100
            / 30
        )
    
    else:
    
        daily_interest = (
            cash_amount
            * cash_rate
            / 100
            / 365
        )
    
    daily_interest_net = (
        daily_interest
        * (
            1
            - cash_tax / 100
        )
    )
    
    monthly_interest_net = (
        daily_interest_net * 30
    )
    
    yearly_interest_net = (
        daily_interest_net * 365
    )
    
    for fund in funds:

        fund["portfolio_pct"] = round(
            (
                fund["value"]
                / fund_total_tl
            ) * 100,
            2
        ) if fund_total_tl else 0
        
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
        + cash_amount
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
        "cash_interest": {

            "bank":
            cash.get(
                "bank",
                ""
            ),
        
            "amount":
            cash_amount,
        
            "rate":
            cash_rate,
        
            "rate_period":
            cash_period,
        
            "tax_rate":
            cash_tax,
        
            "daily_interest":
            round(
                daily_interest_net,
                2
            ),
        
            "monthly_interest":
            round(
                monthly_interest_net,
                2
            ),
        
            "yearly_interest":
            round(
                yearly_interest_net,
                2
            ),
        
            "portfolio_pct":
            round(
                (
                    cash_amount
                    / total_value_tl
                ) * 100,
                2
            ) if total_value_tl else 0
        },
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
            "grams": gold_grams,
            "cost": gold_cost,
            "price": gold_price,
            "value": round(gold_total_tl, 2),
            "cost_value": round(gold_cost_total, 2),
            "profit": round(gold_profit, 2),
        
            "daily_pct": get_asset_daily_change(
                "GOLD"
            ),
        
            "monthly_pct": get_asset_monthly_change(
                "GOLD"
            ),
        
            "portfolio_pct": round(
                (
                    gold_total_tl
                    / total_value_tl
                ) * 100,
                2
            ) if total_value_tl else 0
        },
        "performance": {
        
            "daily":
            get_daily_change(),
        
            "monthly":
            get_monthly_change(),
        
            "best_asset":
            get_best_asset(),
        
            "worst_asset":
            get_worst_asset()
        
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
def run_portfolios():
    init_db()
    users = load_users()
    for user in users:
        report_data = (
            build_report_data(
                user
            )
        )
        print(
            report_data[
                "performance"
            ]
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
        
