import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from services.chart_service import (
    create_portfolio_performance_chart
)

WIDTH = 1800
HEIGHT = 5000


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
    image,
    x,
    y,
    w,
    h,
    title,
    value,
    value_color="#111111",
    subtitle=None,
    icon_path=None
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

    if icon_path:

        icon = Image.open(
            icon_path
        ).convert(
            "RGBA"
        )

        icon = icon.resize(
            (
                48,
                48
            )
        )

        image.paste(
            icon,
            (
                x + 20,
                y + 20
            ),
            icon
        )

    draw.text(
        (
            x + 85,
            y + 25
        ),
        title,
        fill="#666666",
        font=get_font(22)
    )

    draw.text(
        (
            x + 20,
            y + 70
        ),
        value,
        fill=value_color,
        font=get_font(34)
    )

    if subtitle:

        draw.text(
            (
                x + 20,
                y + 125
            ),
            subtitle,
            fill=value_color,
            font=get_font(20)
        )

def create_donut_chart(
    report_data
):

    summary = report_data[
        "summary"
    ]

    values = [
        summary["fund_total_tl"],
        summary["crypto_total_tl"],
        summary["gold_total_tl"],
        summary.get("deposit_total_tl", 0)
    ]
    
    labels = [
        "Fon",
        "Kripto",
        "Altin",
        "Mevduat"
    ]
    
    colors = [
        "#2563EB",
        "#F97316",
        "#EAB308",
        "#10B981"
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

    title_font = get_font(64)
    section_font = get_font(42)
    text_font = get_font(30)

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

    total = max(
    summary["total_value_tl"],
    1
    )
    
    fund_pct = (
        summary["fund_total_tl"]
        / total
    ) * 100
    
    crypto_pct = (
        summary["crypto_total_tl"]
        / total
    ) * 100
    
    gold_pct = (
        summary["gold_total_tl"]
        / total
    ) * 100

    deposit_pct = (
    summary.get("deposit_total_tl", 0)
    / total
    ) * 100
    
    y += 10
    
    draw_card(
        draw,
        image,
        40,
        y,
        400,
        180,
        "TOPLAM DEGER",
        f"{summary['total_value_tl']:,.0f} TL",
        "#16A34A",
        None,
        "icons/money.png"
    )

    daily_tl = perf["daily"]["change_tl"]

    daily_pct = perf["daily"]["change_pct"]
    
    draw_card(
        draw,
        image,
        480,
        y,
        400,
        180,
        "GUNLUK DEGISIM",
        f"{perf['daily']['change_tl']:,.0f} TL",
        "#16A34A",
        f"{perf['daily']['change_pct']:.2f}%",
        "icons/chart.png"
    )
    
    draw_card(
        draw,
        image,
        920,
        y,
        400,
        180,
        "30 GUNLUK DEGISIM",
        f"{perf['monthly']['change_tl']:,.0f} TL",
        "#16A34A",
        f"{perf['monthly']['change_pct']:.2f}%",
        "icons/calendar.png"
    )

    if summary["total_cost_tl"] > 0:
    
        profit_pct = (
            summary["profit_tl"]
            /
            summary["total_cost_tl"]
        ) * 100
    
    else:

        profit_pct = 0
    
    draw_card(
        draw,
        image,
        1360,
        y,
        400,
        180,
        "KAR / ZARAR",
        f"{summary['profit_tl']:,.0f} TL",
        "#16A34A",
        f"{profit_pct:.2f}%",
        "icons/profit.png"
    )
    
    y += 200

    draw_card(
    draw,
    image,
    40,
    y,
    400,
    180,
    "FONLAR",
    f"{summary['fund_total_tl']:,.0f} TL",
    "#2563EB",
    f"%{fund_pct:.2f}",
    "icons/fund.png"
    )

    draw_card(
    draw,
    image,
    480,
    y,
    400,
    180,
    "KRIPTO",
    f"{summary['crypto_total_tl']:,.0f} TL",
    "#F97316",
    f"%{crypto_pct:.2f}",
    "icons/bitcoin.png"
    )

    draw_card(
    draw,
    image,
    920,
    y,
    400,
    180,
    "ALTIN",
    f"{summary['gold_total_tl']:,.0f} TL",
    "#EAB308",
    f"%{gold_pct:.2f}",
    "icons/gold.png"
    )

    draw_card(
    draw,
    image,
    1360,
    y,
    400,
    180,
    "MEVDUAT",
    f"{summary.get('deposit_total_tl',0):,.0f} TL",
    "#10B981",
    f"%{deposit_pct:.2f}",
    "icons/wallet.png"
    )
    
    donut = Image.open(
        "donut_chart.png"
    ).convert(
        "RGBA"
    )

    donut = donut.resize(
        (
            700,
            700
        )
    )

    image.paste(
        donut,
        (
            1100,
            y + 140
        ),
        donut
    )

    legend_x = 1180
    legend_y = y + 780
    
    draw.text(
        (legend_x, legend_y),
        f"■ Fonlar    %{fund_pct:.1f}",
        fill="#2563EB",
        font=get_font(28)
    )
    
    legend_y += 45
    
    draw.text(
        (legend_x, legend_y),
        f"■ Altin     %{gold_pct:.1f}",
        fill="#EAB308",
        font=get_font(28)
    )
    
    legend_y += 45
    
    draw.text(
        (legend_x, legend_y),
        f"■ Kripto    %{crypto_pct:.1f}",
        fill="#F97316",
        font=get_font(28)
    )
    
    legend_y += 45
    
    draw.text(
        (legend_x, legend_y),
        f"■ Mevduat   %{deposit_pct:.1f}",
        fill="#10B981",
        font=get_font(28)
    )

    
    y += 200

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

    draw.text((20, y), "KOD", fill="black", font=get_font(24))
    draw.text((110, y), "DEGER", fill="black", font=get_font(24))
    draw.text((420, y), "GUNLUK", fill="black", font=get_font(24))
    draw.text((590, y), "30 GUN", fill="black", font=get_font(24))
    draw.text((760, y), "%", fill="black", font=get_font(24))
    
    y += 40
    draw.line((50, y, 1300, y), fill="#CCCCCC", width=2)
    y += 20
    for fund in report_data["funds"]:
    
        draw.text(
            (20, y),
            fund["code"],
            fill="black",
            font=text_font
        )
    
        draw.text(
            (110, y),
            f"{fund['value']:,.0f}",
            fill="black",
            font=text_font
        )
    
        draw.text(
            (420, y),
            f"{fund['daily_pct']:.2f}%",
            fill="#16A34A" if fund["daily_pct"] >= 0 else "#DC2626",
            font=text_font
        )
    
        draw.text(
            (590, y),
            f"{fund['monthly_pct']:.2f}%",
            fill="#16A34A" if fund["monthly_pct"] >= 0 else "#DC2626",
            font=text_font
        )
    
        draw.text(
            (760, y),
            f"{fund['portfolio_pct']:.2f}",
            fill="#2563EB",
            font=text_font
        )
    
        y += 40

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
            1650,
            800
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
