"""Generate an isometric top-down pixel-art banner of a gritty urban scene."""

from PIL import Image, ImageDraw
import random

random.seed(42)

WIDTH = 1260
HEIGHT = 500
TILE_W = 64  # isometric tile width
TILE_H = 32  # isometric tile height (2:1 ratio)

# Palette
SKY_BG = (30, 32, 40)
ROAD = (55, 55, 58)
ROAD_DARK = (45, 45, 48)
ROAD_LINE = (160, 150, 50)
SIDEWALK = (95, 90, 82)
SIDEWALK_DARK = (80, 75, 68)
DIRT = (70, 62, 50)
PUDDLE = (40, 50, 65)

# Building colors - grimy
BLDG_ROOF_1 = (75, 70, 65)
BLDG_ROOF_2 = (60, 58, 52)
BLDG_ROOF_DARK = (45, 42, 38)
BLDG_WALL_1 = (100, 85, 70)
BLDG_WALL_2 = (80, 72, 60)
BLDG_WALL_DARK = (60, 55, 48)
BLDG_WALL_RED = (120, 65, 55)
BLDG_WALL_RED_DARK = (90, 50, 42)
BLDG_WINDOW = (50, 60, 75)
BLDG_WINDOW_LIT = (170, 150, 80)
BLDG_WINDOW_BROKEN = (35, 35, 40)

# Car colors
CAR_RED = (140, 45, 40)
CAR_RED_DARK = (100, 35, 30)
CAR_BLUE = (50, 65, 100)
CAR_BLUE_DARK = (35, 48, 75)
CAR_GRAY = (80, 80, 82)
CAR_GRAY_DARK = (55, 55, 58)
CAR_RUST = (110, 60, 35)
CAR_WINDOW = (45, 55, 70)
CAR_WHEEL = (30, 30, 32)

# Tent colors
TENT_BLUE = (45, 70, 120)
TENT_BLUE_S = (35, 55, 95)
TENT_GREEN = (55, 85, 50)
TENT_GREEN_S = (40, 65, 38)
TENT_TARP = (90, 85, 70)
TENT_TARP_S = (70, 65, 55)

# Misc
DUMPSTER = (50, 80, 55)
DUMPSTER_DARK = (35, 60, 40)
TRASH_BAG = (25, 25, 28)
FIRE_BARREL = (90, 50, 30)
SMOKE_1 = (80, 78, 72)
SMOKE_2 = (100, 96, 88)
GRAFFITI = (180, 60, 50)
BC_GOLD = (253, 191, 87)

img = Image.new('RGB', (WIDTH, HEIGHT), SKY_BG)
draw = ImageDraw.Draw(img)


