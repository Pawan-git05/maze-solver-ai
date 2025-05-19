import pygame
import time
import sys
import heapq

# Constants
CELL_SIZE = 20
MARGIN = 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load maze
maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"
maze = []
with open(maze_file, "r") as f:
    for line in f:
        maze.append([int(cell) for cell in line.strip().split()])

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

# Dijkstra Algorithm
def dijkstra(maze, start, end):
    start_time = time.time()
    heap = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while heap:
        current_cost, current = heapq.heappop(heap)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, time.time() - start_time

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    came_from[neighbor] = current

    return None, time.time() - start_time

# Render maze solution and save as image
def render_solution_to_image(maze, path, filename="solution.png"):
    pygame.init()
    surface = pygame.Surface(((CELL_SIZE + MARGIN) * COLS, (CELL_SIZE + MARGIN) * ROWS))

    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE
            if maze[r][c] == 1:
                color = BLACK
            elif maze[r][c] == 2:
                color = GREEN
            elif maze[r][c] == 3:
                color = RED
            rect = pygame.Rect(
                c * (CELL_SIZE + MARGIN),
                r * (CELL_SIZE + MARGIN),
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(surface, color, rect)

    if path:
        for r, c in path:
            if (r, c) != start and (r, c) != end:
                rect = pygame.Rect(
                    c * (CELL_SIZE + MARGIN),
                    r * (CELL_SIZE + MARGIN),
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(surface, BLUE, rect)

    pygame.image.save(surface, filename)
    pygame.quit()

# Solve and render
path, time_taken = dijkstra(maze, start, end)
render_solution_to_image(maze, path)
