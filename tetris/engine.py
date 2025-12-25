import os
import json
import random
from typing import List, Tuple, Optional, Dict

# Github contribution-like grid configuration (standard layout)
# Assumption: 52 columns (weeks) × 7 rows (days)
COLS = 52
ROWS = 7
CELL_SIZE = 11  # px
GAP = 2         # px
ROUND_RX = 2    # corner radius

# Colors
BG_COLOR = "#0D1117"
EMPTY_COLOR = "#161B22"
GRID_STROKE = "#30363D"

# Piece colors (similar to Tetris palette)
PIECE_COLORS = {
    "I": "#58A6FF",   # blue
    "O": "#39D353",   # green
    "T": "#A371F7",   # purple
    "S": "#39D353",   # green
    "Z": "#F85149",   # red
    "J": "#58A6FF",   # blue
    "L": "#DB6D28",   # orange
}

# Tetromino shape definitions by rotation (0-3)
SHAPES: Dict[str, List[List[Tuple[int, int]]]] = {
    "I": [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
    ],
    "O": [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
SVG_FILE = os.path.join(os.path.dirname(__file__), "tetris.svg")


class Piece:
    def __init__(self, kind: str, rotation: int, x: int, y: int):
        self.kind = kind
        self.rotation = rotation % 4
        self.x = x
        self.y = y
        self.color = PIECE_COLORS.get(kind, "#58A6FF")

    def blocks(self) -> List[Tuple[int, int]]:
        return [(self.x + dx, self.y + dy) for (dx, dy) in SHAPES[self.kind][self.rotation]]

    def width_height(self) -> Tuple[int, int]:
        offs = SHAPES[self.kind][self.rotation]
        max_x = max(dx for dx, _ in offs)
        max_y = max(dy for _, dy in offs)
        return max_x + 1, max_y + 1

    def rotate(self) -> "Piece":
        """Return a new piece rotated 90 degrees clockwise."""
        return Piece(self.kind, self.rotation + 1, self.x, self.y)


def new_empty_grid() -> List[List[Optional[str]]]:
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def load_state() -> Dict:
    if not os.path.exists(STATE_FILE):
        return {
            "rows": ROWS,
            "cols": COLS,
            "grid": new_empty_grid(),
            "active_pieces": [],
            "next_piece": random_piece_spec(random.Random(42)),
            "score": 0,
            "rng_seed": random.randint(0, 2**31 - 1),
            "tick": 0,
        }
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("rows") != ROWS or state.get("cols") != COLS:
            state["rows"] = ROWS
            state["cols"] = COLS
        if not isinstance(state.get("grid"), list) or len(state["grid"]) != ROWS:
            state["grid"] = new_empty_grid()
        for r in range(ROWS):
            if not isinstance(state["grid"][r], list) or len(state["grid"][r]) != COLS:
                state["grid"][r] = [None for _ in range(COLS)]
        if not isinstance(state.get("active_pieces"), list):
            state["active_pieces"] = []
        if "next_piece" not in state:
            state["next_piece"] = random_piece_spec(random.Random(42))
        if "score" not in state:
            state["score"] = 0
        if "rng_seed" not in state:
            state["rng_seed"] = random.randint(0, 2**31 - 1)
        if "tick" not in state:
            state["tick"] = 0
        return state
    except Exception:
        return {
            "rows": ROWS,
            "cols": COLS,
            "grid": new_empty_grid(),
            "active_pieces": [],
            "next_piece": random_piece_spec(random.Random(42)),
            "score": 0,
            "rng_seed": random.randint(0, 2**31 - 1),
            "tick": 0,
        }


def save_state(state: Dict) -> None:
    tmp_path = STATE_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp_path, STATE_FILE)


def in_bounds(x: int, y: int) -> bool:
    return 0 <= x < COLS and 0 <= y < ROWS


def collides(grid: List[List[Optional[str]]], blocks: List[Tuple[int, int]]) -> bool:
    for x, y in blocks:
        if not in_bounds(x, y):
            return True
        if grid[y][x] is not None:
            return True
    return False


def place_piece(grid: List[List[Optional[str]]], piece: Piece) -> None:
    for x, y in piece.blocks():
        if in_bounds(x, y):
            grid[y][x] = piece.color


def clear_full_rows(grid: List[List[Optional[str]]]) -> int:
    cleared = 0
    y = ROWS - 1
    while y >= 0:
        if all(grid[y][x] is not None for x in range(COLS)):
            del grid[y]
            grid.insert(0, [None for _ in range(COLS)])
            cleared += 1
        else:
            y -= 1
    return cleared


def random_piece_spec(rng: random.Random) -> Dict:
    """Generate a random piece spec dict."""
    kind = rng.choice(list(SHAPES.keys()))
    rotation = rng.randrange(4)
    dummy = Piece(kind, rotation, 0, 0)
    pw, _ = dummy.width_height()
    max_x = max(0, COLS - pw)
    x = rng.randrange(max_x + 1)
    y = 0
    return {"kind": kind, "rotation": rotation, "x": x, "y": y}


def ensure_active_pieces(state: Dict, min_active: int = 2) -> None:
    rng = random.Random(state.get("rng_seed", 0) + state.get("tick", 0))
    grid = state["grid"]
    active = state["active_pieces"]

    pieces: List[Piece] = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in active]

    while len(pieces) < min_active:
        # Use next_piece as the first new piece
        if len(pieces) == 0 and "next_piece" in state:
            np = state["next_piece"]
            candidate = Piece(np["kind"], np["rotation"], np["x"], np["y"])
            # Generate a new next_piece
            state["next_piece"] = random_piece_spec(rng)
        else:
            candidate = Piece(
                random_piece_spec(rng)["kind"],
                state.get("tick", 0) % 4,
                rng.randrange(COLS - 3),
                0,
            )

        # Try to place without collision
        tried = set()
        attempts = 0
        while attempts < COLS:
            attempts += 1
            if collides(grid, candidate.blocks()):
                tried.add(candidate.x)
                candidate.x = (candidate.x + 1) % COLS
                if candidate.x in tried:
                    break
            else:
                pieces.append(candidate)
                break

        if len(pieces) >= min_active:
            break

    state["active_pieces"] = [{"kind": p.kind, "rotation": p.rotation, "x": p.x, "y": p.y} for p in pieces]


