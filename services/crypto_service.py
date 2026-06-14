import json
import yfinance as yf

with open(
    "config/assets.json",
    "r",
    encoding="utf-8"
) as f:

    ASSETS = json.load(f)


def get_crypto_price(symbol):

    ticker = (
        ASSETS["crypto"]
        .get(symbol.upper(), {})
        .get("ticker")
    )

    if not ticker:
        return None

    hist = yf.Ticker(
        ticker
    ).history(
        period="5d"
    )

    if len(hist) == 0:
        return None

    return float(
        hist["Close"].iloc[-1]
    )
