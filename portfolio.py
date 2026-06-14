import json
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
    report.append("")
    usdtry = get_price(
        "USDTRY=X"
    )
    report.append(
        f"USDTRY: {usdtry}"
    )
    report.append("")
    report.append(
        "🏦 FON PORTFÖYÜ"
    )
    total_fund_value = 0
    for fund in user.get(
        "funds",
        []
    ):
        try:
            price_data = (
                get_fund_price(
                    fund["code"]
                )
            )
            if not price_data:
                continue
            value = (
                price_data["price"]
                * fund["quantity"]
            )
            total_fund_value += value
            report.append(
                f"{fund['code']} | "
                f"{price_data['price']:.4f}"
            )
        except Exception:
            pass
    report.append("")
    report.append(
        f"Toplam Fon: "
        f"{total_fund_value:,.0f} TL"
    )
    report.append("")
    report.append(
        "₿ KRİPTO PORTFÖYÜ"
    )
    total_crypto_usd = 0
    for crypto in user.get(
        "crypto",
        []
    ):
        try:
            price = get_crypto_price(
                crypto["symbol"]
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
        f"Toplam Kripto: "
        f"{total_crypto_usd:,.2f} USD"
    )
    return "\n".join(report)
def main():
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
                f"HATA: {e}"
            )
if __name__ == "__main__":
    main()
