import pygame
import ast
import time
import sys
import heapq

# Constants
CELL_SIZE = 20
MARGIN = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Load maze
maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"

maze = []
with open(maze_file, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            maze.append(ast.literal_eval(line))
        else:
            maze.append(list(map(int, line.split())))

ROWS, COLS = len(maze), len(maze[0])

# Find start and end
start = end = None
for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 2:
            start = (r, c)
        elif maze[r][c] == 3:
            end = (r, c)

if not start or not end:
    raise ValueError("Start or End point not defined in the maze.")

def dijkstra(maze, start, end):
    start_time = time.time()
    visited = set()
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]

    while heap:
        cost, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            path = []
            while current in prev:
                path.append(current)
                current = prev[current]
            path.reverse()
            return path, time.time() - start_time

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] != 1 and neighbor not in visited:
                    new_cost = cost + 1
                    if new_cost < dist.get(neighbor, float('inf')):
                        dist[neighbor] = new_cost
                        prev[neighbor] = current
                        heapq.heappush(heap, (new_cost, neighbor))
    return None, time.time() - start_time

path, time_taken = dijkstra(maze, start, end)

# Visualization
pygame.init()
screen = pygame.display.set_mode(((CELL_SIZE + MARGIN) * COLS, (CELL_SIZE + MARGIN) * ROWS + 40))
pygame.display.set_caption("Dijkstra Pathfinding Visualization")
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
