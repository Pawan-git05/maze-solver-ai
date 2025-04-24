import pygame
import numpy as np
import csv
import sys

# Grid settings
if len(sys.argv) > 1:
    try:
        SIZE = int(sys.argv[1])
        if SIZE < 8 or SIZE > 20:  # Match main.py size range
            raise ValueError("Size must be between 8 and 20")
    except ValueError:
        SIZE = 25  # Fallback to default if invalid
else:
    SIZE = 25  # Default size
ROWS, COLS = SIZE, SIZE
CELL_SIZE = 20
MARGIN = 1

# Colors
BLACK = (0, 0, 0)   # Wall (1)
WHITE = (255, 255, 255)  # Path (0)
GREY = (200, 200, 200)
GREEN = (0, 255, 128)  # Start (2)
RED = (255, 51, 51)    # Goal (3)
BLUE = (30, 144, 255)  # Start button
DARK_GREY = (50, 50, 50)

pygame.init()
WINDOW_SIZE = (COLS * (CELL_SIZE + MARGIN), ROWS * (CELL_SIZE + MARGIN) + 100)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Builder: Click to Draw")
font = pygame.font.SysFont(None, 30)

# Maze grid
grid = np.ones((ROWS, COLS), dtype=int)

start_set = False
goal_set = False
start_pos = []
goal_pos = (-1, -1)

# Mode states
MODE = "PATH"  # PATH, START, END

def draw_button(text, x, y, w, h, active, color):
    pygame.draw.rect(screen, color if active else DARK_GREY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))

# Draw grid and buttons
def draw_interface():
    screen.fill(GREY)
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            if val == 1:
                color = BLACK
            elif val == 0:
                color = WHITE
            elif val == 2:
                color = GREEN
            elif val == 3:
                color = RED
            rect = [(MARGIN + CELL_SIZE) * col + MARGIN,
                    (MARGIN + CELL_SIZE) * row + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color, rect)

    # Updated button positions and sizes
    button_width = 120  # Increased from 100
    button_height = 50  # Increased from 40
    window_width = COLS * (CELL_SIZE + MARGIN)
    margin = 20  # Space between buttons and edges

    # Start button (bottom-left)
    start_x = margin
    start_y = ROWS * (CELL_SIZE + MARGIN) + 10
    draw_button("Add Start", start_x, start_y, button_width, button_height, MODE == "START", BLUE)

    # Path button (bottom-middle)
    path_x = (window_width - button_width) // 2
    path_y = ROWS * (CELL_SIZE + MARGIN) + 10
    draw_button("Add Path", path_x, path_y, button_width, button_height, MODE == "PATH", BLACK)

    # End button (bottom-right)
    end_x = window_width - button_width - margin
    end_y = ROWS * (CELL_SIZE + MARGIN) + 10
    draw_button("Add End", end_x, end_y, button_width, button_height, MODE == "END", RED)

    pygame.display.flip()

def save_maze():
    with open("manual_maze.csv", "w", newline="") as f:
        csv.writer(f).writerows(grid)
    with open("maze_data.txt", "w") as f:
        for row in grid:
            f.write(str(row.tolist()) + "\n")
    print("Maze saved.")

running = True
while running:
    draw_interface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < ROWS * (CELL_SIZE + MARGIN):
                col = x // (CELL_SIZE + MARGIN)
                row = y // (CELL_SIZE + MARGIN)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if grid[row][col] == 2:
                        grid[row][col] = 1
                        if (row, col) in start_pos:
                            start_pos.remove((row, col))
                    elif grid[row][col] == 3:
                        grid[row][col] = 1
                        goal_set = False
                        goal_pos = (-1, -1)
                    elif grid[row][col] == 0:
                        grid[row][col] = 1
                    else:
                        if MODE == "START":
                            if grid[row][col] != 3:
                                grid[row][col] = 2
                                start_pos.append((row, col))
                        elif MODE == "END":
                            if not goal_set and grid[row][col] != 2:
                                grid[row][col] = 3
                                goal_pos = (row, col)
                                goal_set = True
                        elif MODE == "PATH":
                            grid[row][col] = 0
            else:
                # Updated button click detection
                button_width = 120
                button_height = 50
                window_width = COLS * (CELL_SIZE + MARGIN)
                margin = 20
                start_x = margin
                start_y = ROWS * (CELL_SIZE + MARGIN) + 10
                path_x = (window_width - button_width) // 2
                end_x = window_width - button_width - margin

                if start_x <= x <= start_x + button_width and start_y <= y <= start_y + button_height:
                    MODE = "START"
                elif path_x <= x <= path_x + button_width and start_y <= y <= start_y + button_height:
                    MODE = "PATH"
                elif end_x <= x <= end_x + button_width and start_y <= y <= start_y + button_height:
                    MODE = "END"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if start_pos and goal_set:
                    save_maze()
                else:
                    print("Set at least one start and one end before saving.")

pygame.quit()