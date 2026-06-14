import requests


def test_funds():

    funds = [
        "IPV",
        "PHE",
        "TMV",
        "TLY"
    ]

    result = {}

    print("\n===== TEFAS API TEST =====\n")

    for fund in funds:

        url = (
            f"https://www.tefas.gov.tr/api/funds/{fund}"
        )

        try:

            response = requests.get(
                url,
                timeout=30,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            print("\nURL:", url)
            print(
                "STATUS:",
                response.status_code
            )

            print(
                response.text[:500]
            )

            result[fund] = {
                "success":
                response.status_code == 200,
                "status_code":
                response.status_code
            }

        except Exception as e:

            print(
                f"{fund} ERROR:",
                e
            )

            result[fund] = {
                "success": False,
                "error": str(e)
            }

    return result
