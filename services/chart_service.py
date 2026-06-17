def create_portfolio_performance_chart(
output_file=“performance_chart.png”
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
#
# ÜST GRAFİK
#
for asset in assets:
