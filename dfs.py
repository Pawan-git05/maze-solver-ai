# === dfs.py ===
import time
import sys

def read_maze(file_path):
    with open(file_path, 'r') as f: #path is not added yet 
        return [list(map(int, line.strip().split())) for line in f if line.strip()]

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        current = stack.pop()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        if current in visited:
            continue
        visited.add(current)

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                if neighbor not in visited:
                    stack.append(neighbor)
                    came_from[neighbor] = current
    return None

def print_maze_with_path(maze, path):
    maze_with_path = [row[:] for row in maze]
    for x, y in path:
        if maze_with_path[x][y] == 0:
            maze_with_path[x][y] = '*'
    for row in maze_with_path:
        print(' '.join(str(cell) for cell in row))

def get_coordinates(prompt, max_row, max_col):
    while True:
        try:
            coords = input(prompt).strip().split()
            if len(coords) != 2:
                raise ValueError
            x, y = map(int, coords)
            if 0 <= x < max_row and 0 <= y < max_col:
                return (x, y)
            else:
                print("Coordinates out of bounds.")
        except ValueError:
            print("Enter two valid integers separated by space.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        maze_file = sys.argv[1]
    else:
        maze_file = 'maze.txt'

    maze = read_maze(maze_file) 
    rows, cols = len(maze), len(maze[0])

    print("Maze loaded. Dimensions:", rows, "x", cols)

    start = get_coordinates("Enter start position (row col): ", rows, cols)
    end = get_coordinates("Enter end position (row col): ", rows, cols)

    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0:
        print("Start or End point is not on a walkable path (should be 0).")
    else:
        start_time = time.time()
        path = dfs(maze, start, end)
        end_time = time.time()

        if path:
            print("\nPath found:")
            print_maze_with_path(maze, path)
        else:
            print("No path found.")

        print(f"\nTime taken to find the path: {end_time - start_time:.6f} seconds")

