#!/usr/bin/env python3
"""
Breakout Game Engine - Ball breaking green bricks in shape of "TAHIR ATTAR"
Displays on GitHub README via SVG animation
"""

import json
import os
from typing import List, Tuple

# Game configuration
GRID_WIDTH = 28
GRID_HEIGHT = 20
CELL_SIZE = 15
PADDLE_WIDTH = 4
PADDLE_HEIGHT = 1

# Brick pattern for "TAHIR ATTAR" name in pixel art (green blocks)
# 0 = empty, 1 = brick
BRICK_PATTERN = [
    "0000011110001111000011110001111000",
    "0000001100001100000011000001100000",
    "0000001100001100000011000001100000",
    "0000011110001111000011110001111000",
    "0000100001001000000010000101000000",
    "0000100001001000000010000101000000",
    "0000100001001111000010000101111000",
]

class BreakoutGame:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.bricks = set()  # Active brick positions (row, col)
        self.ball_x = GRID_WIDTH // 2
        self.ball_y = GRID_HEIGHT - 3
        self.ball_vx = 1.0
        self.ball_vy = -1.5
        self.paddle_x = GRID_WIDTH // 2
        self.score = 0
        self.tick = 0
        self.game_over = False
        
        self._init_bricks()
        self.load_state()
    
    def _init_bricks(self):
        """Initialize brick pattern spelling TAHIR ATTAR"""
        start_col = 2
        start_row = 2
        
        for row_idx, pattern_row in enumerate(BRICK_PATTERN):
            for col_idx, cell in enumerate(pattern_row):
                if cell == '1':
                    brick_row = start_row + row_idx
                    brick_col = start_col + col_idx
                    if brick_row < GRID_HEIGHT and brick_col < GRID_WIDTH:
                        self.bricks.add((brick_row, brick_col))
    
    def update(self):
        """Update ball position and check collisions"""
        if self.game_over:
            return
        
        self.tick += 1
        
        # Move ball
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # Bounce off walls
        if self.ball_x <= 0 or self.ball_x >= GRID_WIDTH - 1:
            self.ball_vx = -self.ball_vx
            self.ball_x = max(0, min(GRID_WIDTH - 1, self.ball_x))
        
        if self.ball_y <= 0:
            self.ball_vy = -self.ball_vy
            self.ball_y = 0
        
        # Check if ball hit paddle
        paddle_row = GRID_HEIGHT - 1
        if (int(self.ball_y) == paddle_row and 
            self.paddle_x <= self.ball_x <= self.paddle_x + PADDLE_WIDTH):
            self.ball_vy = -abs(self.ball_vy)
            self.ball_y = paddle_row - 1
        
        # Game over if ball falls
        if self.ball_y >= GRID_HEIGHT:
            self.game_over = True
            return
        
        # Check brick collisions
        ball_grid_x = int(self.ball_x)
        ball_grid_y = int(self.ball_y)
        
        if (ball_grid_y, ball_grid_x) in self.bricks:
            self.bricks.remove((ball_grid_y, ball_grid_x))
            self.ball_vy = -self.ball_vy
            self.score += 10
        
        # AI paddle: follow ball
        if self.ball_x < self.paddle_x - 1:
            self.paddle_x -= 1
        elif self.ball_x > self.paddle_x + PADDLE_WIDTH + 1:
            self.paddle_x += 1
        
        self.paddle_x = max(0, min(GRID_WIDTH - PADDLE_WIDTH - 1, self.paddle_x))
        
        # Win condition
        if not self.bricks:
            self.game_over = True
    
    def render_svg(self) -> str:
        """Generate SVG representation of game state"""
        width = GRID_WIDTH * CELL_SIZE
        height = GRID_HEIGHT * CELL_SIZE
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="background:#0d1117">',
        ]
        
        # Draw bricks (green)
        for row, col in self.bricks:
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            svg_parts.append(f'  <rect x="{x}" y="{y}" width="{CELL_SIZE-1}" height="{CELL_SIZE-1}" fill="#39d353" rx="1"/>')
        
        # Draw paddle (white)
        paddle_x = self.paddle_x * CELL_SIZE
        paddle_y = (GRID_HEIGHT - 1) * CELL_SIZE
        svg_parts.append(f'  <rect x="{paddle_x}" y="{paddle_y}" width="{PADDLE_WIDTH * CELL_SIZE}" height="{PADDLE_HEIGHT * CELL_SIZE}" fill="#ffffff" rx="1"/>')
        
        # Draw ball (yellow)
        ball_x = int(self.ball_x) * CELL_SIZE + CELL_SIZE // 2
        ball_y = int(self.ball_y) * CELL_SIZE + CELL_SIZE // 2
        svg_parts.append(f'  <circle cx="{ball_x}" cy="{ball_y}" r="4" fill="#ffeb3b"/>')
        
        # Draw UI panel
        ui_x = width - 90
        ui_y = 10
        svg_parts.append(f'  <rect x="{ui_x-5}" y="{ui_y-5}" width="95" height="60" fill="#161b22" rx="2"/>')
        svg_parts.append(f'  <text x="{ui_x}" y="{ui_y+15}" font-size="12" fill="#8b949e" font-family="monospace">SCORE</text>')
        svg_parts.append(f'  <text x="{ui_x}" y="{ui_y+35}" font-size="16" fill="#39d353" font-family="monospace" font-weight="bold">{self.score}</text>')
        
        bricks_left = len(self.bricks)
        svg_parts.append(f'  <text x="{ui_x}" y="{ui_y+55}" font-size="10" fill="#8b949e" font-family="monospace">Bricks: {bricks_left}</text>')
        
        # Game over message
        if self.game_over:
            status = "WIN!" if not self.bricks else "GAME OVER"
            color = "#39d353" if not self.bricks else "#f85149"
            svg_parts.append(f'  <text x="{width//2}" y="{height//2}" text-anchor="middle" font-size="24" fill="{color}" font-family="monospace" font-weight="bold">{status}</text>')
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def save_state(self):
        """Save game state to JSON"""
        os.makedirs('breakout', exist_ok=True)
        state = {
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'ball_vx': self.ball_vx,
            'ball_vy': self.ball_vy,
            'paddle_x': self.paddle_x,
            'score': self.score,
            'bricks': list(self.bricks),
            'tick': self.tick,
            'game_over': self.game_over,
        }
        with open('breakout/state.json', 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load game state from JSON"""
        if os.path.exists('breakout/state.json'):
            try:
                with open('breakout/state.json', 'r') as f:
                    state = json.load(f)
                self.ball_x = state.get('ball_x', self.ball_x)
                self.ball_y = state.get('ball_y', self.ball_y)
                self.ball_vx = state.get('ball_vx', self.ball_vx)
                self.ball_vy = state.get('ball_vy', self.ball_vy)
                self.paddle_x = state.get('paddle_x', self.paddle_x)
                self.score = state.get('score', 0)
                self.bricks = set(tuple(b) for b in state.get('bricks', []))
                self.tick = state.get('tick', 0)
                self.game_over = state.get('game_over', False)
                
                # Reset if all bricks cleared
                if not self.bricks and not self.game_over:
                    self._init_bricks()
                    self.game_over = False
            except:
                pass


if __name__ == '__main__':
    game = BreakoutGame()
    
    # Run 5 game updates
    for _ in range(5):
        game.update()
    
    # Render and save SVG
    svg = game.render_svg()
    os.makedirs('breakout', exist_ok=True)
    with open('breakout/breakout.svg', 'w') as f:
        f.write(svg)
    
    # Save state
    game.save_state()
    
    print("✓ Breakout game updated")
