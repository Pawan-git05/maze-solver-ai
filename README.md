# 🧠 AI-Based Maze Solver

An intelligent Python-based application that generates mazes and solves them using classical and AI pathfinding algorithms. Features both a **web interface (Flask)** and a **desktop GUI (Tkinter/Pygame)** for interaction.

---

## 🚀 Key Features

- 🔁 **Maze Types**: Generate **random** or **custom manual** mazes
- 🧭 **Pathfinding Algorithms**: A*, BFS, DFS, Dijkstra, and Reinforcement Learning (RL)
- 🌐 **Web App**: Intuitive Flask-based web interface
- 🎮 **Desktop GUI**: Tkinter + Pygame for offline interaction
- 🖼️ **Visual Outputs**: Displays original maze and the solved path as images
- 📊 **Performance Tracking**: Time, path length, and stats per algorithm
- 🧩 **Modular Design**: Clean separation of algorithms, UI, and logic
- 🧰 **Robust Logging**: All events and errors logged in `maze_solver.log`

---

## 🧱 Project Structure

```
maze-solver-ai/
├── app.py                 # Flask web server
├── random_maze.py         # Maze generator logic
├── rl_solver.py           # Reinforcement Learning solver
├── [algorithm files].py   # A*, BFS, DFS, Dijkstra implementations
├── templates/
│   └── index.html         # Web interface
├── solution.png           # Image of solved maze
├── maze.png               # Original generated maze
├── config.py              # Custom settings
├── utils.py               # Helper functions
├── requirements.txt       # Dependency list
├── selected_maze.txt      # Maze file used for solving
└── maze_solver.log        # Error and activity logs
```

---

## 💡 Algorithms Implemented

| Algorithm | Description | Guarantees Shortest Path |
|----------|-------------|---------------------------|
| **A\*** | Uses heuristics (Manhattan distance) | ✅ |
| **BFS** | Explores level-by-level | ✅ |
| **DFS** | Memory-efficient depth search | ❌ |
| **Dijkstra** | Weighted graph shortest path | ✅ |
| **RL Solver** | Chooses best path among all algos | ✅ |

---

## 🌐 Web Usage

### ▶️ Launch App
```bash
python app.py
```

### 📍 Open in Browser
```
http://localhost:5000
```

### 🖱️ How to Use
1. Choose Maze Type (Manual or Random)
2. Set Maze Size (8x8 to 50x50)
3. Select an Algorithm
4. Click **Solve Maze**

---

## 🖥️ Desktop GUI Usage

### ▶️ Run Desktop App
```bash
python main.py
```

### 🔧 Steps
1. Choose maze mode (draw or generate)
2. Select algorithm
3. View maze and solution graphically

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- `pip` package manager

### Setup Instructions
```bash
git clone <repo-url>
cd maze-solver-ai
pip install -r requirements.txt
```

---

## 🛠️ Configuration

Modify `config.py` to:
- Change default maze size
- Adjust color schemes
- Set timeout limits
- Configure image and log paths

---

## 🐞 Troubleshooting

| Issue | Fix |
|-------|-----|
| Import Errors | Run `pip install -r requirements.txt` |
| Maze not rendering | Check `maze.png`/`solution.png` generation |
| Pygame issues | Install manually: `pip install pygame` |
| Port 5000 busy | Change port in `app.py` or `config.py` |
| Image write permission | Ensure you have folder write access |

Logs are stored in `maze_solver.log`.

---

## 🤝 Contributing

1. **Fork** this repository
2. Create your **feature branch**
3. **Commit** your changes with context
4. Submit a **Pull Request** 🚀

---

## 🔮 Roadmap / Future Enhancements

- [ ] Live solving animations
- [ ] 3D maze support
- [ ] Mobile-responsive web interface
- [ ] Advanced visualizations & analytics
- [ ] Multiplayer maze competitions
- [ ] Maze difficulty prediction using ML

---

## 📜 License

Licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

Created with ❤️ using Python, Flask, Tkinter, and classic AI techniques.
