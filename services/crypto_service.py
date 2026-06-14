import json
import yfinance as yf
ASSETS_FILE = "config/assets.json"
def load_assets():
    with open(
        ASSETS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)
def get_crypto_ticker(
    symbol
):
    assets = load_assets()
    crypto = assets.get(
        "crypto",
        {}
    )
    info = crypto.get(
        symbol.upper()
    )
    if not info:
        return None
    return info.get(
        "ticker"
    )
def get_crypto_price(
    symbol
):
    ticker = get_crypto_ticker(
        symbol
    )
    if not ticker:
        print(
            f"TICKER BULUNAMADI: {symbol}"
        )
        return None
    try:
        data = yf.Ticker(
            ticker
        )
        hist = data.history(
            period="5d"
        )
        if len(hist) == 0:
            return None
        return round(
            float(
                hist["Close"].iloc[-1]
            ),
            8
        )
    except Exception as e:
        print(
            f"CRYPTO ERROR {symbol}:",
            e
        )
        return None
def get_crypto_value(
    symbol,
    quantity
):
    price = get_crypto_price(
        symbol
    )
    if price is None:
        return None
    return {
        "symbol": symbol,
        "quantity": quantity,
        "price": price,
        "value_usd": round(
            quantity * price,
            2
        )
    }
def test_crypto():
    assets = load_assets()
    result = {}
    for symbol in assets.get(
        "crypto",
        {}
    ):
        result[symbol] = (
            get_crypto_price(
                symbol
            )
        )
    return result
