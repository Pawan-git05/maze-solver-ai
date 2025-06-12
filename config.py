"""
Configuration settings for the Maze Solver AI project.
"""
import os
import logging
from typing import Dict, Any

# Application settings
APP_CONFIG = {
    'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
    'HOST': os.getenv('HOST', '127.0.0.1'),
    'PORT': int(os.getenv('PORT', 5000)),
    'SECRET_KEY': os.getenv('SECRET_KEY', 'maze-solver-secret-key')
}

# Maze settings
MAZE_CONFIG = {
    'MIN_SIZE': 3,  # Allow smaller mazes for testing
    'MAX_SIZE': 50,
    'DEFAULT_SIZE': 25,
    'CELL_SIZE': 20,
    'MARGIN': 1,
    'MAX_HISTORY': 10
}

# Algorithm settings
ALGORITHM_CONFIG = {
    'TIMEOUT_SECONDS': 30,
    'MAX_PATH_LENGTH': 10000,
    'ANIMATION_DELAY': 0.05
}

# Colors
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'GREY': (200, 200, 200),
    'DARK_GREY': (50, 50, 50),
    'YELLOW': (255, 255, 0),
    'LIGHT_BLUE': (173, 216, 230),
    'ORANGE': (255, 165, 0)
}

# File paths
PATHS = {
    'MANUAL_MAZE': 'manual_maze.txt',
    'RANDOM_MAZE': 'random_maze.txt',
    'MAZE_IMAGE': 'maze.png',
    'SOLUTION_IMAGE': 'solution.png',
    'LOG_FILE': 'maze_solver.log'
}

def setup_logging(level=logging.WARNING):
    """Setup logging configuration with reduced verbosity."""
    # Suppress pygame welcome message
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    # Configure logging with less verbose output
    logging.basicConfig(
        level=level,
        format='%(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(PATHS['LOG_FILE']),
            logging.StreamHandler()
        ]
    )

    # Reduce werkzeug (Flask) logging verbosity
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    return logging.getLogger(__name__)

def validate_maze_size(size: int) -> int:
    """Validate and return a valid maze size."""
    try:
        size = int(size)
        if size < MAZE_CONFIG['MIN_SIZE']:
            return MAZE_CONFIG['MIN_SIZE']
        elif size > MAZE_CONFIG['MAX_SIZE']:
            return MAZE_CONFIG['MAX_SIZE']
        return size
    except (ValueError, TypeError):
        return MAZE_CONFIG['DEFAULT_SIZE']

def get_algorithm_script(algorithm: str) -> str:
    """Get the script filename for a given algorithm."""
    algorithm_map = {
        'astar': 'astar.py',
        'bfs': 'bfs.py',
        'dfs': 'dfs.py',
        'dijkstra': 'dijkstra.py',
        'bidirectional': 'bidirectional.py'
    }
    return algorithm_map.get(algorithm.lower())

def get_algorithm_info() -> Dict[str, Dict[str, str]]:
    """Get information about available algorithms."""
    return {
        'astar': {
            'name': 'A* (A-Star)',
            'description': 'Optimal pathfinding using heuristics for fast performance',
            'complexity': 'O(b^d)',
            'optimal': True,
            'complete': True
        },
        'bfs': {
            'name': 'Breadth-First Search',
            'description': 'Guarantees shortest path by exploring level by level',
            'complexity': 'O(b^d)',
            'optimal': True,
            'complete': True
        },
        'dfs': {
            'name': 'Depth-First Search',
            'description': 'Memory efficient but may not find shortest path',
            'complexity': 'O(b^m)',
            'optimal': False,
            'complete': True
        },
        'dijkstra': {
            'name': 'Dijkstra\'s Algorithm',
            'description': 'Optimal for weighted graphs, similar to BFS for unweighted',
            'complexity': 'O((V + E) log V)',
            'optimal': True,
            'complete': True
        },
        'bidirectional': {
            'name': 'Bidirectional Search',
            'description': 'Searches from both start and end simultaneously',
            'complexity': 'O(b^(d/2))',
            'optimal': True,
            'complete': True
        }
    }
