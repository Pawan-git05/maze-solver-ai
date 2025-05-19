import heapq
import pygame
import sys

TILE_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)

maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"

def load_maze(file_path):
    maze = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("[") and line.endswith("]"):
                maze.append(eval(line.strip()))
            else:
                maze.append(list(map(int, line.strip().split())))
    return maze

def find_point(maze, val):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == val:
                return (r, c)
    return None

def get_neighbors(pos, maze):
    r, c = pos
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            if maze[nr][nc] != 1:
                yield (nr, nc)

def dijkstra_path(maze, start, end):
    dist = {start: 0}
    prev = {}
    queue = [(0, start)]
    while queue:
        d, current = heapq.heappop(queue)
        if current == end:
            break
        for neighbor in get_neighbors(current, maze):
            alt = d + 1
            if neighbor not in dist or alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current
                heapq.heappush(queue, (alt, neighbor))
    path = []
    at = end
    while at in prev:
        path.append(at)
        at = prev[at]
    if at == start:
        path.append(start)
    return path[::-1]

maze = load_maze(maze_file)
start = find_point(maze, 2)
end = find_point(maze, 3)
if not start or not end:
    raise ValueError("Start or End not defined in maze.")

path = dijkstra_path(maze, start, end)

pygame.init()
ROWS, COLS = len(maze), len(maze[0])
surface = pygame.Surface((COLS * TILE_SIZE, ROWS * TILE_SIZE + 40))
font = pygame.font.SysFont(None, 24)

def draw_maze():
    for r in range(ROWS):
        for c in range(COLS):
            val = maze[r][c]
            color = WHITE if val == 0 else BLACK
            if val == 2:
                color = GREEN
            elif val == 3:
                color = RED
            pygame.draw.rect(surface, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, GREY, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    for r, c in path:
        if maze[r][c] not in [2, 3]:
            pygame.draw.rect(surface, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, GREY, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_info():
    label = font.render(f"Path Found: {'Yes' if path else 'No'}", True, (0, 0, 0))
    surface.blit(label, (10, ROWS * TILE_SIZE + 5))

surface.fill(GREY)
draw_maze()
draw_info()
pygame.image.save(surface, "solution.png")
pygame.quit()
