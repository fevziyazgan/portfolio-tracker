import time
import requests

BASE_URL = (
    "https://www.tefas.gov.tr"
    "/api/funds/fonFiyatBilgiGetir"
)


def get_fund_price(
    fund_code
):

    payload = {
        "fonKodu": fund_code.upper(),
        "dil": "TR",
        "periyod": 1
    }

    headers = {
        "User-Agent":
        "Mozilla/5.0",
        "Accept":
        "application/json"
    }

    for _ in range(3):

        try:

            response = requests.post(
                BASE_URL,
                json=payload,
                headers=headers,
                timeout=30
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
                "code":
                latest["fonKodu"],

                "date":
                latest["tarih"],

                "price":
                float(
                    latest["fiyat"]
                ),

                "name":
                latest.get(
                    "fonUnvan",
                    ""
                )
            }

        except Exception:

            time.sleep(2)
    return None
