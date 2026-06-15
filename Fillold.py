from datetime import date, timedelta

from services.db_service import (
    get_connection
)

from services.portfolio_service import (
    build_report_data
)


def main():

    report_data = (
        build_report_data()
    )

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM asset_history"
    )

    cur.execute(
        "DELETE FROM portfolio_history"
    )

    summary = report_data[
        "summary"
    ]

    asset_values = {}

    for fund in report_data[
        "funds"
    ]:

        asset_values[
            fund["code"]
        ] = fund[
            "current_value"
        ]

    asset_values[
        "GOLD"
    ] = report_data[
        "gold"
    ][
        "value"
    ]

    asset_values[
        "CASH"
    ] = report_data[
        "cash"
    ][
        "current_value"
    ]

    asset_values[
        "CRYPTO"
    ] = summary[
        "crypto_total_tl"
    ]

    today = date.today()

    for i in range(30):

        d = (
            today -
            timedelta(
                days=29 - i
            )
        ).isoformat()

        cur.execute(
            """
            INSERT INTO portfolio_history
            (
                date,
                total_value
            )
            VALUES
            (?, ?)
            """,
            (
                d,
                summary[
                    "total_value_tl"
                ]
            )
        )

        for asset_code, value in (
            asset_values.items()
        ):

            cur.execute(
                """
                INSERT INTO asset_history
                (
                    date,
                    asset_code,
                    value
                )
                VALUES
                (?, ?, ?)
                """,
                (
                    d,
                    asset_code,
                    value
                )
            )

    conn.commit()

    conn.close()

    print(
        "30 günlük history oluşturuldu."
    )


if __name__ == "__main__":

    main()