def try_rotate_piece(grid: List[List[Optional[str]]], piece: Piece, other_pieces: List[Piece]) -> bool:
    """Try to rotate piece. Return True if successful."""
    rotated = piece.rotate()
    other_blocks = set()
    for op in other_pieces:
        for b in op.blocks():
            other_blocks.add(b)

    occupied = {(x, y) for y in range(ROWS) for x in range(COLS) if grid[y][x] is not None}

    for bx, by in rotated.blocks():
        if not in_bounds(bx, by) or (bx, by) in occupied or (bx, by) in other_blocks:
            return False

    piece.rotation = rotated.rotation
    return True


def tick(state: Dict) -> None:
    grid = state["grid"]
    pieces: List[Piece] = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in state["active_pieces"]]

    fixed_indexes = set()
    occupied = {(x, y) for y in range(ROWS) for x in range(COLS) if grid[y][x] is not None}

    # Try to rotate pieces that can help complete rows
    for idx, p in enumerate(pieces):
        other_pieces = [pieces[j] for j in range(len(pieces)) if j != idx]
        # Simple heuristic: rotate if it doesn't cause collision
        if state.get("tick", 0) % 3 == 0:  # rotate every 3 ticks
            try_rotate_piece(grid, p, other_pieces)

    # Move pieces down
    for idx, p in enumerate(pieces):
        other_blocks = set()
        for jdx, op in enumerate(pieces):
            if jdx == idx:
                continue
            for b in op.blocks():
                other_blocks.add(b)

        new_blocks = [(x, y + 1) for (x, y) in p.blocks()]
        blocked = False
        for b in new_blocks:
            if not in_bounds(b[0], b[1]) or b in occupied or b in other_blocks:
                blocked = True
                break

        if blocked:
            place_piece(grid, p)
            fixed_indexes.add(idx)
        else:
            p.y += 1

    # Remove fixed pieces
    pieces = [p for idx, p in enumerate(pieces) if idx not in fixed_indexes]

    # Clear rows and update score
    cleared = clear_full_rows(grid)
    if cleared > 0:
        # Standard Tetris scoring: 100, 300, 500, 800 for 1, 2, 3, 4 lines
        scores = {1: 100, 2: 300, 3: 500, 4: 800}
        state["score"] = state.get("score", 0) + scores.get(cleared, 0)

    state["active_pieces"] = [{"kind": p.kind, "rotation": p.rotation, "x": p.x, "y": p.y} for p in pieces]
    state["tick"] = int(state.get("tick", 0)) + 1
    state["rng_seed"] = int(state.get("rng_seed", 0)) ^ (state["tick"] * 2654435761 & 0xFFFFFFFF)

    ensure_active_pieces(state, min_active=2)


