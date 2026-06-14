import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from services.chart_service import (
    create_portfolio_performance_chart
)

WIDTH = 1600
HEIGHT = 4200


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
    value,
    value_color
):

    draw.rounded_rectangle(
        (
            x,
            y,
            x + w,
            y + h
        ),
        radius=20,
        fill="#f5f7fa",
        outline="#d8dee9",
        width=2
    )

    draw.text(
        (
            x + 20,
            y + 15
        ),
        title,
        fill="#666666",
        font=get_font(22)
    )

    draw.text(
        (
            x + 20,
            y + 55
        ),
        value,
        fill=value_color,
        font=get_font(28)
    )


def create_donut_chart(
    report_data
):

    summary = report_data[
        "summary"
    ]

    values = [
        summary[
            "fund_total_tl"
        ],
        summary[
            "crypto_total_tl"
        ],
        summary[
            "gold_total_tl"
        ]
    ]

    labels = [
        "Fon",
        "Kripto",
        "Altin"
    ]

    colors = [
        "#2563EB",
        "#F97316",
        "#EAB308"
    ]

    fig, ax = plt.subplots(
        figsize=(4, 4)
    )

    ax.pie(
        values,
        labels=labels,
        colors=colors,
        startangle=90,
        wedgeprops={
            "width": 0.45
        }
    )

    ax.set_aspect(
        "equal"
    )

    plt.savefig(
        "donut_chart.png",
        transparent=True,
        bbox_inches="tight"
    )

    plt.close()


def create_report_image(
    report_data,
    output_file="report.png"
):

    create_donut_chart(
        report_data
    )
    
    create_portfolio_performance_chart()
    
    image = Image.new(
        "RGB",
        (
            WIDTH,
            HEIGHT
        ),
        "white"
    )

    draw = ImageDraw.Draw(
        image
    )

    title_font = get_font(48)
    section_font = get_font(30)
    text_font = get_font(22)

    y = 30

    draw.text(
        (
            30,
            y
        ),
        "PORTFOY RAPORU",
        fill="black",
        font=title_font
    )

    y += 60

    draw.text(
        (
            30,
            y
        ),
        report_data["date"],
        fill="#666666",
        font=get_font(24)
    )

    y += 70

    summary = report_data[
        "summary"
    ]

    perf = report_data["performance"]
    
y += 170

draw_card(
    draw,
    40,
    y,
    340,
    140,
    "Fonlar",
    f"{summary['fund_total_tl']:,.0f} TL",
    "#2563EB"
)

draw_card(
    draw,
    430,
    y,
    340,
    140,
    "Kripto",
    f"{summary['crypto_total_tl']:,.0f} TL",
    "#F97316"
)

draw_card(
    draw,
    820,
    y,
    340,
    140,
    "Altin",
    f"{summary['gold_total_tl']:,.0f} TL",
    "#EAB308"
)

draw_card(
    draw,
    1210,
    y,
    340,
    140,
    "Maliyet",
    f"{summary['total_cost_tl']:,.0f} TL",
    "#6B7280"
)

y += 200

    
    y += 190

    donut = Image.open(
        "donut_chart.png"
    ).convert(
        "RGBA"
    )

    donut = donut.resize(
        (
            500,
            500
        )
    )

    image.paste(
        donut,
        (
            780,
            y - 20
        ),
        donut
    )

    y += 50

    draw.text(
        (
            40,
            y
        ),
        "PORTFOY DAGILIMI",
        fill="black",
        font=section_font
    )

    y += 50

    draw.text(
        (
            50,
            y
        ),
        f"Fonlar %{summary['fund_total_tl'] / total * 100:.1f}",
        fill="#2563EB",
        font=text_font
    )

    y += 35

    draw.text(
        (
            50,
            y
        ),
        f"Kripto %{summary['crypto_total_tl'] / total * 100:.1f}",
        fill="#F97316",
        font=text_font
    )

    y += 35

    draw.text(
        (
            50,
            y
        ),
        f"Altin %{summary['gold_total_tl'] / total * 100:.1f}",
        fill="#EAB308",
        font=text_font
    )

    y += 90

    draw.text(
        (
            30,
            y
        ),
        "ALTIN",
        fill="black",
        font=section_font
    )

    y += 45

    gold = report_data[
        "gold"
    ]

    draw.text(
        (
            50,
            y
        ),
        f"{gold['grams']} gram",
        fill="black",
        font=text_font
    )

    draw.text(
        (
            850,
            y
        ),
        f"{gold['value']:,.0f} TL",
        fill="black",
        font=text_font
    )

    y += 80

    draw.text(
        (
            30,
            y
        ),
        "FON PORTFOYU",
        fill="black",
        font=section_font
    )

    y += 50

    for fund in report_data[
        "funds"
    ]:

        draw.text(
            (
                50,
                y
            ),
            fund["code"],
            fill="black",
            font=text_font
        )

        draw.text(
            (
                850,
                y
            ),
            f"{fund['value']:,.0f} TL",
            fill="black",
            font=text_font
        )

        y += 35

    y += 50

    draw.text(
        (
            30,
            y
        ),
        "KRIPTO PORTFOYU",
        fill="black",
        font=section_font
    )

    y += 50

    for crypto in report_data[
        "cryptos"
    ]:

        draw.text(
            (
                50,
                y
            ),
            crypto["symbol"],
            fill="black",
            font=text_font
        )

        draw.text(
            (
                850,
                y
            ),
            f"{crypto['value_tl']:,.0f} TL",
            fill="black",
            font=text_font
        )

        y += 35
        
    y += 80

    draw.text(
        (
            30,
            y
        ),
        "30 GUNLUK PERFORMANS",
        fill="black",
        font=section_font
    )
    
    y += 50
    
    chart = Image.open(
        "performance_chart.png"
    )
    
    chart = chart.resize(
        (
            1500,
            600
        )
    )
    
    image.paste(
        chart,
        (
            40,
            y
        )
    )
    
    y += 430
    
    image.save(
        output_file
    )

    return output_file
