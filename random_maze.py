import pygame
import numpy as np
import random
import os

# Grid settings
ROWS, COLS = 25, 25
CELL_SIZE = 20
MARGIN = 1

# Colors
BLACK = (0, 0, 0)   # Wall (1)
WHITE = (255, 255, 255)  # Path (0)
GREY = (200, 200, 200)
GREEN = (0, 255, 128)  # Start (2)
RED = (255, 51, 51)    # Goal (3)
BLUE = (30, 144, 255)  # Button color (Previous/Next)
DARK_GREY = (50, 50, 50)
YELLOW = (255, 255, 0)  # Select button

# Init pygame
pygame.init()
WINDOW_SIZE = (COLS * (CELL_SIZE + MARGIN), ROWS * (CELL_SIZE + MARGIN) + 100)  # Add 100px for buttons
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Random Maze Generator")
font = pygame.font.SysFont(None, 30)

# Maze grid: 1 = wall, 0 = path, 2 = start, 3 = goal
grid = np.ones((ROWS, COLS), dtype=int)  # Initialize all cells as walls

start_set = False
goal_set = False
start_pos = (-1, -1)
goal_pos = (-1, -1)

# Maze history for Previous/Next navigation
maze_history = []
current_maze_index = -1
MAX_HISTORY = 10  # Limit stored mazes to avoid memory issues

def generate_random_maze():
    global grid, start_set, goal_set, start_pos, goal_pos
    # Start with all walls
    grid = np.ones((ROWS, COLS), dtype=int)
    
    # Randomly create paths (0), but leave some walls
    for row in range(1, ROWS-1):
        for col in range(1, COLS-1):
            grid[row][col] = random.choice([0, 1])
    
    # Ensure the start (top-left) and goal (bottom-right) are open
    grid[0][0] = 0  # Start
    grid[ROWS-1][COLS-1] = 0  # Goal
    
    # Ensure there's a valid path between start and goal
    carve_path()
    
    # Reset start and goal
    start_set = False
    goal_set = False
    start_pos = (-1, -1)
    goal_pos = (-1, -1)
    
    # Store maze in history
    maze_history.append(grid.copy())
    global current_maze_index
    current_maze_index = len(maze_history) - 1
    if len(maze_history) > MAX_HISTORY:
        maze_history.pop(0)
        current_maze_index -= 1

def carve_path():
    path_row, path_col = 0, 0
    while path_row < ROWS-1 and path_col < COLS-1:
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
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            if val == 1:
                color = BLACK  # Wall
            elif val == 0:
                color = WHITE  # Path
            elif val == 2:
                color = GREEN  # Start
            elif val == 3:
                color = RED  # Goal
            rect = [(MARGIN + CELL_SIZE) * col + MARGIN,
                    (MARGIN + CELL_SIZE) * row + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color, rect)
    
    # Draw buttons
    button_width = 120
    button_height = 50
    window_width = COLS * (CELL_SIZE + MARGIN)
    margin = 20
    button_y = ROWS * (CELL_SIZE + MARGIN) + 10
    
    # Previous button (bottom-left)
    prev_x = margin
    draw_button("Previous", prev_x, button_y, button_width, button_height, BLUE)
    
    # Select button (bottom-middle)
    select_x = (window_width - button_width) // 2
    draw_button("Select", select_x, button_y, button_width, button_height, YELLOW)
    
    # Next button (bottom-right)
    next_x = window_width - button_width - margin
    draw_button("Next", next_x, button_y, button_width, button_height, BLUE)
    
    pygame.display.flip()

def save_maze():
    if not start_set or not goal_set:
        print("Please set both start and goal nodes before saving!")
        return
    # Save to text file with unique name
    maze_count = len([f for f in os.listdir() if f.startswith("random_maze_") and f.endswith(".txt")])
    filename = f"random_maze_{maze_count + 1}.txt"
    with open(filename, "w") as f:
        for row in grid:
            f.write(str(row.tolist()) + "\n")
    print(f"Saved to {filename}")

def load_previous_maze():
    global grid, current_maze_index, start_set, goal_set, start_pos, goal_pos
    if current_maze_index > 0:
        current_maze_index -= 1
        grid = maze_history[current_maze_index].copy()
        # Reset start and goal
        start_set = False
        goal_set = False
        start_pos = (-1, -1)
        goal_pos = (-1, -1)
        # Reapply start and goal if they exist in the grid
        for row in range(ROWS):
            for col in range(COLS):
                if grid[row][col] == 2:
                    start_set = True
                    start_pos = (row, col)
                elif grid[row][col] == 3:
                    goal_set = True
                    goal_pos = (row, col)

running = True
generate_random_maze()  # Generate initial maze
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < ROWS * (CELL_SIZE + MARGIN):  # Grid area
                col = x // (CELL_SIZE + MARGIN)
                row = y // (CELL_SIZE + MARGIN)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if event.button == 1:  # Left-click
                        if not start_set:
                            grid[row][col] = 2
                            start_pos = (row, col)
                            start_set = True
                        elif not goal_set and (row, col) != start_pos:
                            grid[row][col] = 3
                            goal_pos = (row, col)
                            goal_set = True
                    elif event.button == 3:  # Right-click
                        if (row, col) == start_pos:
                            grid[row][col] = 0
                            start_set = False
                            start_pos = (-1, -1)
                        elif (row, col) == goal_pos:
                            grid[row][col] = 0
                            goal_set = False
                            goal_pos = (-1, -1)
            else:  # Button area
                button_width = 120
                button_height = 50
                window_width = COLS * (CELL_SIZE + MARGIN)
                margin = 20
                button_y = ROWS * (CELL_SIZE + MARGIN) + 10
                prev_x = margin
                select_x = (window_width - button_width) // 2
                next_x = window_width - button_width - margin
                
                if prev_x <= x <= prev_x + button_width and button_y <= y <= button_y + button_height:
                    load_previous_maze()
                elif select_x <= x <= select_x + button_width and button_y <= y <= button_y + button_height:
                    save_maze()
                elif next_x <= x <= next_x + button_width and button_y <= y <= button_y + button_height:
                    generate_random_maze()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_maze()

pygame.quit()