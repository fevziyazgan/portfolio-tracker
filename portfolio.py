import json
import csv
import os
from datetime import datetime
import requests
CONFIG_FILE = "config/users.json"
HISTORY_DIR = "history"
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
                "usdtry",
                "gold",
                "bist100",
                "cds",
                "us10y"
            ])
    return filename
def append_test_row(filename):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            today,
            0,
            0,
            0,
            0,
            0,
            0
        ])
def send_test_message(user):
    token = user["telegram"]["token"]
    chat_id = user["telegram"]["chat_id"]
    text = (
        f"✅ Portfolio Tracker Aktif\n\n"
        f"Kullanıcı: {user['name']}\n"
        f"ID: {user['id']}\n\n"
        f"Yeni mimari başarıyla çalışıyor."
    )
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=30
    )
def main():
    users = load_users()
    for user in users:
        filename = ensure_history_file(user["id"])
        append_test_row(filename)
        send_test_message(user)
        print(
            f"OK -> {user['name']} ({user['id']})"
        )
if __name__ == "__main__":
    main()
