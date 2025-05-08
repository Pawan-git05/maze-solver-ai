import tkinter as tk
from tkinter import ttk
import subprocess
import os
from tkinter import messagebox

def start_maze():
    choice = option.get()
    size = size_option.get()
    maze_file = "manual_maze.txt" if choice == "Manual Maze" else "random_maze.txt"
    
    # Start maze generation process
    # Use "py" instead of "python" to ensure the correct environment
    process = subprocess.Popen(["py", f"{choice.lower().replace(' ', '_')}.py", size])
    process.wait()  # Wait for maze generation to complete

    # Check if maze file was created
    if os.path.exists(maze_file):
        show_algorithm_selection(maze_file)
    else:
        messagebox.showerror("Error", "Maze file was not generated.")

def show_algorithm_selection(maze_file):
    # Disable main window elements
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, ttk.Combobox)):
            widget.config(state="disabled")
    
    # Create algorithm selection window
    algo_window = tk.Toplevel(root)
    algo_window.title("Select Pathfinding Algorithm")
    algo_window.geometry("300x200")
    algo_window.configure(bg="#f0f4f8")
    
    # Title
    tk.Label(algo_window, text="Select Algorithm", font=("Helvetica", 14, "bold"), 
             fg="#2c3e50", bg="#f0f4f8").pack(pady=10)
    
    # Algorithm Dropdown with all options
    algo_option = tk.StringVar(value="A* Algorithm")
    algo_dropdown = ttk.Combobox(algo_window, textvariable=algo_option, 
                                 values=["A* Algorithm", "BFS", "DFS", "Dijkstra"],
                                 state="readonly", width=20)
    algo_dropdown.pack(pady=10)
def show_algorithm_selection(maze_file):
    # Disable main window elements
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, ttk.Combobox)):
            widget.config(state="disabled")
    
    # Create algorithm selection window
    algo_window = tk.Toplevel(root)
    algo_window.title("Select Pathfinding Algorithm")
    algo_window.geometry("300x200")
    algo_window.configure(bg="#f0f4f8")
    
    # Title
    tk.Label(algo_window, text="Select Algorithm", font=("Helvetica", 14, "bold"), 
             fg="#2c3e50", bg="#f0f4f8").pack(pady=10)
    
    # Algorithm Dropdown
    algo_option = tk.StringVar(value="A* Algorithm")
    algo_dropdown = ttk.Combobox(algo_window, textvariable=algo_option, 
                                 values=["A* Algorithm", "BFS", "DFS", "Dijkstra"],
                                 state="readonly", width=20)
    algo_dropdown.pack(pady=10)

    # ✅ Run button function
    def run_algorithm():
        algo = algo_option.get()
        if algo == "A* Algorithm":
            subprocess.Popen(["py", "astar.py", maze_file])
        elif algo == "BFS":
            subprocess.Popen(["py", "bfs.py", maze_file])
        elif algo == "DFS":
            subprocess.Popen(["py", "dfs.py", maze_file])
        elif algo == "Dijkstra":
            subprocess.Popen(["py", "dijkstra.py", maze_file])

        algo_window.destroy()
        root.destroy()  # ✅ This closes the main GUI

    # ✅ Actual Run button
    run_btn = tk.Button(algo_window, text="Run", command=run_algorithm, 
                        font=("Helvetica", 12, "bold"), bg="#2980b9", fg="white",
                        activebackground="#1f618d", activeforeground="white",
                        padx=15, pady=5, bd=0, relief="flat")
    run_btn.pack(pady=10)

# GUI Window Setup
root = tk.Tk()
root.title("Maze Generator")
root.geometry("400x350")
root.configure(bg="#f0f4f8")

# Title
title = tk.Label(root, text="Maze Generator", font=("Helvetica", 20, "bold"), fg="#2c3e50", bg="#f0f4f8")
title.pack(pady=20)

# Subtitle
subtitle = tk.Label(root, text="Choose how you want to generate the maze", font=("Helvetica", 12), fg="#34495e", bg="#f0f4f8")
subtitle.pack(pady=5)

# Maze Type Dropdown
option = tk.StringVar(value="Manual Maze")
maze_dropdown = ttk.Combobox(root, textvariable=option, values=["Manual Maze", "Random Maze"], state="readonly", width=25)
maze_dropdown.pack(pady=10)

# Size Dropdown
size_option = tk.StringVar(value="20")  # default
sizes = [str(i) for i in range(20, 26)]  # Maze sizes from 20 to 25
size_label = tk.Label(root, text="Select Maze Size (NxN)", font=("Helvetica", 12), bg="#f0f4f8", fg="#34495e")
size_label.pack(pady=5)
size_dropdown = ttk.Combobox(root, textvariable=size_option, values=sizes, state="readonly", width=10)
size_dropdown.pack(pady=10)

# Start Button
def on_enter(e): start_btn.config(bg="#3498db", fg="white")
def on_leave(e): start_btn.config(bg="#2980b9", fg="white")

start_btn = tk.Button(root, text="Start", command=start_maze, font=("Helvetica", 13, "bold"),
                      bg="#2980b9", fg="white", activebackground="#1f618d", activeforeground="white",
                      padx=20, pady=8, bd=0, relief="flat")
start_btn.pack(pady=20)
start_btn.bind("<Enter>", on_enter)
start_btn.bind("<Leave>", on_leave)

# Footer
footer = tk.Label(root, text="Built with ❤️ using Python & Pygame", font=("Helvetica", 9), bg="#f0f4f8", fg="#7f8c8d")
footer.pack(side="bottom", pady=10)

root.mainloop()