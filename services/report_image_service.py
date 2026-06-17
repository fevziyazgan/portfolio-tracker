import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from services.chart_service import (
    create_portfolio_performance_chart,
    create_allocation_breakdown_chart,
    create_crypto_performance_chart
)

WIDTH = 1800
HEIGHT = 5200


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
        "Altin",
        "Kripto",
        "Mevduat"
    ]
    
    colors = [
        "#2563EB",
        "#EAB308",
        "#F97316",
        "#10B981"
    ]

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        startangle=90,
        wedgeprops={
            "width": 0.35
        },
        autopct='%1.1f%%',
        textprops={'fontsize': 10}
    )
    
    # Yüzde metinlerini beyaza boya
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_aspect(
        "equal"
    )

    plt.savefig(
        "donut_chart.png",
        transparent=True,
        bbox_inches="tight",
        dpi=150
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
    
    create_allocation_breakdown_chart(
        report_data
    )
    
    create_crypto_performance_chart()
    
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
    f"{cash['current_value']:,.0f} TL",
    "#10B981",
    f"%{cash_pct:.2f}",
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
    f"■ Fonlar\n{summary['fund_total_tl']:,.0f} TL\n({fund_pct:.1f}%)",
    fill="#2563EB",
    font=get_font(24)
    )
    
    legend_y += 100
    
    draw.text(
    (legend_x, legend_y),
    f"■ Altın\n{summary['gold_total_tl']:,.0f} TL\n({gold_pct:.1f}%)",
    fill="#EAB308",
    font=get_font(24)
    )
    
    legend_y += 100
    
    draw.text(
    (legend_x, legend_y),
    f"■ Kripto\n{summary['crypto_total_tl']:,.0f} TL\n({crypto_pct:.1f}%)",
    fill="#F97316",
    font=get_font(24)
    )
    
    legend_y += 100

    cash = report_data[
    "cash_interest"
    ]
    
    draw.text(
    (legend_x, legend_y),
    f"■ Mevduat\n{cash['current_value']:,.0f} TL\n({cash_pct:.1f}%)",
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
        fill="red",
        font=section_font
    )

    y += 45
    
    draw.text((50, y), "BANKA", fill="black", font=get_font(20))
    draw.text((150, y), "DEGER", fill="black", font=get_font(20))
    draw.text((350, y), "GUNLUK", fill="black", font=get_font(20))
    draw.text((500, y), "AYLIK", fill="black", font=get_font(20))
    draw.text((650, y), "PORTFÖY %", fill="black", font=get_font(20))
    y += 35
    draw.line((50, y, 900, y), fill="#CCCCCC", width=2)
    y += 15
    
    draw.text(
        (50, y ),
        cash["bank"],
        fill="black",
        font=get_font(22)
    )
    
    draw.text(
        (150, y ),
        f"{cash['current_value']:,.0f} TL",
        fill="black",
        font=get_font(22)
    )
    
    draw.text(
        (350, y ),
        f"+{cash['daily_interest']:,.0f} TL",
        fill="#10B981",
        font=get_font(22)
    )
    
    draw.text(
        (500, y ),
        f"+{cash['monthly_interest']:,.0f} TL",
        fill="#10B981",
        font=get_font(22)
    )
    
    draw.text(
        (650, y ),
        f"%{cash['portfolio_pct']:.2f}",
        fill="#10B981",
        font=get_font(22)
    )
    
    y += 60

    
    draw.text(
        (
            30,
            y
        ),
        "ALTIN",
        fill="red",
        font=section_font
    )

    y += 45
    draw.text((50, y), "KOD", fill="black", font=get_font(20))
    draw.text((150, y), "DEGER", fill="black", font=get_font(20))
    draw.text((350, y), "GUNLUK", fill="black", font=get_font(20))
    draw.text((500, y), "30 GUN", fill="black", font=get_font(20))
    draw.text((650, y), "PORTFÖY %", fill="black", font=get_font(20))
    
    y += 35
    draw.line((50, y, 900, y), fill="#CCCCCC", width=2)
    y += 15
    
    gold = report_data[
        "gold"
    ]

    draw.text(
        (50, y),
        "GOLD",
        fill="black",
        font=get_font(22)
    )
    
    draw.text(
        (150, y),
        f"{gold['value']:,.0f} TL",
        fill="black",
        font=get_font(22)
    )
    
    draw.text(
        (350, y),
        f"{gold['daily_pct']:.2f}%",
        fill="#16A34A" if gold["daily_pct"] >= 0 else "#DC2626",
        font=get_font(22)
    )
    
    draw.text(
        (500, y),
        f"{gold['monthly_pct']:.2f}%",
        fill="#16A34A" if gold["monthly_pct"] >= 0 else "#DC2626",
        font=get_font(22)
    )
    
    draw.text(
        (650, y),
        f"{gold['portfolio_pct']:.2f}%",
        fill="#EAB308",
        font=get_font(22)
    )

    y += 60

    draw.text(
        (
            30,
            y
        ),
        "FON PORTFOYU",
        fill="red",
        font=section_font
    )

    y += 50

    draw.text((50, y), "KOD", fill="black", font=get_font(20))
    draw.text((150, y), "DEGER", fill="black", font=get_font(20))
    draw.text((350, y), "GUNLUK", fill="black", font=get_font(20))
    draw.text((500, y), "30 GUN", fill="black", font=get_font(20))
    draw.text((650, y), "PORTFÖY %", fill="black", font=get_font(20))
    
    y += 35
    draw.line((50, y, 900, y), fill="#CCCCCC", width=2)
    y += 15
    for fund in report_data["funds"]:
    
        draw.text(
            (50, y),
            fund["code"],
            fill="black",
            font=get_font(20)
        )
    
        draw.text(
            (150, y),
            f"{fund['value']:,.0f} TL",
            fill="black",
            font=get_font(20)
        )
    
        draw.text(
            (350, y),
            f"{fund['daily_pct']:.2f}%",
            fill="#16A34A" if fund["daily_pct"] >= 0 else "#DC2626",
            font=get_font(20)
        )
    
        draw.text(
            (500, y),
            f"{fund['monthly_pct']:.2f}%",
            fill="#16A34A" if fund["monthly_pct"] >= 0 else "#DC2626",
            font=get_font(20)
        )
    
        draw.text(
            (650, y),
            f"{fund['portfolio_pct']:.2f}%",
            fill="#2563EB",
            font=get_font(20)
        )
    
        y += 60

    draw.text(
        (
            30,
            y
        ),
        "KRIPTO PORTFOYU",
        fill="red",
        font=section_font
    )

    y += 50

    draw.text((50, y), "KOD", fill="black", font=get_font(20))
    draw.text((150, y), "DEGER", fill="black", font=get_font(20))
    draw.text((350, y), "GUNLUK", fill="black", font=get_font(20))
    draw.text((500, y), "30 GUN", fill="black", font=get_font(20))
    draw.text((650, y), "PORTFÖY %", fill="black", font=get_font(20))
    
    y += 35
    draw.line((50, y, 900, y), fill="#CCCCCC", width=2)
    y += 15

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
            font=get_font(20)
        )

        draw.text(
            (
                150,
                y
            ),
            f"{crypto['value_tl']:,.0f} TL",
            fill="black",
            font=get_font(20)
        )

        draw.text(
        (350, y),
        f"{crypto['daily_pct']:.2f}%",
        fill="#16A34A" if crypto["daily_pct"] >= 0 else "#DC2626",
        font=get_font(20)
        )
        
        draw.text(
            (500, y),
            f"{crypto['monthly_pct']:.2f}%",
            fill="#16A34A" if crypto["monthly_pct"] >= 0 else "#DC2626",
            font=get_font(20)
        )
        
        draw.text(
            (650, y),
            f"{crypto['portfolio_pct']:.2f}%",
            fill="#F97316",
            font=get_font(20)
        )
        
        y += 30
        
    y += 60

    draw.text(
        (
            30,
            y
        ),
        "PERFORMANS GRAFIKLERI",
        fill="red",
        font=section_font
    )
    
    y += 50
    
    # Üst grafik - Portföy Dağılımı
    draw.text(
        (
            30,
            y
        ),
        "PORTFÖY DAĞILIMI",
        fill="#333333",
        font=get_font(28)
    )
    
    y += 40
    
    allocation_chart = Image.open(
        "allocation_breakdown_chart.png"
    ).convert(
        "RGBA"
    )

    allocation_chart = allocation_chart.resize(
        (
            1650,
            750
        )
    )

    image.paste(
        allocation_chart,
        (
            40,
            y
        ),
        allocation_chart
    )
    
    y += 800
    
    # Alt grafik - Kriptolar tek tek
    draw.text(
        (
            30,
            y
        ),
        "KRİPTO PERFORMANSI",
        fill="#333333",
        font=get_font(28)
    )

    y += 40
    
    crypto_chart = Image.open(
        "crypto_performance_chart.png"
    ).convert(
        "RGBA"
    )

    crypto_chart = crypto_chart.resize(
        (
            1650,
            750
        )
    )

    image.paste(
        crypto_chart,
        (
            40,
            y
        ),
        crypto_chart
    )
    
    y += 800
    
    image.save(
        output_file
    )

    return output_file
