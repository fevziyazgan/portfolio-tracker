import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
WIDTH = 1200

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
        "#2563EB",  # mavi
        "#F97316",  # turuncu
        "#EAB308"   # sari
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
            "width": 0.40
        }
    )
    ax.set_aspect(
        "equal"
    )
    plt.savefig(
        "donut_chart.png",
        bbox_inches="tight",
        transparent=True
    )
    plt.close()
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
        fill="#111111",
        font=get_font(28)
    )
def create_report_image(
    report_data,
    output_file="report.png"
):
    image = Image.new(
        "RGB",
        (
            WIDTH,
            2500
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
    
    create_donut_chart(
    report_data
    )
    
    draw_card(
        draw,
        30,
        y,
        360,
        120,
        "Toplam",
        f"{summary['total_value_tl']:,.0f} TL"
    )
    draw_card(
        draw,
        420,
        y,
        360,
        120,
        "Fonlar",
        f"{summary['fund_total_tl']:,.0f} TL"
    )
    draw_card(
        draw,
        810,
        y,
        360,
        120,
        "Kripto",
        f"{summary['crypto_total_tl']:,.0f} TL"
    )
    y += 150
    draw_card(
        draw,
        30,
        y,
        360,
        120,
        "Altin",
        f"{summary['gold_total_tl']:,.0f} TL"
    )
    draw_card(
        draw,
        420,
        y,
        360,
        120,
        "Maliyet",
        f"{summary['total_cost_tl']:,.0f} TL"
    )
    draw_card(
        draw,
        810,
        y,
        360,
        120,
        "Kar/Zarar",
        f"{summary['profit_tl']:,.0f} TL"
    )
    
y += 190 

donut = Image.open( "donut_chart.png" ).convert( "RGBA" ) 

donut = donut.resize( ( 350, 350 ) ) 

image.paste( donut, ( 780, y - 20 ), donut )
    
donut = donut.resize(
    (
        350,
        350
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
        (
            f"{gold['grams']} gram | "
            f"{gold['price']:,.2f} TL/gr"
        ),
        fill="black",
        font=text_font
    )
    draw.text(
        (
            850,
            y
        ),
        (
            f"{gold['value']:,.0f} TL"
        ),
        fill="black",
        font=text_font
    )
    y += 70
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
            (
                f"{fund['code']} | "
                f"{fund['quantity']} adet"
            ),
            fill="black",
            font=text_font
        )
        draw.text(
            (
                550,
                y
            ),
            (
                f"{fund['price']:,.4f}"
            ),
            fill="black",
            font=text_font
        )
        draw.text(
            (
                850,
                y
            ),
            (
                f"{fund['value']:,.0f} TL"
            ),
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
            (
                f"{crypto['symbol']} | "
                f"{round(crypto['quantity'], 2)} adet"
            ),
            fill="black",
            font=text_font
        )
        draw.text(
            (
                550,
                y
            ),
            (
                f"{crypto['value']:,.2f} USD"
            ),
            fill="black",
            font=text_font
        )
        draw.text(
            (
                850,
                y
            ),
            (
                f"{crypto['value_tl']:,.0f} TL"
            ),
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
        "PIYASA",
        fill="black",
        font=section_font
    )
    y += 50
    market = report_data[
        "market"
    ]
    draw.text(
        (
            50,
            y
        ),
        (
            f"USDTRY : {market['usdtry']}"
        ),
        fill="black",
        font=text_font
    )
    y += 35
    draw.text(
        (
            50,
            y
        ),
        (
            f"BIST100 : {market['bist100']}"
        ),
        fill="black",
        font=text_font
    )
    y += 35
    draw.text(
        (
            50,
            y
        ),
        (
            f"US10Y : {market['us10y']}"
        ),
        fill="black",
        font=text_font
    )
    y += 35
    draw.text(
        (
            50,
            y
        ),
        (
            f"Gram Altin : "
            f"{market['gram_gold']}"
        ),
        fill="black",
        font=text_font
    )
    image.save(
        output_file
    )
    return output_file
