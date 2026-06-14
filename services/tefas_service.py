import requests


def get_fund_price(fund_code):

    url = (
        "https://www.tefas.gov.tr"
        "/api/funds/fonFiyatBilgiGetir"
    )

    payload = {
        "fonKodu": fund_code,
        "dil": "TR",
        "periyod": 1
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0",
                "Accept":
                "application/json"
            }
        )

        print(
            f"\nFUND: {fund_code}"
        )

        print(
            "STATUS:",
            response.status_code
        )

        print(
            response.text[:1000]
        )

        return response.json()

    except Exception as e:

        print(
            f"{fund_code} ERROR:",
            e
        )

        return None


def test_funds():

    result = {}

    for code in [
        "IPV",
        "PHE",
        "TMV",
        "TLY"
    ]:

        result[code] = get_fund_price(
            code
        )

    return result
