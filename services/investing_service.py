import requests

def test_page(url):

    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        },
        timeout=30
    )

    print(
        "STATUS:",
        response.status_code
    )

    print(
        "HTML LENGTH:",
        len(response.text)
    )

    print(
        response.text[:500]
    )
