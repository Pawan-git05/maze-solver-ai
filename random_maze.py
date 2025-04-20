import pygame
import random
import sys

# Config
CELL_SIZE = 40

# Get size from command-line argument
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 10  # Default if no argument

ROWS, COLS = size, size
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)

# Directions: Top, Right, Bottom, Left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Maze and visited matrix
maze = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Final matrix to store expanded walls and paths
matrix = []

def draw_maze(screen):
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            walls = maze[row][col]
            if walls[0]:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 2)
            if walls[1]:
                pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[2]:
                pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[3]:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x, y + CELL_SIZE), 2)

def is_valid(nr, nc):
    return 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc]

def generate_maze(row=0, col=0):
    visited[row][col] = True
    directions = list(enumerate(DIRS))
    random.shuffle(directions)

    for direction, (dr, dc) in directions:
        nr, nc = row + dr, col + dc
        if is_valid(nr, nc):
            maze[row][col][direction] = False
            opposite = (direction + 2) % 4
            maze[nr][nc][opposite] = False
            generate_maze(nr, nc)

def update_matrix():
    rows_exp = ROWS * 2 + 1
    cols_exp = COLS * 2 + 1
    global matrix
    matrix = [[1 for _ in range(cols_exp)] for _ in range(rows_exp)]

    for r in range(ROWS):
        for c in range(COLS):
            mr, mc = r * 2 + 1, c * 2 + 1
            matrix[mr][mc] = 0  # Cell center is a path

            if not maze[r][c][0]:  # No top wall
                matrix[mr - 1][mc] = 0
            if not maze[r][c][1]:  # No right wall
                matrix[mr][mc + 1] = 0
            if not maze[r][c][2]:  # No bottom wall
                matrix[mr + 1][mc] = 0
            if not maze[r][c][3]:  # No left wall
                matrix[mr][mc - 1] = 0

def print_matrix():
    print("\nGenerated Maze Matrix (1 = wall, 0 = path):")
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

def save_matrix_to_file(filename="random_maze.txt"):
    with open(filename, "w") as f:
        for row in matrix:
            f.write(" ".join(str(cell) for cell in row) + "\n")
    print(f"\nExpanded matrix saved to {filename}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Random Maze Generator ({size}x{size})")

    generate_maze()
    draw_maze(screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_matrix()
                print_matrix()
                save_matrix_to_file()
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
