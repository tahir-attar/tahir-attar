import random

CELL = 12
GAP = 2
COLS = 7
ROWS = 52

EMPTY = "#161B22"
GREEN = "#39D353"

# Tetromino shapes
SHAPES = [
    [(0,0),(1,0),(2,0),(3,0)],       # I
    [(0,0),(1,0),(0,1),(1,1)],       # O
    [(1,0),(0,1),(1,1),(2,1)],       # T
    [(1,0),(2,0),(0,1),(1,1)],       # S
    [(0,0),(1,0),(1,1),(2,1)],       # Z
    [(0,0),(0,1),(1,1),(2,1)],       # J
    [(2,0),(0,1),(1,1),(2,1)]        # L
]

grid = [[0]*COLS for _ in range(ROWS)]

def draw_svg(grid):
    w = COLS * (CELL + GAP)
    h = ROWS * (CELL + GAP)
    svg = [f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append("<style>.cell{rx:2;ry:2}</style>")

    for y in range(ROWS):
        for x in range(COLS):
            color = GREEN if grid[y][x] else EMPTY
            svg.append(
                f'<rect x="{x*(CELL+GAP)}" y="{y*(CELL+GAP)}" '
                f'width="{CELL}" height="{CELL}" fill="{color}" class="cell"/>'
            )

    svg.append("</svg>")
    return "\n".join(svg)

# Drop random blocks
for _ in range(20):
    shape = random.choice(SHAPES)
    x_offset = random.randint(0, COLS-3)
    y_offset = random.randint(0, ROWS-3)

    for x,y in shape:
        if 0 <= y+y_offset < ROWS and 0 <= x+x_offset < COLS:
            grid[y+y_offset][x+x_offset] = 1

# Clear full lines
grid = [row for row in grid if not all(row)]
while len(grid) < ROWS:
    grid.insert(0, [0]*COLS)

svg = draw_svg(grid)

with open("tetris/tetris.svg", "w") as f:
    f.write(svg)
