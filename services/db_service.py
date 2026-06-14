import sqlite3
from pathlib import Path
DB_FILE = "data/portfolio.db"
def generate_fake_history():

    from datetime import datetime
    from datetime import timedelta
    import random

    conn = get_connection()
    cur = conn.cursor()

    base = 2500000

    for i in range(30):

        date = (
            datetime.now()
            - timedelta(days=29-i)
        ).strftime(
            "%d.%m.%Y"
        )

        value = (
            base
            + (i * 15000)
            + random.randint(
                -10000,
                10000
            )
        )

        cur.execute(
            """
            INSERT OR REPLACE INTO
            portfolio_history
            (
                date,
                total_value,
                fund_value,
                crypto_value,
                gold_value,
                total_cost,
                profit
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                value,
                value * 0.60,
                value * 0.05,
                value * 0.35,
                value * 0.80,
                value * 0.20
            )
        )

    conn.commit()
    conn.close()

    print(
        "FAKE HISTORY CREATED"
    )
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
            cost REAL,
            price REAL,
            value REAL,
            profit REAL
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
                cost,
                price,
                value,
                profit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                fund["code"],
                "FUND",
                fund["quantity"],
                fund["cost"],
                fund["price"],
                fund["value"],
                fund["profit"]
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
                cost,
                price,
                value,
                profit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                crypto["symbol"],
                "CRYPTO",
                crypto["quantity"],
                crypto["cost"],
                crypto["price"],
                crypto["value_tl"],
                crypto["profit"]
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
            cost,
            price,
            value,
            profit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            date,
            "GOLD",
            "GOLD",
            gold["grams"],
            gold["cost"],
            gold["price"],
            gold["value"],
            gold["profit"]
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

def get_daily_change():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            date,
            total_value
        FROM portfolio_history
        ORDER BY date DESC
        LIMIT 2
        """
    )

    rows = cur.fetchall()

    conn.close()

    if len(rows) < 2:
        return {
            "change_tl": 0,
            "change_pct": 0
        }

    today = rows[0][1]
    yesterday = rows[1][1]

    change_tl = (
        today - yesterday
    )

    change_pct = (
        (change_tl / yesterday) * 100
        if yesterday > 0
        else 0
    )

    return {
        "change_tl": round(
            change_tl,
            2
        ),
        "change_pct": round(
            change_pct,
            2
        )
    }


def get_monthly_change():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            date,
            total_value
        FROM portfolio_history
        ORDER BY date DESC
        LIMIT 30
        """
    )

    rows = cur.fetchall()

    conn.close()

    if len(rows) < 2:
        return {
            "change_tl": 0,
            "change_pct": 0
        }

    latest = rows[0][1]
    oldest = rows[-1][1]

    change_tl = (
        latest - oldest
    )

    change_pct = (
        (change_tl / oldest) * 100
        if oldest > 0
        else 0
    )

    return {
        "change_tl": round(
            change_tl,
            2
        ),
        "change_pct": round(
            change_pct,
            2
        )
    }


def get_history(
    days=30
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            date,
            total_value
        FROM portfolio_history
        ORDER BY date ASC
        LIMIT ?
        """,
        (days,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

    
    conn.commit()
    conn.close()
