
size_option = tk.StringVar(value="15")  # default
sizes = [str(i) for i in range(8, 21)]
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