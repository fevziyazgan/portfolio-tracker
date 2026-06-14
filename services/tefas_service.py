import requests
BASE_URL = (
    "https://www.tefas.gov.tr/"
    "FonAnaliz.aspx"
)
def test_connection(
    fund_code
):
    try:
        response = requests.get(
            f"{BASE_URL}?FonKod={fund_code}",
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
    funds = [
        "IPV",
        "PHE",
        "TMV",
        "TLY"
    ]
    result = {}
    for code in funds:
        result[code] = (
            test_connection(code)
        )
    return result
