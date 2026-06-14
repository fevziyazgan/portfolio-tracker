import matplotlib.pyplot as plt

from services.analytics_service import (
    get_portfolio_history
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

    history = get_portfolio_history(
        30
    )

    if len(history) < 2:

        dates = [
            "G1",
            "G2"
        ]

        values = [
            100,
            100
        ]

    else:

        dates = [
            row[0]
            for row in history
        ]

        values = [
            row[1]
            for row in history
        ]

    plt.figure(
        figsize=(10, 4)
    )

    plt.plot(
        dates,
        values,
        linewidth=3
    )

    plt.fill_between(
        dates,
        values,
        alpha=0.15
    )

    plt.title(
        "30 Gunluk Portfoy Performansi"
    )

    plt.grid(
        alpha=0.25
    )

    plt.xticks(
        rotation=45
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
