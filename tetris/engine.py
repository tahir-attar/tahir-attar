import json, random, os

COLS, ROWS = 7, 52
EMPTY = None

CELL = 11
GAP = 2

COLORS = [
    "#39D353", "#58A6FF", "#F85149",
    "#DB6D28", "#A371F7", "#2EA043"
]

SHAPES = [
    [(0,0),(1,0),(2,0),(3,0)],        # I
    [(0,0),(1,0),(0,1),(1,1)],        # O
    [(1,0),(0,1),(1,1),(2,1)],        # T
    [(1,0),(2,0),(0,1),(1,1)],        # S
    [(0,0),(1,0),(1,1),(2,1)],        # Z
    [(0,0),(0,1),(1,1),(2,1)],        # J
    [(2,0),(0,1),(1,1),(2,1)]         # L
]

STATE_FILE = "tetris/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "grid": [[EMPTY]*COLS for _ in range(ROWS)],
        "falling": []
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def spawn_block():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    x = random.randint(0, COLS-4)
    return {"shape": shape, "x": x, "y": 0, "color": color}

def can_move(grid, block, dy):
    for x,y in block["shape"]:
        ny = y + block["y"] + dy
        nx = x + block["x"]
        if ny >= ROWS or grid[ny][nx] is not None:
            return False
    return True

def lock_block(grid, block):
    for x,y in block["shape"]:
        grid[y+block["y"]][x+block["x"]] = block["color"]

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [EMPTY]*COLS)
    return new_grid

def step():
    state = load_state()
    grid = state["grid"]

    # spawn new blocks if needed
    if len(state["falling"]) < 2:
        state["falling"].append(spawn_block())

    still_falling = []
    for block in state["falling"]:
        if can_move(grid, block, 1):
            block["y"] += 1
            still_falling.append(block)
        else:
            lock_block(grid, block)

    state["falling"] = still_falling
    state["grid"] = clear_lines(grid)
    save_state(state)

    return state

def render_svg(state):
    w = COLS*(CELL+GAP)
    h = ROWS*(CELL+GAP)

    svg = [f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="#0D1117"/>')

    for y in range(ROWS):
        for x in range(COLS):
            fill = state["grid"][y][x] or "#161B22"
            svg.append(
                f'<rect x="{x*(CELL+GAP)}" y="{y*(CELL+GAP)}" '
                f'width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{fill}" stroke="#30363D" stroke-width="0.5"/>'
            )

    for block in state["falling"]:
        for x,y in block["shape"]:
            svg.append(
                f'<rect x="{(x+block["x"])*(CELL+GAP)}" '
                f'y="{(y+block["y"])*(CELL+GAP)}" '
                f'width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{block["color"]}"/>'
            )

    svg.append("</svg>")
    return "\n".join(svg)

state = step()
svg = render_svg(state)

with open("tetris/tetris.svg", "w") as f:
    f.write(svg)