def render_svg(state: Dict, svg_path: str) -> None:
    cols = state.get("cols", COLS)
    rows = state.get("rows", ROWS)
    grid = state["grid"]
    active = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in state["active_pieces"]]
    next_piece_spec = state.get("next_piece", {"kind": "I", "rotation": 0, "x": 0, "y": 0})
    score = state.get("score", 0)

    # Grid dimensions
    width = cols * CELL_SIZE + (cols - 1) * GAP
    height = rows * CELL_SIZE + (rows - 1) * GAP

    # Right panel dimensions (for score and next piece)
    right_panel_width = 140
    right_panel_gap = 10

    total_width = width + right_panel_gap + right_panel_width
    total_height = height

    def cell_xy(c: int, r: int) -> Tuple[int, int]:
        return (c * (CELL_SIZE + GAP), r * (CELL_SIZE + GAP))

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" '
        f'viewBox="0 0 {total_width} {total_height}" style="background:{BG_COLOR}">'
    )

    # Draw empty grid cells
    for r in range(rows):
        for c in range(cols):
            x, y = cell_xy(c, r)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{ROUND_RX}" '
                f'fill="{EMPTY_COLOR}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
            )

    # Overlay fixed blocks
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color:
                x, y = cell_xy(c, r)
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{ROUND_RX}" '
                    f'fill="{color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
                )

    # Overlay falling blocks with smooth animation
    anim_duration = 1.8  # seconds per 1-row drop (matches ~2-minute update cycle)
    for idx, p in enumerate(active):
        color = PIECE_COLORS.get(p.kind, "#58A6FF")
        for block_idx, (c, r) in enumerate(p.blocks()):
            if in_bounds(c, r):
                x, y = cell_xy(c, r)
                # Add slight delay per block for visual effect
                delay = block_idx * 0.05
                parts.append(
                    f'<g>'
                    f'<animateTransform attributeName="transform" type="translate" '
                    f'values="0,0; 0,{CELL_SIZE + GAP}" dur="{anim_duration}s" '
                    f'begin="{delay}s" repeatCount="1" fill="freeze"/>'
                    f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="{ROUND_RX}" '
                    f'fill="{color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
                    f'</g>'
                )

    # Right panel: Score display
    score_x = width + right_panel_gap + 10
    score_y = 20
    parts.append(f'<text x="{score_x}" y="{score_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">SCORE</text>')
    parts.append(f'<text x="{score_x}" y="{score_y + 18}" font-size="20" fill="#58A6FF" font-family="monospace" font-weight="bold">{score}</text>')

    # Right panel: Next piece display
    next_y = score_y + 60
    parts.append(f'<text x="{score_x}" y="{next_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">NEXT</text>')

    # Draw next piece in mini-grid
    next_piece = Piece(next_piece_spec["kind"], next_piece_spec["rotation"], 0, 0)
    mini_cell_size = 8
    mini_gap = 1
    next_grid_y = next_y + 15
    next_grid_x = score_x

    # Draw 4x4 mini grid for next piece
    for mini_r in range(4):
        for mini_c in range(4):
            mx = next_grid_x + mini_c * (mini_cell_size + mini_gap)
            my = next_grid_y + mini_r * (mini_cell_size + mini_gap)
            parts.append(
                f'<rect x="{mx}" y="{my}" width="{mini_cell_size}" height="{mini_cell_size}" rx="1" '
                f'fill="{EMPTY_COLOR}" stroke="{GRID_STROKE}" stroke-width="0.3"/>'
            )

    # Draw next piece blocks
    next_color = PIECE_COLORS.get(next_piece.kind, "#58A6FF")
    for nc, nr in next_piece.blocks():
        mx = next_grid_x + nc * (mini_cell_size + mini_gap)
        my = next_grid_y + nr * (mini_cell_size + mini_gap)
        parts.append(
            f'<rect x="{mx}" y="{my}" width="{mini_cell_size}" height="{mini_cell_size}" rx="1" '
            f'fill="{next_color}" stroke="{GRID_STROKE}" stroke-width="0.3"/>'
        )

    parts.append("</svg>")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))


def main() -> None:
    state = load_state()
    tick(state)
    render_svg(state, SVG_FILE)
    save_state(state)


if __name__ == "__main__":
    main()



