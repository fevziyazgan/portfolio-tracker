import json
import csv
import os
from datetime import datetime
import requests
import yfinance as yf
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
print("TOKEN VAR:", TOKEN is not None)
if TOKEN:
    print("TOKEN LENGTH:", len(TOKEN))
CONFIG_FILE = "config/users.json"
HISTORY_DIR = "history"
def get_tefas_price(fund_code):
    url = (
        "https://www.tefas.gov.tr/FonAnaliz.aspx"
        f"?FonKod={fund_code}"
    )
    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )
        print(
            f"TEFAS {fund_code}:",
            response.status_code
        )
        return response.status_code
    except Exception as e:
        print(
            f"TEFAS ERROR {fund_code}:",
            e
        )
        return None
def load_users():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["users"]
def ensure_history_file(user_id):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    filename = f"{HISTORY_DIR}/{user_id}.csv"
    if not os.path.exists(filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
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
def get_yahoo_price(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="5d")
        if len(hist) == 0:
            return None
        return round(float(hist["Close"].iloc[-1]), 4)
    except Exception as e:
        print(f"ERROR {ticker}: {e}")
        return None
def append_history_row(
    filename,
    usdtry,
    bist100,
    us10y
):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(filename, "a", newline="", encoding="utf-8") as f:
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
def send_test_message(user):
    if not TOKEN:
        print("TOKEN BULUNAMADI")
        return
    chat_id = user["telegram"]["chat_id"]
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": "🚀 Portfolio Tracker test mesajı"
        },
        timeout=30
    )
    print("TELEGRAM STATUS:", response.status_code)
    print("TELEGRAM RESPONSE:", response.text)
def main():

    usdtry = get_yahoo_price("USDTRY=X")
    bist100 = get_yahoo_price("XU100.IS")
    us10y = get_yahoo_price("^TNX")
    print("USDTRY:", usdtry)
    print("BIST100:", bist100)
    print("US10Y:", us10y)
    print("IPV:", get_tefas_price("IPV"))
print("PHE:", get_tefas_price("PHE"))
print("TMV:", get_tefas_price("TMV"))
print("TLY:", get_tefas_price("TLY"))
    users = load_users()
    for user in users:
        filename = ensure_history_file(user["id"])
        append_history_row(
            filename,
            usdtry,
            bist100,
            us10y
        )
        send_test_message(user)
        print(
            f"OK -> {user['name']} ({user['id']})"
        )
if __name__ == "__main__":
    main()
