import pygame
import sys

# Config
CELL_SIZE = 40
ROWS, COLS = 15, 15
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
# Maze: Each cell has [top, right, bottom, left]
maze = [[[False, False, False, False] for _ in range(COLS)] for _ in range(ROWS)]
# Matrix to store simplified wall status (1 = wall, 0 = open)
# We'll assume if a cell has any wall, it's considered a wall
matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
def draw_grid(screen):
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

def toggle_wall(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    cell_x = x % CELL_SIZE
    cell_y = y % CELL_SIZE

    if row >= ROWS or col >= COLS:
        return

    margin = 8  # wall click sensitivity

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
    for row in range(ROWS):
        for col in range(COLS):
            # If any wall is present in that cell, mark as 1 (wall), else 0 (open)
            matrix[row][col] = 1 if any(maze[row][col]) else 0

def print_matrix():
    print("\nGenerated Maze Matrix (1 = wall, 0 = path):")
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Manual Maze Builder")

    clock = pygame.time.Clock()
    running = True

    while running:
        draw_grid(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_matrix()
                print_matrix()  # Print to terminal
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    toggle_wall(event.pos)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
