#!/usr/bin/env python3
"""Generate a simple animated SVG Tetris with clean encoding."""

# Grid config
COLS = 52
ROWS = 7
CELL_SIZE = 11
GAP = 2

def create_svg():
    """Create animated Tetris SVG."""
    width = COLS * CELL_SIZE + (COLS - 1) * GAP
    height = ROWS * CELL_SIZE + (ROWS - 1) * GAP
    right_panel_width = 140
    right_panel_gap = 10
    total_width = width + right_panel_gap + right_panel_width
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}" viewBox="0 0 {total_width} {height}" style="background:#0D1117">
'''
    
    # Draw empty grid
    for r in range(ROWS):
        for c in range(COLS):
            x = c * (CELL_SIZE + GAP)
            y = r * (CELL_SIZE + GAP)
            svg += f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="#161B22" stroke="#30363D" stroke-width="0.5"/>\n'
    
    # Draw some fixed blocks at bottom
    fixed_blocks = [
        (5, 6, "#58A6FF"), (6, 6, "#39D353"), (7, 6, "#A371F7"),
        (25, 6, "#F85149"), (26, 6, "#DB6D28"), (27, 6, "#58A6FF"),
        (45, 6, "#39D353"), (46, 6, "#A371F7"), (47, 6, "#F85149"),
    ]
    for c, r, color in fixed_blocks:
        x = c * (CELL_SIZE + GAP)
        y = r * (CELL_SIZE + GAP)
        svg += f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}" stroke="#30363D" stroke-width="0.5"/>\n'
    
    # Falling block 1 (blue I-piece)
    for i in range(4):
        x = 2 * (CELL_SIZE + GAP)
        y_start = 0 * (CELL_SIZE + GAP) + i * (CELL_SIZE + GAP)
        y_end = 6 * (CELL_SIZE + GAP) + i * (CELL_SIZE + GAP)
        svg += f'<rect x="{x}" y="{y_start}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="#58A6FF" stroke="#30363D" stroke-width="0.5">\n'
        svg += f'<animate attributeName="y" from="{y_start}" to="{y_end}" dur="21s" begin="0s" repeatCount="indefinite"/>\n'
        svg += '</rect>\n'
    
    # Falling block 2 (green O-piece)
    for dr in range(2):
        for dc in range(2):
            x = (26 + dc) * (CELL_SIZE + GAP)
            y_start = (0 + dr) * (CELL_SIZE + GAP)
            y_end = (6 + dr) * (CELL_SIZE + GAP)
            svg += f'<rect x="{x}" y="{y_start}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="#39D353" stroke="#30363D" stroke-width="0.5">\n'
            svg += f'<animate attributeName="y" from="{y_start}" to="{y_end}" dur="21s" begin="3s" repeatCount="indefinite"/>\n'
            svg += '</rect>\n'
    
    # Right panel: Score
    score_x = width + right_panel_gap + 10
    score_y = 20
    svg += f'<text x="{score_x}" y="{score_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">SCORE</text>\n'
    svg += f'<text x="{score_x}" y="{score_y + 18}" font-size="20" fill="#58A6FF" font-family="monospace" font-weight="bold">100</text>\n'
    
    # Right panel: Next
    next_y = score_y + 60
    svg += f'<text x="{score_x}" y="{next_y}" font-size="14" fill="#39D353" font-family="monospace" font-weight="bold">NEXT</text>\n'
    
    # Mini grid for next piece
    mini_size = 8
    mini_gap = 1
    next_grid_y = next_y + 15
    next_grid_x = score_x
    
    # Draw 4x4 grid
    for mini_r in range(4):
        for mini_c in range(4):
            mx = next_grid_x + mini_c * (mini_size + mini_gap)
            my = next_grid_y + mini_r * (mini_size + mini_gap)
            svg += f'<rect x="{mx}" y="{my}" width="{mini_size}" height="{mini_size}" rx="1" fill="#161B22" stroke="#30363D" stroke-width="0.3"/>\n'
    
    # Next piece (T-shape)
    t_blocks = [(1, 0), (0, 1), (1, 1), (2, 1)]
    for nc, nr in t_blocks:
        mx = next_grid_x + nc * (mini_size + mini_gap)
        my = next_grid_y + nr * (mini_size + mini_gap)
        svg += f'<rect x="{mx}" y="{my}" width="{mini_size}" height="{mini_size}" rx="1" fill="#A371F7" stroke="#30363D" stroke-width="0.3"/>\n'
    
    svg += '</svg>\n'
    return svg


if __name__ == "__main__":
    import os
    output_path = os.path.join(os.path.dirname(__file__), "tetris_animated.svg")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(create_svg())
    
    print(f"Generated: {output_path}")
