#!/usr/bin/env python3
"""
Generate a pure SVG Tetris with SMIL animations.
Blocks fall smoothly, rows flash and clear, everything loops seamlessly.
"""

import math

# Grid config
COLS = 52
ROWS = 7
CELL_SIZE = 11
GAP = 2

# Colors
BG_COLOR = "#0D1117"
EMPTY_COLOR = "#161B22"
GRID_STROKE = "#30363D"
PIECE_COLORS = ["#58A6FF", "#39D353", "#A371F7", "#F85149", "#DB6D28"]

def generate_tetris_svg(output_path: str) -> None:
    """Generate an animated SVG Tetris game that loops seamlessly."""
    
    # Grid dimensions
    width = COLS * CELL_SIZE + (COLS - 1) * GAP
    height = ROWS * CELL_SIZE + (ROWS - 1) * GAP
    
    # Right panel
    right_panel_width = 140
    right_panel_gap = 10
    total_width = width + right_panel_gap + right_panel_width
    total_height = height
    
    # Animation parameters
    fall_duration = 3.5  # seconds for block to fall 1 row
    row_clear_duration = 0.6  # flash duration
    total_loop = 28  # seconds before loop (enough for multiple rows)
    
    def cell_xy(c: int, r: int):
        return (c * (CELL_SIZE + GAP), r * (CELL_SIZE + GAP))
    
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}" style="background:{BG_COLOR}">')
    
    # Draw static empty grid
    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_xy(c, r)
            parts.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{EMPTY_COLOR}" stroke="{GRID_STROKE}" stroke-width="0.5"/>')
    
    # Draw static fixed blocks (simulate game state)
    fixed_blocks = [
        # Bottom row (will flash and clear at t=24s)
        (5, 6, "#58A6FF"), (6, 6, "#39D353"), (7, 6, "#A371F7"), (8, 6, "#F85149"),
        (9, 6, "#DB6D28"), (10, 6, "#58A6FF"), (11, 6, "#39D353"), (12, 6, "#A371F7"),
        (13, 6, "#F85149"), (14, 6, "#DB6D28"), (15, 6, "#58A6FF"), (16, 6, "#39D353"),
        (17, 6, "#A371F7"), (18, 6, "#F85149"), (19, 6, "#DB6D28"), (20, 6, "#58A6FF"),
        (21, 6, "#39D353"), (22, 6, "#A371F7"), (23, 6, "#F85149"), (24, 6, "#DB6D28"),
        (25, 6, "#58A6FF"), (26, 6, "#39D353"), (27, 6, "#A371F7"), (28, 6, "#F85149"),
        (29, 6, "#DB6D28"), (30, 6, "#58A6FF"), (31, 6, "#39D353"), (32, 6, "#A371F7"),
        (33, 6, "#F85149"), (34, 6, "#DB6D28"), (35, 6, "#58A6FF"), (36, 6, "#39D353"),
        (37, 6, "#A371F7"), (38, 6, "#F85149"), (39, 6, "#DB6D28"), (40, 6, "#58A6FF"),
        (41, 6, "#39D353"), (42, 6, "#A371F7"), (43, 6, "#F85149"), (44, 6, "#DB6D28"),
        # Row 5 (partially filled)
        (2, 5, "#58A6FF"), (3, 5, "#39D353"), (4, 5, "#A371F7"),
        (47, 5, "#F85149"), (48, 5, "#DB6D28"), (49, 5, "#58A6FF"), (50, 5, "#39D353"), (51, 5, "#A371F7"),
        # Row 4 (sparse)
        (10, 4, "#58A6FF"), (15, 4, "#39D353"), (25, 4, "#A371F7"), (35, 4, "#F85149"), (45, 4, "#DB6D28"),
    ]
    
    for c, r, color in fixed_blocks:
        x, y = cell_xy(c, r)
        parts.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>')
    
    # Animated falling blocks (I-piece, O-piece, S-piece)
    # Block 1: I-piece (blue vertical) starts at top-left, falls down left side
    block1_color = "#58A6FF"
    block1_c, block1_start_r = 2, 0
    for i in range(4):
        x, y = cell_xy(block1_c, block1_start_r + i)
        # Falls from row 0 to row 6 (falls 6 rows = 6 * fall_duration seconds)
        parts.append(
            f'<g><animate attributeName="y" from="{y}" to="{cell_xy(block1_c, 6 + i)[1]}" dur="{6 * fall_duration}s" begin="0s" repeatCount="indefinite"/>'
            f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{block1_color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
            f'</g>'
        )
    
    # Block 2: O-piece (green square) starts at top-center, falls down
    block2_color = "#39D353"
    block2_c, block2_start_r = 26, 0
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        x, y = cell_xy(block2_c + dc, block2_start_r + dr)
        parts.append(
            f'<g><animate attributeName="y" from="{y}" to="{cell_xy(block2_c + dc, 6 + dr)[1]}" dur="{6 * fall_duration}s" begin="2s" repeatCount="indefinite"/>'
            f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{block2_color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
            f'</g>'
        )
    
    # Block 3: S-piece (purple) starts at top-right, falls down
    block3_color = "#A371F7"
    block3_c, block3_start_r = 45, 0
    for dr, dc in [(0, 1), (0, 2), (1, 0), (1, 1)]:
        x, y = cell_xy(block3_c + dc, block3_start_r + dr)
        parts.append(
            f'<g><animate attributeName="y" from="{y}" to="{cell_xy(block3_c + dc, 6 + dr)[1]}" dur="{6 * fall_duration}s" begin="4s" repeatCount="indefinite"/>'
            f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{block3_color}" stroke="{GRID_STROKE}" stroke-width="0.5"/>'
            f'</g>'
        )
    
    # Row 6 (bottom) flash animation - flash at t=24, clear at t=24.6, loop seamlessly
    # Create flashing overlay for entire bottom row
    parts.append(f'<g id="row6-flash">')
    for c in range(COLS):
        x, y = cell_xy(c, 6)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="#FFD700" stroke="{GRID_STROKE}" stroke-width="0.5" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.85;0.9;0.95;1" dur="{total_loop}s" begin="0s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    parts.append('</g>')
    
    # Right panel: Score (animated counter)
    score_x = width + right_panel_gap + 10
    score_y = 20
    parts.append(f'<text x="{score_x}" y="{score_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">SCORE</text>')
    parts.append(f'<text x="{score_x}" y="{score_y + 18}" font-size="20" fill="#58A6FF" font-family="monospace" font-weight="bold">')
    parts.append(f'<animate attributeName="textContent" values="0;100;100;500;500;900;900" keyTimes="0;0.4;0.6;0.8;0.85;0.95;1" dur="{total_loop}s" repeatCount="indefinite"/>')
    parts.append('100</text>')  # Static fallback
    
    # Right panel: Next piece label
    next_y = score_y + 60
    parts.append(f'<text x="{score_x}" y="{next_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">NEXT</text>')
    
    # Next piece mini-grid (4x4) - rotating through different pieces
    mini_cell_size = 8
    mini_gap = 1
    next_grid_y = next_y + 15
    next_grid_x = score_x
    
    # Draw 4x4 empty grid
    for mini_r in range(4):
        for mini_c in range(4):
            mx = next_grid_x + mini_c * (mini_cell_size + mini_gap)
            my = next_grid_y + mini_r * (mini_cell_size + mini_gap)
            parts.append(f'<rect x="{mx}" y="{my}" width="{mini_cell_size}" height="{mini_cell_size}" rx="1" fill="{EMPTY_COLOR}" stroke="{GRID_STROKE}" stroke-width="0.3"/>')
    
    # Animate next piece (T-piece rotating)
    t_blocks = [(1, 0), (0, 1), (1, 1), (2, 1)]  # T-piece
    for nc, nr in t_blocks:
        mx = next_grid_x + nc * (mini_cell_size + mini_gap)
        my = next_grid_y + nr * (mini_cell_size + mini_gap)
        parts.append(
            f'<rect x="{mx}" y="{my}" width="{mini_cell_size}" height="{mini_cell_size}" rx="1" fill="#A371F7" stroke="{GRID_STROKE}" stroke-width="0.3">'
            f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.5;0.85;0.95;1" dur="{total_loop}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    
    # Add watermark text
    parts.append(f'<text x="{width/2}" y="{height - 5}" font-size="10" fill="#30363D" font-family="monospace" text-anchor="middle">TETRIS • Auto-loops</text>')
    
    parts.append('</svg>')
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(parts))
    
    print(f"✅ Generated animated SVG: {output_path}")


if __name__ == "__main__":
    import os
    svg_path = os.path.join(os.path.dirname(__file__), "tetris_animated.svg")
    generate_tetris_svg(svg_path)
