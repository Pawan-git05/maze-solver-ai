import pygame
import random
import sys

# Config
CELL_SIZE = 40
ROWS, COLS = 15, 15
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)

# Directions: Top, Right, Bottom, Left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Maze: each cell = [top, right, bottom, left]
maze = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

def draw_maze(screen):
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            walls = maze[row][col]
            if walls[0]:  # Top
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 2)
            if walls[1]:  # Right
                pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[2]:  # Bottom
                pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[3]:  # Left
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x, y + CELL_SIZE), 2)

def is_valid(nr, nc):
    return 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc]

def generate_maze(row=0, col=0):
    visited[row][col] = True
    directions = list(enumerate(DIRS))  # [(0, (dx, dy)), (1, (dx, dy)), ...]
    random.shuffle(directions)

    for direction, (dr, dc) in directions:
        nr, nc = row + dr, col + dc
        if is_valid(nr, nc):
            # Remove wall between current and next
            maze[row][col][direction] = False
            opposite = (direction + 2) % 4
            maze[nr][nc][opposite] = False
            generate_maze(nr, nc)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Maze Generator")

    generate_maze()  # Build the maze
    draw_maze(screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