class Piece:
    def __init__(self, kind: str, rotation: int, x: int, y: int):
        self.kind = kind
        self.rotation = rotation % 4
        self.x = x
        self.y = y
        self.color = PIECE_COLORS.get(kind, "#58A6FF")

    def blocks(self) -> List[Tuple[int, int]]:
        return [(self.x + dx, self.y + dy) for (dx, dy) in SHAPES[self.kind][self.rotation]]

    def width_height(self) -> Tuple[int, int]:
        offs = SHAPES[self.kind][self.rotation]
        max_x = max(dx for dx, _ in offs)
        max_y = max(dy for _, dy in offs)
        return max_x + 1, max_y + 1


def new_empty_grid() -> List[List[Optional[str]]]:
    return [[None for _ in range(COLS)] for _ in range(ROWS)]


def load_state() -> Dict:
    if not os.path.exists(STATE_FILE):
        return {
            "rows": ROWS,
            "cols": COLS,
            "grid": new_empty_grid(),
            "active_pieces": [],
            "rng_seed": random.randint(0, 2**31 - 1),
            "tick": 0,
        }
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        # Basic validation
        if state.get("rows") != ROWS or state.get("cols") != COLS:
            state["rows"] = ROWS
            state["cols"] = COLS
        if not isinstance(state.get("grid"), list) or len(state["grid"]) != ROWS:
            state["grid"] = new_empty_grid()
        # Clamp grid row lengths
        for r in range(ROWS):
            if not isinstance(state["grid"][r], list) or len(state["grid"][r]) != COLS:
                state["grid"][r] = [None for _ in range(COLS)]
        if not isinstance(state.get("active_pieces"), list):
            state["active_pieces"] = []
        if "rng_seed" not in state:
            state["rng_seed"] = random.randint(0, 2**31 - 1)
        if "tick" not in state:
            state["tick"] = 0
        return state
    except Exception:
        # Reset on corruption
        return {
            "rows": ROWS,
            "cols": COLS,
            "grid": new_empty_grid(),
            "active_pieces": [],
            "rng_seed": random.randint(0, 2**31 - 1),
            "tick": 0,
        }


def save_state(state: Dict) -> None:
    tmp_path = STATE_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp_path, STATE_FILE)


def in_bounds(x: int, y: int) -> bool:
    return 0 <= x < COLS and 0 <= y < ROWS


def collides(grid: List[List[Optional[str]]], blocks: List[Tuple[int, int]]) -> bool:
    for x, y in blocks:
        if not in_bounds(x, y):
            return True
        if grid[y][x] is not None:
            return True
    return False


def place_piece(grid: List[List[Optional[str]]], piece: Piece) -> None:
    for x, y in piece.blocks():
        if in_bounds(x, y):
            grid[y][x] = piece.color


def clear_full_rows(grid: List[List[Optional[str]]]) -> int:
    cleared = 0
    y = ROWS - 1
    while y >= 0:
        if all(grid[y][x] is not None for x in range(COLS)):
            # remove row y and insert empty at top
            del grid[y]
            grid.insert(0, [None for _ in range(COLS)])
            cleared += 1
            # stay at same y to re-check after shift
        else:
            y -= 1
    return cleared


def random_piece(rng: random.Random) -> Piece:
    kind = rng.choice(list(SHAPES.keys()))
    rotation = rng.randrange(4)
    # Spawn near the top, random x that fits width
    dummy = Piece(kind, rotation, 0, 0)
    pw, _ = dummy.width_height()
    max_x = max(0, COLS - pw)
    x = rng.randrange(max_x + 1)
    y = 0
    return Piece(kind, rotation, x, y)


def ensure_active_pieces(state: Dict, min_active: int = 2) -> None:
    rng = random.Random(state.get("rng_seed", 0) + state.get("tick", 0))
    grid = state["grid"]
    active = state["active_pieces"]

    def piece_dict(p: Piece) -> Dict:
        return {"kind": p.kind, "rotation": p.rotation, "x": p.x, "y": p.y}

    # Rehydrate existing pieces into objects
    pieces: List[Piece] = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in active]

    while len(pieces) < min_active:
        candidate = random_piece(rng)
        # try multiple x positions to avoid immediate collision
        tried = set()
        attempts = 0
        while attempts < COLS:
            attempts += 1
            if collides(grid, candidate.blocks()):
                tried.add(candidate.x)
                candidate.x = (candidate.x + 1) % COLS
                if candidate.x in tried:
                    break
            else:
                pieces.append(candidate)
                break
        # If cannot place, skip spawning this cycle
        if len(pieces) >= min_active:
            break
    # Write back
    state["active_pieces"] = [piece_dict(p) for p in pieces]


