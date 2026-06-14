import json
import requests
CONFIG_FILE = "config/sources.json"
def load_sources():
    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)
def get_fund_codes():
    sources = load_sources()
    result = []
    for code, info in sources.items():
        if (
            info.get("provider")
            == "tefas"
        ):
            result.append(code)
    return result
def test_connection(
    fund_code
):
    try:
        response = requests.get(
            (
                "https://www.tefas.gov.tr/"
                f"FonAnaliz.aspx?FonKod={fund_code}"
            ),
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )
        return {
            "success": True,
            "status_code":
                response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
def test_funds():
    result = {}
    for code in get_fund_codes():
        result[code] = (
            test_connection(code)
        )
    return result
def get_price(
    fund_code
):
    """
    Geçici.
    Gerçek TEFAS endpointi
    bulunduğunda sadece bu
    fonksiyon değişecek.
    """
    return {
        "code": fund_code,
        "price": None
    }
