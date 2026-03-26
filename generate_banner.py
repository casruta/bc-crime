"""Generate a pixel-art banner for the bc-crime GitHub repo."""

from PIL import Image, ImageDraw

# Canvas dimensions (matching selfwrite banner proportions)
WIDTH = 1260
HEIGHT = 300

# BC flag colors
BG_COLOR = (0, 39, 118)      # #002776 - BC blue
TEXT_COLOR = (253, 191, 87)   # #FDBF57 - BC gold

# Pixel block size
BLOCK = 12

# 5x7 pixel font definitions (each letter is 5 wide, 7 tall)
FONT = {
    'B': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
    ],
    'C': [
        [0,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [0,1,1,1,1],
    ],
    'R': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    'I': [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [1,1,1,1,1],
    ],
    'M': [
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
    ],
    'E': [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,0],
        [1,0,0,0,0],
        [1,1,1,1,1],
    ],
    ' ': [
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
    ],
}

TEXT = "BC CRIME"

# Calculate total text width
LETTER_WIDTH = 5
LETTER_HEIGHT = 7
SPACING = 2  # blocks between letters
WORD_SPACING = 4  # blocks for space character

total_blocks = 0
for ch in TEXT:
    if ch == ' ':
        total_blocks += WORD_SPACING
    else:
        total_blocks += LETTER_WIDTH + SPACING
total_blocks -= SPACING  # remove trailing spacing

text_width_px = total_blocks * BLOCK
text_height_px = LETTER_HEIGHT * BLOCK

# Center the text
start_x = (WIDTH - text_width_px) // 2
start_y = (HEIGHT - text_height_px) // 2

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Draw each letter
cursor_x = start_x
for ch in TEXT:
    if ch == ' ':
        cursor_x += WORD_SPACING * BLOCK
        continue

    grid = FONT[ch]
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel:
                x = cursor_x + col_idx * BLOCK
                y = start_y + row_idx * BLOCK
                draw.rectangle([x, y, x + BLOCK - 1, y + BLOCK - 1], fill=TEXT_COLOR)

    cursor_x += (LETTER_WIDTH + SPACING) * BLOCK

# Save
img.save('banner.png')
print(f"Banner saved: {WIDTH}x{HEIGHT}, text centered at ({start_x}, {start_y})")
