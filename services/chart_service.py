import matplotlib.pyplot as plt

from services.analytics_service import (
    get_portfolio_history
)


def create_donut_chart(
    labels,
    values,
    output_file="donut_chart.png"
):

    colors = [
        "#2563EB",  # Fonlar
        "#EF4444",  # Kripto
        "#EAB308"   # Altın
    ]

    fig, ax = plt.subplots(
        figsize=(5, 5)
    )

    ax.pie(
        values,
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

    if len(history) == 0:

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

    plt.title(
        "Portfoy Performansi"
    )

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        bbox_inches="tight"
    )

    plt.close()


def create_asset_performance_chart(
    data,
    output_file="asset_chart.png"
):

    labels = [
        item["label"]
        for item in data
    ]

    values = [
        item["value"]
        for item in data
    ]

    plt.figure(
        figsize=(8, 4)
    )

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Varlik Performansi"
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        bbox_inches="tight"
    )

    plt.close()

