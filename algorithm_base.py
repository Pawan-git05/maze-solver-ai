"""
Base class for pathfinding algorithms with animation support.
"""
import os
import pygame
import time
import sys
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Set
from collections import deque
from config import COLORS, MAZE_CONFIG, ALGORITHM_CONFIG, setup_logging
from utils import load_maze_from_file, find_start_end_positions, validate_maze_positions, save_maze_image, get_neighbors

logger = setup_logging()

class PathfindingAlgorithm(ABC):
    """Abstract base class for pathfinding algorithms."""
    
    def __init__(self, maze_file: str, animate: bool = True):
        """
        Initialize the pathfinding algorithm.

        Args:
            maze_file: Path to the maze file
            animate: Whether to show real-time animation
        """
        self.maze_file = maze_file
        self.animate = animate

        # Initialize maze-related attributes
        self.maze = None
        self.rows = 0
        self.cols = 0
        self.start = None
        self.end = None

        # Algorithm state
        self.visited = set()
        self.path = []
        self.came_from = {}
        self.stats = {
            'nodes_explored': 0,
            'path_length': 0,
            'execution_time': 0,
            'success': False
        }

        # Load maze if file exists (for actual execution)
        if maze_file and os.path.exists(maze_file):
            self.load_maze()

    def load_maze(self):
        """Load and validate the maze from file."""
        self.maze = load_maze_from_file(self.maze_file)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])

        # Validate maze
        validate_maze_positions(self.maze)
        self.start, self.ends = find_start_end_positions(self.maze)
        # For backward compatibility, set self.end to the first end point
        self.end = self.ends[0] if self.ends else None

        # Animation setup
        if self.animate:
            self.setup_animation()
    
    def setup_animation(self):
        """Setup pygame for animation."""
        pygame.init()
        self.cell_size = MAZE_CONFIG['CELL_SIZE']
        self.margin = MAZE_CONFIG['MARGIN']
        
        # Calculate window size
        width = (self.cell_size + self.margin) * self.cols
        height = (self.cell_size + self.margin) * self.rows + 100  # Extra space for info
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"{self.__class__.__name__} - Maze Solver")
        self.font = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()
    
    def draw_maze(self, current_pos: Optional[Tuple[int, int]] = None, 
                  frontier: Optional[Set[Tuple[int, int]]] = None):
        """
        Draw the current state of the maze.
        
        Args:
            current_pos: Current position being explored
            frontier: Set of positions in the frontier/queue
        """
        if not self.animate:
            return
            
        self.screen.fill(COLORS['WHITE'])
        
        for row in range(self.rows):
            for col in range(self.cols):
                pos = (row, col)
                val = self.maze[row][col]
                
                # Determine color based on cell type and state
                if val == 1:  # Wall
                    color = COLORS['BLACK']
                elif val == 2:  # Start
                    color = COLORS['GREEN']
                elif val == 3:  # End
                    color = COLORS['RED']
                elif pos in self.visited:  # Visited
                    color = COLORS['LIGHT_BLUE']
                elif frontier and pos in frontier:  # In frontier
                    color = COLORS['YELLOW']
                elif pos == current_pos:  # Current position
                    color = COLORS['ORANGE']
                else:  # Empty path
                    color = COLORS['WHITE']
                
                # Draw cell
                rect = [
                    (self.margin + self.cell_size) * col + self.margin,
                    (self.margin + self.cell_size) * row + self.margin,
                    self.cell_size, self.cell_size
                ]
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLORS['GREY'], rect, 1)
        
        # Draw final path if found
        if self.path:
            for pos in self.path:
                if pos not in [self.start, self.end]:
                    row, col = pos
                    rect = [
                        (self.margin + self.cell_size) * col + self.margin,
                        (self.margin + self.cell_size) * row + self.margin,
                        self.cell_size, self.cell_size
                    ]
                    pygame.draw.rect(self.screen, COLORS['BLUE'], rect)
        
        # Draw statistics
        self.draw_stats()
        
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def draw_stats(self):
        """Draw algorithm statistics on screen."""
        if not self.animate:
            return
            
        y_offset = (self.cell_size + self.margin) * self.rows + 10
        
        stats_text = [
            f"Algorithm: {self.__class__.__name__}",
            f"Nodes Explored: {self.stats['nodes_explored']}",
            f"Path Length: {self.stats['path_length']}",
            f"Time: {self.stats['execution_time']:.3f}s"
        ]
        
        for i, text in enumerate(stats_text):
            surface = self.font.render(text, True, COLORS['BLACK'])
            self.screen.blit(surface, (10, y_offset + i * 25))
    
    def reconstruct_path(self) -> List[Tuple[int, int]]:
        """Reconstruct the path from start to end."""
        if self.end not in self.came_from and self.end != self.start:
            return []
            
        path = []
        current = self.end
        
        while current in self.came_from:
            path.append(current)
            current = self.came_from[current]
        
        path.reverse()
        return path
    
    @abstractmethod
    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Solve the maze using the specific algorithm.
        
        Returns:
            Tuple of (path, statistics)
        """
        pass
    
    def run(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Run the pathfinding algorithm and save results.

        Returns:
            Tuple of (path, statistics)
        """
        logger.info(f"Starting {self.__class__.__name__} algorithm")
        start_time = time.time()

        try:
            # Ensure maze is loaded
            if self.maze is None:
                self.load_maze()

            # Solve the maze
            path, stats = self.solve()

            # Update final statistics
            self.stats.update(stats)
            self.stats['execution_time'] = time.time() - start_time
            self.stats['success'] = path is not None
            self.stats['path_length'] = len(path) if path else 0

            # Always save maze image
            save_maze_image(self.maze, "maze.png")

            # Save solution image only if path found
            if path:
                save_maze_image(self.maze, "solution.png", path)
            else:
                # Create a "no solution" image
                save_maze_image(self.maze, "solution.png")

            # Keep animation window open briefly if animated
            if self.animate:
                if path:
                    self.path = path
                self.draw_maze()
                time.sleep(2)  # Show final result
                pygame.quit()

            logger.info(f"{self.__class__.__name__} completed: {self.stats}")
            return path, self.stats

        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            if self.animate:
                pygame.quit()
            raise
