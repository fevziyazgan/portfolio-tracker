import requests

BASE_URL = (
    "https://www.tefas.gov.tr"
    "/api/funds/fonFiyatBilgiGetir"
)


def get_fund_price(fund_code):

    payload = {
        "fonKodu": fund_code.upper(),
        "dil": "TR",
        "periyod": 1
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        timeout=30,
        headers={
            "User-Agent":
            "Mozilla/5.0",
            "Accept":
            "application/json"
        }
    )

    response.raise_for_status()

    data = response.json()

    result_list = data.get(
        "resultList",
        []
    )

    if not result_list:
        return None

    latest = result_list[-1]

    return {
        "code": latest["fonKodu"],
        "date": latest["tarih"],
        "price": float(
            latest["fiyat"]
        ),
        "name": latest.get(
            "fonUnvan",
            ""
        )
    }


def test_funds():

    result = {}

    for code in [
        "IPV",
        "PHE",
        "TMV",
        "TLY"
    ]:

        try:

            result[code] = (
                get_fund_price(
                    code
                )
            )

        except Exception as e:

            result[code] = {
                "error": str(e)
            }

    return result
