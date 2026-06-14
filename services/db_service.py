import sqlite3
from pathlib import Path
DB_FILE = "data/portfolio.db"
def get_connection():
    Path("data").mkdir(
        exist_ok=True
    )
    return sqlite3.connect(
        DB_FILE
    )
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS portfolio_history (
            date TEXT PRIMARY KEY,
            total_value REAL,
            fund_value REAL,
            crypto_value REAL,
            gold_value REAL,
            total_cost REAL,
            profit REAL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS asset_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            asset_code TEXT,
            asset_type TEXT,
            quantity REAL,
            price REAL,
            value REAL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS market_history (
            date TEXT PRIMARY KEY,
            usdtry REAL,
            bist100 REAL,
            us10y REAL,
            gram_gold REAL
        )
        """
    )
    conn.commit()
    conn.close()
def save_daily_snapshot(report_data):
    conn = get_connection()
    cur = conn.cursor()
    date = report_data["date"]
    summary = report_data["summary"]
    cur.execute(
        """
        INSERT OR REPLACE INTO portfolio_history (
            date,
            total_value,
            fund_value,
            crypto_value,
            gold_value,
            total_cost,
            profit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            date,
            summary["total_value_tl"],
            summary["fund_total_tl"],
            summary["crypto_total_tl"],
            summary["gold_total_tl"],
            summary["total_cost_tl"],
            summary["profit_tl"]
        )
    )
    for fund in report_data["funds"]:
        cur.execute(
            """
            INSERT INTO asset_history (
                date,
                asset_code,
                asset_type,
                quantity,
                price,
                value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                fund["code"],
                "FUND",
                fund["quantity"],
                fund["price"],
                fund["value"]
            )
        )
    for crypto in report_data["cryptos"]:
        cur.execute(
            """
            INSERT INTO asset_history (
                date,
                asset_code,
                asset_type,
                quantity,
                price,
                value
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                crypto["symbol"],
                "CRYPTO",
                crypto["quantity"],
                crypto["price"],
                crypto["value_tl"]
            )
        )
    gold = report_data["gold"]
    cur.execute(
        """
        INSERT INTO asset_history (
            date,
            asset_code,
            asset_type,
            quantity,
            price,
            value
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            date,
            "GOLD",
            "GOLD",
            gold["grams"],
            gold["price"],
            gold["value"]
        )
    )
    market = report_data["market"]
    cur.execute(
        """
        INSERT OR REPLACE INTO market_history (
            date,
            usdtry,
            bist100,
            us10y,
            gram_gold
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            date,
            market["usdtry"],
            market["bist100"],
            market["us10y"],
            market["gram_gold"]
        )
    )
    conn.commit()
    conn.close()
