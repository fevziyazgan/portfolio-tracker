import yfinance as yf
def get_price(
    ticker
):
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
                hist[
                    "Close"
                ].iloc[-1]
            ),
            4
        )
    except Exception as e:
        print(
            f"YAHOO ERROR {ticker}: {e}"
        )
        return None
def get_usdtry():
    return get_price(
        "USDTRY=X"
    )
def get_bist100():
    return get_price(
        "XU100.IS"
    )
def get_us10y():
    return get_price(
        "^TNX"
    )
def get_gold_ounce():
    return get_price(
        "GC=F"
    )
def get_gram_gold():
    ounce = get_gold_ounce()
    usdtry = get_usdtry()
    if (
        ounce is None
        or
        usdtry is None
    ):
        return None
    gram_gold = (
        ounce
        / 31.1035
    ) * usdtry
    return round(
        gram_gold,
        2
    )
