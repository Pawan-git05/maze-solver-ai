import pygame
import random
import sys
import tkinter as tk
from tkinter import ttk

# Config
CELL_SIZE = 40

# Get size from command-line argument
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 10  # Default if no argument

ROWS, COLS = size, size
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)

# Directions: Top, Right, Bottom, Left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Global variables for maze selection
current_maze_idx = 0
mazes = []
visited_list = []

def generate_random_maze():
    global mazes, visited_list
    maze = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    visited_list.append(visited)
    generate_maze(maze, visited, 0, 0)
    mazes.append(maze)

def generate_maze(maze, visited, row, col):
    visited[row][col] = True
    directions = list(enumerate(DIRS))
    random.shuffle(directions)

    for direction, (dr, dc) in directions:
        nr, nc = row + dr, col + dc
        if is_valid(nr, nc, visited):
            maze[row][col][direction] = False
            opposite = (direction + 2) % 4
            maze[nr][nc][opposite] = False
            generate_maze(maze, visited, nr, nc)

def is_valid(nr, nc, visited):
    return 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc]

def update_matrix(maze):
    rows_exp = ROWS * 2 + 1
    cols_exp = COLS * 2 + 1
    matrix = [[1 for _ in range(cols_exp)] for _ in range(rows_exp)]

    for r in range(ROWS):
        for c in range(COLS):
            mr, mc = r * 2 + 1, c * 2 + 1
            matrix[mr][mc] = 0  # Cell center is path

            if not maze[r][c][0]:  # No top wall
                matrix[mr - 1][mc] = 0
            if not maze[r][c][1]:  # No right wall
                matrix[mr][mc + 1] = 0
            if not maze[r][c][2]:  # No bottom wall
                matrix[mr + 1][mc] = 0
            if not maze[r][c][3]:  # No left wall
                matrix[mr][mc - 1] = 0
    return matrix

def draw_maze_preview(canvas, matrix):
    canvas.delete("all")
    rows_exp, cols_exp = len(matrix), len(matrix[0])
    for r in range(rows_exp):
        for c in range(cols_exp):
            if matrix[r][c] == 1:
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = (c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

def draw_maze(screen, maze):
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            walls = maze[row][col]
            if walls[0]:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 2)
            if walls[1]:
                pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[2]:
                pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
            if walls[3]:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x, y + CELL_SIZE), 2)

def print_matrix(matrix):
    print("\nGenerated Maze Matrix (1 = wall, 0 = path):")
    for row in matrix:
        print(" ".join(str(cell) for cell in row))

def save_matrix_to_file(matrix, filename="random_maze.txt"):
    with open(filename, "w") as f:
        for row in matrix:
            f.write(" ".join(str(cell) for cell in row) + "\n")
    print(f"\nExpanded matrix saved to {filename}")

def show_selection_interface():
    global current_maze_idx, mazes
    # Generate a few random mazes for selection
    for _ in range(3):
        generate_random_maze()

    # Tkinter window
    root = tk.Tk()
    root.title("Maze Selection")
    root.configure(bg="#f0f4f8")

    # Max preview canvas size
    MAX_CANVAS_SIZE = 600

    # Use expanded matrix to get real dimensions
    test_matrix = update_matrix(mazes[0])
    rows_exp, cols_exp = len(test_matrix), len(test_matrix[0])

    # Scale cell size so the maze fits in MAX_CANVAS_SIZE
    cell_size_preview = min(MAX_CANVAS_SIZE // cols_exp, MAX_CANVAS_SIZE // rows_exp)
    canvas_width = cols_exp * cell_size_preview
    canvas_height = rows_exp * cell_size_preview

    # Set window size: canvas + buttons
    root.geometry(f"{canvas_width}x{canvas_height + 80}")

    # Canvas for maze preview
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
    canvas.pack(pady=10)

    def draw_maze_preview_scaled(matrix):
        canvas.delete("all")
        for r in range(rows_exp):
            for c in range(cols_exp):
                if matrix[r][c] == 1:
                    x1, y1 = c * cell_size_preview, r * cell_size_preview
                    x2, y2 = x1 + cell_size_preview, y1 + cell_size_preview
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

    draw_maze_preview_scaled(test_matrix)

    # Buttons frame
    button_frame = tk.Frame(root, bg="#f0f4f8")
    button_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

    def update_preview():
        draw_maze_preview_scaled(update_matrix(mazes[current_maze_idx]))

    def previous_maze():
        global current_maze_idx
        current_maze_idx = (current_maze_idx - 1) % len(mazes)
        update_preview()

    def next_maze():
        global current_maze_idx
        current_maze_idx = (current_maze_idx + 1) % len(mazes)
        if current_maze_idx == len(mazes) - 1:
            generate_random_maze()
        update_preview()

    def select_maze():
        root.destroy()
        main_with_selected_maze(mazes[current_maze_idx])

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    tk.Button(button_frame, text="Previous", command=previous_maze, bg="#2980b9", fg="white", padx=20, pady=5).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Select", command=select_maze, bg="#27ae60", fg="white", padx=20, pady=5).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Next", command=next_maze, bg="#2980b9", fg="white", padx=20, pady=5).grid(row=0, column=2, padx=5)

    root.mainloop()

def main_with_selected_maze(selected_maze):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Random Maze Generator ({size}x{size})")

    draw_maze(screen, selected_maze)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                matrix = update_matrix(selected_maze)
                print_matrix(matrix)
                save_matrix_to_file(matrix)
                running = False

    pygame.quit()

if __name__ == "__main__":
    show_selection_interface()