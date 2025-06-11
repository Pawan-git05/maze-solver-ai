# 🧠 Maze Solver AI

A comprehensive Python project that generates mazes and solves them using various AI algorithms with both web and desktop interfaces.

## ✨ Features

- **Multiple Maze Types**: Generate random mazes or draw custom mazes manually
- **AI Algorithms**: A*, BFS, DFS, and Dijkstra pathfinding algorithms
- **Web Interface**: Modern Flask-based web application
- **Desktop GUI**: Tkinter-based desktop application
- **Visual Solutions**: See both the original maze and the solved path
- **Performance Metrics**: Track solving time and algorithm performance
- **Robust Error Handling**: Comprehensive logging and error management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd maze-solver-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Web Interface (Recommended)
```bash
python app.py
```
Then open your browser to `http://localhost:5000`

#### Desktop GUI
```bash
python main.py
```

## 🎮 How to Use

### Web Interface
1. Select maze type (Manual or Random)
2. Choose maze size (8-50)
3. Pick solving algorithm (A*, BFS, DFS, Dijkstra)
4. Click "Solve Maze" to see the results

### Desktop Interface
1. Choose maze generation method
2. Set maze size
3. Generate the maze
4. Select solving algorithm
5. View the solution

## 🧩 Algorithms

- **A* (A-Star)**: Optimal pathfinding using heuristics
- **BFS (Breadth-First Search)**: Guarantees shortest path
- **DFS (Depth-First Search)**: Memory efficient, may not find shortest path
- **Dijkstra**: Optimal for weighted graphs

## 🔧 Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Graphics**: Pygame
- **GUI**: Tkinter
- **Data Processing**: NumPy
- **Image Processing**: Pillow

## 📁 Project Structure

```
maze-solver-ai/
├── app.py              # Flask web application
├── main.py             # Desktop GUI application
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html
├── algorithms/         # Pathfinding algorithms
│   ├── astar.py
│   ├── bfs.py
│   ├── dfs.py
│   └── dijkstra.py
└── maze_generators/    # Maze generation scripts
    ├── manual_maze.py
    └── random_maze.py
```

## 🛠️ Configuration

Edit `config.py` to customize:
- Maze size limits
- Algorithm timeouts
- Color schemes
- File paths
- Logging levels

## 📊 Performance

The application includes performance monitoring:
- Algorithm execution time
- Memory usage tracking
- Success/failure rates
- Path length optimization

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Pygame Issues**: Install pygame separately if needed
   ```bash
   pip install pygame
   ```

3. **Port Already in Use**: Change the port in `config.py`

4. **Image Generation Fails**: Check write permissions in the project directory

### Logs

Check `maze_solver.log` for detailed error information and debugging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🔮 Future Enhancements

- [ ] Real-time solving animation
- [ ] Machine learning-based pathfinding
- [ ] 3D maze support
- [ ] Multiplayer maze challenges
- [ ] Mobile app version
- [ ] Advanced maze patterns
- [ ] Performance benchmarking dashboard
