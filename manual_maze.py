import pygame
import numpy as np
import sys

# Grid settings
if len(sys.argv) > 1:
    try:
        SIZE = int(sys.argv[1])
        if SIZE < 8 or SIZE > 20:
            raise ValueError("Size must be between 8 and 20")
    except ValueError:
        SIZE = 25
else:
    SIZE = 25
ROWS, COLS = SIZE, SIZE
CELL_SIZE = 20
MARGIN = 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 128)
RED = (255, 51, 51)
BLUE = (30, 144, 255)
DARK_GREY = (50, 50, 50)
SAVE_BLUE = (100, 100, 255)

pygame.init()

# Button layout constants
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
BUTTON_SPACING = 10

# Window size
TOTAL_BUTTON_WIDTH = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
EXTRA_BOTTOM_HEIGHT = BUTTON_HEIGHT + BUTTON_MARGIN * 2
WINDOW_WIDTH = max(COLS * (CELL_SIZE + MARGIN), TOTAL_BUTTON_WIDTH + BUTTON_MARGIN * 2)
WINDOW_HEIGHT = ROWS * (CELL_SIZE + MARGIN) + EXTRA_BOTTOM_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Builder: Click to Draw")
font = pygame.font.SysFont(None, 30)

# Maze grid
grid = np.ones((ROWS, COLS), dtype=int)

start_set = False
goal_set = False
start_pos = []
goal_pos = (-1, -1)

MODE = "PATH"

def draw_button(text, x, y, w, h, active, color):
    pygame.draw.rect(screen, color if active else DARK_GREY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))

def draw_interface():
    screen.fill(GREY)
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            color = BLACK if val == 1 else WHITE if val == 0 else GREEN if val == 2 else RED
            rect = [(MARGIN + CELL_SIZE) * col + MARGIN,
                    (MARGIN + CELL_SIZE) * row + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color, rect)

    # Button positions
    total_buttons_width = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
    start_x = (WINDOW_WIDTH - total_buttons_width) // 2
    y = ROWS * (CELL_SIZE + MARGIN) + BUTTON_MARGIN

    path_x = start_x + BUTTON_WIDTH + BUTTON_SPACING
    end_x = path_x + BUTTON_WIDTH + BUTTON_SPACING
    save_x = end_x + BUTTON_WIDTH + BUTTON_SPACING

    draw_button("Add Start", start_x, y, BUTTON_WIDTH, BUTTON_HEIGHT, MODE == "START", BLUE)
    draw_button("Add Path", path_x, y, BUTTON_WIDTH, BUTTON_HEIGHT, MODE == "PATH", BLACK)
    draw_button("Add End", end_x, y, BUTTON_WIDTH, BUTTON_HEIGHT, MODE == "END", RED)
    draw_button("Save Maze", save_x, y, BUTTON_WIDTH, BUTTON_HEIGHT, False, SAVE_BLUE)

    pygame.display.flip()

def save_maze():
    with open("manual_maze.txt", "w") as f:
        for row in grid:
            f.write(str(row.tolist()) + "\n")
    print("Maze saved to manual_maze.txt")

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
                        if MODE == "START" and grid[row][col] != 3:
                            grid[row][col] = 2
                            start_pos.append((row, col))
                        elif MODE == "END" and not goal_set and grid[row][col] != 2:
                            grid[row][col] = 3
                            goal_pos = (row, col)
                            goal_set = True
                        elif MODE == "PATH":
                            grid[row][col] = 0
            else:
                total_buttons_width = 4 * BUTTON_WIDTH + 3 * BUTTON_SPACING
                start_x = (WINDOW_WIDTH - total_buttons_width) // 2
                y_btn = ROWS * (CELL_SIZE + MARGIN) + BUTTON_MARGIN

                path_x = start_x + BUTTON_WIDTH + BUTTON_SPACING
                end_x = path_x + BUTTON_WIDTH + BUTTON_SPACING
                save_x = end_x + BUTTON_WIDTH + BUTTON_SPACING

                if start_x <= x <= start_x + BUTTON_WIDTH and y_btn <= y <= y_btn + BUTTON_HEIGHT:
                    MODE = "START"
                elif path_x <= x <= path_x + BUTTON_WIDTH and y_btn <= y <= y_btn + BUTTON_HEIGHT:
                    MODE = "PATH"
                elif end_x <= x <= end_x + BUTTON_WIDTH and y_btn <= y <= y_btn + BUTTON_HEIGHT:
                    MODE = "END"
                elif save_x <= x <= save_x + BUTTON_WIDTH and y_btn <= y <= y_btn + BUTTON_HEIGHT:
                    if start_pos and goal_set:
                        save_maze()
                        running = False  # Automatically close the GUI
                    else:
                        print("Set at least one start and one end before saving.")

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if start_pos and goal_set:
                    save_maze()
                    running = False
                else:
                    print("Set at least one start and one end before saving.")

pygame.quit()
