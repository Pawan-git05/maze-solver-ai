import heapq
import pygame

TILE_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)

def load_maze(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f if line.strip()]

def find_point(maze, symbol):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == symbol:
                return (r, c)
    return None

def get_neighbors(pos, maze):
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
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

def draw_maze(screen, maze, path):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            color = WHITE
            if val == '#':
                color = BLACK
            elif val == 'S':
                color = GREEN
            elif val == 'E':
                color = RED
            pygame.draw.rect(screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, GREY, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    for r, c in path:
        if maze[r][c] not in ('S', 'E'):
            pygame.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, GREY, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def run_dijkstra(maze_file):
    maze = load_maze(maze_file)
    start = find_point(maze, 'S')
    end = find_point(maze, 'E')

    if not start or not end:
        print("Start or End point not found.")
        return

    path = dijkstra_path(maze, start, end)

    pygame.init()
    screen = pygame.display.set_mode((len(maze[0])*TILE_SIZE, len(maze)*TILE_SIZE))
    pygame.display.set_caption("Dijkstra's Algorithm")

    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(screen, maze, path)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
