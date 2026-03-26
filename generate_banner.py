"""Generate an isometric pixel-art banner depicting an East Hastings-style scene."""

from PIL import Image, ImageDraw
import random

random.seed(42)

WIDTH = 1260
HEIGHT = 400

# Color palette
SKY = (15, 20, 45)           # Dark night sky
GROUND = (45, 45, 50)        # Dark asphalt
GROUND_LINE = (60, 60, 65)   # Sidewalk edge
BUILDING_DARK = (35, 35, 40)
BUILDING_MID = (55, 55, 62)
BUILDING_LIGHT = (75, 75, 82)
BUILDING_WINDOW = (180, 160, 80)
BUILDING_WINDOW_OFF = (40, 40, 48)
BURN_DARK = (30, 20, 15)
BURN_MID = (50, 30, 20)
FIRE_RED = (200, 60, 30)
FIRE_ORANGE = (230, 140, 40)
FIRE_YELLOW = (253, 191, 87)  # BC gold
SMOKE = (80, 75, 70)
SMOKE_LIGHT = (100, 95, 88)
TENT_BLUE = (40, 70, 130)
TENT_BLUE_LIGHT = (60, 90, 155)
TENT_GREEN = (50, 80, 45)
TENT_GREEN_LIGHT = (70, 105, 60)
TENT_ORANGE = (170, 90, 30)
TENT_ORANGE_LIGHT = (200, 120, 50)
CAR_DARK = (40, 40, 42)
CAR_BODY = (70, 30, 30)
CAR_BODY2 = (35, 55, 75)
CAR_WINDOW = (50, 55, 65)
YELLOW_LINE = (180, 160, 50)
BC_BLUE = (0, 39, 118)
BC_GOLD = (253, 191, 87)

img = Image.new('RGB', (WIDTH, HEIGHT), SKY)
draw = ImageDraw.Draw(img)

# Ground plane
GROUND_Y = 260
draw.rectangle([0, GROUND_Y, WIDTH, HEIGHT], fill=GROUND)
draw.line([(0, GROUND_Y), (WIDTH, GROUND_Y)], fill=GROUND_LINE, width=2)

# Dashed yellow center line
for x in range(0, WIDTH, 40):
    draw.rectangle([x, GROUND_Y + 50, x + 20, GROUND_Y + 53], fill=YELLOW_LINE)


