from PIL import Image, ImageDraw
import os

# Create icons directory if it doesn't exist
os.makedirs('icons', exist_ok=True)

# Color palette
GREEN = "#16A34A"
BLUE = "#2563EB"
ORANGE = "#F97316"
GOLD = "#EAB308"
GRAY = "#6B7280"

SIZE = 128
PADDING = 16

def create_icon(filename, draw_func):
    """Create a 128x128 transparent PNG icon"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw)
    img.save(f'icons/{filename}')
    print(f'Created icons/{filename}')

def draw_money(draw):
    """Dollar sign icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=GREEN, outline=GREEN)
    # Dollar sign
    cx, cy = SIZE // 2, SIZE // 2
    draw.line([(cx, cy-20), (cx, cy+20)], fill='white', width=3)
    draw.arc([(cx-12, cy-15), (cx+12, cy-5)], 0, 180, fill='white', width=3)
    draw.arc([(cx-12, cy+5), (cx+12, cy+15)], 0, 180, fill='white', width=3)

def draw_chart(draw):
    """Bar chart icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=BLUE, outline=BLUE)
    # Chart bars
    bar_width = 12
    bar_spacing = 6
    start_x = SIZE // 2 - 25
    base_y = SIZE - 40
    heights = [20, 35, 28, 40]
    for i, height in enumerate(heights):
        x = start_x + i * (bar_width + bar_spacing)
        draw.rectangle([x, base_y-height, x+bar_width, base_y], fill='white')

def draw_calendar(draw):
    """Calendar icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=BLUE, outline=BLUE)
    # Calendar grid
    grid_left = 35
    grid_top = 40
    grid_size = 58
    draw.rectangle([grid_left, grid_top, grid_left+grid_size, grid_top+grid_size], outline='white', width=2)
    # Vertical lines
    for i in range(1, 3):
        x = grid_left + (i * grid_size // 3)
        draw.line([(x, grid_top), (x, grid_top+grid_size)], fill='white', width=1)
    # Horizontal lines
    for i in range(1, 3):
        y = grid_top + (i * grid_size // 3)
        draw.line([(grid_left, y), (grid_left+grid_size, y)], fill='white', width=1)

def draw_profit(draw):
    """Profit/trending up icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=GREEN, outline=GREEN)
    # Upward trend line
    points = [(40, 90), (60, 70), (80, 50), (105, 35)]
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill='white', width=4)
    # Arrow head
    draw.polygon([(105, 35), (100, 45), (110, 42)], fill='white')

def draw_fund(draw):
    """Fund/building icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=BLUE, outline=BLUE)
    # Building shape
    draw.rectangle([40, 50, 88, 95], outline='white', width=2)
    # Windows
    for row in range(2):
        for col in range(2):
            x = 48 + col * 18
            y = 58 + row * 18
            draw.rectangle([x, y, x+10, y+10], outline='white', width=1)

def draw_bitcoin(draw):
    """Bitcoin icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=ORANGE, outline=ORANGE)
    # Bitcoin B symbol
    cx, cy = SIZE // 2, SIZE // 2
    # Vertical line
    draw.line([(cx, cy-18), (cx, cy+18)], fill='white', width=3)
    # Top curve
    draw.arc([(cx-8, cy-15), (cx+12, cy-3)], 0, 180, fill='white', width=3)
    # Bottom curve
    draw.arc([(cx-8, cy+3), (cx+12, cy+15)], 0, 180, fill='white', width=3)

def draw_gold(draw):
    """Gold/precious metals icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=GOLD, outline=GOLD)
    # Gold ingot shape
    draw.polygon([(50, 70), (60, 45), (75, 45), (85, 70), (78, 85), (57, 85)], outline='white', fill=GOLD, width=2)
    draw.line([(62, 55), (73, 55)], fill='white', width=2)
    draw.line([(60, 65), (75, 65)], fill='white', width=2)

def draw_wallet(draw):
    """Wallet/portfolio icon"""
    # Circle background
    draw.ellipse([PADDING, PADDING, SIZE-PADDING, SIZE-PADDING], fill=GREEN, outline=GREEN)
    # Wallet shape
    draw.rectangle([35, 45, 95, 80], outline='white', width=2)
    # Flap
    draw.polygon([(35, 45), (65, 35), (95, 45)], outline='white', fill='white', width=2)
    # Coin indicator
    draw.ellipse([75, 60, 88, 73], outline='white', width=2)

# Create all icons
create_icon('money.png', draw_money)
create_icon('chart.png', draw_chart)
create_icon('calendar.png', draw_calendar)
create_icon('profit.png', draw_profit)
create_icon('fund.png', draw_fund)
create_icon('bitcoin.png', draw_bitcoin)
create_icon('gold.png', draw_gold)
create_icon('wallet.png', draw_wallet)

print("\nAll icons created successfully!")
