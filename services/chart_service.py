def create_portfolio_performance_chart(
output_file="performance_chart.png"
):

from services.analytics_service import (
    get_asset_history,
    get_all_assets
)
crypto_assets = [
    "XRP",
    "LUNC",
    "AGIX",
    "SHIB",
    "TRX",
    "FTT",
    "MBOX",
    "DOGE",
    "ARB",
    "BNB",
    "USDT",
    "AVAX"
]
fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(16, 14)
)
assets = get_all_assets()
crypto_dates = None
crypto_total = []
# ÜST GRAFİK
for asset in assets:
    if asset in crypto_assets:
        history = get_asset_history(asset, 30)
        if len(history) < 2:
            continue
        values = [row[1] for row in history]
        if crypto_dates is None:
            crypto_dates = [
                row[0]
                for row in history
            ]
            crypto_total = values.copy()
        else:
            for i in range(
                min(
                    len(values),
                    len(crypto_total)
                )
            ):
                crypto_total[i] += values[i]
        continue
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
    if base <= 0:
        continue
    normalized = [
        (v / base) * 100
        for v in values
    ]
    ax1.plot(
        dates,
        normalized,
        label=asset,
        linewidth=2
    )
if crypto_dates and len(crypto_total) > 1:
    base = crypto_total[0]
    if base > 0:
        normalized = [
            (v / base) * 100
            for v in crypto_total
        ]
        ax1.plot(
            crypto_dates,
            normalized,
            label="KRIPTO TOPLAM",
            linewidth=3,
            linestyle="--"
        )
ax1.set_title(
    "Ana Varlik Siniflari Performansi"
)
ax1.grid(alpha=0.25)
ax1.tick_params(
    axis="x",
    rotation=45
)
ax1.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5)
)
ax1.set_ylabel(
    "Baslangic = 100"
)
# ALT GRAFİK
for asset in crypto_assets:
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
    if base <= 0:
        continue
    normalized = [
        (v / base) * 100
        for v in values
    ]
    ax2.plot(
        dates,
        normalized,
        label=asset,
        linewidth=2
    )
ax2.set_title(
    "Kripto Varliklar Performansi"
)
ax2.grid(alpha=0.25)
ax2.tick_params(
    axis="x",
    rotation=45
)
ax2.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5)
)
ax2.set_ylabel(
    "Baslangic = 100"
)
plt.tight_layout()
plt.savefig(
    output_file,
    dpi=200,
    bbox_inches="tight"
)
plt.close()
