"""
Utility functions for the Maze Solver AI project.
"""
import os
import ast
import base64
import logging
import pygame
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from config import COLORS, PATHS, MAZE_CONFIG

logger = logging.getLogger(__name__)

class MazeError(Exception):
    """Custom exception for maze-related errors."""
    pass

class AlgorithmError(Exception):
    """Custom exception for algorithm-related errors."""
    pass

def load_maze_from_file(filename: str) -> List[List[int]]:
    """
    Load maze from file with proper error handling.
    
    Args:
        filename: Path to the maze file
        
    Returns:
        2D list representing the maze
        
    Raises:
        MazeError: If file cannot be loaded or parsed
    """
    if not os.path.exists(filename):
        raise MazeError(f"Maze file '{filename}' not found")
    
    try:
        maze = []
        with open(filename, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    if line.startswith("[") and line.endswith("]"):
                        row = ast.literal_eval(line)
                    else:
                        row = list(map(int, line.split()))
                    maze.append(row)
                except (ValueError, SyntaxError) as e:
                    raise MazeError(f"Invalid maze format at line {line_num}: {e}")
        
        if not maze:
            raise MazeError("Maze file is empty")
            
        # Validate maze dimensions
        rows = len(maze)
        cols = len(maze[0]) if maze else 0
        
        if rows < 3 or cols < 3:
            raise MazeError("Maze must be at least 3x3")
            
        # Check if all rows have the same length
        for i, row in enumerate(maze):
            if len(row) != cols:
                raise MazeError(f"Inconsistent row length at row {i+1}")
                
        logger.info(f"Successfully loaded maze from {filename}: {rows}x{cols}")
        return maze
        
    except Exception as e:
        if isinstance(e, MazeError):
            raise
        raise MazeError(f"Error loading maze from {filename}: {e}")

def find_start_end_positions(maze: List[List[int]]) -> Tuple[Optional[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Find start (2) and end (3) positions in the maze.

    Args:
        maze: 2D list representing the maze

    Returns:
        Tuple of (start_position, list_of_end_positions)
    """
    start = None
    ends = []
    rows, cols = len(maze), len(maze[0])

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 2:
                start = (r, c)
            elif maze[r][c] == 3:
                ends.append((r, c))

    return start, ends

def validate_maze_positions(maze: List[List[int]]) -> None:
    """
    Validate that maze has proper start and end positions.

    Args:
        maze: 2D list representing the maze

    Raises:
        MazeError: If start or end positions are missing or invalid
    """
    start, ends = find_start_end_positions(maze)

    if start is None:
        raise MazeError("Start position (2) not found in maze")
    if len(ends) == 0:
        raise MazeError("At least one end position (3) must be present in maze")

    logger.info(f"Maze validation passed: start={start}, ends={ends}")

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode image file to base64 string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string
        
    Raises:
        FileNotFoundError: If image file doesn't exist
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found")
        
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        raise

def save_maze_image(maze: List[List[int]], filename: str, path: Optional[List[Tuple[int, int]]] = None) -> None:
    """
    Save maze as PNG image.
    
    Args:
        maze: 2D list representing the maze
        filename: Output filename
        path: Optional path to highlight in the maze
    """
    try:
        rows, cols = len(maze), len(maze[0])
        cell_size = MAZE_CONFIG['CELL_SIZE']
        margin = MAZE_CONFIG['MARGIN']
        
        # Create surface
        surface = pygame.Surface(((cell_size + margin) * cols, (cell_size + margin) * rows))
        surface.fill(COLORS['GREY'])
        
        # Draw maze
        for row in range(rows):
            for col in range(cols):
                val = maze[row][col]
                pos = (row, col)
                
                # Determine color
                if val == 0:  # Path
                    color = COLORS['WHITE']
                elif val == 1:  # Wall
                    color = COLORS['BLACK']
                elif val == 2:  # Start
                    color = COLORS['GREEN']
                elif val == 3:  # End
                    color = COLORS['RED']
                else:
                    color = COLORS['GREY']
                
                # Highlight path if provided
                if path and pos in path and val not in [2, 3]:
                    color = COLORS['BLUE']
                
                # Draw cell
                rect = [
                    (margin + cell_size) * col + margin,
                    (margin + cell_size) * row + margin,
                    cell_size, cell_size
                ]
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, COLORS['GREY'], rect, 1)
        
        pygame.image.save(surface, filename)
        logger.info(f"Maze image saved to {filename}")
        
    except Exception as e:
        logger.error(f"Error saving maze image to {filename}: {e}")
        raise

def get_neighbors(pos: Tuple[int, int], rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    Get valid neighboring positions (up, down, left, right).
    
    Args:
        pos: Current position (row, col)
        rows: Number of rows in maze
        cols: Number of columns in maze
        
    Returns:
        List of valid neighbor positions
    """
    r, c = pos
    neighbors = []
    
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
            
    return neighbors

def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calculate Manhattan distance between two positions.
    
    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)
        
    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def cleanup_temp_files() -> None:
    """Clean up temporary files."""
    temp_files = [PATHS['MAZE_IMAGE'], PATHS['SOLUTION_IMAGE']]
    
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not remove temporary file {file_path}: {e}")
