import requests
BASE_URL = "https://www.tefas.gov.tr/FonAnaliz.aspx"
def test_connection(fund_code):
    try:
        response = requests.get(
            f"{BASE_URL}?FonKod={fund_code}",
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        return {
            "success": True,
            "status_code": response.status_code
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
    results = {}
    for code in funds:
        results[code] = test_connection(
            code
        )
    return results
def get_fund_price(fund_code):
    """
    Geçici fonksiyon.
    Gerçek TEFAS veri endpointi
    bulunduğunda bu fonksiyon
    güncellenecek.
    """
    result = test_connection(
        fund_code
    )
    if not result["success"]:
        return None
    return {
        "fund_code": fund_code,
        "price": None,
        "status_code":
            result["status_code"]
    }
