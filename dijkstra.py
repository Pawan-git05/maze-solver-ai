# dijkstra.py
import pygame
import sys
import heapq
import os

CELL_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
GRAY = (220, 220, 220)

def read_maze(file_path):
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file if line.strip()]

def find_points(maze):
    start = end = None
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == 'S':
                start = (r, c)
            elif val == 'E':
                end = (r, c)
    return start, end

def get_neighbors(pos, maze):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    rows, cols = len(maze), len(maze[0])
    x, y = pos
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '1':
            yield (nx, ny)

def dijkstra(maze, start, end):
    dist = {start: 0}
    prev = {}
    visited = set()
    heap = [(0, start)]

    while heap:
        cost, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        for neighbor in get_neighbors(current, maze):
            new_cost = cost + 1
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))

    path = []
    node = end
    while node in prev:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path

def draw_maze(screen, maze, path):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            color = WHITE
            if val == '1':
                color = BLACK
            elif val == 'S':
                color = GREEN
            elif val == 'E':
                color = RED
            pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    for r, c in path:
        if maze[r][c] not in ('S', 'E'):
            pygame.draw.rect(screen, BLUE, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            pygame.time.delay(30)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dijkstra.py <maze_file.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    maze = read_maze(file_path)
    start, end = find_points(maze)

    if not start or not end:
        print("Error: Maze must contain 'S' (start) and 'E' (end).")
        sys.exit(1)

    path = dijkstra(maze, start, end)

    pygame.init()
    screen = pygame.display.set_mode((len(maze[0]) * CELL_SIZE, len(maze) * CELL_SIZE))
    pygame.display.set_caption("Dijkstra's Algorithm")

    draw_maze(screen, maze, path)

    # Wait for exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
