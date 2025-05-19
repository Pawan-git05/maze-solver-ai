import pygame
import numpy as np
import random
import os
import sys

# Grid size from command-line or default
if len(sys.argv) > 1:
    try:
        SIZE = int(sys.argv[1])
        if SIZE < 8 or SIZE > 25:
            raise ValueError("Size must be between 8 and 25")
    except ValueError:
        SIZE = 25
else:
    SIZE = 25

ROWS, COLS = SIZE, SIZE
CELL_SIZE = max(10, 600 // SIZE)
MARGIN = 1

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 128)
RED = (255, 51, 51)
BLUE = (30, 144, 255)
DARK_GREY = (50, 50, 50)
YELLOW = (255, 255, 0)

pygame.init()
font = pygame.font.SysFont(None, 24)

instruction_lines = ["First select Start (green) and End (red)", "Click again to deselect if wrong."]
INSTRUCTION_HEIGHT = len(instruction_lines) * 28
GRID_TOP_OFFSET = INSTRUCTION_HEIGHT + 10
BOTTOM_BUTTONS_HEIGHT = 80
WINDOW_HEIGHT = GRID_TOP_OFFSET + ROWS * (CELL_SIZE + MARGIN) + BOTTOM_BUTTONS_HEIGHT
WINDOW_WIDTH = max(300, COLS * (CELL_SIZE + MARGIN))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Maze Generator")

grid = np.ones((ROWS, COLS), dtype=int)
start_set = False
goal_set = False
start_pos = (-1, -1)
goal_pos = (-1, -1)

maze_history = []
current_maze_index = -1
MAX_HISTORY = 10

def generate_random_maze():
    global grid, start_set, goal_set, start_pos, goal_pos
    grid = np.ones((ROWS, COLS), dtype=int)
    for row in range(1, ROWS - 1):
        for col in range(1, COLS - 1):
            grid[row][col] = random.choice([0, 1])
    grid[0][0] = 0
    grid[ROWS - 1][COLS - 1] = 0
    carve_path()
    start_set = goal_set = False
    start_pos = goal_pos = (-1, -1)
    maze_history.append(grid.copy())
    global current_maze_index
    current_maze_index = len(maze_history) - 1
    if len(maze_history) > MAX_HISTORY:
        maze_history.pop(0)
        current_maze_index -= 1

def carve_path():
    path_row, path_col = 0, 0
    while path_row < ROWS - 1 and path_col < COLS - 1:
        grid[path_row][path_col] = 0
        if random.choice([True, False]):
            path_row += 1
        else:
            path_col += 1
    grid[path_row][path_col] = 0

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))

def draw_grid():
    screen.fill(GREY)
    for i, line in enumerate(instruction_lines):
        text_surf = font.render(line, True, DARK_GREY)
        text_x = (WINDOW_WIDTH - text_surf.get_width()) // 2
        text_y = 10 + i * 28
        screen.blit(text_surf, (text_x, text_y))

    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            color = WHITE if val == 0 else BLACK
            if val == 2:
                color = GREEN
            elif val == 3:
                color = RED
            rect = [(MARGIN + CELL_SIZE) * col + MARGIN,
                    (MARGIN + CELL_SIZE) * row + MARGIN + GRID_TOP_OFFSET,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

    button_y = GRID_TOP_OFFSET + ROWS * (CELL_SIZE + MARGIN) + 10
    margin = 20
    draw_button("Previous", margin, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE)
    draw_button("Select", (WINDOW_WIDTH - BUTTON_WIDTH) // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, YELLOW)
    draw_button("Next", WINDOW_WIDTH - BUTTON_WIDTH - margin, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE)

    pygame.display.flip()

def save_maze():
    if not start_set or not goal_set:
        print("Please set both start and goal nodes before saving!")
        return
    with open("random_maze.txt", "w") as f:
        for row in grid:
            f.write(" ".join(map(str, row.tolist())) + "\n")
    print("Saved to random_maze.txt")

    # 🔍 Also save maze image
    surface = pygame.Surface(((CELL_SIZE + MARGIN) * COLS, (CELL_SIZE + MARGIN) * ROWS))
    surface.fill(GREY)
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            color = WHITE if val == 0 else BLACK
            if val == 2:
                color = GREEN
            elif val == 3:
                color = RED
            rect = [(MARGIN + CELL_SIZE) * col + MARGIN,
                    (MARGIN + CELL_SIZE) * row + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, GREY, rect, 1)
    pygame.image.save(surface, "maze.png")
    print("Maze image saved to maze.png")

def load_previous_maze():
    global grid, current_maze_index, start_set, goal_set, start_pos, goal_pos
    if current_maze_index > 0:
        current_maze_index -= 1
        grid = maze_history[current_maze_index].copy()
        start_set = goal_set = False
        start_pos = goal_pos = (-1, -1)
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col] == 2:
                    start_set = True
                    start_pos = (row, col)
                elif grid[row][col] == 3:
                    goal_set = True
                    goal_pos = (row, col)

generate_random_maze()
running = True
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if GRID_TOP_OFFSET <= y < GRID_TOP_OFFSET + ROWS * (CELL_SIZE + MARGIN):
                col = x // (CELL_SIZE + MARGIN)
                row = (y - GRID_TOP_OFFSET) // (CELL_SIZE + MARGIN)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if event.button == 1:
                        if (row, col) == start_pos:
                            grid[row][col] = 0
                            start_pos = (-1, -1)
                            start_set = False
                        elif (row, col) == goal_pos:
                            grid[row][col] = 0
                            goal_pos = (-1, -1)
                            goal_set = False
                        elif not start_set:
                            grid[row][col] = 2
                            start_pos = (row, col)
                            start_set = True
                        elif not goal_set and (row, col) != start_pos:
                            grid[row][col] = 3
                            goal_pos = (row, col)
                            goal_set = True
            else:
                button_y = GRID_TOP_OFFSET + ROWS * (CELL_SIZE + MARGIN) + 10
                margin = 20
                prev_x = margin
                select_x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
                next_x = WINDOW_WIDTH - BUTTON_WIDTH - margin

                if prev_x <= x <= prev_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
                    load_previous_maze()
                elif select_x <= x <= select_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
                    save_maze()
                    running = False
                elif next_x <= x <= next_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
                    generate_random_maze()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_maze()
                running = False

pygame.quit()
