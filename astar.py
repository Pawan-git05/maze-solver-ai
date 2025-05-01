import heapq
import time
import sys

def read_maze(file_path):
    maze = []
    with open(file_path, 'r') as f:
        for line in f:
            row = list(map(int, line.strip(' []\n').split(',')))
            maze.append(row)
    return maze

def find_start_and_end(maze):
    start = end = None
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == 2:
                start = (i, j)
            elif val == 3:
                end = (i, j)
    return start, end

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def astar(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] in (0, 3):
                temp_g = g_score[current] + 1
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score = temp_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    return None  # No path found

def print_maze_with_path(maze, path):
    maze_with_path = [row[:] for row in maze]
    for x, y in path:
        if maze_with_path[x][y] == 0:
            maze_with_path[x][y] = '*'
    for row in maze_with_path:
        print(' '.join(str(cell) for cell in row))

# === MAIN EXECUTION ===
if __name__ == "__main__":
    if len(sys.argv) > 1:
        maze_file = sys.argv[1]
    else:
        print("Maze file not provided.")
        sys.exit(1)

    maze = read_maze(maze_file)
    start, end = find_start_and_end(maze)

    if start is None or end is None:
        print("Start (2) or End (3) point not found in the maze.")
        sys.exit(1)

    print("Maze loaded. Dimensions:", len(maze), "x", len(maze[0]))

    start_time = time.time()
    path = astar(maze, start, end)
    end_time = time.time()

    if path:
        print("\nPath found:\n")
        print_maze_with_path(maze, path)
    else:
        print("No path found.")

    print(f"\nTime taken to find the path: {end_time - start_time:.6f} seconds")
    input("\nPress Enter to close...")
