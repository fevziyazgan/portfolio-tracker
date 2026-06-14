from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WIDTH = 1200
PADDING = 30


def get_font(size):
    try:
        return ImageFont.truetype(
            "DejaVuSans.ttf",
            size
        )
    except Exception:
        return ImageFont.load_default()


def draw_card(
    draw,
    x,
    y,
    w,
    h,
    title,
    value
):
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=20,
        fill="#f5f7fa",
        outline="#d8dee9",
        width=2
    )

    title_font = get_font(22)
    value_font = get_font(34)

    draw.text(
        (x + 20, y + 15),
        title,
        fill="#666666",
        font=title_font
    )

    draw.text(
        (x + 20, y + 55),
        value,
        fill="#111111",
        font=value_font
    )


def create_report_image(
    report_data,
    output_file="report.png"
):
    height = 1800

    image = Image.new(
        "RGB",
        (WIDTH, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    title_font = get_font(48)
    date_font = get_font(24)
    section_font = get_font(28)
    text_font = get_font(24)

    y = 30

    draw.text(
        (PADDING, y),
        "PORTFOY RAPORU",
        fill="black",
        font=title_font
    )

    y += 60

    draw.text(
        (PADDING, y),
        report_data["date"],
        fill="#666666",
        font=date_font
    )

    y += 60

    summary = report_data["summary"]

    draw_card(
        draw,
        30,
        y,
        260,
        120,
        "Toplam",
        f"{summary['total_value_tl']:,.0f} TL"
    )

    draw_card(
        draw,
        320,
        y,
        260,
        120,
        "Fonlar",
        f"{summary['fund_total_tl']:,.0f} TL"
    )

    draw_card(
        draw,
        610,
        y,
        260,
        120,
        "Kripto",
        f"{summary['crypto_total_tl']:,.0f} TL"
    )

    draw_card(
        draw,
        900,
        y,
        260,
        120,
        "Altin",
        f"{summary['gold_total_tl']:,.0f} TL"
    )

    y += 180

    draw.text(
        (30, y),
        "FON PORTFOYU",
        fill="black",
        font=section_font
    )

    y += 50

    for fund in report_data["funds"]:

        draw.text(
            (50, y),
            fund["code"],
            fill="black",
            font=text_font
        )

        draw.text(
            (900, y),
            f"{fund['value']:,.0f} TL",
            fill="black",
            font=text_font
        )

        y += 35

    y += 40

    draw.text(
        (30, y),
        "KRIPTO PORTFOYU",
        fill="black",
        font=section_font
    )

    y += 50

    for crypto in report_data["cryptos"]:

        draw.text(
            (50, y),
            crypto["symbol"],
            fill="black",
            font=text_font
        )

        draw.text(
            (900, y),
            f"{crypto['value']:,.2f} USD",
            fill="black",
            font=text_font
        )

        y += 35

    y += 40

    draw.text(
        (30, y),
        "PIYASA",
        fill="black",
        font=section_font
    )

    y += 50

    market = report_data["market"]

    draw.text(
        (50, y),
        f"USDTRY : {market['usdtry']}",
        fill="black",
        font=text_font
    )

    y += 35

    draw.text(
        (50, y),
        f"BIST100 : {market['bist100']}",
        fill="black",
        font=text_font
    )

    y += 35

    draw.text(
        (50, y),
        f"US10Y : {market['us10y']}",
        fill="black",
        font=text_font
    )

    image.save(output_file)

    return output_file
