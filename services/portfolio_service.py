import json
from datetime import datetime
from services.yahoo_service import get_price
from services.tefas_service import get_fund_price
from services.crypto_service import get_crypto_price
from services.telegram_service import send_message
CONFIG_FILE = "config/users.json"
def load_users():
    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)
    return data["users"]
def build_report(user):
    report = []
    report.append(
        "📊 PORTFÖY RAPORU"
    )
    report.append(
        datetime.now().strftime(
            "%d.%m.%Y"
        )
    )
    report.append("")
    report.append(
        "═══════════════"
    )
    report.append(
        "🏦 ANA PORTFÖY"
    )
    report.append(
        "═══════════════"
    )
    report.append("")
    total_fund_value = 0
    for fund in user.get(
        "funds",
        []
    ):
        try:
            fund_data = (
                get_fund_price(
                    fund["code"]
                )
            )
            if not fund_data:
                continue
            price = fund_data[
                "price"
            ]
            value = (
                price
                * fund["quantity"]
            )
            total_fund_value += value
            report.append(
                f"{fund['code']} | "
                f"{price:.4f}"
            )
        except Exception:
            pass
    report.append("")
    report.append(
        f"💰 Toplam Fon: "
        f"{total_fund_value:,.0f} TL"
    )
    report.append("")
    report.append("")
    report.append(
        "═══════════════"
    )
    report.append(
        "₿ KRİPTO PORTFÖYÜ"
    )
    report.append(
        "═══════════════"
    )
    report.append("")
    total_crypto_usd = 0
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
                crypto["quantity"]
                * price
            )
            total_crypto_usd += value
            report.append(
                f"{crypto['symbol']} | "
                f"{price:.6f}$"
            )
        except Exception:
            pass
    report.append("")
    report.append(
        f"💰 Toplam Kripto: "
        f"{total_crypto_usd:,.2f} USD"
    )
    report.append("")
    report.append("")
    report.append(
        "═══════════════"
    )
    report.append(
        "📈 PİYASA"
    )
    report.append(
        "═══════════════"
    )
    report.append("")
    try:
        usdtry = get_price(
            "USDTRY=X"
        )
        report.append(
            f"USDTRY : {usdtry}"
        )
    except Exception:
        pass
    try:
        bist100 = get_price(
            "XU100.IS"
        )
        report.append(
            f"BIST100 : {bist100}"
        )
    except Exception:
        pass
    try:
        us10y = get_price(
            "^TNX"
        )
        report.append(
            f"US10Y : {us10y}"
        )
    except Exception:
        pass
    return "\n".join(
        report
    )
def run_portfolios():
    users = load_users()
    for user in users:
        try:
            report = build_report(
                user
            )
            send_message(
                user["telegram"]["chat_id"],
                report
            )
        except Exception as e:
            print(
                f"ERROR: {e}"
            )