def iso_to_screen(ix, iy):
    """Convert isometric grid coords to screen coords."""
    sx = WIDTH // 2 + (ix - iy) * (TILE_W // 2)
    sy = 80 + (ix + iy) * (TILE_H // 2)
    return sx, sy


def draw_iso_tile(ix, iy, color, color2=None):
    """Draw a flat isometric diamond tile."""
    sx, sy = iso_to_screen(ix, iy)
    hw, hh = TILE_W // 2, TILE_H // 2
    points = [(sx, sy - hh), (sx + hw, sy), (sx, sy + hh), (sx - hw, sy)]
    draw.polygon(points, fill=color)
    if color2:
        # Add texture lines
        for i in range(3):
            offset = (i + 1) * (hh // 4)
            draw.line([(sx - hw + offset * 2, sy - hh + offset),
                       (sx + hw - offset * 2, sy - hh + offset)], fill=color2, width=1)


def draw_iso_block(ix, iy, bw, bd, bh, roof_color, wall_left, wall_right, details=None):
    """Draw an isometric box/building from top-down view."""
    sx, sy = iso_to_screen(ix, iy)
    hw, hh = TILE_W // 2, TILE_H // 2

    # Scale to block size
    w = int(hw * bw)
    d = int(hw * bd)
    h = int(bh)

    # Top-left corner of the base
    bx = sx
    by = sy

    # Right wall (facing right-down)
    right_wall = [
        (bx + w, by - h),
        (bx + w + d, by + d * hh // hw - h),
        (bx + w + d, by + d * hh // hw),
        (bx + w, by),
    ]
    draw.polygon(right_wall, fill=wall_right)

    # Left wall (facing left-down)
    left_wall = [
        (bx, by + w * hh // hw - h),
        (bx + d, by + w * hh // hw + d * hh // hw - h),
        (bx + d, by + w * hh // hw + d * hh // hw),
        (bx, by + w * hh // hw),
    ]
    draw.polygon(left_wall, fill=wall_left)

    # Roof (top face)
    roof = [
        (bx, by + w * hh // hw - h),
        (bx + w, by - h),
        (bx + w + d, by + d * hh // hw - h),
        (bx + d, by + w * hh // hw + d * hh // hw - h),
    ]
    draw.polygon(roof, fill=roof_color)

    return bx, by, w, d, h


def draw_building(ix, iy, stories, bw=1.8, bd=1.5, style='beige', damaged=False):
    """Draw a multi-story building with windows."""
    h = stories * 22

    if style == 'beige':
        roof, wl, wr = BLDG_ROOF_1, BLDG_WALL_1, BLDG_WALL_2
    elif style == 'red':
        roof, wl, wr = BLDG_ROOF_2, BLDG_WALL_RED, BLDG_WALL_RED_DARK
    else:
        roof, wl, wr = BLDG_ROOF_DARK, BLDG_WALL_DARK, BLDG_WALL_2

    if damaged:
        roof = tuple(max(0, c - 15) for c in roof)
        wl = tuple(max(0, c - 10) for c in wl)
        wr = tuple(max(0, c - 10) for c in wr)

    bx, by, w, d, bh_px = draw_iso_block(ix, iy, bw, bd, h, roof, wl, wr)

    # Windows on left wall
    sx, sy = iso_to_screen(ix, iy)
    hw, hh = TILE_W // 2, TILE_H // 2
    base_y = sy + int(hw * bw) * hh // hw

    for floor in range(stories):
        for win in range(max(1, int(bd * 2))):
            wy = base_y - (floor + 1) * 22 + 8
            wx = sx + 6 + win * 14
            wy_adj = wy + win * 3
            if damaged and random.random() > 0.5:
                wc = BLDG_WINDOW_BROKEN
            elif random.random() > 0.6:
                wc = BLDG_WINDOW_LIT
            else:
                wc = BLDG_WINDOW
            draw.rectangle([wx, wy_adj, wx + 6, wy_adj + 8], fill=wc)

    # Windows on right wall
    right_base_x = sx + int(hw * bw)
    for floor in range(stories):
        for win in range(max(1, int(bw * 2))):
            wy = sy - h + (floor) * 22 + 8
            wx = right_base_x + 6 + win * 14
            wy_adj = wy + win * 2
            if damaged and random.random() > 0.5:
                wc = BLDG_WINDOW_BROKEN
            elif random.random() > 0.6:
                wc = BLDG_WINDOW_LIT
            else:
                wc = BLDG_WINDOW
            draw.rectangle([wx, wy_adj, wx + 6, wy_adj + 8], fill=wc)

    # Roof details (vents, stains)
    rx, ry = sx + int(hw * bd) // 2, sy + int(hw * bw) * hh // hw // 2 - h
    if random.random() > 0.4:
        draw.rectangle([rx - 3, ry - 5, rx + 3, ry], fill=BLDG_ROOF_DARK)
    if damaged:
        # Smoke
        for _ in range(3):
            smx = rx + random.randint(-15, 15)
            smy = ry + random.randint(-20, -5)
            sms = random.randint(4, 10)
            draw.ellipse([smx, smy, smx + sms, smy + sms], fill=SMOKE_1)
        # Graffiti streak on wall
        gx = sx + random.randint(5, 30)
        gy = base_y - random.randint(10, 30)
        draw.rectangle([gx, gy, gx + random.randint(8, 20), gy + 3], fill=GRAFFITI)


def draw_car_iso(sx, sy, color, color_dark, abandoned=False, angle=0):
    """Draw a small isometric car from top-down view."""
    # Car body (diamond-ish shape)
    cw, ch = 22, 10
    if angle == 0:  # facing right
        body = [(sx, sy), (sx + cw, sy - ch), (sx + cw * 2, sy), (sx + cw, sy + ch)]
        draw.polygon(body, fill=color)
        # Windshield
        draw.polygon([(sx + 8, sy), (sx + cw, sy - ch + 3), (sx + cw + 4, sy - ch + 5), (sx + 12, sy + 2)],
                     fill=CAR_WINDOW)
        # Wheels
        draw.ellipse([sx + 2, sy + ch - 4, sx + 8, sy + ch + 2], fill=CAR_WHEEL)
        draw.ellipse([sx + cw + 8, sy - 2, sx + cw + 14, sy + 4], fill=CAR_WHEEL)
    else:  # facing down
        body = [(sx, sy), (sx + ch, sy - cw // 2), (sx + ch * 2, sy), (sx + ch, sy + cw // 2)]
        draw.polygon(body, fill=color)
        draw.polygon([(sx + 4, sy), (sx + ch, sy - cw // 2 + 4), (sx + ch + 2, sy - cw // 2 + 6), (sx + 6, sy + 2)],
                     fill=CAR_WINDOW)
        draw.ellipse([sx + 2, sy - 4, sx + 7, sy + 2], fill=CAR_WHEEL)
        draw.ellipse([sx + ch + 6, sy - 2, sx + ch + 11, sy + 4], fill=CAR_WHEEL)

    if abandoned:
        # Rust spots
        for _ in range(4):
            rx = sx + random.randint(5, cw + 10)
            ry = sy + random.randint(-ch, ch)
            draw.rectangle([rx, ry, rx + 3, ry + 2], fill=CAR_RUST)
        # Broken window
        draw.rectangle([sx + 10, sy - 2, sx + 14, sy + 1], fill=BLDG_WINDOW_BROKEN)


def draw_tent_iso(sx, sy, color, color_shadow, size=1.0):
    """Draw a small isometric tent from above."""
    s = int(18 * size)
    h = int(10 * size)
    # Ridge tent shape from above
    top = [(sx, sy), (sx + s, sy - h), (sx + s * 2, sy), (sx + s, sy + h)]
    draw.polygon(top, fill=color)
    # Ridge line
    draw.line([(sx + 2, sy), (sx + s * 2 - 2, sy)], fill=color_shadow, width=2)
    # Shadow side
    shadow = [(sx + s, sy), (sx + s * 2, sy), (sx + s, sy + h)]
    draw.polygon(shadow, fill=color_shadow)


def draw_dumpster(sx, sy):
    """Draw an isometric dumpster from above."""
    w, d, h = 16, 10, 8
    # Body
    body = [(sx, sy), (sx + w, sy - d // 2), (sx + w + d, sy), (sx + d, sy + d // 2)]
    draw.polygon(body, fill=DUMPSTER)
    # Lid
    draw.polygon([(sx, sy - h), (sx + w, sy - d // 2 - h), (sx + w + d, sy - h), (sx + d, sy + d // 2 - h)],
                 fill=DUMPSTER_DARK)
    # Left wall
    draw.polygon([(sx, sy - h), (sx + d, sy + d // 2 - h), (sx + d, sy + d // 2), (sx, sy)], fill=DUMPSTER)


def draw_trash(sx, sy, count=5):
    """Scatter trash bags and debris."""
    for _ in range(count):
        tx = sx + random.randint(-12, 12)
        ty = sy + random.randint(-8, 8)
        ts = random.randint(3, 6)
        tc = random.choice([TRASH_BAG, DIRT, (60, 55, 48), (40, 38, 35)])
        draw.ellipse([tx, ty, tx + ts, ty + ts], fill=tc)


def draw_puddle(sx, sy):
    """Draw a dirty puddle."""
    pw = random.randint(10, 25)
    ph = random.randint(5, 12)
    draw.ellipse([sx, sy, sx + pw, sy + ph], fill=PUDDLE)


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
                    draw.rectangle([bx, by, bx + block - 2, by + block - 2], fill=color)
                    # Slight shadow
                    draw.rectangle([bx + 1, by + 1, bx + block - 1, by + block - 1], fill=color)
        cx += (len(grid[0]) + 1) * block


# ====== SCENE LAYOUT ======

# Ground: fill with road and sidewalk tiles
GRID_W, GRID_H = 14, 12

for iy in range(GRID_H):
    for ix in range(GRID_W):
        sx, sy = iso_to_screen(ix, iy)
        hw, hh = TILE_W // 2, TILE_H // 2

        # Road in the middle rows, sidewalk on edges
        is_road_h = 4 <= iy <= 7  # horizontal road
        is_road_v = 5 <= ix <= 8  # vertical road

        if is_road_h or is_road_v:
            color = ROAD if (ix + iy) % 2 == 0 else ROAD_DARK
            # Road markings
            points = [(sx, sy - hh), (sx + hw, sy), (sx, sy + hh), (sx - hw, sy)]
            draw.polygon(points, fill=color)
            # Center line dashes
            if is_road_h and iy == 5 and ix % 2 == 0:
                draw.line([(sx - 8, sy), (sx + 8, sy)], fill=ROAD_LINE, width=1)
            if is_road_v and ix == 6 and iy % 2 == 0:
                draw.line([(sx, sy - 4), (sx, sy + 4)], fill=ROAD_LINE, width=1)
            # Random cracks
            if random.random() > 0.7:
                cx = sx + random.randint(-10, 10)
                cy = sy + random.randint(-5, 5)
                draw.line([(cx, cy), (cx + random.randint(-8, 8), cy + random.randint(-4, 4))],
                         fill=(40, 40, 42), width=1)
        else:
            color = SIDEWALK if (ix + iy) % 2 == 0 else SIDEWALK_DARK
            points = [(sx, sy - hh), (sx + hw, sy), (sx, sy + hh), (sx - hw, sy)]
            draw.polygon(points, fill=color)
            # Dirt patches on sidewalk
            if random.random() > 0.6:
                draw.ellipse([sx - 5, sy - 3, sx + 5, sy + 3], fill=DIRT)

# ====== BUILDINGS ======

# Top-left block
draw_building(0, 0, 4, bw=2.0, bd=1.8, style='red', damaged=True)
draw_building(0, 2, 3, bw=1.5, bd=1.5, style='beige', damaged=False)

# Top-right block
draw_building(9, 0, 5, bw=2.2, bd=2.0, style='dark', damaged=True)
draw_building(11, 0, 3, bw=1.8, bd=1.5, style='red', damaged=False)

# Bottom-left block
draw_building(0, 8, 4, bw=2.0, bd=2.0, style='beige', damaged=True)
draw_building(2, 9, 3, bw=1.5, bd=1.5, style='dark', damaged=False)

# Bottom-right block
draw_building(9, 8, 6, bw=2.5, bd=2.0, style='red', damaged=True)
draw_building(11, 9, 3, bw=1.8, bd=1.8, style='beige', damaged=False)

# ====== CARS ON ROADS ======

# Cars on horizontal road
draw_car_iso(480, 230, CAR_RED, CAR_RED_DARK, abandoned=True, angle=0)
draw_car_iso(600, 260, CAR_GRAY, CAR_GRAY_DARK, abandoned=True, angle=0)
draw_car_iso(720, 240, CAR_BLUE, CAR_BLUE_DARK, abandoned=False, angle=0)

# Cars on vertical road
draw_car_iso(560, 170, CAR_GRAY, CAR_GRAY_DARK, abandoned=True, angle=1)
draw_car_iso(620, 310, CAR_RED, CAR_RED_DARK, abandoned=True, angle=1)
draw_car_iso(680, 350, CAR_BLUE, CAR_BLUE_DARK, abandoned=False, angle=1)

# ====== TENTS along sidewalks ======

# Left sidewalk tents
draw_tent_iso(280, 200, TENT_BLUE, TENT_BLUE_S, 1.0)
draw_tent_iso(310, 220, TENT_GREEN, TENT_GREEN_S, 0.9)
draw_tent_iso(250, 240, TENT_TARP, TENT_TARP_S, 1.1)

# Right sidewalk tents
draw_tent_iso(800, 250, TENT_BLUE, TENT_BLUE_S, 1.0)
draw_tent_iso(840, 270, TENT_TARP, TENT_TARP_S, 0.8)
draw_tent_iso(780, 290, TENT_GREEN, TENT_GREEN_S, 0.9)

# Bottom tents
draw_tent_iso(450, 340, TENT_TARP, TENT_TARP_S, 1.0)
draw_tent_iso(500, 360, TENT_BLUE, TENT_BLUE_S, 0.9)

# Top tents
draw_tent_iso(380, 150, TENT_GREEN, TENT_GREEN_S, 0.85)
draw_tent_iso(420, 160, TENT_TARP, TENT_TARP_S, 1.0)

# ====== DUMPSTERS & TRASH ======

draw_dumpster(320, 180)
draw_dumpster(760, 230)
draw_dumpster(430, 330)
draw_dumpster(850, 310)

draw_trash(300, 195, 8)
draw_trash(750, 245, 6)
draw_trash(420, 345, 7)
draw_trash(840, 325, 5)

# Scattered trash on road
draw_trash(550, 250, 4)
draw_trash(650, 280, 3)
draw_trash(500, 200, 4)

# ====== PUDDLES ======

draw_puddle(520, 255)
draw_puddle(670, 270)
draw_puddle(580, 300)
draw_puddle(440, 220)

# ====== PIXEL TEXT ======

draw_pixel_text("BC CRIME", 420, 18, BC_GOLD, block=9)

img.save('banner.png')
print(f"Isometric banner saved: {WIDTH}x{HEIGHT}")