def tick(state: Dict) -> None:
    grid = state["grid"]
    # Hydrate pieces
    pieces: List[Piece] = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in state["active_pieces"]]

    fixed_indexes = set()

    # Build occupied set from current grid (fixed blocks only)
    occupied = {(x, y) for y in range(ROWS) for x in range(COLS) if grid[y][x] is not None}

    # Try to move each piece down by 1
    for idx, p in enumerate(pieces):
        # Build blocker set: all other pieces' blocks, but NOT this piece
        other_blocks = set()
        for jdx, op in enumerate(pieces):
            if jdx == idx:
                continue
            for b in op.blocks():
                other_blocks.add(b)

        # Try to move down by 1
        new_blocks = [(x, y + 1) for (x, y) in p.blocks()]
        
        # Check collision: out of bounds, fixed grid, or other falling pieces
        blocked = False
        for b in new_blocks:
            if not in_bounds(b[0], b[1]):
                blocked = True
                break
            if b in occupied or b in other_blocks:
                blocked = True
                break
        
        if blocked:
            # Fix this piece into the grid
            place_piece(grid, p)
            fixed_indexes.add(idx)
        else:
            # Piece can fall, move it down
            p.y += 1

    # Remove fixed pieces from active list
    pieces = [p for idx, p in enumerate(pieces) if idx not in fixed_indexes]

    # Clear any full rows
    cleared = clear_full_rows(grid)

    # Update state with remaining active pieces
    state["active_pieces"] = [{"kind": p.kind, "rotation": p.rotation, "x": p.x, "y": p.y} for p in pieces]
    state["tick"] = int(state.get("tick", 0)) + 1

    # Keep RNG evolving slightly even if seed unchanged
    state["rng_seed"] = int(state.get("rng_seed", 0)) ^ (state["tick"] * 2654435761 & 0xFFFFFFFF)

    # Ensure at least 2 active pieces after fixing/clearing
    ensure_active_pieces(state, min_active=2)


def render_svg(state: Dict, svg_path: str) -> None:
    cols = state.get("cols", COLS)
    rows = state.get("rows", ROWS)
    grid = state["grid"]
    active = [Piece(p["kind"], p["rotation"], p["x"], p["y"]) for p in state["active_pieces"]]

    # Compute size
    width = cols * CELL_SIZE + (cols - 1) * GAP
    height = rows * CELL_SIZE + (rows - 1) * GAP

    def cell_xy(c: int, r: int) -> Tuple[int, int]:
        return (
            c * (CELL_SIZE + GAP),
            r * (CELL_SIZE + GAP),
        )

    # SVG header
    parts: List[str] = []
    parts.append(f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\" style=\"background:{BG_COLOR}\">")

    # Draw empty grid cells (with stroke so grid is visible)
    for r in range(rows):
        for c in range(cols):
            x, y = cell_xy(c, r)
            parts.append(
                f"<rect x=\"{x}\" y=\"{y}\" width=\"{CELL_SIZE}\" height=\"{CELL_SIZE}\" rx=\"{ROUND_RX}\" fill=\"{EMPTY_COLOR}\" stroke=\"{GRID_STROKE}\" stroke-width=\"0.5\"/>"
            )

    # Overlay fixed blocks
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color:
                x, y = cell_xy(c, r)
                parts.append(
                    f"<rect x=\"{x}\" y=\"{y}\" width=\"{CELL_SIZE}\" height=\"{CELL_SIZE}\" rx=\"{ROUND_RX}\" fill=\"{color}\" stroke=\"{GRID_STROKE}\" stroke-width=\"0.5\"/>"
                )

    # Overlay falling blocks
    for p in active:
        color = PIECE_COLORS.get(p.kind, "#58A6FF")
        for (c, r) in p.blocks():
            if in_bounds(c, r):
                x, y = cell_xy(c, r)
                parts.append(
                    f"<rect x=\"{x}\" y=\"{y}\" width=\"{CELL_SIZE}\" height=\"{CELL_SIZE}\" rx=\"{ROUND_RX}\" fill=\"{color}\" stroke=\"{GRID_STROKE}\" stroke-width=\"0.5\"/>"
                )

    parts.append("</svg>")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))


def main() -> None:
    state = load_state()
    # One frame tick: move down and fix/clear as necessary
    tick(state)
    # Render the entire grid
    render_svg(state, SVG_FILE)
    # Persist updated state
    save_state(state)


if __name__ == "__main__":
    main()
