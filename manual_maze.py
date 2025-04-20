import pygame
import sys

# Config
CELL_SIZE = 40

# Get size from command-line argument
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 10  # default size

ROWS, COLS = size, size
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)

# Maze: Each cell has [top, right, bottom, left]
maze = [[[False, False, False, False] for _ in range(COLS)] for _ in range(ROWS)]

# Matrix to store expanded layout (2N+1 x 2N+1)
matrix = []

def draw_grid(screen):
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

def toggle_wall(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    cell_x = x % CELL_SIZE
    cell_y = y % CELL_SIZE

    if row >= ROWS or col >= COLS:
        return

    margin = 8

    if cell_y < margin:
        maze[row][col][0] = not maze[row][col][0]
        if row > 0:
            maze[row - 1][col][2] = maze[row][col][0]
    elif cell_x > CELL_SIZE - margin:
        maze[row][col][1] = not maze[row][col][1]
        if col < COLS - 1:
            maze[row][col + 1][3] = maze[row][col][1]
    elif cell_y > CELL_SIZE - margin:
        maze[row][col][2] = not maze[row][col][2]
        if row < ROWS - 1:
            maze[row + 1][col][0] = maze[row][col][2]
    elif cell_x < margin:
        maze[row][col][3] = not maze[row][col][3]
        if col > 0:
            maze[row][col - 1][1] = maze[row][col][3]

def update_matrix():
    rows_exp = ROWS * 2 + 1
    cols_exp = COLS * 2 + 1
    global matrix
    matrix = [[1 for _ in range(cols_exp)] for _ in range(rows_exp)]

    for r in range(ROWS):
        for c in range(COLS):
            mr, mc = r * 2 + 1, c * 2 + 1
            matrix[mr][mc] = 0  # Cell center is path

            if not maze[r][c][0]:  # No top wall
                matrix[mr - 1][mc] = 0
            if not maze[r][c][1]:  # No right wall
                matrix[mr][mc + 1] = 0
            if not maze[r][c][2]:  # No bottom wall
                matrix[mr + 1][mc] = 0
            if not maze[r][c][3]:  # No left wall
                matrix[mr][mc - 1] = 0

def print_matrix():
    print("\nExpanded Maze Matrix (1 = wall, 0 = path):")
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

def save_matrix_to_file(filename="manual_maze.txt"):
    with open(filename, "w") as f:
        for row in matrix:
            f.write(" ".join(str(cell) for cell in row) + "\n")
    print(f"\nMatrix saved to {filename}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Manual Maze Builder ({size}x{size})")

    clock = pygame.time.Clock()
    running = True

    while running:
        draw_grid(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_matrix()
                print_matrix()
                save_matrix_to_file()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    toggle_wall(event.pos)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
