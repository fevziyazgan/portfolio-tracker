import yfinance as yf
def get_price(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(
            period="5d"
        )
        if len(hist) == 0:
            return None
        return round(
            float(
                hist["Close"].iloc[-1]
            ),
            4
        )
    except Exception as e:
        print(
            f"YAHOO ERROR {ticker}: {e}"
        )
        return None
