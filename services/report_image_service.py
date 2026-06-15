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

    cash = report_data[
        "cash_interest"
    ]

    values = [
        summary["fund_total_tl"],
        summary["gold_total_tl"],
        summary["crypto_total_tl"],
        cash["current_value"]
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
            "width": 0.35
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

    cash = report_data[
        "cash_interest"
    ]
    
    cash_pct = (
        cash["current_value"]
        / total
        * 100
    ) if total else 0
    
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

    center_x = 1450
    center_y = y + 490
    
    draw.text(
        (
            center_x - 60,
            center_y - 35
        ),
        "TOPLAM",
        fill="#666666",
        font=get_font(24)
    )
    
    draw.text(
        (
            center_x - 100,
            center_y + 10
        ),
        f"{summary['total_value_tl']:,.0f} TL",
        fill="#111111",
        font=get_font(30)
    )
    
    legend_x = 1280
    legend_y = y + 780
    
    draw.text(
    (legend_x, legend_y),
    f"■ Fonlar\n{summary['fund_total_tl']:,.0f} TL (%{fund_pct:.1f})",
    fill="#2563EB",
    font=get_font(24)
    )
    
    legend_y += 80
    
    draw.text(
    (legend_x, legend_y),
    f"■ Altın\n{summary['gold_total_tl']:,.0f} TL (%{gold_pct:.1f})",
    fill="#EAB308",
    font=get_font(24)
    )
    
    legend_y += 80
    
    draw.text(
    (legend_x, legend_y),
    f"■ Kripto\n{summary['crypto_total_tl']:,.0f} TL (%{crypto_pct:.1f})",
    fill="#F97316",
    font=get_font(24)
    )
    
    legend_y += 80

    cash = report_data[
    "cash_interest"
    ]
    
    draw.text(
    (legend_x, legend_y),
    f"■ Mevduat\n{cash['current_value']:,.0f} TL (%{deposit_pct:.1f})",
    fill="#10B981",
    font=get_font(24)
    )

    
    y += 200

    cash = report_data[
    "cash_interest"
    ]
    
    values = [
    summary["fund_total_tl"],
    summary["gold_total_tl"],
    summary["crypto_total_tl"],
    cash["current_value"]
    ]

    colors = [
    "#2563EB",  # Fon
    "#EAB308",  # Altın
    "#F97316",  # Kripto
    "#10B981"   # Mevduat
    ]
    
    draw.text(
        (30, y),
        "MEVDUAT",
        fill="black",
        font=section_font
    )

    y += 45
    
    draw.text((50, y), "BANKA", fill="black", font=get_font(24))
    draw.text((180, y), "DEGER", fill="black", font=get_font(24))
    draw.text((450, y), "GUNLUK", fill="black", font=get_font(24))
    draw.text((620, y), "AYLIK", fill="black", font=get_font(24))
    draw.text((790, y), "PORTFÖY %", fill="black", font=get_font(24))
    y += 40
    draw.line((50, y, 1000, y), fill="#CCCCCC", width=2)
    y += 20
    
    draw.text(
        (50, y + 55),
        cash["bank"],
        fill="black",
        font=get_font(26)
    )
    
    draw.text(
        (180, y + 55),
        f"{cash['current_value']:,.0f} TL",
        fill="black",
        font=get_font(26)
    )
    
    draw.text(
        (450, y + 55),
        f"+{cash['daily_interest']:,.0f} TL",
        fill="#10B981",
        font=get_font(26)
    )
    
    draw.text(
        (620, y + 55),
        f"+{cash['monthly_interest']:,.0f} TL",
        fill="#10B981",
        font=get_font(26)
    )
    
    draw.text(
        (790, y + 55),
        f"%{cash['portfolio_pct']:.2f}",
        fill="#10B981",
        font=get_font(26)
    )
    
    y += 80

    
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
    draw.text((50, y), "KOD", fill="black", font=get_font(24))
    draw.text((180, y), "DEGER", fill="black", font=get_font(24))
    draw.text((450, y), "GUNLUK", fill="black", font=get_font(24))
    draw.text((620, y), "30 GUN", fill="black", font=get_font(24))
    draw.text((790, y), "PORTFÖY %", fill="black", font=get_font(24))
    
    y += 40
    draw.line((50, y, 1000, y), fill="#CCCCCC", width=2)
    y += 20
    
    gold = report_data[
        "gold"
    ]

    draw.text(
        (50, y),
        "GOLD",
        fill="black",
        font=text_font
    )
    
    draw.text(
        (180, y),
        f"{gold['value']:,.0f} TL",
        fill="black",
        font=text_font
    )
    
    draw.text(
        (450, y),
        f"{gold['daily_pct']:.2f}%",
        fill="#16A34A" if gold["daily_pct"] >= 0 else "#DC2626",
        font=text_font
    )
    
    draw.text(
        (620, y),
        f"{gold['monthly_pct']:.2f}%",
        fill="#16A34A" if gold["monthly_pct"] >= 0 else "#DC2626",
        font=text_font
    )
    
    draw.text(
        (790, y),
        f"{gold['portfolio_pct']:.2f}%",
        fill="#EAB308",
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

    draw.text((50, y), "KOD", fill="black", font=get_font(24))
    draw.text((180, y), "DEGER", fill="black", font=get_font(24))
    draw.text((450, y), "GUNLUK", fill="black", font=get_font(24))
    draw.text((620, y), "30 GUN", fill="black", font=get_font(24))
    draw.text((790, y), "PORTFÖY %", fill="black", font=get_font(24))
    
    y += 40
    draw.line((50, y, 1000, y), fill="#CCCCCC", width=2)
    y += 20
    for fund in report_data["funds"]:
    
        draw.text(
            (50, y),
            fund["code"],
            fill="black",
            font=text_font
        )
    
        draw.text(
            (180, y),
            f"{fund['value']:,.0f} TL",
            fill="black",
            font=text_font
        )
    
        draw.text(
            (450, y),
            f"{fund['daily_pct']:.2f}%",
            fill="#16A34A" if fund["daily_pct"] >= 0 else "#DC2626",
            font=text_font
        )
    
        draw.text(
            (620, y),
            f"{fund['monthly_pct']:.2f}%",
            fill="#16A34A" if fund["monthly_pct"] >= 0 else "#DC2626",
            font=text_font
        )
    
        draw.text(
            (790, y),
            f"{fund['portfolio_pct']:.2f}%",
            fill="#2563EB",
            font=text_font
        )
    
        y += 80

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

    draw.text((50, y), "KOD", fill="black", font=get_font(24))
    draw.text((180, y), "DEGER", fill="black", font=get_font(24))
    draw.text((450, y), "GUNLUK", fill="black", font=get_font(24))
    draw.text((620, y), "30 GUN", fill="black", font=get_font(24))
    draw.text((790, y), "PORTFÖY %", fill="black", font=get_font(24))
    
    y += 40
    draw.line((50, y, 1000, y), fill="#CCCCCC", width=2)
    y += 20

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
                180,
                y
            ),
            f"{crypto['value_tl']:,.0f} TL",
            fill="black",
            font=text_font
        )

        draw.text(
        (450, y),
        f"{crypto['daily_pct']:.2f}%",
        fill="#16A34A" if crypto["daily_pct"] >= 0 else "#DC2626",
        font=text_font
        )
        
        draw.text(
            (620, y),
            f"{crypto['monthly_pct']:.2f}%",
            fill="#16A34A" if crypto["monthly_pct"] >= 0 else "#DC2626",
            font=text_font
        )
        
        draw.text(
            (790, y),
            f"{crypto['portfolio_pct']:.2f}%",
            fill="#F97316",
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
