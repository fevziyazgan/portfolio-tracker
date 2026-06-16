from services.db_service import (
    get_connection
)

def get_all_assets():

    conn = get_connection()

    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT DISTINCT
            asset_code
        FROM asset_history
        ORDER BY asset_code
        """
    ).fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]
    


def get_daily_change():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT total_value
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

    today = rows[0][0]
    yesterday = rows[1][0]

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
        SELECT total_value
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

    latest = rows[0][0]
    oldest = rows[-1][0]

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


def get_portfolio_history(
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


def get_asset_history(
    asset_code,
    days=30
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            date,
            value
        FROM asset_history a
        WHERE asset_code = ?
        AND id = (
            SELECT MAX(id)
            FROM asset_history
            WHERE asset_code = a.asset_code
            AND date = a.date
        )
        ORDER BY id ASC
        LIMIT ?
        """,
        (
            asset_code,
            days
        )
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def get_asset_return(
    asset_code
):

    history = get_asset_history(
        asset_code
    )

    if len(history) < 2:

        return {
            "return_tl": 0,
            "return_pct": 0
        }

    first = history[0][1]
    last = history[-1][1]

    change_tl = (
        last - first
    )

    change_pct = (
        (change_tl / first) * 100
        if first > 0
        else 0
    )

    return {
        "return_tl": round(
            change_tl,
            2
        ),
        "return_pct": round(
            change_pct,
            2
        )
    }


def get_best_asset():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT DISTINCT
            asset_code
        FROM asset_history
        """
    )

    assets = [
        row[0]
        for row in cur.fetchall()
    ]

    conn.close()

    if not assets:

        return None

    best = None
    best_return = -999999

    for asset in assets:

        perf = get_asset_return(
            asset
        )

        if (
            perf["return_pct"]
            > best_return
        ):

            best_return = (
                perf["return_pct"]
            )

            best = {
                "asset": asset,
                "return_pct":
                best_return
            }

    return best


def get_asset_daily_change(asset_code):

    history = get_asset_history(
        asset_code,
        2
    )

    if len(history) < 2:
        return 0

    previous = history[-2][1]
    current = history[-1][1]

    if previous == 0:
        return 0

    return round(
        (
            (current - previous)
            / previous
        ) * 100,
        2
    )


def get_asset_monthly_change(asset_code):

    history = get_asset_history(
        asset_code,
        30
    )

    if len(history) < 2:
        return 0

    first = history[0][1]
    last = history[-1][1]

    if first == 0:
        return 0

    return round(
        (
            (last - first)
            / first
        ) * 100,
        2
    )

def get_worst_asset():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT DISTINCT
            asset_code
        FROM asset_history
        """
    )

    assets = [
        row[0]
        for row in cur.fetchall()
    ]

    conn.close()

    if not assets:

        return None

    worst = None
    worst_return = 999999

    for asset in assets:

        perf = get_asset_return(
            asset
        )

        if (
            perf["return_pct"]
            < worst_return
        ):

            worst_return = (
                perf["return_pct"]
            )

            worst = {
                "asset": asset,
                "return_pct":
                worst_return
            }

    return worst

