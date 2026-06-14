#!/usr/bin/env python3
"""
Generate 8 minimal flat PNG dashboard icons
Size: 128x128 px with transparent background
Style: Bloomberg/TradingView dashboard
"""

from PIL import Image, ImageDraw
import os

# Create icons directory
os.makedirs('icons', exist_ok=True)

# Color palette
COLORS = {
    'green': '#16A34A',
    'blue': '#2563EB',
    'orange': '#F97316',
    'gold': '#EAB308',
    'gray': '#6B7280',
    'white': '#FFFFFF'
}

SIZE = 128
STROKE_WIDTH = 2.5


def create_icon(filename, color, draw_func):
    """Create a 128x128 transparent PNG icon"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw, color)
    filepath = f'icons/{filename}'
    img.save(filepath)
    print(f'✓ Created {filepath}')


def draw_money_icon(draw, color):
    """Dollar sign in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Dollar symbol
    cx, cy = SIZE // 2, SIZE // 2
    # Vertical line
    draw.line([(cx, cy - 22), (cx, cy + 22)], fill=COLORS['white'], width=int(STROKE_WIDTH))
    # Top curve
    draw.arc([(cx - 14, cy - 18), (cx + 14, cy - 8)], 0, 180, fill=COLORS['white'], width=int(STROKE_WIDTH))
    # Bottom curve
    draw.arc([(cx - 14, cy + 8), (cx + 14, cy + 18)], 0, 180, fill=COLORS['white'], width=int(STROKE_WIDTH))


def draw_chart_icon(draw, color):
    """Bar chart in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Bar chart
    bar_width = 14
    spacing = 8
    start_x = SIZE // 2 - 30
    base_y = SIZE - 32
    bar_heights = [16, 32, 26, 38]
    
    for i, height in enumerate(bar_heights):
        x = start_x + i * (bar_width + spacing)
        draw.rectangle(
            [x, base_y - height, x + bar_width, base_y],
            fill=COLORS['white'],
            outline=COLORS['white']
        )


def draw_calendar_icon(draw, color):
    """Calendar grid in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Calendar grid
    grid_x, grid_y = 34, 38
    grid_size = 60
    
    # Outer rectangle
    draw.rectangle(
        [grid_x, grid_y, grid_x + grid_size, grid_y + grid_size],
        outline=COLORS['white'],
        width=int(STROKE_WIDTH)
    )
    
    # Vertical dividers
    for i in range(1, 3):
        x = grid_x + (grid_size // 3) * i
        draw.line([(x, grid_y), (x, grid_y + grid_size)], fill=COLORS['white'], width=1)
    
    # Horizontal dividers
    for i in range(1, 3):
        y = grid_y + (grid_size // 3) * i
        draw.line([(grid_x, y), (grid_x + grid_size, y)], fill=COLORS['white'], width=1)


def draw_profit_icon(draw, color):
    """Trending up arrow in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Upward trend line
    points = [(35, 95), (55, 70), (75, 50), (105, 32)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=COLORS['white'], width=int(STROKE_WIDTH + 1))
    
    # Arrow head
    draw.polygon([(105, 32), (98, 44), (110, 40)], fill=COLORS['white'])


def draw_fund_icon(draw, color):
    """Building/Fund in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Building shape
    draw.rectangle(
        [38, 48, 90, 96],
        outline=COLORS['white'],
        width=int(STROKE_WIDTH)
    )
    
    # Windows (2x2 grid)
    for row in range(2):
        for col in range(2):
            x = 46 + col * 20
            y = 56 + row * 18
            draw.rectangle(
                [x, y, x + 12, y + 12],
                outline=COLORS['white'],
                width=1
            )


def draw_bitcoin_icon(draw, color):
    """Bitcoin symbol in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Bitcoin B symbol
    cx, cy = SIZE // 2, SIZE // 2
    # Vertical line
    draw.line([(cx, cy - 20), (cx, cy + 20)], fill=COLORS['white'], width=int(STROKE_WIDTH + 1))
    # Top curve
    draw.arc(
        [(cx - 10, cy - 18), (cx + 14, cy - 4)],
        0, 180,
        fill=COLORS['white'],
        width=int(STROKE_WIDTH)
    )
    # Bottom curve
    draw.arc(
        [(cx - 10, cy + 4), (cx + 14, cy + 18)],
        0, 180,
        fill=COLORS['white'],
        width=int(STROKE_WIDTH)
    )


def draw_gold_icon(draw, color):
    """Gold ingot in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Gold ingot shape
    ingot_points = [(45, 75), (55, 42), (73, 42), (83, 75), (76, 88), (52, 88)]
    draw.polygon(ingot_points, outline=COLORS['white'], width=int(STROKE_WIDTH))
    
    # Horizontal stripes
    draw.line([(58, 52), (70, 52)], fill=COLORS['white'], width=int(STROKE_WIDTH))
    draw.line([(56, 65), (72, 65)], fill=COLORS['white'], width=int(STROKE_WIDTH))


def draw_wallet_icon(draw, color):
    """Wallet/Portfolio in circle"""
    margin = 12
    # Circle background
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color,
        outline=color
    )
    # Wallet main body
    draw.rectangle(
        [32, 44, 96, 84],
        outline=COLORS['white'],
        width=int(STROKE_WIDTH)
    )
    
    # Wallet flap
    draw.polygon(
        [(32, 44), (64, 30), (96, 44)],
        outline=COLORS['white'],
        width=int(STROKE_WIDTH)
    )
    
    # Coin indicator
    draw.ellipse(
        [72, 58, 88, 74],
        outline=COLORS['white'],
        width=int(STROKE_WIDTH)
    )


# Create all icons
icons = [
    ('money.png', COLORS['green'], draw_money_icon),
    ('chart.png', COLORS['blue'], draw_chart_icon),
    ('calendar.png', COLORS['blue'], draw_calendar_icon),
    ('profit.png', COLORS['green'], draw_profit_icon),
    ('fund.png', COLORS['blue'], draw_fund_icon),
    ('bitcoin.png', COLORS['orange'], draw_bitcoin_icon),
    ('gold.png', COLORS['gold'], draw_gold_icon),
    ('wallet.png', COLORS['green'], draw_wallet_icon),
]

print("Generating 8 dashboard icons...\n")
for filename, color, draw_func in icons:
    create_icon(filename, color, draw_func)

print("\n✅ All icons generated successfully in icons/ folder!")
