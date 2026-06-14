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
    try:
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
            "code":
            latest.get(
                "fonKodu"
            ),
            "date":
            latest.get(
                "tarih"
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
            )
        }
    except Exception as e:
        print(
            f"TEFAS ERROR {fund_code}:",
            e
        )
        return None
def get_fund_initial_cost(
    fund_code
):
    """
    İlk çalıştırmada
    maliyet atamak için
    güncel fiyat döndürür.
    """
    data = get_fund_price(
        fund_code
    )
    if not data:
        return None
    return data[
        "price"
    ]
def test_funds():
    result = {}
    for code in [
        "IPV",
        "PHE",
        "TMV",
        "TLY"
    ]:
        result[
            code
        ] = get_fund_price(
            code
        )
    return result