def draw_iso_box(x, y, w, h, d, color_top, color_left, color_right):
    """Draw an isometric box at position (x, y) with width w, height h, depth d."""
    # Top face
    top = [
        (x, y),
        (x + w, y - w // 2),
        (x + w + d, y - w // 2 + d // 2),
        (x + d, y + d // 2),
    ]
    draw.polygon(top, fill=color_top)

    # Left face
    left = [
        (x, y),
        (x + d, y + d // 2),
        (x + d, y + d // 2 + h),
        (x, y + h),
    ]
    draw.polygon(left, fill=color_left)

    # Right face
    right = [
        (x + d, y + d // 2),
        (x + w + d, y - w // 2 + d // 2),
        (x + w + d, y - w // 2 + d // 2 + h),
        (x + d, y + d // 2 + h),
    ]
    draw.polygon(right, fill=color_right)


def draw_building(x, y, w, h, d, burned=False, has_fire=False):
    """Draw an isometric building."""
    if burned:
        draw_iso_box(x, y, w, h, d, BURN_DARK, BURN_MID, BURN_DARK)
    else:
        draw_iso_box(x, y, w, h, d, BUILDING_LIGHT, BUILDING_MID, BUILDING_DARK)

    # Windows on left face
    win_rows = h // 20
    win_cols = max(1, d // 25)
    for row in range(win_rows):
        for col in range(win_cols):
            wy = y + 10 + row * 20
            wx = x + 8 + col * 25
            wy_offset = (8 + col * 25) // 2
            if burned:
                wc = BURN_DARK if random.random() > 0.3 else FIRE_ORANGE
            else:
                wc = BUILDING_WINDOW if random.random() > 0.4 else BUILDING_WINDOW_OFF
            draw.rectangle([wx, wy + wy_offset, wx + 10, wy + wy_offset + 12], fill=wc)

    # Windows on right face
    for row in range(win_rows):
        for col in range(max(1, w // 25)):
            wy = y - w // 2 + d // 2 + 10 + row * 20
            wx = x + d + 8 + col * 25
            if burned:
                wc = BURN_DARK if random.random() > 0.3 else FIRE_RED
            else:
                wc = BUILDING_WINDOW if random.random() > 0.5 else BUILDING_WINDOW_OFF
            draw.rectangle([wx, wy, wx + 10, wy + 12], fill=wc)

    if has_fire:
        # Draw flames on top
        for _ in range(8):
            fx = x + random.randint(5, w + d - 10)
            fy = y - random.randint(5, 30)
            fs = random.randint(3, 8)
            fc = random.choice([FIRE_RED, FIRE_ORANGE, FIRE_YELLOW])
            draw.ellipse([fx, fy, fx + fs, fy + fs], fill=fc)
        # Smoke
        for _ in range(5):
            sx = x + random.randint(0, w + d)
            sy = y - random.randint(25, 60)
            ss = random.randint(8, 18)
            sc = random.choice([SMOKE, SMOKE_LIGHT])
            draw.ellipse([sx, sy, sx + ss, sy + ss], fill=sc)


def draw_tent(x, y, color, color_light, size=1):
    """Draw a small isometric tent."""
    s = int(30 * size)
    h = int(20 * size)
    # Triangle front
    points_front = [(x, y), (x + s, y), (x + s // 2, y - h)]
    draw.polygon(points_front, fill=color_light)
    # Side
    points_side = [(x + s, y), (x + s + s // 2, y + s // 4), (x + s, y - h)]
    draw.polygon(points_side, fill=color)
    # Opening
    ox = x + s // 2 - 4
    draw.rectangle([ox, y - 8, ox + 8, y], fill=(20, 20, 25))


def draw_car(x, y, flipped=False, burned=False):
    """Draw a small isometric car."""
    body = CAR_DARK if burned else random.choice([CAR_BODY, CAR_BODY2])
    window = BURN_DARK if burned else CAR_WINDOW

    # Body
    draw.rectangle([x, y, x + 50, y + 18], fill=body)
    # Roof / cabin
    draw.rectangle([x + 12, y - 12, x + 40, y], fill=body)
    # Windows
    draw.rectangle([x + 14, y - 10, x + 24, y - 2], fill=window)
    draw.rectangle([x + 27, y - 10, x + 38, y - 2], fill=window)
    # Wheels
    draw.ellipse([x + 5, y + 14, x + 16, y + 24], fill=(25, 25, 25))
    draw.ellipse([x + 34, y + 14, x + 45, y + 24], fill=(25, 25, 25))

    if burned:
        # Fire and smoke
        for _ in range(4):
            fx = x + random.randint(5, 45)
            fy = y - random.randint(12, 30)
            fs = random.randint(3, 7)
            fc = random.choice([FIRE_RED, FIRE_ORANGE, FIRE_YELLOW])
            draw.ellipse([fx, fy, fx + fs, fy + fs], fill=fc)
        for _ in range(3):
            sx = x + random.randint(10, 40)
            sy = y - random.randint(25, 50)
            ss = random.randint(6, 14)
            draw.ellipse([sx, sy, sx + ss, sy + ss], fill=SMOKE)


def draw_debris(x, y):
    """Scatter small debris pixels."""
    for _ in range(8):
        dx = x + random.randint(-10, 10)
        dy = y + random.randint(-5, 5)
        ds = random.randint(1, 4)
        dc = random.choice([BURN_DARK, BURN_MID, GROUND_LINE])
        draw.rectangle([dx, dy, dx + ds, dy + ds], fill=dc)


def draw_pixel_text(text, x, y, color, block=8):
    """Draw pixel-font text."""
    font = {
        'B': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
        'C': [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[0,1,1,1,1]],
        'R': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,1,0],[1,0,0,0,1],[1,0,0,0,1]],
        'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
        'M': [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
        'E': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
        ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    }
    cx = x
    for ch in text:
        grid = font.get(ch, font[' '])
        for row_i, row in enumerate(grid):
            for col_i, px in enumerate(row):
                if px:
                    bx = cx + col_i * block
                    by = y + row_i * block
                    draw.rectangle([bx, by, bx + block - 1, by + block - 1], fill=color)
        cx += (len(grid[0]) + 1) * block


# --- SCENE COMPOSITION ---

# Background buildings (far row, smaller)
draw_building(30, 80, 60, 170, 50, burned=False)
draw_building(150, 60, 55, 190, 45, burned=True, has_fire=True)
draw_building(280, 90, 50, 160, 55, burned=False)
draw_building(400, 50, 65, 200, 50, burned=True, has_fire=False)
draw_building(530, 70, 55, 180, 45, burned=False)
draw_building(650, 55, 60, 195, 50, burned=True, has_fire=True)
draw_building(790, 85, 50, 165, 45, burned=False)
draw_building(900, 65, 60, 185, 50, burned=False)
draw_building(1030, 75, 55, 175, 45, burned=True, has_fire=False)
draw_building(1140, 60, 50, 190, 40, burned=False)

# Tents on sidewalk
draw_tent(80, GROUND_Y - 5, TENT_BLUE, TENT_BLUE_LIGHT, 1.0)
draw_tent(180, GROUND_Y - 2, TENT_GREEN, TENT_GREEN_LIGHT, 0.8)
draw_tent(300, GROUND_Y - 5, TENT_ORANGE, TENT_ORANGE_LIGHT, 1.1)
draw_tent(440, GROUND_Y - 3, TENT_BLUE, TENT_BLUE_LIGHT, 0.9)
draw_tent(560, GROUND_Y - 5, TENT_GREEN, TENT_GREEN_LIGHT, 1.0)
draw_tent(700, GROUND_Y - 2, TENT_ORANGE, TENT_ORANGE_LIGHT, 0.85)
draw_tent(830, GROUND_Y - 4, TENT_BLUE, TENT_BLUE_LIGHT, 1.0)
draw_tent(970, GROUND_Y - 3, TENT_GREEN, TENT_GREEN_LIGHT, 0.9)
draw_tent(1100, GROUND_Y - 5, TENT_ORANGE, TENT_ORANGE_LIGHT, 1.0)

# Cars on the road
draw_car(120, GROUND_Y + 30, burned=True)
draw_car(350, GROUND_Y + 65, burned=True)
draw_car(600, GROUND_Y + 35, burned=False)
draw_car(780, GROUND_Y + 60, burned=True)
draw_car(1000, GROUND_Y + 40, burned=False)

# Debris scattered
for dx in range(50, 1200, 80):
    draw_debris(dx + random.randint(-20, 20), GROUND_Y + random.randint(10, 90))

# Pixel text overlay: "BC CRIME" in BC gold
draw_pixel_text("BC CRIME", 370, 15, BC_GOLD, block=10)

# Subtle gradient overlay at bottom for depth
for y_fade in range(HEIGHT - 40, HEIGHT):
    alpha = (y_fade - (HEIGHT - 40)) / 40
    fade_color = tuple(int(c * (1 - alpha * 0.5)) for c in GROUND)
    draw.line([(0, y_fade), (WIDTH, y_fade)], fill=fade_color)

img.save('banner.png')
print(f"Banner saved: {WIDTH}x{HEIGHT}")
