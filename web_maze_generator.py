"""
Web-based maze generator for creating random mazes without GUI.
This module generates multiple random mazes for web interface selection.
"""

import os
# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import numpy as np
import random
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class WebMazeGenerator:
    """Generate random mazes for web interface without GUI dependencies."""
    
    def __init__(self, size: int = 25):
        """
        Initialize maze generator.

        Args:
            size: Size of the maze (size x size)
        """
        self.size = max(8, min(30, size))  # Clamp size between 8 and 30
        
    def generate_single_maze(self, should_be_solvable: bool = True) -> List[List[int]]:
        """
        Generate a single random maze without pre-set start and end points.

        Args:
            should_be_solvable: Whether this maze should have a solution (ignored for now)

        Returns:
            2D list representing the maze (0=path, 1=wall) - no start/end points set
        """
        # Initialize maze with walls
        maze = np.ones((self.size, self.size), dtype=int)

        # Create random paths in the interior
        for row in range(1, self.size - 1):
            for col in range(1, self.size - 1):
                # 40% chance of being a wall, 60% chance of being a path
                maze[row][col] = random.choice([0, 0, 0, 1, 1])

        # Ensure corners are paths to provide good starting options
        maze[0][0] = 0  # Top-left
        maze[0][self.size - 1] = 0  # Top-right
        maze[self.size - 1][0] = 0  # Bottom-left
        maze[self.size - 1][self.size - 1] = 0  # Bottom-right

        # Carve some guaranteed paths for connectivity
        self._carve_connectivity_paths(maze)

        # Add some random path connections
        self._add_random_connections(maze)

        return maze.tolist()
    
    def _carve_connectivity_paths(self, maze: np.ndarray) -> None:
        """
        Carve some paths to ensure basic connectivity in the maze.

        Args:
            maze: The maze array to modify
        """
        # Create a few connecting paths to ensure the maze isn't too fragmented

        # Horizontal path across the middle
        mid_row = self.size // 2
        for col in range(0, self.size, 2):
            if col < self.size:
                maze[mid_row][col] = 0

        # Vertical path down the middle
        mid_col = self.size // 2
        for row in range(0, self.size, 2):
            if row < self.size:
                maze[row][mid_col] = 0

        # Connect corners to center with some paths
        # Top-left to center
        for i in range(min(self.size // 3, 5)):
            if i < self.size and i < self.size:
                maze[i][i] = 0

        # Bottom-right to center
        for i in range(max(self.size - self.size // 3, self.size - 5), self.size):
            if i >= 0 and i < self.size:
                maze[i][i] = 0
    
    def _add_random_connections(self, maze: np.ndarray) -> None:
        """
        Add some random path connections to make the maze more interesting.
        
        Args:
            maze: The maze array to modify
        """
        # Add some random horizontal connections
        for _ in range(self.size // 4):
            row = random.randint(1, self.size - 2)
            col = random.randint(1, self.size - 2)
            
            # Create a small path cluster
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if random.random() < 0.6:  # 60% chance
                            maze[nr][nc] = 0
    
    def generate_multiple_mazes(self, count: int = 5) -> List[List[List[int]]]:
        """
        Generate multiple random mazes without pre-set start/end points.

        Args:
            count: Number of mazes to generate

        Returns:
            List of mazes, each maze is a 2D list (0=path, 1=wall)
        """
        mazes = []
        print(f"🎲 Generating {count} random mazes (no start/end points)")

        for i in range(count):
            try:
                maze = self.generate_single_maze()
                mazes.append(maze)
                print(f"✅ Generated maze {i+1}: ready for start/end point selection")
            except Exception as e:
                print(f"❌ Error generating maze {i + 1}: {e}")
                # Generate a simple fallback maze
                fallback_maze = self._generate_fallback_maze()
                mazes.append(fallback_maze)

        return mazes
    
    def _generate_fallback_maze(self) -> List[List[int]]:
        """
        Generate a simple fallback maze in case of errors.

        Returns:
            Simple maze without start/end points
        """
        maze = np.ones((self.size, self.size), dtype=int)

        # Create simple cross pattern
        mid_row = self.size // 2
        mid_col = self.size // 2

        # Horizontal line
        for col in range(self.size):
            maze[mid_row][col] = 0

        # Vertical line
        for row in range(self.size):
            maze[row][mid_col] = 0

        # Add some interior paths
        for i in range(2, self.size - 2, 2):
            for j in range(2, self.size - 2, 2):
                if random.random() < 0.3:  # 30% chance
                    maze[i][j] = 0

        # Ensure corners are paths
        maze[0][0] = 0
        maze[0][self.size - 1] = 0
        maze[self.size - 1][0] = 0
        maze[self.size - 1][self.size - 1] = 0

        return maze.tolist()
    
    def validate_maze(self, maze: List[List[int]]) -> bool:
        """
        Validate that a maze has at least one path from any point to any other.
        
        Args:
            maze: The maze to validate
            
        Returns:
            True if maze is valid, False otherwise
        """
        if not maze or len(maze) == 0:
            return False
        
        # Find all path cells
        path_cells = []
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 0:
                    path_cells.append((i, j))
        
        if len(path_cells) < 2:
            return False  # Need at least 2 path cells
        
        # Simple connectivity check using BFS from first path cell
        start = path_cells[0]
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            row, col = queue.pop(0)
            
            # Check all 4 directions
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                
                if (0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and 
                    (nr, nc) not in visited and maze[nr][nc] == 0):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        # Check if we can reach most path cells
        reachable_ratio = len(visited) / len(path_cells)
        return reachable_ratio > 0.5  # At least 50% of paths should be reachable


def generate_web_mazes(size: int, count: int = 5) -> List[List[List[int]]]:
    """
    Convenience function to generate multiple mazes.
    
    Args:
        size: Size of each maze
        count: Number of mazes to generate
        
    Returns:
        List of generated mazes
    """
    generator = WebMazeGenerator(size)
    return generator.generate_multiple_mazes(count)


if __name__ == "__main__":
    # Test the generator
    generator = WebMazeGenerator(15)
    mazes = generator.generate_multiple_mazes(3)
    
    print(f"Generated {len(mazes)} mazes")
    for i, maze in enumerate(mazes):
        print(f"\nMaze {i + 1}:")
        for row in maze:
            print(''.join(['█' if cell == 1 else '·' for cell in row]))