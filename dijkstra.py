import pygame
import time
import sys
import heapq
from utils import load_maze_from_file, find_start_end_positions
from config import MAZE_CONFIG, COLORS

# Constants
CELL_SIZE = MAZE_CONFIG['CELL_SIZE']
MARGIN = MAZE_CONFIG['MARGIN']
WHITE = COLORS['WHITE']
BLACK = COLORS['BLACK']
GREEN = COLORS['GREEN']
RED = COLORS['RED']
BLUE = COLORS['BLUE']

# Global variables (will be set in main)
maze = None
ROWS, COLS = 0, 0
start, ends = None, []

# Dijkstra Algorithm
def dijkstra(maze, start, ends):
    start_time = time.time()
    heap = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}
    reached_end = None

    while heap:
        current_cost, current = heapq.heappop(heap)

        if current in ends:
            reached_end = current
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, time.time() - start_time, reached_end

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    came_from[neighbor] = current

    return None, time.time() - start_time, None

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
            if (r, c) != start and (r, c) not in ends:
                rect = pygame.Rect(
                    c * (CELL_SIZE + MARGIN),
                    r * (CELL_SIZE + MARGIN),
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(surface, BLUE, rect)

    pygame.image.save(surface, filename)
    pygame.quit()

def main():
    """Main function to run Dijkstra algorithm."""
    global maze, ROWS, COLS, start, ends

    # Load maze
    maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"
    maze = load_maze_from_file(maze_file)

    ROWS, COLS = len(maze), len(maze[0])

    # Find start and ends
    start, ends = find_start_end_positions(maze)

    if not start or not ends:
        raise ValueError("Start or End point not defined in the maze.")

    # Solve and render
    path, time_taken, reached_end = dijkstra(maze, start, ends)

    # Always save maze image first
    render_maze_to_image(maze, "maze.png")

    # Save solution image
    render_solution_to_image(maze, path)

    # Print results with clear success/failure indication
    if path:
        print(f"Dijkstra Path found! Length: {len(path)}")
        print(f"SUCCESS: Path successfully found using Dijkstra algorithm")
    else:
        print("Dijkstra No path found")
        print("FAILURE: No path exists between start and end points")

    print(f"Time taken: {time_taken:.3f} seconds")

def render_maze_to_image(maze, filename="maze.png"):
    """Render just the maze without solution."""
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

    pygame.image.save(surface, filename)
    pygame.quit()

if __name__ == "__main__":
    main()
