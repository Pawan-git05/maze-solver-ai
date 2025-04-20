import heapq
import time
import sys

def read_maze(file_path):
    with open(file_path, 'r') as f:
        return [list(map(int, line.strip().split())) for line in f if line.strip()]

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
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:  # up, down, left, right
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
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

# === MAIN EXECUTION ===
if __name__ == "__main__":
    # Get maze file from command-line argument
    if len(sys.argv) > 1:
        maze_file = sys.argv[1]
    else:
        maze_file = 'maze.txt'  # Fallback

    maze = read_maze(maze_file)
    rows, cols = len(maze), len(maze[0])

    print("Maze loaded. Dimensions:", rows, "x", cols)

    start = get_coordinates("Enter start position (row col): ", rows, cols)
    end = get_coordinates("Enter end position (row col): ", rows, cols)

    if maze[start[0]][start[1]] != 0 or maze[end[0]][end[1]] != 0:
        print("Start or End point is not on a walkable path (should be 0).")
    else:
        # Start the timer before calling A* algorithm
        start_time = time.time()

        path = astar(maze, start, end)

        # Stop the timer after A* finishes
        end_time = time.time()

        if path:
            print("\nPath found:")
            print_maze_with_path(maze, path)
        else:
            print("No path found.")

        # Calculate and print the time taken to find the path
        time_taken = end_time - start_time
        print(f"\nTime taken to find the path: {time_taken:.6f} seconds")