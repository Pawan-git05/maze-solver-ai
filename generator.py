import tkinter as tk
from tkinter import ttk
import subprocess

def start_maze():
    choice = option.get()
    if choice == "Manual Maze":
        subprocess.Popen(["python", "manual_maze.py"])
    elif choice == "Random Maze":
        subprocess.Popen(["python", "random_maze.py"])

# GUI Window Setup
root = tk.Tk()
root.title(" Maze Generator")
root.geometry("400x300")
root.configure(bg="#f0f4f8")  # Soft background

# Title
title = tk.Label(root, text="Maze Generator", font=("Helvetica", 20, "bold"), fg="#2c3e50", bg="#f0f4f8")
title.pack(pady=20)

# Subtitle
subtitle = tk.Label(root, text="Choose how you want to generate the maze", font=("Helvetica", 12), fg="#34495e", bg="#f0f4f8")
subtitle.pack(pady=5)

# Dropdown
option = tk.StringVar(value="Manual Maze")
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff", font=("Helvetica", 11))
dropdown = ttk.Combobox(root, textvariable=option, values=["Manual Maze", "Random Maze"], state="readonly", width=25)
dropdown.pack(pady=20)

# Start Button Styling
def on_enter(e):
    start_btn.config(bg="#3498db", fg="white")

def on_leave(e):
    start_btn.config(bg="#2980b9", fg="white")

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
