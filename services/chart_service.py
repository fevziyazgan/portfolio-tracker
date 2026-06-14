import matplotlib.pyplot as plt

from services.analytics_service import (
    get_portfolio_history,
    get_asset_history
)


def create_donut_chart(
    labels,
    values,
    output_file="donut_chart.png"
):

    safe_values = [
        max(0, v)
        for v in values
    ]

    if sum(safe_values) == 0:

        safe_values = [
            1,
            1,
            1
        ]

    colors = [
        "#2563EB",
        "#F97316",
        "#EAB308"
    ]

    fig, ax = plt.subplots(
        figsize=(5, 5)
    )

    ax.pie(
        safe_values,
        labels=labels,
        colors=colors,
        startangle=90,
        wedgeprops={
            "width": 0.45
        }
    )

    ax.set_aspect(
        "equal"
    )

    plt.savefig(
        output_file,
        bbox_inches="tight",
        transparent=True
    )

    plt.close()

def create_portfolio_performance_chart(
    output_file="performance_chart.png"
):

    plt.figure(
        figsize=(12, 5)
    )

    assets = [
        "IPV",
        "PHE",
        "TMV",
        "TLY",
        "GOLD"
    ]

    for asset in assets:

        history = get_asset_history(
            asset,
            30
        )

        if len(history) < 2:
            continue

        dates = [
            row[0]
            for row in history
        ]

        values = [
            row[1]
            for row in history
        ]

        base = values[0]

        values = [
            (
                v / base
            ) * 100
            for v in values
        ]

        plt.plot(
            dates,
            values,
            label=asset,
            linewidth=2
        )

    portfolio = (
        get_portfolio_history(
            30
        )
    )

    if len(portfolio) > 1:

        dates = [
            row[0]
            for row in portfolio
        ]

        values = [
            row[1]
            for row in portfolio
        ]

        base = values[0]

        values = [
            (
                v / base
            ) * 100
            for v in values
        ]

        plt.plot(
            dates,
            values,
            label="PORTFOY",
            linewidth=4,
            linestyle="--"
        )

    plt.title(
        "30 Gunluk Performans"
    )

    plt.legend()

    plt.grid(
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        bbox_inches="tight"
    )

    plt.close()



def create_allocation_table_data(
    report_data
):

    summary = report_data[
        "summary"
    ]

    total = max(
        1,
        summary[
            "total_value_tl"
        ]
    )

    return [

        {
            "name":
            "Fonlar",

            "value":
            summary[
                "fund_total_tl"
            ],

            "percent":
            round(
                summary[
                    "fund_total_tl"
                ]
                / total
                * 100,
                2
            )
        },

        {
            "name":
            "Kripto",

            "value":
            summary[
                "crypto_total_tl"
            ],

            "percent":
            round(
                summary[
                    "crypto_total_tl"
                ]
                / total
                * 100,
                2
            )
        },

        {
            "name":
            "Altin",

            "value":
            summary[
                "gold_total_tl"
            ],

            "percent":
            round(
                summary[
                    "gold_total_tl"
                ]
                / total
                * 100,
                2
            )
        }
    ]
