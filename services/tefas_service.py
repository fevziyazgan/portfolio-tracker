import json
import time
import requests

BASE_URL = (
    "https://www.tefas.gov.tr"
    "/api/funds/fonFiyatBilgiGetir"
)

ASSETS_FILE = (
    "config/assets.json"
)


def load_assets():

    with open(
        ASSETS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def get_fund_codes():

    assets = load_assets()

    return list(
        assets.get(
            "funds",
            {}
        ).keys()
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

    for attempt in range(3):

        try:

            response = requests.post(
                BASE_URL,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            data = response.json()

            import json

            print(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )
)
            
            result_list = data.get(
                "resultList",
                []
            )

            if not result_list:

                print(
                    f"TEFAS VERISI BULUNAMADI: "
                    f"{fund_code}"
                )

                return None

            latest = result_list[-1]

            return {
                "code":
                latest.get(
                    "fonKodu",
                    fund_code.upper()
                ),

                "date":
                latest.get(
                    "tarih",
                    ""
                ),

                "price":
                float(
                    latest.get(
                        "fiyat",
                        0
                    )
                ),

                "name":
                latest.get(
                    "fonUnvan",
                    ""
                ).strip()
            }

        except Exception as e:

            print(
                f"TEFAS ERROR "
                f"{fund_code} "
                f"(TRY {attempt + 1}/3): "
                f"{e}"
            )

            time.sleep(2)

    print(
        f"TEFAS FAILED: "
        f"{fund_code}"
    )

    return None


def test_tefas():

    result = {}

    for fund in get_fund_codes():

        result[
            fund
        ] = get_fund_price(
            fund
        )

    return result
