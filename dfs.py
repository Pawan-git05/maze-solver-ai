import pygame
import ast
import time
import sys

# Constants
CELL_SIZE = 20
MARGIN = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Load maze from file
if len(sys.argv) > 1:
    maze_file = sys.argv[1]
else:
    maze_file = "manual_maze.txt"

maze = []
with open(maze_file, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            maze.append(ast.literal_eval(line))
        else:
            maze.append(list(map(int, line.split())))

ROWS, COLS = len(maze), len(maze[0])

# Find start and end positions
start = end = None
for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 2:
            start = (r, c)
        elif maze[r][c] == 3:
            end = (r, c)

if not start or not end:
    raise ValueError("Start or End point not defined in the maze.")

# DFS algorithm
def dfs(maze, start, end):
    start_time = time.time()
    stack = [start]
    came_from = {}
    visited = set()

    while stack:
        current = stack.pop()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            duration = time.time() - start_time
            return path, duration

        visited.add(current)

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] != 1 and neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in came_from:
                        came_from[neighbor] = current

    return None, time.time() - start_time

path, time_taken = dfs(maze, start, end)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(((CELL_SIZE + MARGIN) * COLS, (CELL_SIZE + MARGIN) * ROWS + 40))
pygame.display.set_caption("DFS Pathfinding Visualization")
font = pygame.font.SysFont(None, 24)

def draw_maze():
    for r in range(ROWS):
        for c in range(COLS):
            pos = (r, c)
            val = maze[r][c]

            if val == 1:
                color = BLACK
            elif val == 0:
                color = WHITE
            elif val == 2:
                color = GREEN
            elif val == 3:
                color = RED
            else:
                color = GREY

            if path and pos in path and pos != start and pos != end:
                color = BLUE

            rect = [(CELL_SIZE + MARGIN) * c + MARGIN,
                    (CELL_SIZE + MARGIN) * r + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, color, rect)

    for r in range(ROWS):
        for c in range(COLS):
            rect = [(CELL_SIZE + MARGIN) * c + MARGIN,
                    (CELL_SIZE + MARGIN) * r + MARGIN,
                    CELL_SIZE, CELL_SIZE]
            pygame.draw.rect(screen, GREY, rect, 1)

def draw_info():
    label = font.render(f"Path Found: {'Yes' if path else 'No'} | Time: {time_taken:.4f} sec", True, (0, 0, 0))
    screen.blit(label, (10, (CELL_SIZE + MARGIN) * ROWS + 5))

# Main loop
running = True
while running:
    screen.fill(GREY)
    draw_maze()
    draw_info()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
